from fastapi import FastAPI
from kubernetes import client, config
import os

app = FastAPI(title="K8s Pod Info API")

# Try to load in-cluster config first, fall back to kubeconfig
try:
    config.load_incluster_config()
except config.ConfigException:
    config.load_kube_config()

v1 = client.CoreV1Api()

@app.get("/healthz")
async def health_check():
    return {"status": "healthy"}

@app.get("/pod-info")
async def get_pod_info():
    # Get the pod name from the environment variable
    pod_name = os.environ.get("POD_NAME", "unknown")
    
    try:
        # Get pod details from Kubernetes API
        pod = v1.read_namespaced_pod(name=pod_name, namespace="default")
        return {
            "pod_name": pod_name,
            "pod_ip": pod.status.pod_ip,
            "node_name": pod.spec.node_name,
            "namespace": pod.metadata.namespace
        }
    except Exception as e:
        return {
            "pod_name": pod_name,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 