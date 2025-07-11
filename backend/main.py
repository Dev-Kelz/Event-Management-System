from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import date

app = FastAPI()

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class Event(BaseModel):
    id: int
    title: str
    date: str

# In-memory user storage
users_db = []

# In-memory event storage
events_db = [
    {"id": 1, "title": "React Native Workshop", "date": "2024-07-01"},
    {"id": 2, "title": "FastAPI Webinar", "date": "2024-07-10"},
]

@app.post("/register")
def register(user: User):
    # Check if user already exists
    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="User already exists")
    users_db.append(user.dict())
    return {"success": True, "message": "User registered successfully"}

@app.post("/login")
def login(login_req: LoginRequest):
    # Check if user exists and password matches
    user = next((u for u in users_db if u["email"] == login_req.email and u["password"] == login_req.password), None)
    if user:
        return {"success": True, "message": "Login successful"}
    else:
        return {"success": False, "message": "Invalid email or password"}

@app.get("/events/", response_model=List[Event])
def get_events():
    return events_db

@app.post("/events/", response_model=Event)
def create_event(event: Event):
    events_db.append(event.dict())
    return event
