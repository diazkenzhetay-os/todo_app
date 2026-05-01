from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import auth, tasks
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Task
from datetime import datetime, timezone

# Подключаем тёмную тему и описание проекта
app = FastAPI(
    title="Менеджер задач",
    description="Учебный проект на FastAPI с регистрацией и управлением задачами",
    version="1.0",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    swagger_ui_css_url="/static/swagger-dark.css"
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(tasks.router)

# Подключаем статические файлы (для CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Функция для демо-данных
def create_demo_data():
    db: Session = SessionLocal()

    demo_user = db.query(User).filter(User.email == "demo@example.com").first()
    if not demo_user:
        demo_user = User(email="demo@example.com", hashed_password="12345")
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

        task1 = Task(
            title="Сделать домашку",
            description="Математика, глава 5",
            status=False,
            user_id=demo_user.id,
            created_at=datetime.now(timezone.utc)
        )
        task2 = Task(
            title="Купить продукты",
            description="Хлеб, молоко, яйца",
            status=True,
            user_id=demo_user.id,
            created_at=datetime.now(timezone.utc)
        )

        db.add_all([task1, task2])
        db.commit()

    db.close()

# Вызов функции при старте
create_demo_data()