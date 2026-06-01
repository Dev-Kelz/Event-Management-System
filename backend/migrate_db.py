# migrate_db.py
"""
Database migration script to add missing columns
"""
import os
from sqlalchemy import text
from database import engine, SessionLocal
from models import Base

def migrate_database():
    """Add missing columns to database tables"""
    
    db = SessionLocal()
    
    try:
        print("=" * 50)
        print("Database Migration")
        print("=" * 50)
        
        # Migrate users table - add is_admin column
        print("\n[INFO] Checking users table...")
        check_query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='is_admin'
        """)
        
        result = db.execute(check_query).fetchone()
        
        if result:
            print("[INFO] Column 'is_admin' already exists in users table.")
        else:
            print("[INFO] Adding 'is_admin' column to users table...")
            alter_query = text("""
                ALTER TABLE users 
                ADD COLUMN is_admin BOOLEAN DEFAULT FALSE
            """)
            db.execute(alter_query)
            db.commit()
            print("[SUCCESS] Column 'is_admin' added successfully!")
        
        # Migrate events table - add time column
        print("\n[INFO] Checking events table for 'time' column...")
        check_time = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='events' AND column_name='time'
        """)
        
        if db.execute(check_time).fetchone():
            print("[INFO] Column 'time' already exists in events table.")
        else:
            print("[INFO] Adding 'time' column to events table...")
            alter_query = text("""
                ALTER TABLE events 
                ADD COLUMN time VARCHAR(5)
            """)
            db.execute(alter_query)
            db.commit()
            print("[SUCCESS] Column 'time' added successfully!")
        
        # Migrate events table - add view_count column
        print("\n[INFO] Checking events table for 'view_count' column...")
        check_view_count = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='events' AND column_name='view_count'
        """)
        
        if db.execute(check_view_count).fetchone():
            print("[INFO] Column 'view_count' already exists in events table.")
        else:
            print("[INFO] Adding 'view_count' column to events table...")
            alter_query = text("""
                ALTER TABLE events 
                ADD COLUMN view_count INTEGER DEFAULT 0
            """)
            db.execute(alter_query)
            db.commit()
            print("[SUCCESS] Column 'view_count' added successfully!")
        
        # Migrate events table - add attendee_count column
        print("\n[INFO] Checking events table for 'attendee_count' column...")
        check_attendee_count = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='events' AND column_name='attendee_count'
        """)
        
        if db.execute(check_attendee_count).fetchone():
            print("[INFO] Column 'attendee_count' already exists in events table.")
        else:
            print("[INFO] Adding 'attendee_count' column to events table...")
            alter_query = text("""
                ALTER TABLE events 
                ADD COLUMN attendee_count INTEGER DEFAULT 0
            """)
            db.execute(alter_query)
            db.commit()
            print("[SUCCESS] Column 'attendee_count' added successfully!")
        
        # Also ensure all other columns exist
        print("\n[INFO] Verifying database schema...")
        Base.metadata.create_all(bind=engine)
        print("[SUCCESS] Database schema verified!")
        
        print("\n" + "=" * 50)
        print("Migration completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n[ERROR] Migration failed: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    migrate_database()
