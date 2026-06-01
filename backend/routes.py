from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date, timedelta
from sqlalchemy import func
from database import SessionLocal
from models import User, Event, EventRegistration, EventFeedback, EventAnalytics, EventTask, EventStage, Notification, PushToken, EventReminder
from auth import hash_password, verify_password
import logging
import json

logger = logging.getLogger(__name__)

# Pydantic models
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

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

class UserProfile(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phone: Optional[str] = None
    bio: Optional[str] = None

class FeedbackCreate(BaseModel):
    event_id: int
    user_id: int
    rating: int  # 1-5
    comment: Optional[str] = None

class RegistrationCreate(BaseModel):
    event_id: int
    user_id: int

class TaskCreate(BaseModel):
    event_id: int
    stage_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"  # low, medium, high
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

class StageCreate(BaseModel):
    name: str
    description: Optional[str] = None
    order: Optional[int] = 0

class PushTokenCreate(BaseModel):
    user_id: int
    token: str
    device_type: str  # ios or android

class NotificationCreate(BaseModel):
    user_id: int
    event_id: Optional[int] = None
    title: str
    message: str
    type: str
    data: Optional[str] = None

class ReminderCreate(BaseModel):
    event_id: int
    user_id: int
    remind_at: datetime
    reminder_type: str

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create router
router = APIRouter()

# Auth Routes
@router.post("/register")
async def register(user: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user.email) | (User.username == user.username)
        ).first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Create new user
        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
            is_active=True,
            is_admin=False
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"New user registered: {user.email}")
        
        return {
            "success": True,
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    try:
        # Find user by email
        user = db.query(User).filter(User.email == credentials.email).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not user.is_active:
            raise HTTPException(status_code=401, detail="Account is inactive")
        
        # Verify password
        if not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        logger.info(f"User logged in: {user.email}")
        
        return {
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Event Routes
@router.get("/events")
async def get_events(db: Session = Depends(get_db)):
    """Get all events"""
    try:
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
                    "created_at": event.created_at.isoformat()
                }
                for event in events
            ]
        }
    except Exception as e:
        logger.error(f"Get events error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/events")
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """Create a new event"""
    try:
        new_event = Event(
            title=event.title,
            description=event.description,
            date=event.date,
            location=event.location,
            created_by=event.created_by
        )
        
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        
        logger.info(f"New event created: {event.title}")
        
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
                "created_at": new_event.created_at.isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Create event error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/{event_id}")
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific event"""
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return {
            "success": True,
            "event": {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "date": event.date.isoformat(),
                "location": event.location,
                "created_by": event.created_by,
                "created_at": event.created_at.isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get event error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/events/{event_id}")
async def update_event(event_id: int, event_data: EventUpdate, db: Session = Depends(get_db)):
    """Update an event"""
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Update fields if provided
        if event_data.title is not None:
            event.title = event_data.title
        if event_data.description is not None:
            event.description = event_data.description
        if event_data.date is not None:
            event.date = event_data.date
        if event_data.location is not None:
            event.location = event_data.location
        
        db.commit()
        db.refresh(event)
        
        logger.info(f"Event updated: {event.title}")
        
        return {
            "success": True,
            "message": "Event updated successfully",
            "event": {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "date": event.date.isoformat(),
                "location": event.location
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update event error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/events/{event_id}")
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete an event"""
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        db.delete(event)
        db.commit()
        
        logger.info(f"Event deleted: {event.title}")
        
        return {
            "success": True,
            "message": "Event deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete event error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# User Profile Routes
@router.get("/users/{user_id}")
async def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Get user profile"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get user profile error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Analytics Routes
@router.get("/analytics/event/{event_id}")
async def get_event_analytics(event_id: int, db: Session = Depends(get_db)):
    """Get analytics for a specific event"""
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Get registration count
        registration_count = db.query(EventRegistration).filter(
            EventRegistration.event_id == event_id
        ).count()
        
        # Get attendance count
        attendance_count = db.query(EventRegistration).filter(
            EventRegistration.event_id == event_id,
            EventRegistration.status == "attended"
        ).count()
        
        # Get average rating
        avg_rating = db.query(func.avg(EventFeedback.rating)).filter(
            EventFeedback.event_id == event_id
        ).scalar() or 0
        
        # Get total feedback count
        feedback_count = db.query(EventFeedback).filter(
            EventFeedback.event_id == event_id
        ).count()
        
        # Get daily analytics
        daily_analytics = db.query(EventAnalytics).filter(
            EventAnalytics.event_id == event_id
        ).order_by(EventAnalytics.date.desc()).limit(30).all()
        
        return {
            "success": True,
            "analytics": {
                "event_id": event_id,
                "event_title": event.title,
                "view_count": event.view_count,
                "registration_count": registration_count,
                "attendance_count": attendance_count,
                "attendance_rate": round((attendance_count / registration_count * 100) if registration_count > 0 else 0, 2),
                "average_rating": round(float(avg_rating), 2),
                "feedback_count": feedback_count,
                "daily_data": [
                    {
                        "date": str(day.date),
                        "views": day.views,
                        "registrations": day.registrations,
                        "attendees": day.attendees,
                        "shares": day.shares
                    }
                    for day in daily_analytics
                ]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get event analytics error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/dashboard")
async def get_dashboard_analytics(user_id: int, db: Session = Depends(get_db)):
    """Get overall analytics dashboard for event organizer"""
    try:
        # Get all events created by this user
        events = db.query(Event).filter(Event.created_by == user_id).all()
        
        total_events = len(events)
        total_views = sum(event.view_count for event in events)
        
        # Get total registrations across all events
        total_registrations = db.query(EventRegistration).filter(
            EventRegistration.event_id.in_([e.id for e in events])
        ).count() if events else 0
        
        # Get average rating across all events
        avg_rating = db.query(func.avg(EventFeedback.rating)).filter(
            EventFeedback.event_id.in_([e.id for e in events])
        ).scalar() or 0 if events else 0
        
        # Get top performing events
        event_stats = []
        for event in events:
            reg_count = db.query(EventRegistration).filter(
                EventRegistration.event_id == event.id
            ).count()
            
            event_rating = db.query(func.avg(EventFeedback.rating)).filter(
                EventFeedback.event_id == event.id
            ).scalar() or 0
            
            event_stats.append({
                "id": event.id,
                "title": event.title,
                "date": str(event.date),
                "views": event.view_count,
                "registrations": reg_count,
                "rating": round(float(event_rating), 2) if event_rating else 0
            })
        
        # Sort by registrations
        event_stats.sort(key=lambda x: x["registrations"], reverse=True)
        
        return {
            "success": True,
            "dashboard": {
                "total_events": total_events,
                "total_views": total_views,
                "total_registrations": total_registrations,
                "average_rating": round(float(avg_rating), 2),
                "top_events": event_stats[:5]  # Top 5 events
            }
        }
    except Exception as e:
        logger.error(f"Get dashboard analytics error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Registration Routes
@router.post("/registrations")
async def register_for_event(registration: RegistrationCreate, db: Session = Depends(get_db)):
    """Register for an event"""
    try:
        # Check if event exists
        event = db.query(Event).filter(Event.id == registration.event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Check if already registered
        existing = db.query(EventRegistration).filter(
            EventRegistration.event_id == registration.event_id,
            EventRegistration.user_id == registration.user_id
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Already registered for this event")
        
        # Create registration
        new_registration = EventRegistration(
            event_id=registration.event_id,
            user_id=registration.user_id,
            status="registered"
        )
        
        db.add(new_registration)
        
        # Update event attendee count
        event.attendee_count += 1
        
        # Update analytics
        today = date.today()
        analytics = db.query(EventAnalytics).filter(
            EventAnalytics.event_id == registration.event_id,
            EventAnalytics.date == today
        ).first()
        
        if analytics:
            analytics.registrations += 1
        else:
            analytics = EventAnalytics(
                event_id=registration.event_id,
                date=today,
                registrations=1
            )
            db.add(analytics)
        
        db.commit()
        db.refresh(new_registration)
        
        return {
            "success": True,
            "message": "Successfully registered for event",
            "registration_id": new_registration.id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Event registration error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/registrations/{registration_id}/check-in")
async def check_in_event(registration_id: int, db: Session = Depends(get_db)):
    """Check in to an event"""
    try:
        registration = db.query(EventRegistration).filter(
            EventRegistration.id == registration_id
        ).first()
        
        if not registration:
            raise HTTPException(status_code=404, detail="Registration not found")
        
        registration.status = "attended"
        registration.check_in_time = datetime.utcnow()
        
        # Update analytics
        today = date.today()
        analytics = db.query(EventAnalytics).filter(
            EventAnalytics.event_id == registration.event_id,
            EventAnalytics.date == today
        ).first()
        
        if analytics:
            analytics.attendees += 1
        else:
            analytics = EventAnalytics(
                event_id=registration.event_id,
                date=today,
                attendees=1
            )
            db.add(analytics)
        
        db.commit()
        
        return {
            "success": True,
            "message": "Successfully checked in"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Check-in error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Feedback Routes
@router.post("/feedback")
async def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    """Submit feedback for an event"""
    try:
        # Validate rating
        if feedback.rating < 1 or feedback.rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        # Check if event exists
        event = db.query(Event).filter(Event.id == feedback.event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Check if already submitted feedback
        existing = db.query(EventFeedback).filter(
            EventFeedback.event_id == feedback.event_id,
            EventFeedback.user_id == feedback.user_id
        ).first()
        
        if existing:
            # Update existing feedback
            existing.rating = feedback.rating
            existing.comment = feedback.comment
            existing.created_at = datetime.utcnow()
        else:
            # Create new feedback
            new_feedback = EventFeedback(
                event_id=feedback.event_id,
                user_id=feedback.user_id,
                rating=feedback.rating,
                comment=feedback.comment
            )
            db.add(new_feedback)
        
        db.commit()
        
        return {
            "success": True,
            "message": "Feedback submitted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Submit feedback error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedback/event/{event_id}")
async def get_event_feedback(event_id: int, db: Session = Depends(get_db)):
    """Get all feedback for an event"""
    try:
        feedbacks = db.query(EventFeedback).filter(
            EventFeedback.event_id == event_id
        ).order_by(EventFeedback.created_at.desc()).all()
        
        return {
            "success": True,
            "feedback": [
                {
                    "id": fb.id,
                    "user_id": fb.user_id,
                    "rating": fb.rating,
                    "comment": fb.comment,
                    "created_at": fb.created_at.isoformat()
                }
                for fb in feedbacks
            ]
        }
    except Exception as e:
        logger.error(f"Get feedback error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/events/{event_id}/view")
async def track_event_view(event_id: int, db: Session = Depends(get_db)):
    """Track when someone views an event"""
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Increment view count
        event.view_count += 1
        
        # Update daily analytics
        today = date.today()
        analytics = db.query(EventAnalytics).filter(
            EventAnalytics.event_id == event_id,
            EventAnalytics.date == today
        ).first()
        
        if analytics:
            analytics.views += 1
        else:
            analytics = EventAnalytics(
                event_id=event_id,
                date=today,
                views=1
            )
            db.add(analytics)
        
        db.commit()
        
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Track view error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Task Management Routes
@router.get("/stages")
async def get_stages(db: Session = Depends(get_db)):
    """Get all event stages"""
    try:
        stages = db.query(EventStage).order_by(EventStage.order).all()
        
        return {
            "success": True,
            "stages": [
                {
                    "id": stage.id,
                    "name": stage.name,
                    "description": stage.description,
                    "order": stage.order
                }
                for stage in stages
            ]
        }
    except Exception as e:
        logger.error(f"Get stages error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stages")
async def create_stage(stage: StageCreate, db: Session = Depends(get_db)):
    """Create a new event stage"""
    try:
        new_stage = EventStage(
            name=stage.name,
            description=stage.description,
            order=stage.order
        )
        
        db.add(new_stage)
        db.commit()
        db.refresh(new_stage)
        
        return {
            "success": True,
            "message": "Stage created successfully",
            "stage": {
                "id": new_stage.id,
                "name": new_stage.name,
                "description": new_stage.description,
                "order": new_stage.order
            }
        }
    except Exception as e:
        logger.error(f"Create stage error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/{event_id}/tasks")
async def get_event_tasks(event_id: int, stage_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Get all tasks for an event, optionally filtered by stage"""
    try:
        # Verify event exists
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Build query
        query = db.query(EventTask).filter(EventTask.event_id == event_id)
        
        if stage_id:
            query = query.filter(EventTask.stage_id == stage_id)
        
        tasks = query.order_by(EventTask.created_at.desc()).all()
        
        return {
            "success": True,
            "tasks": [
                {
                    "id": task.id,
                    "event_id": task.event_id,
                    "stage_id": task.stage_id,
                    "title": task.title,
                    "description": task.description,
                    "is_completed": task.is_completed,
                    "priority": task.priority,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "assigned_to": task.assigned_to,
                    "created_by": task.created_by,
                    "created_at": task.created_at.isoformat(),
                    "completed_at": task.completed_at.isoformat() if task.completed_at else None
                }
                for task in tasks
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get event tasks error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tasks")
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task for an event"""
    try:
        # Verify event exists
        event = db.query(Event).filter(Event.id == task.event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Verify stage exists if provided
        if task.stage_id:
            stage = db.query(EventStage).filter(EventStage.id == task.stage_id).first()
            if not stage:
                raise HTTPException(status_code=404, detail="Stage not found")
        
        new_task = EventTask(
            event_id=task.event_id,
            stage_id=task.stage_id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            due_date=task.due_date,
            assigned_to=task.assigned_to,
            created_by=task.created_by
        )
        
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        return {
            "success": True,
            "message": "Task created successfully",
            "task": {
                "id": new_task.id,
                "event_id": new_task.event_id,
                "stage_id": new_task.stage_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_completed": new_task.is_completed,
                "priority": new_task.priority,
                "due_date": new_task.due_date.isoformat() if new_task.due_date else None,
                "created_at": new_task.created_at.isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create task error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/tasks/{task_id}")
async def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    """Update a task"""
    try:
        task = db.query(EventTask).filter(EventTask.id == task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Update fields if provided
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.is_completed is not None:
            task.is_completed = task_data.is_completed
            if task_data.is_completed:
                task.completed_at = datetime.utcnow()
            else:
                task.completed_at = None
        if task_data.priority is not None:
            task.priority = task_data.priority
        if task_data.due_date is not None:
            task.due_date = task_data.due_date
        if task_data.stage_id is not None:
            task.stage_id = task_data.stage_id
        if task_data.assigned_to is not None:
            task.assigned_to = task_data.assigned_to
        
        db.commit()
        db.refresh(task)
        
        return {
            "success": True,
            "message": "Task updated successfully",
            "task": {
                "id": task.id,
                "title": task.title,
                "is_completed": task.is_completed,
                "priority": task.priority,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update task error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    try:
        task = db.query(EventTask).filter(EventTask.id == task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        db.delete(task)
        db.commit()
        
        return {
            "success": True,
            "message": "Task deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete task error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tasks/{task_id}/toggle")
async def toggle_task_completion(task_id: int, db: Session = Depends(get_db)):
    """Toggle task completion status"""
    try:
        task = db.query(EventTask).filter(EventTask.id == task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task.is_completed = not task.is_completed
        task.completed_at = datetime.utcnow() if task.is_completed else None
        
        db.commit()
        db.refresh(task)
        
        return {
            "success": True,
            "message": "Task status updated",
            "is_completed": task.is_completed
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Toggle task error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Notification Routes
@router.post("/push-tokens")
async def register_push_token(token_data: PushTokenCreate, db: Session = Depends(get_db)):
    """Register or update a push notification token for a user"""
    try:
        # Check if token already exists
        existing_token = db.query(PushToken).filter(PushToken.token == token_data.token).first()
        
        if existing_token:
            existing_token.user_id = token_data.user_id
            existing_token.device_type = token_data.device_type
            existing_token.is_active = True
            existing_token.updated_at = datetime.utcnow()
        else:
            new_token = PushToken(
                user_id=token_data.user_id,
                token=token_data.token,
                device_type=token_data.device_type
            )
            db.add(new_token)
        
        db.commit()
        
        return {
            "success": True,
            "message": "Push token registered successfully"
        }
    except Exception as e:
        logger.error(f"Register push token error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/notifications/{user_id}")
async def get_user_notifications(user_id: int, unread_only: bool = False, db: Session = Depends(get_db)):
    """Get notifications for a user"""
    try:
        query = db.query(Notification).filter(Notification.user_id == user_id)
        
        if unread_only:
            query = query.filter(Notification.is_read == False)
        
        notifications = query.order_by(Notification.sent_at.desc()).all()
        
        return {
            "success": True,
            "notifications": [
                {
                    "id": notif.id,
                    "title": notif.title,
                    "message": notif.message,
                    "type": notif.type,
                    "event_id": notif.event_id,
                    "is_read": notif.is_read,
                    "sent_at": notif.sent_at.isoformat(),
                    "read_at": notif.read_at.isoformat() if notif.read_at else None,
                    "data": json.loads(notif.data) if notif.data else None
                }
                for notif in notifications
            ]
        }
    except Exception as e:
        logger.error(f"Get notifications error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/notifications")
async def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    """Create a new notification"""
    try:
        new_notification = Notification(
            user_id=notification.user_id,
            event_id=notification.event_id,
            title=notification.title,
            message=notification.message,
            type=notification.type,
            data=notification.data
        )
        
        db.add(new_notification)
        db.commit()
        db.refresh(new_notification)
        
        return {
            "success": True,
            "message": "Notification created successfully",
            "notification_id": new_notification.id
        }
    except Exception as e:
        logger.error(f"Create notification error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: int, db: Session = Depends(get_db)):
    """Mark a notification as read"""
    try:
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        notification.is_read = True
        notification.read_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "success": True,
            "message": "Notification marked as read"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Mark notification read error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/notifications/{user_id}/read-all")
async def mark_all_notifications_read(user_id: int, db: Session = Depends(get_db)):
    """Mark all notifications as read for a user"""
    try:
        db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({
            "is_read": True,
            "read_at": datetime.utcnow()
        })
        
        db.commit()
        
        return {
            "success": True,
            "message": "All notifications marked as read"
        }
    except Exception as e:
        logger.error(f"Mark all read error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reminders")
async def create_reminder(reminder: ReminderCreate, db: Session = Depends(get_db)):
    """Create an event reminder"""
    try:
        # Check if reminder already exists
        existing = db.query(EventReminder).filter(
            EventReminder.event_id == reminder.event_id,
            EventReminder.user_id == reminder.user_id,
            EventReminder.reminder_type == reminder.reminder_type
        ).first()
        
        if existing:
            return {
                "success": True,
                "message": "Reminder already exists",
                "reminder_id": existing.id
            }
        
        new_reminder = EventReminder(
            event_id=reminder.event_id,
            user_id=reminder.user_id,
            remind_at=reminder.remind_at,
            reminder_type=reminder.reminder_type
        )
        
        db.add(new_reminder)
        db.commit()
        db.refresh(new_reminder)
        
        return {
            "success": True,
            "message": "Reminder created successfully",
            "reminder_id": new_reminder.id
        }
    except Exception as e:
        logger.error(f"Create reminder error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reminders/{event_id}/{user_id}")
async def get_event_reminders(event_id: int, user_id: int, db: Session = Depends(get_db)):
    """Get reminders for an event and user"""
    try:
        reminders = db.query(EventReminder).filter(
            EventReminder.event_id == event_id,
            EventReminder.user_id == user_id
        ).all()
        
        return {
            "success": True,
            "reminders": [
                {
                    "id": reminder.id,
                    "reminder_type": reminder.reminder_type,
                    "remind_at": reminder.remind_at.isoformat(),
                    "is_sent": reminder.is_sent
                }
                for reminder in reminders
            ]
        }
    except Exception as e:
        logger.error(f"Get reminders error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/reminders/{reminder_id}")
async def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """Delete an event reminder"""
    try:
        reminder = db.query(EventReminder).filter(EventReminder.id == reminder_id).first()
        
        if not reminder:
            raise HTTPException(status_code=404, detail="Reminder not found")
        
        db.delete(reminder)
        db.commit()
        
        return {
            "success": True,
            "message": "Reminder deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete reminder error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
