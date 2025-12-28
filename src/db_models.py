"""
Database Models
SQLAlchemy models for PostgreSQL database schema.
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, JSON, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Feedback(Base):
    """
    Feedback model representing citizen feedback entries.
    Matches the existing JSON schema structure for backward compatibility.
    """
    __tablename__ = "feedback"
    
    # Primary key and identification
    id = Column(String(50), primary_key=True, index=True)
    feedback_id = Column(String(50), index=True)  # Duplicate for compatibility
    
    # Timestamps
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Citizen information
    name = Column(String(200))
    citizen_name = Column(String(200))  # Duplicate for compatibility
    email = Column(String(200), index=True)
    citizen_email = Column(String(200))  # Duplicate for compatibility
    phone = Column(String(50))
    citizen_phone = Column(String(50))  # Duplicate for compatibility
    
    # Feedback details
    feedback_type = Column(String(100), index=True)
    category = Column(String(100), index=True)
    urgency = Column(String(50), index=True)
    
    # Location
    area = Column(String(200))
    address = Column(Text)
    location = Column(Text)
    
    # Content
    title = Column(String(500))
    feedback = Column(Text)
    
    # AI Analysis
    sentiment = Column(String(50), index=True)
    sentiment_score = Column(Float)
    keywords = Column(JSON)  # Array of keywords stored as JSON
    summary = Column(Text)
    
    # Status and management
    status = Column(String(50), default='New', index=True)
    admin_notes = Column(Text)
    assigned_to = Column(String(200))
    priority = Column(String(50), default='Normal', index=True)
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'feedback_id': self.feedback_id or self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'name': self.name,
            'citizen_name': self.citizen_name or self.name,
            'email': self.email,
            'citizen_email': self.citizen_email or self.email,
            'phone': self.phone,
            'citizen_phone': self.citizen_phone or self.phone,
            'feedback_type': self.feedback_type,
            'category': self.category,
            'urgency': self.urgency,
            'area': self.area,
            'address': self.address,
            'location': self.location,
            'title': self.title,
            'feedback': self.feedback,
            'sentiment': self.sentiment,
            'sentiment_score': self.sentiment_score,
            'keywords': self.keywords or [],
            'summary': self.summary,
            'status': self.status,
            'admin_notes': self.admin_notes or '',
            'assigned_to': self.assigned_to or '',
            'priority': self.priority or 'Normal'
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Create model instance from dictionary."""
        return Feedback(
            id=data.get('id'),
            feedback_id=data.get('feedback_id') or data.get('id'),
            timestamp=datetime.fromisoformat(data['timestamp']) if isinstance(data.get('timestamp'), str) else data.get('timestamp'),
            updated_at=datetime.fromisoformat(data['updated_at']) if isinstance(data.get('updated_at'), str) else data.get('updated_at'),
            name=data.get('name'),
            citizen_name=data.get('citizen_name') or data.get('name'),
            email=data.get('email'),
            citizen_email=data.get('citizen_email') or data.get('email'),
            phone=data.get('phone'),
            citizen_phone=data.get('citizen_phone') or data.get('phone'),
            feedback_type=data.get('feedback_type'),
            category=data.get('category'),
            urgency=data.get('urgency'),
            area=data.get('area'),
            address=data.get('address'),
            location=data.get('location'),
            title=data.get('title'),
            feedback=data.get('feedback'),
            sentiment=data.get('sentiment'),
            sentiment_score=data.get('sentiment_score'),
            keywords=data.get('keywords', []),
            summary=data.get('summary'),
            status=data.get('status', 'New'),
            admin_notes=data.get('admin_notes', ''),
            assigned_to=data.get('assigned_to', ''),
            priority=data.get('priority', 'Normal')
        )
    
    def __repr__(self):
        return f"<Feedback(id='{self.id}', title='{self.title}', status='{self.status}')>"
