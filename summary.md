
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
