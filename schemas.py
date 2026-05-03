from pydantic import BaseModel

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

class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_to: int
    project_id: int

class TaskUpdate(BaseModel):
    status: str