"""
Feedback Analyzer Module
AI-powered analysis for citizen feedback including sentiment analysis,
keyword extraction, and summarization.
"""

import re
from collections import Counter
from typing import Dict, List, Any, Optional

# Try to import advanced AI components
try:
    from .ai.advanced_nlp import AdvancedNLPAnalyzer
    ADVANCED_AI_AVAILABLE = True
except ImportError:
    ADVANCED_AI_AVAILABLE = False

class FeedbackAnalyzer:
    """
    Analyzes citizen feedback using AI techniques.
    Provides sentiment analysis, keyword extraction, and summarization.
    Uses advanced transformer models when available, falls back to rule-based analysis.
    """
    
    def __init__(self):
        """Initialize the feedback analyzer."""
        self.advanced_analyzer = None
        
        # Initialize advanced AI if available
        if ADVANCED_AI_AVAILABLE:
            try:
                self.advanced_analyzer = AdvancedNLPAnalyzer()
                print("✓ Advanced AI analyzer initialized")
            except Exception as e:
                print(f"⚠️ Advanced AI initialization failed: {e}")
                self.advanced_analyzer = None
        
        # Fallback: Basic rule-based analyzer
        self._init_basic_analyzer()
    
    def _init_basic_analyzer(self):
        """Initialize basic rule-based analyzer components."""
        # Positive words for sentiment analysis
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'helpful', 'efficient', 'friendly', 'professional', 'satisfied',
            'happy', 'pleased', 'appreciate', 'thank', 'thanks', 'love',
            'perfect', 'best', 'improved', 'improvement', 'better', 'nice',
            'clean', 'safe', 'beautiful', 'convenient', 'quick', 'fast',
            'responsive', 'supportive', 'outstanding', 'impressive', 'positive'
        }
        
        # Negative words for sentiment analysis
        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'poor', 'worst',
            'disappointing', 'disappointed', 'frustrated', 'frustrating',
            'slow', 'delayed', 'broken', 'damaged', 'unsafe', 'dangerous',
            'dirty', 'unclean', 'rude', 'unprofessional', 'unhelpful',
            'inefficient', 'waste', 'problem', 'issue', 'complaint',
            'failed', 'failure', 'never', 'hate', 'angry', 'annoyed',
            'unacceptable', 'ridiculous', 'incompetent', 'neglected'
        }
        
        # Common stop words to filter out
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are',
            'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must',
            'shall', 'can', 'need', 'dare', 'ought', 'used', 'it', 'its',
            'this', 'that', 'these', 'those', 'i', 'me', 'my', 'myself',
            'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
            'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
            'her', 'hers', 'herself', 'they', 'them', 'their', 'theirs',
            'themselves', 'what', 'which', 'who', 'whom', 'when', 'where',
            'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
            'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also',
            'now', 'here', 'there', 'then', 'once', 'if', 'about', 'into',
            'through', 'during', 'before', 'after', 'above', 'below',
            'between', 'under', 'again', 'further', 'any', 'being', 'get',
            'got', 'getting', 'am', 'up', 'down', 'out', 'off', 'over'
        }
        
        # Category-specific keywords
        self.category_keywords = {
            'infrastructure': ['road', 'bridge', 'building', 'construction', 'repair', 'maintenance', 'pothole', 'sidewalk', 'street'],
            'transportation': ['bus', 'train', 'traffic', 'parking', 'transit', 'commute', 'route', 'schedule', 'delay'],
            'healthcare': ['hospital', 'clinic', 'doctor', 'nurse', 'medical', 'health', 'emergency', 'appointment', 'treatment'],
            'education': ['school', 'teacher', 'student', 'library', 'program', 'class', 'learning', 'curriculum', 'education'],
            'environment': ['park', 'tree', 'pollution', 'recycling', 'waste', 'green', 'clean', 'nature', 'sustainability'],
            'safety': ['police', 'fire', 'emergency', 'crime', 'security', 'safe', 'patrol', 'response', 'protection'],
            'services': ['permit', 'license', 'office', 'staff', 'service', 'wait', 'process', 'application', 'document']
        }
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive analysis on the feedback text.
        Uses advanced AI when available, falls back to rule-based analysis.
        
        Args:
            text: The feedback text to analyze
            
        Returns:
            Dictionary containing sentiment, score, keywords, and summary
        """
        # Use advanced AI if available
        if self.advanced_analyzer and self.advanced_analyzer.models_loaded:
            try:
                # Get comprehensive analysis from advanced AI
                advanced_result = self.advanced_analyzer.analyze_comprehensive(text)
                
                # Format to match expected output structure
                return {
                    "sentiment": advanced_result['sentiment']['sentiment'],
                    "sentiment_score": advanced_result['sentiment']['sentiment_score'],
                    "keywords": advanced_result['summary'].get('summary', '').split()[:5] if isinstance(advanced_result['summary'].get('summary'), str) else ["general feedback"],
                    "summary": advanced_result['summary'].get('summary', text[:100]),
                    "method": "advanced_ai",
                    "confidence": advanced_result['sentiment'].get('confidence', 0.5),
                    "category": advanced_result['category'].get('category', 'General'),
                    "entities": advanced_result['entities'].get('entities', {})
                }
                
            except Exception as e:
                print(f"Advanced AI analysis failed, falling back to basic: {e}")
        
        # Fallback to basic rule-based analysis
        return self._analyze_basic(text)
    
    def _analyze_basic(self, text: str) -> Dict[str, Any]:
        """
        Basic rule-based analysis as fallback.
        
        Args:
            text: The feedback text to analyze
            
        Returns:
            Dictionary containing sentiment, score, keywords, and summary
        """
        # Clean and tokenize text
        cleaned_text = self._clean_text(text)
        words = self._tokenize(cleaned_text)
        
        # Perform basic analyses
        sentiment, sentiment_score = self._analyze_sentiment_basic(words)
        keywords = self._extract_keywords_basic(words)
        summary = self._generate_summary_basic(text, sentiment)
        category = self.detect_category(text)
        
        return {
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "keywords": keywords,
            "summary": summary,
            "method": "basic_rule_based",
            "confidence": 0.5,  # Lower confidence for basic analysis
            "category": category,
            "entities": {}
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean the text by removing special characters and extra whitespace."""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters except spaces
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        return text.split()
    
    def _analyze_sentiment_basic(self, words: List[str]) -> tuple:
        """
        Analyze sentiment using basic word counting.
        
        Returns:
            Tuple of (sentiment_label, sentiment_score)
        """
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            return "Neutral", 0.0
        
        # Calculate sentiment score (-1 to 1)
        sentiment_score = (positive_count - negative_count) / total_sentiment_words
        
        # Normalize to 0-1 range for display
        normalized_score = (sentiment_score + 1) / 2
        
        # Determine sentiment label
        if sentiment_score > 0.2:
            sentiment = "Positive"
        elif sentiment_score < -0.2:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
        return sentiment, normalized_score
    
    def _extract_keywords_basic(self, words: List[str], top_n: int = 5) -> List[str]:
        """
        Extract the most important keywords using basic frequency analysis.
        
        Args:
            words: List of words from the feedback
            top_n: Number of keywords to extract
            
        Returns:
            List of top keywords
        """
        # Filter out stop words and short words
        meaningful_words = [
            word for word in words 
            if word not in self.stop_words and len(word) > 2
        ]
        
        # Count word frequencies
        word_counts = Counter(meaningful_words)
        
        # Get top keywords
        keywords = [word for word, count in word_counts.most_common(top_n)]
        
        return keywords if keywords else ["general feedback"]
    
    def _generate_summary_basic(self, text: str, sentiment: str) -> str:
        """
        Generate a basic summary of the feedback.
        
        Args:
            text: Original feedback text
            sentiment: Detected sentiment
            
        Returns:
            A brief summary string
        """
        # Get first sentence or first 100 characters
        sentences = text.split('.')
        first_sentence = sentences[0].strip() if sentences else text[:100]
        
        # Truncate if too long
        if len(first_sentence) > 150:
            first_sentence = first_sentence[:147] + "..."
        
        # Add sentiment context
        sentiment_prefix = {
            "Positive": "Positive feedback: ",
            "Negative": "Concern raised: ",
            "Neutral": "General feedback: "
        }
        
        return sentiment_prefix.get(sentiment, "") + first_sentence
    
    def detect_category(self, text: str) -> str:
        """
        Automatically detect the category based on content.
        
        Args:
            text: Feedback text
            
        Returns:
            Detected category string
        """
        text_lower = text.lower()
        category_scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            category_scores[category] = score
        
        if max(category_scores.values()) > 0:
            return max(category_scores, key=category_scores.get).title()
        return "General"
    
    def get_urgency_indicators(self, text: str) -> Dict[str, bool]:
        """
        Check for urgency indicators in the feedback.
        
        Args:
            text: Feedback text
            
        Returns:
            Dictionary of urgency indicators
        """
        text_lower = text.lower()
        
        urgency_words = ['urgent', 'emergency', 'immediate', 'critical', 'dangerous', 'asap', 'now']
        time_pressure = ['today', 'tomorrow', 'deadline', 'hurry', 'quickly']
        safety_concerns = ['unsafe', 'hazard', 'risk', 'danger', 'injury', 'accident']
        
        return {
            "has_urgency_words": any(word in text_lower for word in urgency_words),
            "has_time_pressure": any(word in text_lower for word in time_pressure),
            "has_safety_concerns": any(word in text_lower for word in safety_concerns)
        }
