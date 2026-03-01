from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base schema (common fields)
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

# Schema for creating Todo (POST)  
class TodoCreate(TodoBase):
    pass

# Schema for updating Todo (PUT/PATCH)
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = False

    
# Schema for response (what API returns)
class TodoResponse(TodoBase):
    id: int
    is_completed: bool = False
    created_at: datetime
