
import sys
import os
import json

# Ensure parent directory is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import app


def test_predict():
    client = app.test_client()
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.get_json()


def test_invalid_input():
    client = app.test_client()
    response = client.post("/predict", json={"sepal_length": "invalid"})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_metrics():
    client = app.test_client()
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "Total Predictions" in response.get_data(as_text=True)
