"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class AnalysisRequest(BaseModel):
    """Request schema for analysis"""
    company_name: Optional[str] = None
    company_context: Optional[str] = None


class JobStatus(BaseModel):
    """Job status response"""
    id: str
    status: str
    progress: float
    error_message: Optional[str] = None
    created_at: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class TranscriptSegment(BaseModel):
    """Transcript segment with timing"""
    text: str
    start_time: float
    end_time: float
    speaker: Optional[str] = None
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None


class AudioFeatures(BaseModel):
    """Audio features extracted from speech"""
    confidence_timeline: List[Dict[str, Any]]
    stress_indicators: List[Dict[str, Any]]
    overall_confidence: float
    hesitation_count: int
    speech_rate: float
    pitch_variation: float


class SentimentAnalysis(BaseModel):
    """Sentiment analysis results"""
    segments: List[TranscriptSegment]
    overall_sentiment: str
    sentiment_distribution: Dict[str, float]
    key_topics: List[str]
    financial_metrics: List[Dict[str, Any]]


class ChartAnalysis(BaseModel):
    """Chart analysis results"""
    chart_descriptions: List[str]
    extracted_data: List[Dict[str, Any]]
    inconsistencies: List[str]


class ClaudeAnalysis(BaseModel):
    """Claude AI analysis"""
    executive_summary: str
    risk_indicators: List[str]
    opportunities: List[str]
    red_flags: List[str]
    confidence_assessment: str
    overall_recommendation: str


class AnalysisResults(BaseModel):
    """Complete analysis results"""
    id: str
    company_name: Optional[str]
    status: str
    overall_confidence: Optional[float]
    overall_sentiment: Optional[str]
    risk_level: Optional[str]

    transcript: Optional[List[TranscriptSegment]]
    audio_features: Optional[AudioFeatures]
    sentiment_analysis: Optional[SentimentAnalysis]
    chart_analysis: Optional[ChartAnalysis]
    claude_analysis: Optional[ClaudeAnalysis]

    created_at: Optional[str]
    completed_at: Optional[str]


__all__ = [
    "AnalysisRequest",
    "JobStatus",
    "TranscriptSegment",
    "AudioFeatures",
    "SentimentAnalysis",
    "ChartAnalysis",
    "ClaudeAnalysis",
    "AnalysisResults",
]
