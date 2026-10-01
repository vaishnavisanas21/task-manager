from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tasks = []

class Task(BaseModel):
    title: str
    description: str
    priority: str
    due_date: str
    completed: bool = False

@app.get("/")
def home():
    return {"message": "Task Manager API running"}

@app.post("/tasks")
def create_task(task: Task):
    task_dict = task.dict()
    task_dict["id"] = len(tasks)
    tasks.append(task_dict)
    return {"message": "task added successfully", "task": task_dict}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    if task_id < 0 or task_id >= len(tasks):
        return {"error": "task not found"}

    updated_dict = updated_task.dict()
    updated_dict["id"] = task_id
    tasks[task_id] = updated_dict

    return {"message": "task updated", "task": updated_dict}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        return {"error": "invalid id"}

    deleted = tasks.pop(task_id)
    return {"message": "task deleted", "task": deleted}

@app.get("/tasks/search/{keyword}")
def search_tasks(keyword: str):
    return [
        task for task in tasks
        if keyword.lower() in task["title"].lower()
    ]