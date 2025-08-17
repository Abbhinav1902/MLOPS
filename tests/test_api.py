
import pytest
from src.app import app
import threading
import time

@pytest.fixture
def client():
    app.config["TESTING"] = True
    # Start Flask app in a separate thread
    def run_app():
        app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
    thread = threading.Thread(target=run_app)
    thread.daemon = True
    thread.start()
    time.sleep(1)  # Wait for server to start
    with app.test_client() as client:
        yield client
    # No explicit thread cleanup needed due to daemon

def test_predict(client):
    response = client.post("/predict", json={
        "sepal_length": 5.0,
        "sepal_width": 3.4,
        "petal_length": 1.5,
        "petal_width": 0.2
    })
    assert response.status_code == 200
    assert "prediction" in response.json

def test_invalid_input(client):
    response = client.post("/predict", json={"sepal_length": "invalid"})
    assert response.status_code == 400
    assert "error" in response.json
