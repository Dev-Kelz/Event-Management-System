import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from database import engine, SessionLocal
from models import Base, User, Event
from auth import hash_password, verify_password
from config import settings
from routes import router

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.is_production else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create tables
logger.info("Creating database tables...")
Base.metadata.create_all(bind=engine)
logger.info("Database tables created successfully")

app = FastAPI(
    title="FastAPI Admin",
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware with secure settings
app.add_middleware(
    SessionMiddleware, 
    secret_key=settings.SECRET_KEY,
    max_age=settings.SESSION_MAX_AGE,
    https_only=settings.is_production  # Only send cookies over HTTPS in production
)

# Include API routes
app.include_router(router, prefix="/api")

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form.get("username"), form.get("password")
        
        if not username or not password:
            logger.warning("Login attempt with missing credentials")
            return False

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            
            if not user:
                logger.warning(f"Login attempt for non-existent user: {username}")
                return False
            
            if not user.is_active:
                logger.warning(f"Login attempt for inactive user: {username}")
                return False
            
            password_valid = verify_password(password, user.hashed_password)

            if not password_valid or not user.is_admin:
                logger.warning(f"Failed login attempt for user: {username}")
                return False

            request.session.update({"user": username})
            logger.info(f"Successful login for user: {username}")
            return True
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            return False
        finally:
            db.close()

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        user = request.session.get("user")
        return bool(user)
    

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.is_active, User.is_admin]
    column_searchable_list = [User.username, User.email]
    column_sortable_list = [User.id, User.username]
    
    # Hide password in detail views
    column_details_exclude_list = [User.hashed_password]
    
    # Show hashed_password field in forms but with password widget
    form_widget_args = {
        "hashed_password": {
            "type": "password"
        }
    }
    
    form_args = {
        "hashed_password": {
            "label": "Password",
            "description": "Enter the user's password (it will be hashed automatically)"
        }
    }
    
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    
    async def on_model_change(self, data, model, is_created, request):
        # Handle password hashing on create/update
        if "hashed_password" in data and data["hashed_password"]:
            password = data["hashed_password"]
            # Only hash if it's not already hashed
            # Bcrypt hashes are always 60 characters and start with $2
            if len(password) != 60 or not password.startswith("$2"):
                try:
                    data["hashed_password"] = hash_password(password)
                    logger.info(f"Password hashed for user: {data.get('username', 'unknown')}")
                except Exception as e:
                    logger.error(f"Error hashing password: {str(e)}")
                    raise ValueError("Failed to hash password")
        return data

    async def on_model_delete(self, model, request):
        """Handle user deletion and cascade to related records"""
        from models import Event, EventRegistration, EventFeedback
        
        db = SessionLocal()
        try:
            user_id = model.id
            
            # Delete related records
            # Delete user's feedback
            db.query(EventFeedback).filter(EventFeedback.user_id == user_id).delete()
            
            # Delete user's event registrations
            db.query(EventRegistration).filter(EventRegistration.user_id == user_id).delete()
            
            # Delete or reassign events created by this user
            # Option 1: Delete events (uncomment if you want to delete)
            # db.query(Event).filter(Event.created_by == user_id).delete()
            
            # Option 2: Set created_by to NULL or another admin (safer)
            events = db.query(Event).filter(Event.created_by == user_id).all()
            if events:
                # Find first admin user to reassign events to
                admin_user = db.query(User).filter(User.is_admin == True, User.id != user_id).first()
                if admin_user:
                    for event in events:
                        event.created_by = admin_user.id
                    logger.info(f"Reassigned {len(events)} events from user {user_id} to admin {admin_user.id}")
                else:
                    # No other admin, delete the events
                    db.query(Event).filter(Event.created_by == user_id).delete()
                    logger.warning(f"Deleted {len(events)} events - no admin to reassign to")
            
            db.commit()
            logger.info(f"Successfully deleted user {model.username} and related records")
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting user: {str(e)}")
            raise ValueError(f"Cannot delete user: {str(e)}")
        finally:
            db.close()

    def is_accessible(self, request: Request) -> bool:
        return request.session.get("user") is not None


class EventAdmin(ModelView, model=Event):
    column_list = [Event.id, Event.title, Event.date, Event.location, Event.created_by, Event.created_at]
    column_searchable_list = [Event.title, Event.location]
    column_sortable_list = [Event.id, Event.title, Event.date, Event.created_at]
    column_default_sort = (Event.created_at, True)  # Sort by created_at descending
    
    name = "Event"
    name_plural = "Events"
    icon = "fa-solid fa-calendar"
    
    def is_accessible(self, request: Request) -> bool:
        return request.session.get("user") is not None


# Create authentication backend and admin panel
authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(EventAdmin)

logger.info(f"Admin panel initialized in {settings.ENVIRONMENT} mode")
