from datetime import date
from typing import Optional

from pydantic import BaseModel


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    date: date
    location: Optional[str] = None
    created_by: int


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None
    location: Optional[str] = None
