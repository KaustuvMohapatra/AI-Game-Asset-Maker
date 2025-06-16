import uuid
import os
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict

# Import your refactored generation logic (we'll create this in the next step)
from worker import run_asset_generation

# --- FastAPI App Setup ---
app = FastAPI()

# In-memory "database" to track job status. For a real app, use Redis or a DB.
jobs: Dict[str, Dict] = {}

# --- Pydantic Models for API Data Validation ---
class GameGenerationRequest(BaseModel):
    title: str
    character: str
    background: str
    reward: str
    enemy: str
    levels: int

# --- CORS Middleware ---
# This allows your React app (running on a different port) to talk to this server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static File Serving ---
# This makes the 'assets' directory available at http://127.0.0.1:8000/assets
# Your React app uses this to display the generated images.
if not os.path.exists("assets"):
    os.makedirs("assets")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")


# --- API Endpoints ---
@app.post("/generate-game")
async def generate_game(request: GameGenerationRequest, background_tasks: BackgroundTasks):
    """
    This endpoint kicks off the asset generation process.
    It immediately returns a task_id so the frontend doesn't have to wait.
    """
    task_id = str(uuid.uuid4())
    
    # Store job info
    jobs[task_id] = {"status": "QUEUED", "result": None}
    
    # Run the actual heavy lifting in the background
    background_tasks.add_task(run_asset_generation, task_id, request.dict(), jobs)
    
    return {"task_id": task_id}


@app.get("/status/{task_id}")
async def get_status(task_id: str):
    """
    This endpoint lets the frontend poll for the status of a generation job.
    """
    job = jobs.get(task_id, {})
    # The frontend expects 'result' to be a dict with URLs on success
    # The worker function will populate this.
    return {"task_id": task_id, "status": job.get("status", "FAILURE"), "result": job.get("result")}

# To run the server:
# In your terminal, in the 'backend' directory, run:
# uvicorn api:app --reload