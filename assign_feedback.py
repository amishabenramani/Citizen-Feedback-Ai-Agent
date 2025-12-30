"""
Assign Feedback to Staff Members Based on Category
Proper workflow: Assign feedback before moving to In Progress or Closed
"""

from src.data_manager import DataManager

def assign_feedback_to_staff():
    """
    Assign feedback to staff members based on their department/category.
    This ensures proper workflow - items must be assigned before moving to In Progress/Closed.
    """
    print("Assigning feedback to staff members...")
    
    try:
        dm = DataManager()
        
        # Get all feedback
        df = dm.get_feedback_dataframe()
        
        # Get all staff
        all_staff = dm.get_all_staff(active_only=True)
        staff_dict = {s['name']: s for s in all_staff}
        
        # Define category to staff mapping
        category_staff_mapping = {
            'Roads & Infrastructure': 'John Anderson',  # Public Works
            'Parks & Recreation': 'Emily Johnson',  # Parks & Recreation
            'Transportation': 'Michael Chen',  # Transportation
            'Public Safety': 'Sarah Martinez',  # Public Safety
            'Environmental Services': 'David Williams',  # Environmental Services
            'Community Development': 'Lisa Brown',  # Community Development
            'Sanitation': 'David Williams',  # Environmental Services
        }
        
        print("\nAssigning feedback to staff...")
        assigned_count = 0
        
        for _, row in df.iterrows():
            feedback_id = row['id']
            current_assigned = row.get('assigned_to', '')
            category = row.get('category', 'Unknown')
            status = row.get('status', 'New')
            
            # Determine which staff should be assigned
            staff_name = category_staff_mapping.get(category)
            
            if not staff_name:
                # Default to the first available staff for unknown categories
                staff_name = list(staff_dict.keys())[0] if staff_dict else None
            
            # Only assign if not already assigned
            if staff_name and (not current_assigned or current_assigned == ''):
                # Update assignment
                dm.update_feedback(feedback_id, {'assigned_to': staff_name})
                assigned_count += 1
                print(f"✓ Assigned '{row.get('title', 'Untitled')}' → {staff_name} ({category})")
        
        print(f"\n✓ Successfully assigned {assigned_count} feedback items to staff!")
        
        # Display summary
        print("\nAssignment Summary:")
        for staff_name, staff in staff_dict.items():
            assigned_feedback = df[df['assigned_to'] == staff_name]
            count = len(assigned_feedback)
            if count > 0:
                print(f"  • {staff_name} ({staff.get('department', 'N/A')}): {count} items")
        
    except Exception as e:
        print(f"✗ Error assigning feedback: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    assign_feedback_to_staff()
