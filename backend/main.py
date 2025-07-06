from fastapi import FastAPI
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

class Event(BaseModel):
    id: int
    title: str
    date: str

# In-memory event storage
events_db = [
    {"id": 1, "title": "React Native Workshop", "date": "2024-07-01"},
    {"id": 2, "title": "FastAPI Webinar", "date": "2024-07-10"},
]

@app.get("/events/", response_model=List[Event])
def get_events():
    return events_db

@app.post("/events/", response_model=Event)
def create_event(event: Event):
    events_db.append(event.dict())
    return event
