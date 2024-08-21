from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class ConfigDict:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: str
    status: str
    due_date: str

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
