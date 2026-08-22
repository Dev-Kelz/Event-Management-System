from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String

from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    location = Column(String(255), nullable=True)
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    view_count = Column(Integer, default=0)
    attendee_count = Column(Integer, default=0)


class EventRegistration(Base):
    __tablename__ = "event_registrations"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="registered")
    check_in_time = Column(DateTime, nullable=True)


class EventFeedback(Base):
    __tablename__ = "event_feedback"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class EventAnalytics(Base):
    __tablename__ = "event_analytics"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    views = Column(Integer, default=0)
    registrations = Column(Integer, default=0)
    attendees = Column(Integer, default=0)
    shares = Column(Integer, default=0)


class EventReminder(Base):
    __tablename__ = "event_reminders"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    remind_at = Column(DateTime, nullable=False)
    reminder_type = Column(String(50), nullable=False)
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
