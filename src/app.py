
from flask import Flask, request, jsonify, Response
from pydantic import BaseModel, ValidationError
import joblib
import pandas as pd
import sqlite3
from prometheus_client import Counter, generate_latest, REGISTRY

app = Flask(__name__)

# Load model
model = joblib.load("models/RandomForest.pkl")

# SQLite logging
conn = sqlite3.connect("logs.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS logs (input TEXT, prediction INTEGER)"
)
conn.commit()

# Prometheus counter
prediction_counter = Counter(
    "iris_predictions_total",
    "Total number of predictions",
    ["prediction"]
)


class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = IrisInput(**request.get_json())

        df = pd.DataFrame([data.dict()])
        df.columns = [
            "sepal length (cm)",
            "sepal width (cm)",
            "petal length (cm)",
            "petal width (cm)"
        ]

        prediction = model.predict(df)[0]
        prediction_counter.labels(prediction=str(prediction)).inc()

        cursor.execute(
            "INSERT INTO logs (input, prediction) VALUES (?, ?)",
            (str(data.dict()), int(prediction))
        )
        conn.commit()

        return jsonify({"prediction": int(prediction)})

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/metrics", methods=["GET"])
def metrics():
    cursor.execute("SELECT COUNT(*) FROM logs")
    count = cursor.fetchone()[0]

    cursor.execute("SELECT prediction, COUNT(*) FROM logs GROUP BY prediction")
    distribution = {str(row[0]): row[1] for row in cursor.fetchall()}

    prometheus_metrics = generate_latest(REGISTRY)

    return Response(
        f"Total Predictions: {count}\n"
        f"Prediction Distribution: {distribution}\n"
        + prometheus_metrics.decode(),
        mimetype="text/plain"
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
