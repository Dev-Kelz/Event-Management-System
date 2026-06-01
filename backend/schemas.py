# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class EventCreate(BaseModel):
    title: str
    date: str
    time: str
    location: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class Event(BaseModel):
    id: int
    title: str
    date: str
    time: str
    location: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class FeedbackBase(BaseModel):
    rating: int
    comment: Optional[str] = None


class FeedbackCreate(FeedbackBase):
    event_id: int


class Feedback(FeedbackBase):
    id: int
    user_id: int
    event_id: int
    created_at: datetime
    user: User

    class Config:
        from_attributes = True
