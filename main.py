from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import database 
from schedular import start_scheduler
from pathlib import Path

app = FastAPI(title="ToDo Telegram Mini App")

BASE_DIR = Path(__file__).resolve().parent

@app.on_event("startup")
def on_startup():
    start_scheduler()

class TaskCreateSchema(BaseModel):
    title: str
    deadline: str
    chat_id: int

@app.get("/api/tasks/{chat_id}")
def get_tasks(chat_id: int):
    return database.get_tasks(chat_id)

@app.post("/api/tasks")
def create_tasks(data: TaskCreateSchema):
    if not data.title or not data.deadline:
        raise HTTPException(status_code=400, detail="Title and deadline are required")

    new_task = database.add_task(
        title=data.title,
        deadline=data.deadline,
        chat_id=data.chat_id
    )
    return {"status": "ok", "task": new_task}

@app.post("/api/tasks/{task_id}/complete")
def complete_task(task_id: int):
    task = database.mark_task_completed(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "ok", "task": task}

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse(BASE_DIR / "static" / "index.html")