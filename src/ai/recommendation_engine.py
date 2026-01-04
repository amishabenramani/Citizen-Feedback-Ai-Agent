"""
Recommendation Engine Module
Intelligent recommendation system combining all AI components.
"""

import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class RecommendationEngine:
    """
    AI-powered recommendation engine for:
    - Smart feedback prioritization
    - Automated action suggestions
    - Resource allocation recommendations
    - Trend-based insights
    """

    def __init__(self, advanced_nlp=None, ml_predictor=None, openai_assistant=None, text_embeddings=None):
        """
        Initialize recommendation engine with AI components.

        Args:
            advanced_nlp: Advanced NLP analyzer instance
            ml_predictor: ML predictor instance
            openai_assistant: OpenAI assistant instance
            text_embeddings: Text embeddings instance
        """
        self.nlp = advanced_nlp
        self.ml = ml_predictor
        self.openai = openai_assistant
        self.embeddings = text_embeddings

    def analyze_feedback_comprehensive(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive AI analysis of a single feedback item.

        Args:
            feedback_data: Feedback dictionary

        Returns:
            Complete analysis with recommendations
        """
        analysis = {
            'feedback_id': feedback_data.get('id'),
            'timestamp': datetime.now().isoformat(),
            'analyses': {},
            'recommendations': {},
            'confidence_scores': {}
        }

        # 1. Advanced NLP Analysis
        if self.nlp:
            try:
                text = feedback_data.get('feedback', '')
                nlp_result = self.nlp.analyze_comprehensive(text)

                analysis['analyses']['nlp'] = nlp_result
                analysis['confidence_scores']['nlp'] = nlp_result.get('text_length', 0) > 10

            except Exception as e:
                analysis['analyses']['nlp'] = {'error': str(e)}

        # 2. ML-based Priority Prediction
        if self.ml:
            try:
                priority_result = self.ml.predict_priority(feedback_data)
                analysis['analyses']['priority_ml'] = priority_result
                analysis['confidence_scores']['priority'] = priority_result.get('confidence', 0)

            except Exception as e:
                analysis['analyses']['priority_ml'] = {'error': str(e)}

        # 3. SLA Breach Prediction
        if self.ml:
            try:
                sla_result = self.ml.predict_sla_breach_probability(feedback_data)
                analysis['analyses']['sla_prediction'] = sla_result
                analysis['confidence_scores']['sla'] = sla_result.get('confidence', 0)

            except Exception as e:
                analysis['analyses']['sla_prediction'] = {'error': str(e)}

        # 4. Similar Feedback Detection
        if self.embeddings:
            try:
                feedback_id = feedback_data.get('id')
                if feedback_id:
                    similar = self.embeddings.find_similar_feedback(feedback_id, top_k=3)
                    analysis['analyses']['similar_feedback'] = similar
                    analysis['confidence_scores']['similarity'] = len(similar) > 0

            except Exception as e:
                analysis['analyses']['similar_feedback'] = {'error': str(e)}

        # 5. OpenAI-powered Analysis (if available)
        if self.openai and self.openai.is_available():
            try:
                # Generate response suggestion
                response_suggestion = self.openai.generate_response_suggestion(feedback_data)
                analysis['analyses']['response_suggestion'] = response_suggestion

                # Complex classification
                complex_classification = self.openai.classify_complex_feedback(feedback_data)
                analysis['analyses']['complex_classification'] = complex_classification

                analysis['confidence_scores']['openai'] = True

            except Exception as e:
                analysis['analyses']['openai'] = {'error': str(e)}

        # Generate unified recommendations
        analysis['recommendations'] = self._generate_unified_recommendations(analysis)

        return analysis

    def _generate_unified_recommendations(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate unified recommendations from all AI analyses."""
        recommendations = {
            'priority_level': 'Medium',
            'urgency_action': 'Standard processing',
            'department_suggestions': [],
            'estimated_resolution_time': '3-5 business days',
            'action_items': [],
            'risk_level': 'Low',
            'similar_cases': 0,
            'confidence_level': 'Medium'
        }

        # Priority determination
        priority_scores = []

        # ML priority prediction
        if 'priority_ml' in analysis['analyses']:
            ml_priority = analysis['analyses']['priority_ml'].get('predicted_priority', 'Medium')
            priority_map = {'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}
            priority_scores.append(priority_map.get(ml_priority, 2))

        # NLP sentiment-based priority
        if 'nlp' in analysis['analyses']:
            sentiment = analysis['analyses']['nlp'].get('sentiment', 'Neutral')
            if sentiment == 'Negative':
                priority_scores.append(3)  # Higher priority for negative feedback
            elif sentiment == 'Positive':
                priority_scores.append(1)  # Lower priority for positive feedback

        # SLA risk
        if 'sla_prediction' in analysis['analyses']:
            breach_prob = analysis['analyses']['sla_prediction'].get('breach_probability', 0)
            if breach_prob > 0.7:
                priority_scores.append(4)
                recommendations['risk_level'] = 'High'
            elif breach_prob > 0.4:
                priority_scores.append(3)
                recommendations['risk_level'] = 'Medium'

        # Calculate final priority
        if priority_scores:
            avg_priority = sum(priority_scores) / len(priority_scores)
            if avg_priority >= 3.5:
                recommendations['priority_level'] = 'Critical'
                recommendations['urgency_action'] = 'Immediate attention required'
            elif avg_priority >= 2.5:
                recommendations['priority_level'] = 'High'
                recommendations['urgency_action'] = 'Expedited processing'
            elif avg_priority >= 1.5:
                recommendations['priority_level'] = 'Medium'
            else:
                recommendations['priority_level'] = 'Low'
                recommendations['urgency_action'] = 'Standard processing'

        # Department suggestions
        departments = set()

        if 'complex_classification' in analysis['analyses']:
            dept = analysis['analyses']['complex_classification'].get('suggested_department')
            if dept:
                departments.add(dept)

        # Category-based department mapping
        category_dept_map = {
            'Infrastructure': 'Public Works',
            'Transportation': 'Transportation',
            'Healthcare': 'Health Department',
            'Education': 'Education Department',
            'Environment': 'Environmental Services',
            'Safety': 'Public Safety',
            'Utilities': 'Public Utilities',
            'Housing': 'Housing Authority'
        }

        feedback_category = analysis.get('analyses', {}).get('nlp', {}).get('category', {}).get('category')
        if feedback_category in category_dept_map:
            departments.add(category_dept_map[feedback_category])

        recommendations['department_suggestions'] = list(departments)

        # Resolution time estimation
        urgency = analysis.get('analyses', {}).get('priority_ml', {}).get('predicted_priority', 'Medium')
        time_estimates = {
            'Critical': '1-2 business days',
            'High': '2-3 business days',
            'Medium': '3-5 business days',
            'Low': '1-2 weeks'
        }
        recommendations['estimated_resolution_time'] = time_estimates.get(urgency, '3-5 business days')

        # Action items
        action_items = []

        if recommendations['priority_level'] in ['Critical', 'High']:
            action_items.append("Assign dedicated staff immediately")
            action_items.append("Schedule follow-up within 24 hours")

        if recommendations['risk_level'] == 'High':
            action_items.append("Monitor SLA compliance closely")
            action_items.append("Prepare escalation procedures")

        if 'similar_feedback' in analysis['analyses']:
            similar_count = len(analysis['analyses']['similar_feedback'])
            recommendations['similar_cases'] = similar_count
            if similar_count > 2:
                action_items.append(f"Review {similar_count} similar cases for systemic issues")

        recommendations['action_items'] = action_items

        # Confidence level
        confidence_scores = analysis.get('confidence_scores', {})
        avg_confidence = sum(confidence_scores.values()) / len(confidence_scores) if confidence_scores else 0.5

        if avg_confidence > 0.8:
            recommendations['confidence_level'] = 'High'
        elif avg_confidence > 0.6:
            recommendations['confidence_level'] = 'Medium'
        else:
            recommendations['confidence_level'] = 'Low'

        return recommendations

    def analyze_bulk_feedback(self, feedback_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze multiple feedback items for patterns and insights.

        Args:
            feedback_list: List of feedback dictionaries

        Returns:
            Bulk analysis results
        """
        bulk_analysis = {
            'total_feedbacks': len(feedback_list),
            'timestamp': datetime.now().isoformat(),
            'pattern_analysis': {},
            'priority_distribution': {},
            'category_insights': {},
            'trend_analysis': {},
            'recommendations': []
        }

        if not feedback_list:
            return bulk_analysis

        # Convert to DataFrame for analysis
        df = pd.DataFrame(feedback_list)

        # Priority distribution
        if 'urgency' in df.columns:
            bulk_analysis['priority_distribution'] = df['urgency'].value_counts().to_dict()

        # Category insights
        if 'category' in df.columns:
            category_counts = df['category'].value_counts()
            bulk_analysis['category_insights'] = {
                'top_categories': category_counts.head(5).to_dict(),
                'total_categories': len(category_counts)
            }

        # Sentiment analysis
        if 'sentiment' in df.columns:
            sentiment_dist = df['sentiment'].value_counts().to_dict()
            bulk_analysis['pattern_analysis']['sentiment_distribution'] = sentiment_dist

            # Calculate sentiment trend
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                df = df.sort_values('timestamp')
                rolling_sentiment = df['sentiment_score'].rolling(window=10).mean()
                bulk_analysis['trend_analysis']['sentiment_trend'] = rolling_sentiment.dropna().tolist()

        # OpenAI theme analysis (if available)
        if self.openai and self.openai.is_available() and len(feedback_list) > 5:
            try:
                theme_analysis = self.openai.analyze_feedback_themes(feedback_list)
                bulk_analysis['pattern_analysis']['ai_themes'] = theme_analysis
            except Exception as e:
                bulk_analysis['pattern_analysis']['ai_themes'] = {'error': str(e)}

        # Generate bulk recommendations
        bulk_analysis['recommendations'] = self._generate_bulk_recommendations(bulk_analysis)

        return bulk_analysis

    def _generate_bulk_recommendations(self, bulk_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on bulk analysis."""
        recommendations = []

        # Priority-based recommendations
        priority_dist = bulk_analysis.get('priority_distribution', {})
        high_priority = priority_dist.get('High', 0) + priority_dist.get('Critical', 0)
        total = bulk_analysis.get('total_feedbacks', 1)

        if high_priority / total > 0.3:
            recommendations.append("⚠️ High volume of urgent feedback - consider resource reallocation")

        # Category-based recommendations
        top_categories = bulk_analysis.get('category_insights', {}).get('top_categories', {})
        if top_categories:
            top_category = max(top_categories, key=top_categories.get)
            recommendations.append(f"📊 Focus on {top_category} issues - highest volume category")

        # Sentiment-based recommendations
        sentiment_dist = bulk_analysis.get('pattern_analysis', {}).get('sentiment_distribution', {})
        negative_pct = sentiment_dist.get('Negative', 0) / total if total > 0 else 0

        if negative_pct > 0.5:
            recommendations.append("😟 High negative sentiment - review service quality")
        elif negative_pct < 0.2:
            recommendations.append("🙂 Generally positive feedback - maintain good service")

        # AI theme recommendations
        ai_themes = bulk_analysis.get('pattern_analysis', {}).get('ai_themes', {})
        if 'themes' in ai_themes and ai_themes['themes']:
            top_theme = ai_themes['themes'][0]
            recommendations.append(f"🎯 Address '{top_theme.get('theme', 'Unknown')}' - most common theme")

        if not recommendations:
            recommendations.append("✅ Feedback patterns look normal - continue standard operations")

        return recommendations

    def get_system_health(self) -> Dict[str, Any]:
        """Get health status of all AI components."""
        health = {
            'timestamp': datetime.now().isoformat(),
            'components': {},
            'overall_status': 'healthy',
            'issues': []
        }

        # Check NLP component
        if self.nlp:
            health['components']['nlp'] = {
                'available': self.nlp.models_loaded,
                'status': 'operational' if self.nlp.models_loaded else 'failed'
            }
        else:
            health['components']['nlp'] = {'available': False, 'status': 'not_initialized'}

        # Check ML component
        if self.ml:
            training_status = self.ml.get_training_status()
            health['components']['ml'] = {
                'available': True,
                'training_status': training_status,
                'status': 'operational' if any(training_status.values()) else 'not_trained'
            }
        else:
            health['components']['ml'] = {'available': False, 'status': 'not_initialized'}

        # Check OpenAI component
        if self.openai:
            health['components']['openai'] = {
                'available': self.openai.is_available(),
                'status': 'operational' if self.openai.is_available() else 'api_unavailable'
            }
        else:
            health['components']['openai'] = {'available': False, 'status': 'not_initialized'}

        # Check embeddings component
        if self.embeddings:
            health['components']['embeddings'] = {
                'available': self.embeddings.is_available(),
                'has_index': self.embeddings.index is not None,
                'status': 'operational' if self.embeddings.is_available() else 'model_unavailable'
            }
        else:
            health['components']['embeddings'] = {'available': False, 'status': 'not_initialized'}

        # Overall status
        operational_components = sum(1 for comp in health['components'].values()
                                   if comp['status'] == 'operational')
        total_components = len(health['components'])

        if operational_components == total_components:
            health['overall_status'] = 'healthy'
        elif operational_components >= total_components / 2:
            health['overall_status'] = 'degraded'
        else:
            health['overall_status'] = 'unhealthy'

        # Collect issues
        for comp_name, comp_status in health['components'].items():
            if comp_status['status'] != 'operational':
                health['issues'].append(f"{comp_name}: {comp_status['status']}")

        return health

    def optimize_resources(self, current_workload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide resource optimization recommendations.

        Args:
            current_workload: Current system workload data

        Returns:
            Optimization recommendations
        """
        recommendations = {
            'staffing_adjustments': [],
            'process_improvements': [],
            'system_optimizations': [],
            'priority_actions': []
        }

        # Analyze workload patterns
        high_priority_count = current_workload.get('high_priority_count', 0)
        total_staff = current_workload.get('total_staff', 1)
        avg_resolution_time = current_workload.get('avg_resolution_time', 5)

        # Staffing recommendations
        workload_ratio = high_priority_count / total_staff
        if workload_ratio > 5:
            recommendations['staffing_adjustments'].append(
                "Critical: High workload ratio - consider immediate staff augmentation"
            )
        elif workload_ratio > 3:
            recommendations['staffing_adjustments'].append(
                "Consider additional staff training or temporary help"
            )

        # Process improvements
        if avg_resolution_time > 7:
            recommendations['process_improvements'].append(
                "Streamline resolution processes to reduce average time"
            )

        if self.nlp and self.nlp.models_loaded:
            recommendations['system_optimizations'].append(
                "NLP models operational - AI analysis active"
            )

        return recommendations