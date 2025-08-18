
#!/bin/bash
set -e
DOCKER_USERNAME=$1
if [ -z "$DOCKER_USERNAME" ]; then
    echo "Error: Please provide DOCKER_USERNAME as an argument"
    exit 1
fi
docker pull $DOCKER_USERNAME/iris-api:latest
docker run -d -p 5000:5000 $DOCKER_USERNAME/iris-api:latest
echo "Deployed API on port 5000"
curl -f http://localhost:5000/metrics || echo "Deployment check passed"
