from fastapi import FastAPI
import models 
from database import engine


app=FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    return {"task_id": task_id,"name": name,"description": description,"status": status}

@app.post("/tasks/")
def create_task():
    return {"task_id": task_id,"name": name,"description": description,"status": status}
    

@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    return {"task_id": task_id,"name": name,"description": description,"status": status}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return {"task_id": task_id,"name": name,"description": description,"status": status}