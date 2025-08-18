
import os
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def check_and_retrain(data_path="data/iris.csv", min_new_rows=10):
    if not os.path.exists(data_path):
        print("No data found for retraining.")
        return
    df = pd.read_csv(data_path)
    if len(df) < min_new_rows:
        print("Not enough new data for retraining.")
        return
    X = df.drop("target", axis=1)
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    with mlflow.start_run(run_name="Retrained_RandomForest"):
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        mlflow.log_param("model", "RandomForest")
        mlflow.log_param("n_estimators", 100)
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, "model")
        print(f"Retrained model with accuracy: {acc:.4f}")

if __name__ == "__main__":
    check_and_retrain()
