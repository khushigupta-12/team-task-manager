from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

import models
import schemas
from database import engine, SessionLocal
from auth import hash_password, verify_password, create_token

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Backend with DB working 🚀"}

# 🔐 SIGNUP
@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

# 🔐 LOGIN
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"user_id": db_user.id})

    return {"access_token": token}

# 📁 CREATE PROJECT (Admin only)
@app.post("/projects")
def create_project(
    project: schemas.ProjectCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create project")

    new_project = models.Project(
        name=project.name,
        description=project.description,
        created_by=user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {"message": "Project created by admin"}

# 📁 GET PROJECTS
@app.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

# 📌 CREATE TASK
@app.post("/tasks")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(
        title=task.title,
        description=task.description,
        assigned_to=task.assigned_to,
        project_id=task.project_id,
        status="Todo",
        due_date=task.due_date
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "Task created"}

# 📌 GET TASKS
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

# 📌 UPDATE TASK
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.status = task.status
    db.commit()

    return {"message": "Task updated"}

# 📊 DASHBOARD
@app.get("/dashboard")
def dashboard(user_id: int = 1, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.assigned_to == user_id).all()

    total = len(tasks)

    todo = len([t for t in tasks if t.status == "Todo"])
    in_progress = len([t for t in tasks if t.status == "In Progress"])
    done = len([t for t in tasks if t.status == "Done"])

    overdue = len([
        t for t in tasks
        if t.due_date and t.due_date < datetime.now() and t.status != "Done"
    ])

    return {
        "total_tasks": total,
        "todo": todo,
        "in_progress": in_progress,
        "done": done,
        "overdue": overdue,
        "tasks": tasks
    }