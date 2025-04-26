from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import redis
import os
from typing import Dict

app = FastAPI(title="K8s Redis API")
templates = Jinja2Templates(directory="templates")

# Initialize Redis client
redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.get("/healthz")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def read_root(request: Request):
    # Get all keys from Redis
    keys = redis_client.keys("*")
    key_values = {}
    for key in keys:
        value = redis_client.get(key)
        key_values[key] = value
    return templates.TemplateResponse("index.html", {"request": request, "key_values": key_values})

@app.post("/redis")
async def set_redis_value(key: str = Form(...), value: str = Form(...)):
    try:
        redis_client.set(key, value)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/redis/{key}")
async def delete_redis_value(key: str):
    try:
        redis_client.delete(key)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 