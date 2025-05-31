from fastapi import Depends, FastAPI, HTTPException, status
import models 
from database import SessionLocal, engine, get_db
from schemas import TaskSchema


app=FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/tasks")
def read_tasks(db:SessionLocal = Depends(get_db)):
    db_tasks = db.query(models.Task).all()
    return db_tasks
    

@app.get("/tasks/{task_id}")
def read_task(task_id: int,db:SessionLocal = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.post("/tasks/",status_code=status.HTTP_201_CREATED)
def create_task(task: TaskSchema,db:SessionLocal = Depends(get_db)):
    db_task = models.Task(name=task.taskname, description=task.description, status=task.status)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.put("/tasks/{task_id}")
def update_task(task_id:int,task: TaskSchema,db:SessionLocal = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.name = task.taskname
    db_task.description = task.description
    db_task.status = task.status
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id:int,db:SessionLocal = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return db_task