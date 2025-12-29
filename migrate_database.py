"""
Database Migration Script
Adds latitude and longitude columns to the feedback table.
"""

from src.database import Database
from sqlalchemy import text


def migrate():
    """Add latitude and longitude columns to feedback table."""
    print("🔄 Starting database migration...")
    
    try:
        # Initialize database connection
        Database.initialize()
        print("✅ Connected to database")
        
        # Add columns
        with Database.session_scope() as session:
            # Check if columns exist
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='feedback' 
                AND column_name IN ('latitude', 'longitude');
            """)
            
            result = session.execute(check_query)
            existing_columns = [row[0] for row in result]
            
            if 'latitude' in existing_columns and 'longitude' in existing_columns:
                print("✅ Columns already exist - no migration needed")
                return
            
            # Add latitude column
            if 'latitude' not in existing_columns:
                print("⏳ Adding latitude column...")
                session.execute(text("""
                    ALTER TABLE feedback 
                    ADD COLUMN latitude FLOAT;
                """))
                session.execute(text("""
                    CREATE INDEX idx_feedback_latitude ON feedback(latitude);
                """))
                print("✅ Added latitude column with index")
            
            # Add longitude column
            if 'longitude' not in existing_columns:
                print("⏳ Adding longitude column...")
                session.execute(text("""
                    ALTER TABLE feedback 
                    ADD COLUMN longitude FLOAT;
                """))
                session.execute(text("""
                    CREATE INDEX idx_feedback_longitude ON feedback(longitude);
                """))
                print("✅ Added longitude column with index")
            
            session.commit()
            print("✅ Migration completed successfully!")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure PostgreSQL is running")
        print("2. Check database connection in data/db_config.json")
        print("3. Verify you have ALTER TABLE permissions")
        raise


if __name__ == "__main__":
    migrate()
