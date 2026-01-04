"""
ML Predictor Module
Machine learning models for priority prediction, SLA forecasting, and pattern recognition.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class MLPredictor:
    """
    Machine Learning predictor for:
    - Feedback priority prediction
    - SLA breach probability
    - Resolution time estimation
    - Pattern recognition
    """

    def __init__(self, model_dir: str = "models"):
        """
        Initialize the ML predictor.

        Args:
            model_dir: Directory to save/load models
        """
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)

        self.priority_model = None
        self.sla_model = None
        self.time_model = None
        self.label_encoders = {}
        self.scaler = StandardScaler()

        self.is_trained = {
            'priority': False,
            'sla': False,
            'time': False
        }

        # Load existing models if available
        self._load_models()

    def _load_models(self):
        """Load pre-trained models if they exist."""
        try:
            if (self.model_dir / 'priority_model.pkl').exists():
                self.priority_model = joblib.load(self.model_dir / 'priority_model.pkl')
                self.is_trained['priority'] = True

            if (self.model_dir / 'sla_model.pkl').exists():
                self.sla_model = joblib.load(self.model_dir / 'sla_model.pkl')
                self.is_trained['sla'] = True

            if (self.model_dir / 'time_model.pkl').exists():
                self.time_model = joblib.load(self.model_dir / 'time_model.pkl')
                self.is_trained['time'] = True

            if (self.model_dir / 'label_encoders.pkl').exists():
                self.label_encoders = joblib.load(self.model_dir / 'label_encoders.pkl')

            if (self.model_dir / 'scaler.pkl').exists():
                self.scaler = joblib.load(self.model_dir / 'scaler.pkl')

            print("✓ ML models loaded successfully")

        except Exception as e:
            print(f"⚠️ Failed to load ML models: {e}")

    def _save_models(self):
        """Save trained models."""
        try:
            if self.priority_model:
                joblib.dump(self.priority_model, self.model_dir / 'priority_model.pkl')
            if self.sla_model:
                joblib.dump(self.sla_model, self.model_dir / 'sla_model.pkl')
            if self.time_model:
                joblib.dump(self.time_model, self.model_dir / 'time_model.pkl')

            joblib.dump(self.label_encoders, self.model_dir / 'label_encoders.pkl')
            joblib.dump(self.scaler, self.model_dir / 'scaler.pkl')

            print("✓ ML models saved successfully")

        except Exception as e:
            print(f"⚠️ Failed to save ML models: {e}")

    def prepare_priority_training_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare data for priority prediction training.

        Args:
            df: DataFrame with feedback data

        Returns:
            Tuple of (features, target)
        """
        df_copy = df.copy()

        # Create target variable based on urgency and status
        urgency_map = {'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}
        df_copy['priority_target'] = df_copy['urgency'].map(urgency_map).fillna(2)

        # Feature engineering
        features = pd.DataFrame()

        # Categorical features
        categorical_cols = ['category', 'sentiment']
        for col in categorical_cols:
            if col in df_copy.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    df_copy[col] = df_copy[col].fillna('Unknown')
                    self.label_encoders[col].fit(df_copy[col].astype(str))
                features[col] = self.label_encoders[col].transform(df_copy[col].astype(str).fillna('Unknown'))

        # Numerical features
        features['text_length'] = df_copy['feedback'].str.len().fillna(0)
        features['word_count'] = df_copy['feedback'].str.split().str.len().fillna(0)
        features['has_urgent_words'] = df_copy['feedback'].str.lower().str.contains(
            'urgent|emergency|critical|asap|immediate', na=False
        ).astype(int)

        # Sentiment score
        features['sentiment_score'] = df_copy['sentiment_score'].fillna(0)

        # Time-based features
        if 'timestamp' in df_copy.columns:
            df_copy['timestamp'] = pd.to_datetime(df_copy['timestamp'], errors='coerce')
            features['hour_of_day'] = df_copy['timestamp'].dt.hour.fillna(12)
            features['day_of_week'] = df_copy['timestamp'].dt.dayofweek.fillna(0)

        return features, df_copy['priority_target']

    def train_priority_predictor(self, df: pd.DataFrame, test_size: float = 0.2) -> Dict[str, Any]:
        """
        Train the priority prediction model.

        Args:
            df: Training data
            test_size: Test set size

        Returns:
            Training results
        """
        try:
            X, y = self.prepare_priority_training_data(df)

            if len(X) < 10:
                return {'success': False, 'message': 'Not enough training data'}

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )

            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)

            # Train model
            self.priority_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                class_weight='balanced'
            )

            self.priority_model.fit(X_train_scaled, y_train)

            # Evaluate
            y_pred = self.priority_model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)

            self.is_trained['priority'] = True
            self._save_models()

            return {
                'success': True,
                'accuracy': accuracy,
                'classification_report': classification_report(y_test, y_pred, output_dict=True)
            }

        except Exception as e:
            return {'success': False, 'message': str(e)}

    def predict_priority(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict priority for new feedback.

        Args:
            feedback_data: Feedback data dictionary

        Returns:
            Prediction results
        """
        if not self.is_trained['priority']:
            return {
                'predicted_priority': 'Medium',
                'confidence': 0.5,
                'method': 'default'
            }

        try:
            # Prepare input features
            features = pd.DataFrame([{
                'category': feedback_data.get('category', 'General'),
                'sentiment': feedback_data.get('sentiment', 'Neutral'),
                'text_length': len(feedback_data.get('feedback', '')),
                'word_count': len(feedback_data.get('feedback', '').split()),
                'has_urgent_words': 1 if any(word in feedback_data.get('feedback', '').lower()
                                           for word in ['urgent', 'emergency', 'critical', 'asap', 'immediate']) else 0,
                'sentiment_score': feedback_data.get('sentiment_score', 0.0),
                'hour_of_day': 12,  # Default midday
                'day_of_week': 0    # Default Monday
            }])

            # Encode categorical features
            for col in ['category', 'sentiment']:
                if col in self.label_encoders:
                    try:
                        features[col] = self.label_encoders[col].transform(features[col])
                    except:
                        features[col] = 0  # Unknown category

            # Scale features
            features_scaled = self.scaler.transform(features)

            # Make prediction
            prediction = self.priority_model.predict(features_scaled)[0]
            probabilities = self.priority_model.predict_proba(features_scaled)[0]
            confidence = max(probabilities)

            priority_map = {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Critical'}

            return {
                'predicted_priority': priority_map.get(prediction, 'Medium'),
                'confidence': float(confidence),
                'probabilities': {
                    'Low': float(probabilities[0]),
                    'Medium': float(probabilities[1]),
                    'High': float(probabilities[2]),
                    'Critical': float(probabilities[3])
                },
                'method': 'ml_model'
            }

        except Exception as e:
            print(f"Priority prediction failed: {e}")
            return {
                'predicted_priority': 'Medium',
                'confidence': 0.5,
                'method': 'fallback'
            }

    def prepare_sla_training_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare data for SLA breach prediction.

        Args:
            df: DataFrame with resolved feedback

        Returns:
            Tuple of (features, target)
        """
        df_copy = df.copy()

        # Filter resolved tickets
        resolved = df_copy[df_copy['status'].isin(['Resolved', 'Closed'])].copy()

        if len(resolved) < 10:
            raise ValueError("Not enough resolved tickets for SLA training")

        # Calculate if SLA was breached
        resolved['timestamp'] = pd.to_datetime(resolved['timestamp'], errors='coerce')
        resolved['resolved_at'] = pd.to_datetime(resolved.get('resolved_at', resolved['timestamp']), errors='coerce')

        # Calculate resolution time in hours
        resolved['resolution_hours'] = (resolved['resolved_at'] - resolved['timestamp']).dt.total_seconds() / 3600

        # Define SLA targets (hours)
        sla_targets = {'Low': 168, 'Medium': 72, 'High': 24, 'Critical': 4}
        resolved['sla_target'] = resolved['urgency'].map(sla_targets).fillna(72)

        # Target: 1 if breached, 0 if met
        resolved['sla_breached'] = (resolved['resolution_hours'] > resolved['sla_target']).astype(int)

        # Features for prediction
        features = pd.DataFrame()

        # Encode categorical features
        for col in ['category', 'urgency', 'sentiment']:
            if col in resolved.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    resolved[col] = resolved[col].fillna('Unknown')
                    self.label_encoders[col].fit(resolved[col].astype(str))
                features[col] = self.label_encoders[col].transform(resolved[col].astype(str).fillna('Unknown'))

        # Numerical features
        features['text_length'] = resolved['feedback'].str.len().fillna(0)
        features['sentiment_score'] = resolved['sentiment_score'].fillna(0)
        features['hour_of_day'] = resolved['timestamp'].dt.hour.fillna(12)

        return features, resolved['sla_breached']

    def train_sla_predictor(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Train SLA breach prediction model.

        Args:
            df: Training data with resolved tickets

        Returns:
            Training results
        """
        try:
            X, y = self.prepare_sla_training_data(df)

            if len(X) < 20:
                return {'success': False, 'message': 'Not enough resolved tickets for SLA training'}

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)

            self.sla_model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                class_weight='balanced'
            )

            self.sla_model.fit(X_train_scaled, y_train)

            y_pred = self.sla_model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)

            self.is_trained['sla'] = True
            self._save_models()

            return {
                'success': True,
                'accuracy': accuracy,
                'classification_report': classification_report(y_test, y_pred, output_dict=True)
            }

        except Exception as e:
            return {'success': False, 'message': str(e)}

    def predict_sla_breach_probability(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict SLA breach probability for new feedback.

        Args:
            feedback_data: Feedback data

        Returns:
            Breach probability prediction
        """
        if not self.is_trained['sla']:
            return {'breach_probability': 0.3, 'method': 'default'}

        try:
            features = pd.DataFrame([{
                'category': feedback_data.get('category', 'General'),
                'urgency': feedback_data.get('urgency', 'Medium'),
                'sentiment': feedback_data.get('sentiment', 'Neutral'),
                'text_length': len(feedback_data.get('feedback', '')),
                'sentiment_score': feedback_data.get('sentiment_score', 0.0),
                'hour_of_day': 12
            }])

            # Encode categorical features
            for col in ['category', 'urgency', 'sentiment']:
                if col in self.label_encoders:
                    try:
                        features[col] = self.label_encoders[col].transform(features[col])
                    except:
                        features[col] = 0

            features_scaled = self.scaler.transform(features)
            probabilities = self.sla_model.predict_proba(features_scaled)[0]

            # Probability of breach (class 1)
            breach_prob = probabilities[1]

            return {
                'breach_probability': float(breach_prob),
                'confidence': float(max(probabilities)),
                'method': 'ml_model'
            }

        except Exception as e:
            print(f"SLA prediction failed: {e}")
            return {'breach_probability': 0.3, 'method': 'fallback'}

    def get_training_status(self) -> Dict[str, bool]:
        """Get training status of all models."""
        return self.is_trained.copy()

    def retrain_all_models(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Retrain all ML models with new data.

        Args:
            df: Complete feedback dataset

        Returns:
            Training results for all models
        """
        results = {}

        # Train priority model
        priority_result = self.train_priority_predictor(df)
        results['priority'] = priority_result

        # Train SLA model (only if we have resolved tickets)
        resolved_count = len(df[df['status'].isin(['Resolved', 'Closed'])])
        if resolved_count >= 20:
            sla_result = self.train_sla_predictor(df)
            results['sla'] = sla_result
        else:
            results['sla'] = {'success': False, 'message': f'Need at least 20 resolved tickets, have {resolved_count}'}

        return results