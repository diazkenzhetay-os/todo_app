from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Task
from schemas import TaskCreate, TaskOut
from typing import List

router = APIRouter(prefix="/задачи", tags=["Задачи"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.put("/обновить/{task_id}", response_model=TaskOut)
def update_task_status(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    task.status = not task.status  # переключаем статус
    db.commit()
    db.refresh(task)
    return task

@router.post("/создать", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(title=task.title, description=task.description, user_id=1)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/все", response_model=List[TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()
