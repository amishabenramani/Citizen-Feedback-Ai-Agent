"""
Data Manager Module
Handles all data storage, retrieval, and management operations for citizen feedback.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import pandas as pd


class DataManager:
    """
    Manages citizen feedback data storage and retrieval.
    Uses JSON file storage for persistence.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the data manager.
        
        Args:
            data_dir: Directory to store data files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.feedback_file = self.data_dir / "feedback.json"
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure the data file exists."""
        if not self.feedback_file.exists():
            self._save_data([])
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """
        Load feedback data from file.
        
        Returns:
            List of feedback entries
        """
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, data: List[Dict[str, Any]]):
        """
        Save feedback data to file.
        
        Args:
            data: List of feedback entries to save
        """
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    def generate_id(self) -> str:
        """
        Generate a unique ID for a feedback entry.
        
        Returns:
            Unique string ID
        """
        return str(uuid.uuid4())[:8].upper()
    
    def add_feedback(self, feedback: Dict[str, Any]) -> str:
        """
        Add a new feedback entry.
        
        Args:
            feedback: Feedback data dictionary
            
        Returns:
            ID of the added feedback
        """
        data = self._load_data()
        
        # Ensure required fields
        if 'id' not in feedback:
            feedback['id'] = self.generate_id()
        if 'timestamp' not in feedback:
            feedback['timestamp'] = datetime.now().isoformat()
        if 'status' not in feedback:
            feedback['status'] = 'New'
        
        data.append(feedback)
        self._save_data(data)
        
        return feedback['id']
    
    def get_feedback_by_id(self, feedback_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific feedback entry by ID.
        
        Args:
            feedback_id: The ID of the feedback to retrieve
            
        Returns:
            Feedback dictionary or None if not found
        """
        data = self._load_data()
        for entry in data:
            if entry.get('id') == feedback_id:
                return entry
        return None
    
    def get_all_feedback(self) -> List[Dict[str, Any]]:
        """
        Get all feedback entries.
        
        Returns:
            List of all feedback entries
        """
        return self._load_data()
    
    def get_feedback_dataframe(self) -> pd.DataFrame:
        """
        Get all feedback as a pandas DataFrame.
        
        Returns:
            DataFrame with all feedback data
        """
        data = self._load_data()
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data)
    
    def update_feedback(self, feedback_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update a feedback entry.
        
        Args:
            feedback_id: ID of the feedback to update
            updates: Dictionary of fields to update
            
        Returns:
            True if update was successful, False otherwise
        """
        data = self._load_data()
        
        for i, entry in enumerate(data):
            if entry.get('id') == feedback_id:
                data[i].update(updates)
                data[i]['updated_at'] = datetime.now().isoformat()
                self._save_data(data)
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
        Delete a feedback entry.
        
        Args:
            feedback_id: ID of the feedback to delete
            
        Returns:
            True if deletion was successful
        """
        data = self._load_data()
        original_length = len(data)
        
        data = [entry for entry in data if entry.get('id') != feedback_id]
        
        if len(data) < original_length:
            self._save_data(data)
            return True
        return False
    
    def clear_all_data(self):
        """Clear all feedback data."""
        self._save_data([])
    
    def get_feedback_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get feedback entries by category.
        
        Args:
            category: Category to filter by
            
        Returns:
            List of matching feedback entries
        """
        data = self._load_data()
        return [entry for entry in data if entry.get('category') == category]
    
    def get_feedback_by_sentiment(self, sentiment: str) -> List[Dict[str, Any]]:
        """
        Get feedback entries by sentiment.
        
        Args:
            sentiment: Sentiment to filter by (Positive, Negative, Neutral)
            
        Returns:
            List of matching feedback entries
        """
        data = self._load_data()
        return [entry for entry in data if entry.get('sentiment') == sentiment]
    
    def get_feedback_by_status(self, status: str) -> List[Dict[str, Any]]:
        """
        Get feedback entries by status.
        
        Args:
            status: Status to filter by
            
        Returns:
            List of matching feedback entries
        """
        data = self._load_data()
        return [entry for entry in data if entry.get('status') == status]
    
    def get_feedback_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Get feedback entries within a date range.
        
        Args:
            start_date: Start of the date range
            end_date: End of the date range
            
        Returns:
            List of matching feedback entries
        """
        data = self._load_data()
        filtered = []
        
        for entry in data:
            try:
                entry_date = datetime.fromisoformat(entry.get('timestamp', ''))
                if start_date <= entry_date <= end_date:
                    filtered.append(entry)
            except (ValueError, TypeError):
                continue
        
        return filtered
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the feedback data.
        
        Returns:
            Dictionary with various statistics
        """
        data = self._load_data()
        
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
        Import feedback from a pandas DataFrame.
        
        Args:
            df: DataFrame with feedback data
            
        Returns:
            Number of records imported
        """
        data = self._load_data()
        
        for _, row in df.iterrows():
            entry = row.to_dict()
            if 'id' not in entry or pd.isna(entry.get('id')):
                entry['id'] = self.generate_id()
            if 'timestamp' not in entry or pd.isna(entry.get('timestamp')):
                entry['timestamp'] = datetime.now().isoformat()
            if 'status' not in entry or pd.isna(entry.get('status')):
                entry['status'] = 'New'
            data.append(entry)
        
        self._save_data(data)
        return len(df)
    
    def export_to_json(self, filepath: str) -> bool:
        """
        Export all feedback to a JSON file.
        
        Args:
            filepath: Path to export file
            
        Returns:
            True if export was successful
        """
        try:
            data = self._load_data()
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception:
            return False
