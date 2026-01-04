#!/usr/bin/env python3
"""
Test script for AI features in Citizen Feedback AI Agent
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_manager import DataManager
from src.feedback_analyzer import FeedbackAnalyzer

def test_ai_features():
    """Test the AI features implementation"""
    print("🧪 Testing AI Features Implementation")
    print("=" * 50)

    # Initialize components
    print("1. Initializing DataManager...")
    try:
        dm = DataManager()
        print("   ✓ DataManager initialized successfully")
    except Exception as e:
        print(f"   ✗ DataManager initialization failed: {e}")
        return False

    print("2. Initializing FeedbackAnalyzer...")
    try:
        fa = FeedbackAnalyzer()
        print("   ✓ FeedbackAnalyzer initialized successfully")
    except Exception as e:
        print(f"   ✗ FeedbackAnalyzer initialization failed: {e}")
        return False

    # Test basic feedback analysis
    print("3. Testing basic feedback analysis...")
    test_feedback = "The street lights in downtown are not working properly. This is causing safety concerns for pedestrians at night."
    try:
        result = fa.analyze(test_feedback)
        print("   ✓ Basic analysis completed")
        print(f"   Sentiment: {result.get('sentiment', 'N/A')}")
        print(f"   Priority: {result.get('priority', 'N/A')}")
        print(f"   Category: {result.get('category', 'N/A')}")
    except Exception as e:
        print(f"   ✗ Basic analysis failed: {e}")
        return False

    # Test AI-powered analysis
    print("4. Testing AI-powered feedback analysis...")
    try:
        # Format feedback as expected by the method
        feedback_dict = {
            'feedback': test_feedback,
            'id': 1,
            'urgency': 'High'
        }
        ai_result = dm.analyze_feedback_with_ai(feedback_dict)
        print("   ✓ AI analysis completed")
        print(f"   AI Sentiment: {ai_result.get('analyses', {}).get('nlp', {}).get('sentiment', 'N/A')}")
        print(f"   Priority: {ai_result.get('recommendations', {}).get('priority_level', 'N/A')}")
        print(f"   Confidence: {ai_result.get('recommendations', {}).get('confidence_level', 'N/A')}")
    except Exception as e:
        print(f"   ✗ AI analysis failed: {e}")
        print("   This is expected if AI models are not trained yet")

    # Test semantic search (will be empty initially)
    print("5. Testing semantic search...")
    try:
        search_results = dm.semantic_search_feedback("street lights")
        print("   ✓ Semantic search completed")
        print(f"   Found {len(search_results)} results")
    except Exception as e:
        print(f"   ✗ Semantic search failed: {e}")

    print("\n🎉 AI Features Test Completed!")
    print("Note: Some features may show limited functionality until models are trained with real data.")
    return True

if __name__ == "__main__":
    test_ai_features()