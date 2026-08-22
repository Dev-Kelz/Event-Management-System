from app.models import Event


def list_events(db):
    return db.query(Event).order_by(Event.created_at.desc()).all()
