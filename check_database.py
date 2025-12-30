"""
Check Database Tables and Structure
Shows all tables in the database with their structure
"""

from src.database import Database
from sqlalchemy import inspect

def check_database_tables():
    """Check and display all tables in the database."""
    print("Checking database structure...")
    print("="*60)
    
    try:
        # Initialize database
        Database.initialize()
        
        # Create inspector
        inspector = inspect(Database._engine)
        
        # Get all table names
        table_names = inspector.get_table_names()
        
        print(f"\n📊 Total Tables: {len(table_names)}")
        print("="*60)
        
        if not table_names:
            print("No tables found in database!")
            return
        
        # Show each table and its columns
        for i, table_name in enumerate(table_names, 1):
            print(f"\n{i}. TABLE: {table_name.upper()}")
            print("-"*60)
            
            # Get columns
            columns = inspector.get_columns(table_name)
            print(f"   Columns ({len(columns)}):")
            
            for col in columns:
                col_name = col['name']
                col_type = str(col['type'])
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                primary = "PRIMARY KEY" if col.get('primary_key') else ""
                
                print(f"   - {col_name:20} {col_type:20} {nullable:10} {primary}")
            
            # Get indexes
            indexes = inspector.get_indexes(table_name)
            if indexes:
                print(f"\n   Indexes ({len(indexes)}):")
                for idx in indexes:
                    cols = ', '.join(idx['column_names'])
                    unique = "UNIQUE" if idx['unique'] else ""
                    print(f"   - {idx['name']}: ({cols}) {unique}")
            
            # Get foreign keys
            fks = inspector.get_foreign_keys(table_name)
            if fks:
                print(f"\n   Foreign Keys ({len(fks)}):")
                for fk in fks:
                    print(f"   - {fk['constrained_columns']} → {fk['referred_table']}.{fk['referred_columns']}")
        
        print("\n" + "="*60)
        print("Database Structure Summary:")
        print("="*60)
        
        # Count total columns
        total_columns = sum(len(inspector.get_columns(t)) for t in table_names)
        print(f"Total Tables:  {len(table_names)}")
        print(f"Total Columns: {total_columns}")
        
        # Show table purposes
        print("\nTable Purposes:")
        print("-"*60)
        if 'feedback' in table_names:
            print("✓ feedback        - Stores citizen feedback/complaints")
        if 'staff' in table_names:
            print("✓ staff           - Stores staff member information")
        
        print("\n✅ Database check complete!")
        
    except Exception as e:
        print(f"✗ Error checking database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database_tables()
