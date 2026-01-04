"""
Data Manager Module
Handles all data storage, retrieval, and management operations for citizen feedback.
Uses PostgreSQL database for persistent storage.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import pandas as pd
from sqlalchemy import and_, or_
from sqlalchemy.exc import SQLAlchemyError

from .database import Database
from .db_models import Feedback, Staff

# Try to import AI components
try:
    from .ai import AdvancedNLPAnalyzer, MLPredictor, OpenAIAssistant, TextEmbeddings, RecommendationEngine
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("⚠️ AI components not available, using basic analysis")


class DataManager:
    """
    Manages citizen feedback data storage and retrieval.
    Uses PostgreSQL database for persistence.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the data manager.
        
        Args:
            data_dir: Directory path (maintained for compatibility, not used)
        """
        try:
            # Initialize database connection
            Database.initialize()
            Database.create_tables()
            print("✓ Connected to PostgreSQL database")
        except Exception as e:
            print(f"✗ PostgreSQL connection failed: {e}")
            raise RuntimeError(f"Cannot initialize DataManager without PostgreSQL: {e}")
        
        # Initialize AI components if available
        self.ai_components = {}
        if AI_AVAILABLE:
            try:
                self.ai_components['nlp'] = AdvancedNLPAnalyzer()
                self.ai_components['ml'] = MLPredictor()
                self.ai_components['openai'] = OpenAIAssistant()
                self.ai_components['embeddings'] = TextEmbeddings()
                self.ai_components['recommendation_engine'] = RecommendationEngine(
                    advanced_nlp=self.ai_components.get('nlp'),
                    ml_predictor=self.ai_components.get('ml'),
                    openai_assistant=self.ai_components.get('openai'),
                    text_embeddings=self.ai_components.get('embeddings')
                )
                print("✓ AI components initialized")
            except Exception as e:
                print(f"⚠️ AI components initialization failed: {e}")
                self.ai_components = {}
        else:
            print("ℹ️ AI components not available")
    
    def generate_id(self) -> str:
        """
        Generate a unique ID for a feedback entry.
        
        Returns:
            Unique string ID
        """
        return str(uuid.uuid4())[:8].upper()
    
    def add_feedback(self, feedback: Dict[str, Any]) -> str:
        """
        Add a new feedback entry to PostgreSQL.
        
        Args:
            feedback: Feedback data dictionary
            
        Returns:
            ID of the added feedback
            
        Raises:
            Exception: If database operation fails
        """
        # Ensure required fields
        if 'id' not in feedback:
            feedback['id'] = self.generate_id()
        if 'timestamp' not in feedback:
            feedback['timestamp'] = datetime.now().isoformat()
        if 'status' not in feedback:
            feedback['status'] = 'New'
        
        with Database.session_scope() as session:
            # Create feedback model from dict
            fb = Feedback.from_dict(feedback)
            session.add(fb)
        
        return feedback['id']
    
    def get_feedback_by_id(self, feedback_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific feedback entry by ID from PostgreSQL.
        
        Args:
            feedback_id: The ID of the feedback to retrieve
            
        Returns:
            Feedback dictionary or None if not found
        """
        with Database.session_scope() as session:
            fb = session.query(Feedback).filter(Feedback.id == feedback_id).first()
            return fb.to_dict() if fb else None
    
    def get_all_feedback(self) -> List[Dict[str, Any]]:
        """
        Get all feedback entries from PostgreSQL.
        
        Returns:
            List of all feedback entries
        """
        with Database.session_scope() as session:
            feedbacks = session.query(Feedback).order_by(Feedback.timestamp.desc()).all()
            return [fb.to_dict() for fb in feedbacks]
    
    def get_feedback_dataframe(self) -> pd.DataFrame:
        """
        Get all feedback as a pandas DataFrame.
        
        Returns:
            DataFrame with all feedback data
        """
        data = self.get_all_feedback()
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data)
    
    def update_feedback(self, feedback_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update a feedback entry in PostgreSQL.
        
        Args:
            feedback_id: ID of the feedback to update
            updates: Dictionary of fields to update
            
        Returns:
            True if update was successful, False otherwise
        """
        updates['updated_at'] = datetime.now().isoformat()
        
        with Database.session_scope() as session:
            fb = session.query(Feedback).filter(Feedback.id == feedback_id).first()
            if fb:
                for key, value in updates.items():
                    if hasattr(fb, key):
                        setattr(fb, key, value)
                return True
            return False
    
    def update_status(self, feedback_id: str, new_status: str) -> bool:
        """
        Update the status of a feedback entry.
        
        Args:
            feedback_id: ID of the feedback
            new_status: New status value
            
        Returns:
            True if update was successful
        """
        return self.update_feedback(feedback_id, {'status': new_status})
    
    def delete_feedback(self, feedback_id: str) -> bool:
        """
        Delete a feedback entry from PostgreSQL.
        
        Args:
            feedback_id: ID of the feedback to delete
            
        Returns:
            True if deletion was successful
        """
        with Database.session_scope() as session:
            fb = session.query(Feedback).filter(Feedback.id == feedback_id).first()
            if fb:
                session.delete(fb)
                return True
            return False
    
    def clear_all_data(self):
        """Clear all feedback data from PostgreSQL."""
        with Database.session_scope() as session:
            session.query(Feedback).delete()
    
    def get_feedback_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get feedback entries by category from PostgreSQL.
        
        Args:
            category: Category to filter by
            
        Returns:
            List of matching feedback entries
        """
        with Database.session_scope() as session:
            feedbacks = session.query(Feedback).filter(Feedback.category == category).all()
            return [fb.to_dict() for fb in feedbacks]
    
    def get_feedback_by_sentiment(self, sentiment: str) -> List[Dict[str, Any]]:
        """
        Get feedback entries by sentiment from PostgreSQL.
        
        Args:
            sentiment: Sentiment to filter by (Positive, Negative, Neutral)
            
        Returns:
            List of matching feedback entries
        """
        with Database.session_scope() as session:
            feedbacks = session.query(Feedback).filter(Feedback.sentiment == sentiment).all()
            return [fb.to_dict() for fb in feedbacks]
    
    def get_feedback_by_status(self, status: str) -> List[Dict[str, Any]]:
        """
        Get feedback entries by status from PostgreSQL.
        
        Args:
            status: Status to filter by
            
        Returns:
            List of matching feedback entries
        """
        with Database.session_scope() as session:
            feedbacks = session.query(Feedback).filter(Feedback.status == status).all()
            return [fb.to_dict() for fb in feedbacks]
    
    def get_feedback_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Get feedback entries within a date range from PostgreSQL.
        
        Args:
            start_date: Start of the date range
            end_date: End of the date range
            
        Returns:
            List of matching feedback entries
        """
        with Database.session_scope() as session:
            feedbacks = session.query(Feedback).filter(
                and_(Feedback.timestamp >= start_date, Feedback.timestamp <= end_date)
            ).all()
            return [fb.to_dict() for fb in feedbacks]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the feedback data.
        
        Returns:
            Dictionary with various statistics
        """
        data = self.get_all_feedback()
        
        if not data:
            return {
                "total": 0,
                "by_category": {},
                "by_sentiment": {},
                "by_status": {},
                "by_urgency": {}
            }
        
        df = pd.DataFrame(data)
        
        stats = {
            "total": len(data),
            "by_category": df['category'].value_counts().to_dict() if 'category' in df else {},
            "by_sentiment": df['sentiment'].value_counts().to_dict() if 'sentiment' in df else {},
            "by_status": df['status'].value_counts().to_dict() if 'status' in df else {},
            "by_urgency": df['urgency'].value_counts().to_dict() if 'urgency' in df else {}
        }
        
        # Calculate average sentiment score
        if 'sentiment_score' in df:
            stats['avg_sentiment_score'] = df['sentiment_score'].mean()
        
        return stats
    
    def import_from_dataframe(self, df: pd.DataFrame) -> int:
        """
        Import feedback from a pandas DataFrame into PostgreSQL.
        
        Args:
            df: DataFrame with feedback data
            
        Returns:
            Number of records imported
        """
        count = 0
        for _, row in df.iterrows():
            entry = row.to_dict()
            if 'id' not in entry or pd.isna(entry.get('id')):
                entry['id'] = self.generate_id()
            if 'timestamp' not in entry or pd.isna(entry.get('timestamp')):
                entry['timestamp'] = datetime.now().isoformat()
            if 'status' not in entry or pd.isna(entry.get('status')):
                entry['status'] = 'New'
            
            with Database.session_scope() as session:
                fb = Feedback.from_dict(entry)
                session.add(fb)
            count += 1
        
        return count
    
    def export_to_json(self, filepath: str) -> bool:
        """
        Export all feedback from PostgreSQL to a JSON file.
        
        Args:
            filepath: Path to export file
            
        Returns:
            True if export was successful
        """
        import json
        try:
            data = self.get_all_feedback()
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception:
            return False
    
    # ==================== STAFF MANAGEMENT ====================
    
    def add_staff(self, staff_data: Dict[str, Any]) -> Optional[int]:
        """
        Add a new staff member.
        
        Args:
            staff_data: Dictionary containing staff information
            
        Returns:
            Staff ID if successful, None otherwise
        """
        try:
            with Database.session_scope() as session:
                staff = Staff.from_dict(staff_data)
                session.add(staff)
                session.flush()
                return staff.id
        except SQLAlchemyError as e:
            print(f"Error adding staff: {e}")
            return None
    
    def get_all_staff(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """
        Get all staff members.
        
        Args:
            active_only: If True, return only active staff
            
        Returns:
            List of staff dictionaries
        """
        try:
            with Database.session_scope() as session:
                query = session.query(Staff)
                if active_only:
                    query = query.filter(Staff.active == 'Active')
                staff_list = query.order_by(Staff.name).all()
                return [s.to_dict() for s in staff_list]
        except SQLAlchemyError as e:
            print(f"Error getting staff: {e}")
            return []
    
    def get_staff_by_id(self, staff_id: int) -> Optional[Dict[str, Any]]:
        """
        Get staff member by ID.
        
        Args:
            staff_id: Staff ID
            
        Returns:
            Staff dictionary or None if not found
        """
        try:
            with Database.session_scope() as session:
                staff = session.query(Staff).filter(Staff.id == staff_id).first()
                return staff.to_dict() if staff else None
        except SQLAlchemyError as e:
            print(f"Error getting staff: {e}")
            return None
    
    def update_staff(self, staff_id: int, updates: Dict[str, Any]) -> bool:
        """
        Update staff member information.
        
        Args:
            staff_id: Staff ID
            updates: Dictionary of fields to update
            
        Returns:
            True if successful
        """
        try:
            with Database.session_scope() as session:
                staff = session.query(Staff).filter(Staff.id == staff_id).first()
                if staff:
                    for key, value in updates.items():
                        if hasattr(staff, key):
                            setattr(staff, key, value)
                    staff.updated_at = datetime.utcnow()
                    return True
                return False
        except SQLAlchemyError as e:
            print(f"Error updating staff: {e}")
            return False
    
    def delete_staff(self, staff_id: int) -> bool:
        """
        Delete staff member (soft delete - mark as inactive).
        
        Args:
            staff_id: Staff ID
            
        Returns:
            True if successful
        """
        try:
            with Database.session_scope() as session:
                staff = session.query(Staff).filter(Staff.id == staff_id).first()
                if staff:
                    staff.active = 'Inactive'
                    staff.updated_at = datetime.utcnow()
                    return True
                return False
        except SQLAlchemyError as e:
            print(f"Error deleting staff: {e}")
            return False
    
    def get_staff_names(self, active_only: bool = True) -> List[str]:
        """
        Get list of staff names for dropdowns.
        
        Args:
            active_only: If True, return only active staff
            
        Returns:
            List of staff names
        """
        staff_list = self.get_all_staff(active_only)
        return [s['name'] for s in staff_list]
    
    # ==================== AI-POWERED METHODS ====================
    
    def analyze_feedback_with_ai(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive AI analysis on feedback.
        
        Args:
            feedback_data: Feedback dictionary
            
        Returns:
            Complete AI analysis results
        """
        if 'recommendation_engine' not in self.ai_components:
            # Fallback to basic analysis
            return self._basic_feedback_analysis(feedback_data)
        
        try:
            return self.ai_components['recommendation_engine'].analyze_feedback_comprehensive(feedback_data)
        except Exception as e:
            print(f"AI analysis failed, using basic analysis: {e}")
            return self._basic_feedback_analysis(feedback_data)
    
    def _basic_feedback_analysis(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Basic feedback analysis without AI."""
        text = feedback_data.get('feedback', '')
        
        # Basic sentiment analysis
        positive_words = {'good', 'great', 'excellent', 'happy', 'satisfied'}
        negative_words = {'bad', 'terrible', 'awful', 'angry', 'disappointed'}
        
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        if positive_count > negative_count:
            sentiment = 'Positive'
        elif negative_count > positive_count:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return {
            'feedback_id': feedback_data.get('id'),
            'timestamp': datetime.now().isoformat(),
            'analyses': {
                'nlp': {
                    'sentiment': sentiment,
                    'sentiment_score': 0.5 if sentiment == 'Neutral' else (0.8 if sentiment == 'Positive' else 0.2),
                    'method': 'basic'
                }
            },
            'recommendations': {
                'priority_level': feedback_data.get('urgency', 'Medium'),
                'urgency_action': 'Standard processing',
                'confidence_level': 'Low'
            }
        }
    
    def train_ai_models(self) -> Dict[str, Any]:
        """
        Train all available AI models with current data.
        
        Returns:
            Training results
        """
        results = {'success': False, 'models_trained': [], 'errors': []}
        
        if not self.ai_components:
            results['errors'].append('No AI components available')
            return results
        
        # Get training data
        feedback_data = self.get_all_feedback()
        if len(feedback_data) < 10:
            results['errors'].append('Insufficient data for training')
            return results
        
        # Train ML models
        if 'ml' in self.ai_components:
            try:
                ml_results = self.ai_components['ml'].retrain_all_models(feedback_data)
                results['models_trained'].append('ml_models')
                results.update(ml_results)
            except Exception as e:
                results['errors'].append(f'ML training failed: {e}')
        
        # Build embeddings index
        if 'embeddings' in self.ai_components:
            try:
                success = self.ai_components['embeddings'].build_search_index(feedback_data)
                if success:
                    results['models_trained'].append('embeddings_index')
                else:
                    results['errors'].append('Embeddings index building failed')
            except Exception as e:
                results['errors'].append(f'Embeddings training failed: {e}')
        
        results['success'] = len(results['models_trained']) > 0
        return results
    
    def get_ai_insights(self) -> Dict[str, Any]:
        """
        Get AI-powered insights from all feedback data.
        
        Returns:
            Comprehensive insights
        """
        feedback_data = self.get_all_feedback()
        
        if not feedback_data:
            return {'error': 'No feedback data available'}
        
        insights = {
            'total_feedbacks': len(feedback_data),
            'timestamp': datetime.now().isoformat(),
            'basic_stats': self.get_statistics()
        }
        
        # AI-powered insights
        if 'recommendation_engine' in self.ai_components:
            try:
                bulk_analysis = self.ai_components['recommendation_engine'].analyze_bulk_feedback(feedback_data)
                insights['ai_analysis'] = bulk_analysis
            except Exception as e:
                insights['ai_analysis'] = {'error': str(e)}
        
        # Theme analysis (OpenAI)
        if 'openai' in self.ai_components and self.ai_components['openai'].is_available():
            try:
                theme_analysis = self.ai_components['openai'].analyze_feedback_themes(feedback_data)
                insights['theme_analysis'] = theme_analysis
            except Exception as e:
                insights['theme_analysis'] = {'error': str(e)}
        
        # Embedding insights
        if 'embeddings' in self.ai_components:
            try:
                embedding_insights = self.ai_components['embeddings'].get_feedback_insights()
                insights['embedding_insights'] = embedding_insights
            except Exception as e:
                insights['embedding_insights'] = {'error': str(e)}
        
        return insights
    
    def semantic_search_feedback(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform semantic search on feedback data.
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            Similar feedback items
        """
        if 'embeddings' not in self.ai_components:
            # Fallback to keyword search
            return self._keyword_search_feedback(query, top_k)
        
        try:
            return self.ai_components['embeddings'].semantic_search(query, top_k)
        except Exception as e:
            print(f"Semantic search failed, using keyword search: {e}")
            return self._keyword_search_feedback(query, top_k)
    
    def _keyword_search_feedback(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Fallback keyword-based search."""
        all_feedback = self.get_all_feedback()
        query_lower = query.lower()
        
        # Simple relevance scoring
        scored_results = []
        for fb in all_feedback:
            text = f"{fb.get('title', '')} {fb.get('feedback', '')}".lower()
            score = sum(1 for word in query_lower.split() if word in text)
            if score > 0:
                fb_copy = fb.copy()
                fb_copy['relevance_score'] = score
                scored_results.append(fb_copy)
        
        # Sort by relevance and return top results
        scored_results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return scored_results[:top_k]
    
    def generate_ai_response_suggestion(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate AI-powered response suggestion.
        
        Args:
            feedback_data: Feedback data
            
        Returns:
            Response suggestion
        """
        if 'openai' not in self.ai_components or not self.ai_components['openai'].is_available():
            return {
                'response': 'AI response generation not available. Please configure OpenAI API key.',
                'method': 'unavailable'
            }
        
        try:
            return self.ai_components['openai'].generate_response_suggestion(feedback_data)
        except Exception as e:
            return {
                'response': f'Error generating response: {str(e)}',
                'method': 'error'
            }
    
    def get_ai_system_health(self) -> Dict[str, Any]:
        """
        Get health status of AI system.
        
        Returns:
            AI system health report
        """
        if 'recommendation_engine' not in self.ai_components:
            return {'status': 'unavailable', 'message': 'AI components not initialized'}
        
        try:
            return self.ai_components['recommendation_engine'].get_system_health()
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def update_ai_models(self, new_feedback: List[Dict[str, Any]]) -> bool:
        """
        Update AI models with new feedback data.
        
        Args:
            new_feedback: New feedback items
            
        Returns:
            Success status
        """
        success = True
        
        # Update embeddings index
        if 'embeddings' in self.ai_components:
            try:
                self.ai_components['embeddings'].update_index(new_feedback)
            except Exception as e:
                print(f"Embeddings update failed: {e}")
                success = False
        
        # Retrain ML models if enough new data
        if len(new_feedback) >= 10 and 'ml' in self.ai_components:
            try:
                all_data = self.get_all_feedback()
                self.ai_components['ml'].retrain_all_models(all_data)
            except Exception as e:
                print(f"ML model update failed: {e}")
                success = False
        
        return success
