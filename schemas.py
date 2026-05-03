from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

class UserLogin(BaseModel):
    email: str
    password: str

class ProjectCreate(BaseModel):
    name: str
    description: str

# ✅ ONLY ONE TaskCreate
class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_to: int
    project_id: int
    due_date: datetime   # ✅ added

class TaskUpdate(BaseModel):
    status: str