"""
OpenAI Integration Module
GPT-powered features for response generation, theme analysis, and intelligent assistance.
"""

import os
import openai
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OpenAIAssistant:
    """
    OpenAI-powered assistant for:
    - Response suggestion generation
    - Theme analysis and insights
    - Intelligent feedback categorization
    - Automated content generation
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize OpenAI assistant.

        Args:
            api_key: OpenAI API key (optional, will use env var)
            model: GPT model to use
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.client = None

        if self.api_key:
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
                print("✓ OpenAI client initialized successfully")
            except Exception as e:
                print(f"⚠️ Failed to initialize OpenAI client: {e}")
        else:
            print("⚠️ OpenAI API key not found. Set OPENAI_API_KEY environment variable.")

    def is_available(self) -> bool:
        """Check if OpenAI is available."""
        return self.client is not None

    def generate_response_suggestion(self, feedback: Dict[str, Any],
                                   tone: str = "professional",
                                   max_length: int = 300) -> Dict[str, Any]:
        """
        Generate suggested response for government officials.

        Args:
            feedback: Feedback data dictionary
            tone: Response tone (professional, empathetic, formal)
            max_length: Maximum response length

        Returns:
            Generated response with metadata
        """
        if not self.is_available():
            return {
                'response': 'OpenAI integration not available. Please configure API key.',
                'method': 'unavailable'
            }

        prompt = f"""
        As a government official responding to citizen feedback, generate a professional, empathetic response.

        FEEDBACK DETAILS:
        - Category: {feedback.get('category', 'General')}
        - Title: {feedback.get('title', 'Untitled')}
        - Description: {feedback.get('feedback', '')}
        - Sentiment: {feedback.get('sentiment', 'Neutral')}
        - Urgency: {feedback.get('urgency', 'Medium')}
        - Citizen Name: {feedback.get('name', 'Citizen')}

        REQUIREMENTS:
        1. Acknowledge the citizen's concern and show empathy
        2. Provide clear next steps or solutions
        3. Include realistic timeline if applicable
        4. Maintain {tone} tone throughout
        5. Keep response under {max_length} characters
        6. End with contact information offer

        Generate the response:
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )

            generated_response = response.choices[0].message.content.strip()

            return {
                'response': generated_response,
                'method': 'openai',
                'model': self.model,
                'tone': tone,
                'length': len(generated_response),
                'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else None
            }

        except Exception as e:
            print(f"OpenAI response generation failed: {e}")
            return {
                'response': f'Error generating response: {str(e)}',
                'method': 'error'
            }

    def analyze_feedback_themes(self, feedback_list: List[Dict[str, Any]],
                               max_feedbacks: int = 50) -> Dict[str, Any]:
        """
        Analyze common themes and patterns in feedback data.

        Args:
            feedback_list: List of feedback dictionaries
            max_feedbacks: Maximum number of feedbacks to analyze

        Returns:
            Theme analysis results
        """
        if not self.is_available():
            return {'themes': [], 'method': 'unavailable'}

        # Limit feedback for API constraints
        sample_feedbacks = feedback_list[:max_feedbacks]

        # Prepare feedback summaries
        feedback_summaries = []
        for fb in sample_feedbacks:
            summary = f"Category: {fb.get('category', 'N/A')} | Sentiment: {fb.get('sentiment', 'N/A')} | {fb.get('title', 'Untitled')}: {fb.get('feedback', '')[:200]}..."
            feedback_summaries.append(summary)

        prompt = f"""
        Analyze these {len(sample_feedbacks)} citizen feedback messages and identify the top 5 common themes or issues.

        FEEDBACK DATA:
        {chr(10).join(f"- {summary}" for summary in feedback_summaries)}

        ANALYSIS REQUIREMENTS:
        1. Identify recurring themes or problems
        2. Calculate frequency of each theme
        3. Provide specific examples for each theme
        4. Suggest priority levels for addressing each theme
        5. Recommend actionable solutions

        Format your response as a JSON object with this structure:
        {{
            "themes": [
                {{
                    "theme": "Theme name",
                    "frequency": 15,
                    "percentage": 30.0,
                    "examples": ["example 1", "example 2"],
                    "priority": "High/Medium/Low",
                    "recommendations": ["solution 1", "solution 2"]
                }}
            ],
            "total_feedbacks": {len(sample_feedbacks)},
            "analysis_period": "current_dataset"
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.3,  # Lower temperature for more consistent analysis
                response_format={"type": "json_object"}
            )

            result_text = response.choices[0].message.content.strip()

            try:
                analysis_result = json.loads(result_text)
                analysis_result['method'] = 'openai'
                analysis_result['model'] = self.model
                return analysis_result
            except json.JSONDecodeError:
                return {
                    'themes': [],
                    'error': 'Failed to parse analysis results',
                    'raw_response': result_text,
                    'method': 'openai_error'
                }

        except Exception as e:
            print(f"OpenAI theme analysis failed: {e}")
            return {
                'themes': [],
                'error': str(e),
                'method': 'error'
            }

    def generate_action_plan(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an action plan for addressing specific feedback.

        Args:
            feedback: Individual feedback item

        Returns:
            Action plan with steps and timeline
        """
        if not self.is_available():
            return {'action_plan': [], 'method': 'unavailable'}

        prompt = f"""
        Create a detailed action plan to address this citizen feedback.

        FEEDBACK:
        - Category: {feedback.get('category', 'General')}
        - Title: {feedback.get('title', 'Untitled')}
        - Description: {feedback.get('feedback', '')}
        - Urgency: {feedback.get('urgency', 'Medium')}
        - Sentiment: {feedback.get('sentiment', 'Neutral')}

        Generate an action plan with:
        1. Immediate actions (within 24 hours)
        2. Short-term solutions (1-7 days)
        3. Long-term improvements (1-4 weeks)
        4. Responsible departments
        5. Success metrics

        Format as JSON:
        {{
            "immediate_actions": ["action1", "action2"],
            "short_term": ["action1", "action2"],
            "long_term": ["action1", "action2"],
            "departments": ["dept1", "dept2"],
            "timeline": "X weeks",
            "success_metrics": ["metric1", "metric2"]
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.4,
                response_format={"type": "json_object"}
            )

            result_text = response.choices[0].message.content.strip()

            try:
                action_plan = json.loads(result_text)
                action_plan['method'] = 'openai'
                return action_plan
            except json.JSONDecodeError:
                return {
                    'action_plan': [],
                    'error': 'Failed to parse action plan',
                    'method': 'openai_error'
                }

        except Exception as e:
            print(f"OpenAI action plan generation failed: {e}")
            return {
                'action_plan': [],
                'error': str(e),
                'method': 'error'
            }

    def classify_complex_feedback(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Advanced classification for complex or ambiguous feedback.

        Args:
            feedback: Feedback data

        Returns:
            Enhanced classification results
        """
        if not self.is_available():
            return {'categories': [], 'method': 'unavailable'}

        prompt = f"""
        Analyze this citizen feedback and provide detailed classification.

        FEEDBACK TEXT: {feedback.get('feedback', '')}

        Provide classification in JSON format:
        {{
            "primary_category": "main category",
            "secondary_categories": ["cat1", "cat2"],
            "urgency_level": "High/Medium/Low",
            "sentiment_impact": "Positive/Negative/Neutral",
            "key_issues": ["issue1", "issue2"],
            "suggested_department": "department name",
            "complexity_level": "Simple/Moderate/Complex",
            "estimated_resolution_time": "X days"
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.2,
                response_format={"type": "json_object"}
            )

            result_text = response.choices[0].message.content.strip()

            try:
                classification = json.loads(result_text)
                classification['method'] = 'openai'
                return classification
            except json.JSONDecodeError:
                return {
                    'primary_category': 'General',
                    'method': 'openai_error'
                }

        except Exception as e:
            print(f"OpenAI classification failed: {e}")
            return {
                'primary_category': 'General',
                'method': 'error'
            }

    def generate_weekly_report(self, feedback_data: List[Dict[str, Any]],
                              time_period: str = "week") -> Dict[str, Any]:
        """
        Generate comprehensive weekly/monthly reports.

        Args:
            feedback_data: List of feedback items
            time_period: Report period (week/month)

        Returns:
            Generated report
        """
        if not self.is_available():
            return {'report': '', 'method': 'unavailable'}

        # Calculate basic statistics
        total_feedbacks = len(feedback_data)
        categories = {}
        sentiments = {}
        urgencies = {}

        for fb in feedback_data:
            cat = fb.get('category', 'Unknown')
            sent = fb.get('sentiment', 'Unknown')
            urg = fb.get('urgency', 'Unknown')

            categories[cat] = categories.get(cat, 0) + 1
            sentiments[sent] = sentiments.get(sent, 0) + 1
            urgencies[urg] = urgencies.get(urg, 0) + 1

        prompt = f"""
        Generate a comprehensive {time_period}ly report for citizen feedback system.

        STATISTICS:
        - Total Feedback: {total_feedbacks}
        - Categories: {categories}
        - Sentiments: {sentiments}
        - Urgency Levels: {urgencies}

        SAMPLE FEEDBACK TITLES:
        {chr(10).join([f"- {fb.get('title', 'Untitled')}" for fb in feedback_data[:10]])}

        Generate a professional report including:
        1. Executive Summary
        2. Key Trends and Patterns
        3. Top Issues and Categories
        4. Sentiment Analysis
        5. Recommendations for Improvement
        6. Action Items

        Keep the report concise but comprehensive.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1200,
                temperature=0.5
            )

            report = response.choices[0].message.content.strip()

            return {
                'report': report,
                'method': 'openai',
                'period': time_period,
                'total_feedbacks': total_feedbacks,
                'generated_at': time.time()
            }

        except Exception as e:
            print(f"OpenAI report generation failed: {e}")
            return {
                'report': f'Error generating {time_period}ly report: {str(e)}',
                'method': 'error'
            }

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get OpenAI API usage statistics."""
        if not self.is_available():
            return {'available': False}

        # Note: OpenAI doesn't provide usage stats through API
        # This would need to be tracked separately
        return {
            'available': True,
            'model': self.model,
            'note': 'Usage tracking requires separate implementation'
        }