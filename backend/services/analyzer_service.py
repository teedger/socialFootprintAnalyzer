"""
Main Analyzer Service
Orchestrates data collection and analysis
"""
from typing import Dict, List
from datetime import datetime
from .data_aggregator import DataAggregator
from .ai_analyzer import AIAnalyzer
from backend.models.schemas import (
    AnalysisResult,
    SentimentBreakdown,
    PlatformStats,
    Mention
)


class AnalyzerService:
    """Main service that orchestrates the analysis process"""

    def __init__(self):
        self.data_aggregator = DataAggregator()
        self.ai_analyzer = AIAnalyzer()

    async def analyze_footprint(self, query: str) -> AnalysisResult:
        """
        Complete analysis pipeline:
        1. Collect data from multiple sources
        2. Analyze sentiment
        3. Calculate scores
        4. Generate recommendations
        """

        # Step 1: Aggregate data
        raw_mentions = await self.data_aggregator.aggregate(query)

        # Step 2: Analyze sentiment for each mention
        mentions_with_sentiment = []
        sentiments = []

        for mention in raw_mentions:
            text_to_analyze = f"{mention.get('title', '')} {mention.get('snippet', '')}"
            sentiment = self.ai_analyzer.analyze_sentiment(text_to_analyze)
            sentiments.append(sentiment)

            mentions_with_sentiment.append({
                **mention,
                "sentiment": sentiment
            })

        # Step 3: Calculate scores
        visibility_score = self.ai_analyzer.calculate_visibility_score(raw_mentions)
        perception_score = self.ai_analyzer.calculate_perception_score(sentiments)

        # Step 4: Calculate sentiment breakdown
        sentiment_breakdown = self._calculate_sentiment_breakdown(sentiments)

        # Step 5: Calculate platform distribution
        platform_distribution = self._calculate_platform_distribution(raw_mentions)

        # Step 6: Extract keywords
        all_text = [f"{m.get('title', '')} {m.get('snippet', '')}" for m in raw_mentions]
        keywords = self.ai_analyzer.extract_keywords(all_text)

        # Step 7: Prepare top mentions
        top_mentions = self._prepare_top_mentions(mentions_with_sentiment[:10])

        # Step 8: Generate recommendations
        analysis_data = {
            "visibility_score": visibility_score,
            "perception_score": perception_score,
            "total_mentions": len(raw_mentions),
            "platform_distribution": platform_distribution,
            "sentiment_breakdown": sentiment_breakdown
        }
        recommendations = await self.ai_analyzer.generate_recommendations(analysis_data)

        # Step 9: Build final result
        result = AnalysisResult(
            query=query,
            visibility_score=visibility_score,
            perception_score=perception_score,
            total_mentions=len(raw_mentions),
            sentiment_breakdown=sentiment_breakdown,
            platform_distribution=platform_distribution,
            top_mentions=top_mentions,
            keywords=keywords,
            recommendations=recommendations,
            analyzed_at=datetime.now().isoformat()
        )

        return result

    def _calculate_sentiment_breakdown(self, sentiments: List[str]) -> SentimentBreakdown:
        """Calculate sentiment breakdown with percentages"""
        total = len(sentiments) if sentiments else 1

        positive = sentiments.count("positive")
        neutral = sentiments.count("neutral")
        negative = sentiments.count("negative")

        return SentimentBreakdown(
            positive=positive,
            neutral=neutral,
            negative=negative,
            positive_percent=round((positive / total) * 100, 1),
            neutral_percent=round((neutral / total) * 100, 1),
            negative_percent=round((negative / total) * 100, 1)
        )

    def _calculate_platform_distribution(self, mentions: List[Dict]) -> List[PlatformStats]:
        """Calculate distribution of mentions across platforms"""
        from collections import Counter

        if not mentions:
            return []

        platforms = [m.get("platform", "Unknown") for m in mentions]
        platform_counts = Counter(platforms)
        total = len(mentions)

        distribution = []
        for platform, count in platform_counts.most_common():
            distribution.append(PlatformStats(
                platform=platform,
                count=count,
                percentage=round((count / total) * 100, 1)
            ))

        return distribution

    def _prepare_top_mentions(self, mentions: List[Dict]) -> List[Mention]:
        """Convert raw mentions to Mention objects"""
        top_mentions = []

        for m in mentions:
            mention = Mention(
                platform=m.get("platform", "Unknown"),
                title=m.get("title", ""),
                url=m.get("url", ""),
                snippet=m.get("snippet", ""),
                sentiment=m.get("sentiment"),
                date=m.get("date")
            )
            top_mentions.append(mention)

        return top_mentions
