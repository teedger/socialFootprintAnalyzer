"""
AI/NLP Analysis Service
Performs sentiment analysis, keyword extraction, and scoring
"""
from typing import List, Dict, Tuple
from textblob import TextBlob
import openai
from config import Config
import json
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)


class AIAnalyzer:
    """AI-powered analysis of online presence data"""

    def __init__(self):
        self.config = Config()
        if self.config.OPENAI_API_KEY:
            openai.api_key = self.config.OPENAI_API_KEY

    def analyze_sentiment(self, text: str) -> str:
        """
        Analyze sentiment of text using TextBlob
        Returns: 'positive', 'neutral', or 'negative'
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity

            if polarity > self.config.SENTIMENT_THRESHOLD_POSITIVE:
                return "positive"
            elif polarity < self.config.SENTIMENT_THRESHOLD_NEGATIVE:
                return "negative"
            else:
                return "neutral"
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return "neutral"

    def calculate_visibility_score(self, mentions: List[Dict]) -> int:
        """
        Calculate visibility score (0-100) based on:
        - Number of mentions
        - Diversity of platforms
        - Recency (if available)
        """
        if not mentions:
            return 0

        # Base score from number of mentions (max 50 points)
        mention_count = len(mentions)
        mention_score = min(mention_count * 2, 50)

        # Platform diversity score (max 30 points)
        platforms = set(m.get("platform", "") for m in mentions)
        diversity_score = min(len(platforms) * 5, 30)

        # Quality score based on sources (max 20 points)
        quality_platforms = {"News", "LinkedIn", "Google Search"}
        quality_count = sum(1 for m in mentions if m.get("platform") in quality_platforms)
        quality_score = min(quality_count * 2, 20)

        total_score = mention_score + diversity_score + quality_score
        return min(int(total_score), 100)

    def calculate_perception_score(self, sentiments: List[str]) -> int:
        """
        Calculate perception score (0-100) based on sentiment analysis
        Positive = good, Negative = bad
        """
        if not sentiments:
            return 50  # Neutral default

        positive_count = sentiments.count("positive")
        negative_count = sentiments.count("negative")
        neutral_count = sentiments.count("neutral")
        total = len(sentiments)

        # Weight: positive +1, neutral 0, negative -1
        weighted_score = (positive_count - negative_count) / total

        # Convert to 0-100 scale (where 50 is neutral)
        perception_score = 50 + (weighted_score * 50)
        return int(max(0, min(100, perception_score)))

    def extract_keywords(self, texts: List[str], top_n: int = 10) -> List[str]:
        """
        Extract top keywords from all text snippets
        """
        try:
            # Combine all texts
            combined_text = " ".join(texts)
            blob = TextBlob(combined_text)

            # Extract noun phrases
            noun_phrases = blob.noun_phrases

            # Count frequency
            from collections import Counter
            word_freq = Counter(noun_phrases)

            # Get top N most common
            top_keywords = [word for word, count in word_freq.most_common(top_n)]
            return top_keywords
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return []

    async def generate_recommendations(self, analysis_data: Dict) -> List[str]:
        """
        Generate AI-powered recommendations using OpenAI
        """
        if not self.config.OPENAI_API_KEY:
            return self._generate_rule_based_recommendations(analysis_data)

        try:
            # Prepare prompt for OpenAI
            # Convert PlatformStats objects to platform names
            platforms = analysis_data.get('platform_distribution', [])
            platform_names = ', '.join([p.platform if hasattr(p, 'platform') else p['platform'] for p in platforms])

            prompt = f"""
Based on the following social footprint analysis, provide 3-5 specific, actionable recommendations
to improve online presence and reputation:

Visibility Score: {analysis_data.get('visibility_score', 0)}/100
Perception Score: {analysis_data.get('perception_score', 0)}/100
Total Mentions: {analysis_data.get('total_mentions', 0)}
Platforms: {platform_names}
Sentiment: {analysis_data.get('sentiment_breakdown', {})}

Provide recommendations as a JSON array of strings.
"""

            client = openai.OpenAI(api_key=self.config.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert digital marketing and reputation management consultant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            recommendations_text = response.choices[0].message.content

            # Try to parse as JSON, fallback to splitting by newlines
            try:
                recommendations = json.loads(recommendations_text)
            except:
                recommendations = [line.strip() for line in recommendations_text.split('\n') if line.strip() and not line.strip().startswith('[') and not line.strip().startswith(']')]

            return recommendations[:5]

        except Exception as e:
            print(f"Error generating AI recommendations: {e}")
            return self._generate_rule_based_recommendations(analysis_data)

    def _generate_rule_based_recommendations(self, analysis_data: Dict) -> List[str]:
        """
        Generate recommendations using rule-based logic (fallback)
        """
        recommendations = []
        visibility = analysis_data.get('visibility_score', 0)
        perception = analysis_data.get('perception_score', 0)
        platforms = analysis_data.get('platform_distribution', [])
        sentiment = analysis_data.get('sentiment_breakdown', {})

        # Visibility recommendations
        if visibility < 30:
            recommendations.append("Increase your online visibility by creating professional profiles on LinkedIn and other platforms")
        elif visibility < 60:
            recommendations.append("Enhance your presence by regularly sharing content and engaging with your professional community")

        # Perception recommendations
        if perception < 40:
            recommendations.append("Address negative mentions and focus on building positive content to improve your reputation")
        elif perception > 70:
            recommendations.append("Maintain your positive reputation by continuing to engage professionally online")

        # Platform-specific recommendations
        platform_names = [p.platform if hasattr(p, 'platform') else p['platform'] for p in platforms]
        if 'LinkedIn' not in platform_names:
            recommendations.append("Create a LinkedIn profile to establish professional credibility")
        if 'News' not in platform_names and visibility > 50:
            recommendations.append("Consider pursuing media opportunities to increase authoritative mentions")

        # Sentiment-based recommendations
        negative_percent = sentiment.get('negative_percent', 0)
        if negative_percent > 20:
            recommendations.append("Monitor and respond to negative mentions professionally to improve perception")

        # Default recommendations if list is too short
        if len(recommendations) < 3:
            recommendations.append("Regularly update your online profiles with current information and achievements")
            recommendations.append("Engage with your audience through thoughtful comments and original content")

        return recommendations[:5]
