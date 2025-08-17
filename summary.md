
# MLOps Pipeline Summary

## Architecture
- **Data**: Iris dataset, versioned with DVC
- **Models**: Logistic Regression, Random Forest
- **Tracking**: MLflow with model registration
- **API**: Flask with Pydantic validation
- **Container**: Docker (python:3.9-slim)
- **CI/CD**: GitHub Actions (linting, testing, Docker build/push)
- **Monitoring**: SQLite logging, Prometheus metrics, /metrics endpoint
- **Re-training**: Trigger script for new data

## Highlights
- MLflow tracks experiments, parameters, and metrics, with the best model registered.
- Flask API validates inputs with Pydantic and logs predictions to SQLite.
- Prometheus metrics exposed for monitoring.
- GitHub Actions automates linting, testing, and Docker deployment.
- Re-training script triggers model updates on new data.

## Setup Instructions
1. Clone the repository: `git clone https://<YOUR_GITHUB_USERNAME>:<YOUR_PERSONAL_ACCESS_TOKEN>@github.com/Abbhinav1902/MLOPS.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the API: `python src/app.py`
4. Deploy with Docker: `./deploy.sh <DOCKER_USERNAME>`
5. Access API at `http://localhost:5000/predict`
6. Monitor metrics at `http://localhost:5000/metrics`
7. Retrain model: `python src/retrain.py`
