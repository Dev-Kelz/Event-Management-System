from datetime import date
from typing import Optional

from pydantic import BaseModel


class TaskCreate(BaseModel):
    event_id: int
    stage_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    due_date: Optional[date] = None
    assigned_to: Optional[int] = None
    created_by: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None
    stage_id: Optional[int] = None
    assigned_to: Optional[int] = None
