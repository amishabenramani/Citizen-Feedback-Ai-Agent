"""
Add Sample Feedback Data
Creates 10 realistic feedback entries in the database.
"""

from src.data_manager import DataManager
from datetime import datetime, timedelta
import random

def add_sample_feedback():
    """Add 10 sample feedback entries."""
    print("Adding sample feedback data...")
    
    try:
        dm = DataManager()
        
        # Sample feedback data
        feedback_samples = [
            {
                'title': 'Pothole on Main Street',
                'feedback': 'There is a large pothole on Main Street near the intersection with Oak Avenue. It is getting worse and is a safety hazard for cyclists and vehicles.',
                'name': 'Robert Jackson',
                'email': 'robert.jackson@email.com',
                'phone': '+1-555-1001',
                'category': 'Roads & Infrastructure',
                'feedback_type': 'Complaint',
                'urgency': 'High',
                'area': 'Downtown',
                'address': '234 Main Street',
                'status': 'New',
                'sentiment': 'Negative',
                'sentiment_score': 0.15,
                'keywords': ['pothole', 'road', 'safety', 'hazard'],
                'summary': 'Report of dangerous pothole on Main Street requiring immediate repair',
                'latitude': 40.7128,
                'longitude': -74.0060
            },
            {
                'title': 'Park Maintenance Issues',
                'feedback': 'Central Park needs better maintenance. The playground equipment is rusty and the grass area needs mowing. Overall condition has deteriorated.',
                'name': 'Michelle Davis',
                'email': 'michelle.davis@email.com',
                'phone': '+1-555-1002',
                'category': 'Parks & Recreation',
                'feedback_type': 'Complaint',
                'urgency': 'Medium',
                'area': 'Central Park',
                'address': 'Central Park',
                'status': 'In Review',
                'sentiment': 'Negative',
                'sentiment_score': 0.25,
                'keywords': ['park', 'maintenance', 'equipment', 'grass'],
                'summary': 'Park maintenance concerns - rusty equipment and unkempt grounds',
                'latitude': 40.7829,
                'longitude': -73.9654
            },
            {
                'title': 'Excellent Public Transportation Service',
                'feedback': 'I want to commend the bus drivers for their professionalism and courtesy. They always greet passengers with a smile and maintain the buses very well.',
                'name': 'James Wilson',
                'email': 'james.wilson@email.com',
                'phone': '+1-555-1003',
                'category': 'Transportation',
                'feedback_type': 'Praise',
                'urgency': 'Low',
                'area': 'Downtown Transit Hub',
                'address': '123 Transit Center',
                'status': 'Closed',
                'sentiment': 'Positive',
                'sentiment_score': 0.92,
                'keywords': ['bus', 'service', 'driver', 'professional', 'excellent'],
                'summary': 'Positive feedback about bus service and driver professionalism',
                'latitude': 40.7505,
                'longitude': -73.9972
            },
            {
                'title': 'Street Light Outage on Oak Avenue',
                'feedback': 'Multiple street lights are out on Oak Avenue between 5th and 7th Street. This creates a dark and unsafe area, especially at night.',
                'name': 'Sarah Thompson',
                'email': 'sarah.thompson@email.com',
                'phone': '+1-555-1004',
                'category': 'Public Safety',
                'feedback_type': 'Complaint',
                'urgency': 'High',
                'area': 'Oak Avenue',
                'address': 'Oak Avenue between 5th-7th St',
                'status': 'In Progress',
                'sentiment': 'Negative',
                'sentiment_score': 0.20,
                'keywords': ['lights', 'safety', 'dark', 'street'],
                'summary': 'Emergency report: Multiple street lights out creating safety hazard',
                'latitude': 40.7489,
                'longitude': -73.9680
            },
            {
                'title': 'Water Quality Complaint',
                'feedback': 'The water quality from my tap has been poor lately. It has a brown tint and unusual smell. I am concerned about health and safety.',
                'name': 'David Anderson',
                'email': 'david.anderson@email.com',
                'phone': '+1-555-1005',
                'category': 'Environmental Services',
                'feedback_type': 'Complaint',
                'urgency': 'Critical',
                'area': 'Residential District A',
                'address': '456 Elm Street',
                'status': 'New',
                'sentiment': 'Negative',
                'sentiment_score': 0.10,
                'keywords': ['water', 'quality', 'health', 'safety', 'contamination'],
                'summary': 'Critical: Water quality issue - brown water with unusual odor',
                'latitude': 40.7614,
                'longitude': -73.9776
            },
            {
                'title': 'Suggestion: More Public WiFi Hotspots',
                'feedback': 'It would be great if the city could install more public WiFi hotspots in parks and community centers. This would help residents stay connected.',
                'name': 'Jennifer Lee',
                'email': 'jennifer.lee@email.com',
                'phone': '+1-555-1006',
                'category': 'Community Development',
                'feedback_type': 'Suggestion',
                'urgency': 'Low',
                'area': 'Downtown',
                'address': 'Multiple Locations',
                'status': 'New',
                'sentiment': 'Positive',
                'sentiment_score': 0.68,
                'keywords': ['wifi', 'connectivity', 'public', 'suggestion'],
                'summary': 'Suggestion for expanding public WiFi infrastructure',
                'latitude': 40.7128,
                'longitude': -74.0060
            },
            {
                'title': 'Trash Collection Delay',
                'feedback': 'Trash collection has been delayed by 2 days this week. This is causing overflow issues and attracting rodents. Please maintain schedule.',
                'name': 'Michael Chen',
                'email': 'michael.chen@email.com',
                'phone': '+1-555-1007',
                'category': 'Sanitation',
                'feedback_type': 'Complaint',
                'urgency': 'High',
                'area': 'Commercial District',
                'address': '789 Business Ave',
                'status': 'In Review',
                'sentiment': 'Negative',
                'sentiment_score': 0.22,
                'keywords': ['trash', 'collection', 'delay', 'sanitation'],
                'summary': 'Complaint about delayed trash collection causing overflow',
                'latitude': 40.7505,
                'longitude': -73.9747
            },
            {
                'title': 'Community Center Hours Extension',
                'feedback': 'Could the community center extend their hours on weekends? Many working residents would benefit from later availability for evening programs.',
                'name': 'Amanda White',
                'email': 'amanda.white@email.com',
                'phone': '+1-555-1008',
                'category': 'Parks & Recreation',
                'feedback_type': 'Suggestion',
                'urgency': 'Medium',
                'area': 'North District',
                'address': 'North Community Center',
                'status': 'In Review',
                'sentiment': 'Neutral',
                'sentiment_score': 0.55,
                'keywords': ['hours', 'community', 'center', 'weekend'],
                'summary': 'Request to extend community center weekend hours',
                'latitude': 40.7800,
                'longitude': -73.9500
            },
            {
                'title': 'Traffic Signal Malfunction',
                'feedback': 'The traffic signal at the corner of 5th and Main has been stuck on red for vehicles for several minutes. This is causing major congestion.',
                'name': 'Christopher Garcia',
                'email': 'christopher.garcia@email.com',
                'phone': '+1-555-1009',
                'category': 'Transportation',
                'feedback_type': 'Complaint',
                'urgency': 'High',
                'area': 'Downtown',
                'address': '5th and Main Street',
                'status': 'In Progress',
                'sentiment': 'Negative',
                'sentiment_score': 0.18,
                'keywords': ['traffic', 'signal', 'congestion', 'malfunction'],
                'summary': 'Traffic signal malfunction causing congestion',
                'latitude': 40.7200,
                'longitude': -74.0020
            },
            {
                'title': 'Community Garden Success',
                'feedback': 'The new community garden has been wonderful for the neighborhood. It brings people together and provides fresh produce. Great initiative!',
                'name': 'Linda Martinez',
                'email': 'linda.martinez@email.com',
                'phone': '+1-555-1010',
                'category': 'Community Development',
                'feedback_type': 'Praise',
                'urgency': 'Low',
                'area': 'West Side',
                'address': 'West Side Community Garden',
                'status': 'Closed',
                'sentiment': 'Positive',
                'sentiment_score': 0.88,
                'keywords': ['garden', 'community', 'fresh', 'initiative', 'wonderful'],
                'summary': 'Positive feedback on community garden project',
                'latitude': 40.7300,
                'longitude': -74.0100
            }
        ]
        
        print("\nAdding feedback entries...")
        for i, feedback in enumerate(feedback_samples, 1):
            feedback_id = dm.add_feedback(feedback)
            if feedback_id:
                print(f"✓ Added feedback #{i}: {feedback['title']}")
            else:
                print(f"✗ Failed to add feedback #{i}")
        
        print(f"\n✓ Successfully added {len(feedback_samples)} feedback entries!")
        
        # Display summary
        df = dm.get_feedback_dataframe()
        print(f"\nDatabase Summary:")
        print(f"  Total Feedback: {len(df)}")
        if 'status' in df.columns:
            print(f"  By Status: {df['status'].value_counts().to_dict()}")
        if 'urgency' in df.columns:
            print(f"  By Urgency: {df['urgency'].value_counts().to_dict()}")
        if 'sentiment' in df.columns:
            print(f"  By Sentiment: {df['sentiment'].value_counts().to_dict()}")
        
    except Exception as e:
        print(f"✗ Error adding feedback: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_sample_feedback()
