"""
Data models and schemas for the Social Footprint Analyzer
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class SearchRequest(BaseModel):
    """Request model for footprint analysis"""
    query: str = Field(..., min_length=2, max_length=200, description="Name or organization to analyze")


class Mention(BaseModel):
    """Single mention from a source"""
    platform: str
    title: str
    url: str
    snippet: str
    sentiment: Optional[str] = None
    date: Optional[str] = None


class PlatformStats(BaseModel):
    """Statistics for a specific platform"""
    platform: str
    count: int
    percentage: float


class SentimentBreakdown(BaseModel):
    """Sentiment analysis breakdown"""
    positive: int
    neutral: int
    negative: int
    positive_percent: float
    neutral_percent: float
    negative_percent: float


class AnalysisResult(BaseModel):
    """Complete analysis result"""
    query: str
    visibility_score: int = Field(..., ge=0, le=100)
    perception_score: int = Field(..., ge=0, le=100)
    total_mentions: int
    sentiment_breakdown: SentimentBreakdown
    platform_distribution: List[PlatformStats]
    top_mentions: List[Mention]
    keywords: List[str]
    recommendations: List[str]
    analyzed_at: str


class ProgressUpdate(BaseModel):
    """Progress update during analysis"""
    status: str
    message: str
    progress: int = Field(..., ge=0, le=100)
