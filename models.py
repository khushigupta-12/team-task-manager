from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base

# 👤 USER
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

# 📁 PROJECT
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))

# 📌 TASK (ONLY ONE CLASS)
class Task(Base):
    __tablename__ = "tasks_new"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(String, default="Todo")
    assigned_to = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    due_date = Column(DateTime, nullable=True)  # ✅ added