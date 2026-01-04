"""
AI Module for Citizen Feedback AI Agent
Advanced AI capabilities including NLP, ML predictions, and external integrations.
"""

from .advanced_nlp import AdvancedNLPAnalyzer
from .ml_predictor import MLPredictor
from .openai_integration import OpenAIAssistant
from .text_embeddings import TextEmbeddings
from .recommendation_engine import RecommendationEngine

__all__ = [
    'AdvancedNLPAnalyzer',
    'MLPredictor',
    'OpenAIAssistant',
    'TextEmbeddings',
    'RecommendationEngine'
]