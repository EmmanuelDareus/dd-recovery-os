import time
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from config import BASE_DIR
from src.core.engine import CoreEngine
from src.utils.logger import logger

app = FastAPI(title="Modular App", version="1.0.0")

# Initialize engine
engine = CoreEngine(name="ModularEngine")
engine.start()

class DataInput(BaseModel):
    data: str

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware that logs every incoming request and processing time."""
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(f"METHOD: {request.method} | PATH: {request.url.path} | STATUS: {response.status_code} | TIME: {process_time:.2f}ms")
    return response

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    return {
        "status": "success",
        "message": "Application is live and running!",
        "working_directory": str(BASE_DIR),
        "engine_status": engine.is_running
    }

@app.post("/process")
def process_data(payload: DataInput):
    try:
        logger.info(f"Processing payload data: {payload.data}")
        result = engine.process(payload.data)
        return {
            "status": "success",
            "engine_name": engine.name,
            "result": result
        }
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))