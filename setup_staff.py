"""
Setup Staff Table and Add Initial Staff Data
Creates the staff table and adds sample staff members.
"""

from src.database import Database
from src.data_manager import DataManager
from src.db_models import Base, Staff

def setup_staff_table():
    """Create staff table and add initial data."""
    print("Setting up staff management...")
    
    try:
        # Initialize database
        Database.initialize()
        
        # Create tables (including new Staff table)
        Base.metadata.create_all(Database._engine)
        print("✓ Staff table created")
        
        # Initialize data manager
        dm = DataManager()
        
        # Check if staff already exist
        existing_staff = dm.get_all_staff(active_only=False)
        if existing_staff:
            print(f"✓ {len(existing_staff)} staff members already exist")
            print("\nExisting staff:")
            for staff in existing_staff:
                print(f"  - {staff['name']} ({staff['department']}) - {staff['active']}")
            return
        
        # Add initial staff members
        staff_data = [
            {
                'name': 'John Anderson',
                'email': 'john.anderson@city.gov',
                'phone': '+1-555-0101',
                'department': 'Public Works',
                'role': 'Senior Inspector',
                'active': 'Active'
            },
            {
                'name': 'Sarah Martinez',
                'email': 'sarah.martinez@city.gov',
                'phone': '+1-555-0102',
                'department': 'Public Safety',
                'role': 'Safety Coordinator',
                'active': 'Active'
            },
            {
                'name': 'Michael Chen',
                'email': 'michael.chen@city.gov',
                'phone': '+1-555-0103',
                'department': 'Transportation',
                'role': 'Traffic Manager',
                'active': 'Active'
            },
            {
                'name': 'Emily Johnson',
                'email': 'emily.johnson@city.gov',
                'phone': '+1-555-0104',
                'department': 'Parks & Recreation',
                'role': 'Facilities Manager',
                'active': 'Active'
            },
            {
                'name': 'David Williams',
                'email': 'david.williams@city.gov',
                'phone': '+1-555-0105',
                'department': 'Environmental Services',
                'role': 'Environmental Specialist',
                'active': 'Active'
            },
            {
                'name': 'Lisa Brown',
                'email': 'lisa.brown@city.gov',
                'phone': '+1-555-0106',
                'department': 'Community Development',
                'role': 'Community Liaison',
                'active': 'Active'
            },
        ]
        
        print("\nAdding staff members...")
        for staff in staff_data:
            staff_id = dm.add_staff(staff)
            if staff_id:
                print(f"✓ Added: {staff['name']} ({staff['department']})")
            else:
                print(f"✗ Failed to add: {staff['name']}")
        
        print("\n✓ Staff setup complete!")
        print(f"✓ Added {len(staff_data)} staff members")
        
        # Display all staff
        all_staff = dm.get_all_staff()
        print(f"\nActive staff members ({len(all_staff)}):")
        for staff in all_staff:
            print(f"  • {staff['name']} - {staff['department']} ({staff['role']})")
        
    except Exception as e:
        print(f"✗ Error setting up staff: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_staff_table()
