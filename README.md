# Kubernetes Pod Info API

A FastAPI application that provides health check and pod information endpoints using the Kubernetes API.

## Features

- `/healthz` endpoint for health checks
- `/pod-info` endpoint that returns pod information using the Kubernetes API

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application locally:
```bash
python main.py
```

## Kubernetes Deployment

To deploy this application to Kubernetes:

1. Create a Docker image with the application
2. Deploy the application to your Kubernetes cluster
3. Make sure to set the `POD_NAME` environment variable in your deployment manifest

Example deployment manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pod-info-api
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pod-info-api
  template:
    metadata:
      labels:
        app: pod-info-api
    spec:
      containers:
      - name: pod-info-api
        image: your-image:tag
        ports:
        - containerPort: 8000
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
```

## API Endpoints

- `GET /healthz`: Returns the health status of the application
- `GET /pod-info`: Returns information about the pod running the application

## Notes

- The application will try to use in-cluster configuration first, then fall back to kubeconfig
- Make sure the service account has the necessary permissions to read pod information 