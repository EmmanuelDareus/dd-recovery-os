import time
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from config import BASE_DIR
from src.core.engine import CoreEngine
from src.content.engine import ContentManager
from src.utils.logger import logger

app = FastAPI(title="Content & Recovery OS API", version="1.0.0")

# Initialize engines
engine = CoreEngine(name="ModularEngine")
engine.start()

content_manager = ContentManager()

class DataInput(BaseModel):
    data: str

class ProjectInput(BaseModel):
    title: str
    platform: str = "YouTube"

class StageUpdateInput(BaseModel):
    title: str
    stage: str

@app.middleware("http")
async def log_requests(request: Request, call_next):
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
        "message": "Content & Recovery OS API is live and running!",
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

@app.post("/content/project")
def add_content_project(payload: ProjectInput):
    logger.info(f"Creating new content project: {payload.title} on {payload.platform}")
    return content_manager.create_project(payload.title, payload.platform)

@app.get("/content/projects")
def list_content_projects():
    logger.info("Listing all content projects.")
    return {"projects": content_manager.projects}

@app.post("/content/stage")
def update_project_stage(payload: StageUpdateInput):
    logger.info(f"Updating stage for project '{payload.title}' to '{payload.stage}'")
    result = content_manager.update_stage(payload.title, payload.stage)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)