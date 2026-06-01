# create_admin.py
import sys
import getpass
import re
from database import SessionLocal
from models import User, Base
from auth import hash_password
from database import engine

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Returns: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    return True, ""

def create_admin_user():
    """Interactive admin user creation with validation"""
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create a database session
    db = SessionLocal()
    
    try:
        print("=" * 50)
        print("Create Admin User")
        print("=" * 50)
        
        # Get username
        while True:
            username = input("\nEnter admin username (default: admin): ").strip()
            if not username:
                username = "admin"
            
            # Check if user already exists
            existing_user = db.query(User).filter(User.username == username).first()
            if existing_user:
                print(f"❌ User '{username}' already exists!")
                print(f"   Email: {existing_user.email}")
                print(f"   Admin: {existing_user.is_admin}")
                print(f"   Active: {existing_user.is_active}")
                
                overwrite = input("\nDo you want to create a different user? (yes/no): ").strip().lower()
                if overwrite in ['yes', 'y']:
                    continue
                else:
                    return
            break
        
        # Get email
        while True:
            email = input("Enter admin email: ").strip()
            if not email:
                print("❌ Email cannot be empty!")
                continue
            if not validate_email(email):
                print("❌ Invalid email format!")
                continue
            
            # Check if email already exists
            existing_email = db.query(User).filter(User.email == email).first()
            if existing_email:
                print(f"❌ Email '{email}' is already in use!")
                continue
            break
        
        # Get password
        while True:
            password = getpass.getpass("Enter admin password: ")
            if not password:
                print("❌ Password cannot be empty!")
                continue
            
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"❌ {error_msg}")
                print("\nPassword requirements:")
                print("  • At least 8 characters long")
                print("  • At least one uppercase letter")
                print("  • At least one lowercase letter")
                print("  • At least one digit")
                continue
            
            password_confirm = getpass.getpass("Confirm password: ")
            if password != password_confirm:
                print("❌ Passwords do not match!")
                continue
            break
        
        # Create admin user
        admin_user = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            is_active=True,
            is_admin=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("\n" + "=" * 50)
        print("✅ Admin user created successfully!")
        print("=" * 50)
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Admin: Yes")
        print(f"Active: Yes")
        print("\nYou can now login to the admin panel!")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error creating admin user: {str(e)}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()

