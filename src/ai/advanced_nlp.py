"""
Advanced NLP Analyzer Module
Transformer-based NLP for sentiment analysis, summarization, and classification.
"""

import os
import warnings
from typing import Dict, List, Any, Optional
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import logging

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')
logging.getLogger("transformers").setLevel(logging.ERROR)

class AdvancedNLPAnalyzer:
    """
    Advanced NLP analyzer using transformer models for:
    - Sentiment analysis with confidence scores
    - Text summarization
    - Zero-shot classification
    - Named entity recognition
    """

    def __init__(self, use_gpu: bool = False):
        """
        Initialize the advanced NLP analyzer.

        Args:
            use_gpu: Whether to use GPU acceleration if available
        """
        self.device = 0 if use_gpu and torch.cuda.is_available() else -1
        self.models_loaded = False

        try:
            self._load_models()
            self.models_loaded = True
            print("✓ Advanced NLP models loaded successfully")
        except Exception as e:
            print(f"⚠️ Failed to load advanced NLP models: {e}")
            print("Falling back to basic analysis")
            self.models_loaded = False

    def _load_models(self):
        """Load all transformer models."""
        # Sentiment Analysis Model (Twitter-optimized RoBERTa)
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=self.device,
            return_all_scores=True
        )

        # Summarization Model (BART)
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=self.device
        )

        # Zero-shot Classification for categories
        self.zero_shot_classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=self.device
        )

        # Named Entity Recognition
        self.ner_pipeline = pipeline(
            "ner",
            model="dbmdz/bert-large-cased-finetuned-conll03-english",
            device=self.device,
            aggregation_strategy="simple"
        )

    def analyze_sentiment_advanced(self, text: str) -> Dict[str, Any]:
        """
        Advanced sentiment analysis with detailed scores.

        Args:
            text: Input text to analyze

        Returns:
            Dictionary with sentiment analysis results
        """
        if not self.models_loaded or not text.strip():
            return self._fallback_sentiment(text)

        try:
            # Get sentiment scores
            results = self.sentiment_pipeline(text)

            if not results or len(results) == 0:
                return self._fallback_sentiment(text)

            # Process results (results is a list with one dict)
            scores = results[0] if isinstance(results, list) else results

            # Map labels to our format
            label_map = {
                'LABEL_0': 'Negative',
                'LABEL_1': 'Neutral',
                'LABEL_2': 'Positive'
            }

            # Find the highest scoring sentiment
            best_sentiment = max(scores, key=lambda x: x['score'])
            sentiment = label_map.get(best_sentiment['label'], 'Neutral')
            confidence = best_sentiment['score']

            # Calculate sentiment score (-1 to 1 range)
            if sentiment == 'Positive':
                sentiment_score = confidence
            elif sentiment == 'Negative':
                sentiment_score = -confidence
            else:
                sentiment_score = 0.0

            # Get all scores for detailed breakdown
            all_scores = {label_map.get(score['label'], score['label']): score['score'] for score in scores}

            return {
                'sentiment': sentiment,
                'sentiment_score': sentiment_score,
                'confidence': confidence,
                'all_scores': all_scores,
                'method': 'transformer'
            }

        except Exception as e:
            print(f"Advanced sentiment analysis failed: {e}")
            return self._fallback_sentiment(text)

    def _fallback_sentiment(self, text: str) -> Dict[str, Any]:
        """Fallback sentiment analysis using basic word lists."""
        # Simple word-based sentiment for fallback
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
                         'helpful', 'efficient', 'friendly', 'professional', 'satisfied',
                         'happy', 'pleased', 'appreciate', 'thank', 'thanks', 'love',
                         'perfect', 'best', 'improved', 'improvement', 'better', 'nice'}

        negative_words = {'bad', 'terrible', 'awful', 'horrible', 'poor', 'worst',
                         'disappointing', 'disappointed', 'frustrated', 'frustrating',
                         'slow', 'delayed', 'broken', 'damaged', 'unsafe', 'dangerous',
                         'dirty', 'unclean', 'rude', 'unprofessional', 'unhelpful',
                         'inefficient', 'waste', 'problem', 'issue', 'complaint'}

        words = text.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)

        total_sentiment_words = positive_count + negative_count

        if total_sentiment_words == 0:
            return {
                'sentiment': 'Neutral',
                'sentiment_score': 0.0,
                'confidence': 0.5,
                'method': 'fallback'
            }

        sentiment_score = (positive_count - negative_count) / total_sentiment_words
        confidence = min(abs(sentiment_score), 0.8)  # Cap confidence for fallback

        if sentiment_score > 0.1:
            sentiment = 'Positive'
        elif sentiment_score < -0.1:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'

        return {
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'confidence': confidence,
            'method': 'fallback'
        }

    def smart_summarize(self, text: str, max_length: int = 50, min_length: int = 10) -> Dict[str, Any]:
        """
        Generate AI-powered summary of feedback text.

        Args:
            text: Input text to summarize
            max_length: Maximum summary length
            min_length: Minimum summary length

        Returns:
            Dictionary with summary and metadata
        """
        if not self.models_loaded or not text.strip():
            return self._fallback_summarize(text)

        # Don't summarize very short texts
        word_count = len(text.split())
        if word_count < 20:
            return {
                'summary': text,
                'method': 'no_summary',
                'original_length': word_count
            }

        try:
            # Generate summary
            summary_result = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True
            )

            summary = summary_result[0]['summary_text']

            return {
                'summary': summary,
                'method': 'transformer',
                'original_length': word_count,
                'summary_length': len(summary.split())
            }

        except Exception as e:
            print(f"Advanced summarization failed: {e}")
            return self._fallback_summarize(text)

    def _fallback_summarize(self, text: str) -> Dict[str, Any]:
        """Fallback summarization using extractive methods."""
        sentences = text.split('.')
        if len(sentences) <= 2:
            return {
                'summary': text,
                'method': 'fallback',
                'original_length': len(text.split())
            }

        # Simple extractive summary: take first and last sentences
        first_sentence = sentences[0].strip()
        last_sentence = sentences[-2].strip() if sentences[-1].strip() == '' else sentences[-1].strip()

        if len(first_sentence.split()) > 10:
            summary = first_sentence
        else:
            summary = f"{first_sentence}. {last_sentence}"

        return {
            'summary': summary,
            'method': 'fallback',
            'original_length': len(text.split())
        }

    def classify_category_advanced(self, text: str, categories: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Advanced category classification using zero-shot learning.

        Args:
            text: Input text to classify
            categories: List of possible categories (optional)

        Returns:
            Dictionary with classification results
        """
        if categories is None:
            categories = [
                "infrastructure", "transportation", "healthcare", "education",
                "environment", "safety", "services", "utilities", "finance",
                "housing", "employment", "general"
            ]

        if not self.models_loaded or not text.strip():
            return self._fallback_category_classification(text, categories)

        try:
            # Zero-shot classification
            result = self.zero_shot_classifier(text, categories)

            # Get top prediction
            top_category = result['labels'][0]
            confidence = result['scores'][0]

            # Get all scores
            all_scores = dict(zip(result['labels'], result['scores']))

            return {
                'category': top_category.title(),
                'confidence': confidence,
                'all_scores': all_scores,
                'method': 'zero_shot'
            }

        except Exception as e:
            print(f"Advanced category classification failed: {e}")
            return self._fallback_category_classification(text, categories)

    def _fallback_category_classification(self, text: str, categories: List[str]) -> Dict[str, Any]:
        """Fallback category classification using keyword matching."""
        # Simple keyword-based classification
        category_keywords = {
            "infrastructure": ["road", "bridge", "building", "construction", "repair", "maintenance",
                             "pothole", "sidewalk", "street", "highway", "infrastructure"],
            "transportation": ["bus", "train", "traffic", "parking", "transit", "commute", "route",
                             "schedule", "delay", "transport", "vehicle"],
            "healthcare": ["hospital", "clinic", "doctor", "nurse", "medical", "health", "emergency",
                          "appointment", "treatment", "medicine", "patient"],
            "education": ["school", "teacher", "student", "library", "program", "class", "learning",
                         "curriculum", "education", "university", "college"],
            "environment": ["park", "tree", "pollution", "recycling", "waste", "green", "clean",
                           "nature", "sustainability", "environment"],
            "safety": ["police", "fire", "emergency", "crime", "security", "safe", "patrol",
                      "response", "protection", "safety"],
            "services": ["permit", "license", "office", "staff", "service", "wait", "process",
                        "application", "document", "government", "administration"],
            "utilities": ["water", "electricity", "power", "gas", "utility", "bill", "service"],
            "finance": ["tax", "money", "payment", "fee", "budget", "financial", "cost"],
            "housing": ["house", "apartment", "home", "rent", "property", "housing", "building"],
            "employment": ["job", "work", "employment", "unemployed", "hire", "career"]
        }

        text_lower = text.lower()
        category_scores = {}

        for category, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            category_scores[category] = score

        if max(category_scores.values()) > 0:
            best_category = max(category_scores, key=category_scores.get)
            confidence = min(category_scores[best_category] / 5.0, 0.9)  # Normalize confidence
        else:
            best_category = "general"
            confidence = 0.1

        return {
            'category': best_category.title(),
            'confidence': confidence,
            'method': 'keyword_matching'
        }

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """
        Extract named entities from text.

        Args:
            text: Input text

        Returns:
            Dictionary with extracted entities
        """
        if not self.models_loaded or not text.strip():
            return {'entities': [], 'method': 'unavailable'}

        try:
            entities = self.ner_pipeline(text)

            # Group entities by type
            entity_groups = {}
            for entity in entities:
                entity_type = entity['entity_group']
                if entity_type not in entity_groups:
                    entity_groups[entity_type] = []
                entity_groups[entity_type].append({
                    'text': entity['word'],
                    'confidence': entity['score'],
                    'start': entity['start'],
                    'end': entity['end']
                })

            return {
                'entities': entity_groups,
                'method': 'transformer'
            }

        except Exception as e:
            print(f"Entity extraction failed: {e}")
            return {'entities': [], 'method': 'failed'}

    def analyze_comprehensive(self, text: str) -> Dict[str, Any]:
        """
        Comprehensive analysis combining all NLP capabilities.

        Args:
            text: Input text to analyze

        Returns:
            Complete analysis results
        """
        if not text.strip():
            return {
                'sentiment': {'sentiment': 'Neutral', 'sentiment_score': 0.0, 'confidence': 0.0},
                'summary': {'summary': '', 'method': 'empty_text'},
                'category': {'category': 'General', 'confidence': 0.0},
                'entities': {'entities': []},
                'processing_time': 0
            }

        import time
        start_time = time.time()

        # Run all analyses
        sentiment = self.analyze_sentiment_advanced(text)
        summary = self.smart_summarize(text)
        category = self.classify_category_advanced(text)
        entities = self.extract_entities(text)

        processing_time = time.time() - start_time

        return {
            'sentiment': sentiment,
            'summary': summary,
            'category': category,
            'entities': entities,
            'processing_time': round(processing_time, 3),
            'text_length': len(text.split())
        }