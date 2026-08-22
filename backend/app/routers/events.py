from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models import Event

router = APIRouter()


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    date: date
    location: Optional[str] = None
    created_by: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/events")
async def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).order_by(Event.created_at.desc()).all()
    return {
        "success": True,
        "events": [
            {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "date": event.date.isoformat(),
                "location": event.location,
                "created_by": event.created_by,
                "created_at": event.created_at.isoformat(),
            }
            for event in events
        ],
    }


@router.post("/events")
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    new_event = Event(
        title=event.title,
        description=event.description,
        date=event.date,
        location=event.location,
        created_by=event.created_by,
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {
        "success": True,
        "message": "Event created successfully",
        "event": {
            "id": new_event.id,
            "title": new_event.title,
            "description": new_event.description,
            "date": new_event.date.isoformat(),
            "location": new_event.location,
            "created_by": new_event.created_by,
            "created_at": new_event.created_at.isoformat(),
        },
    }


@router.get("/events/{event_id}")
async def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"success": True, "event": event.__dict__}
