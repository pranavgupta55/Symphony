"""
Database models for Symphony AI
"""
from sqlalchemy import Column, String, DateTime, Integer, Float, Text, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()


def generate_uuid():
    """Generate a unique ID"""
    return str(uuid.uuid4())


class AnalysisJob(Base):
    """Analysis job model"""
    __tablename__ = "analysis_jobs"

    id = Column(String, primary_key=True, default=generate_uuid)
    company_name = Column(String, nullable=True)
    company_context = Column(Text, nullable=True)

    # File paths
    audio_path = Column(String, nullable=False)
    chart_paths = Column(JSON, nullable=True)  # List of chart file paths

    # Status
    status = Column(String, default="pending")  # pending, processing, completed, failed
    progress = Column(Float, default=0.0)  # 0-100
    error_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Results (stored as JSON)
    transcript = Column(JSON, nullable=True)
    audio_features = Column(JSON, nullable=True)
    sentiment_analysis = Column(JSON, nullable=True)
    chart_analysis = Column(JSON, nullable=True)
    fusion_results = Column(JSON, nullable=True)
    claude_analysis = Column(JSON, nullable=True)

    # Summary metrics
    overall_confidence = Column(Float, nullable=True)
    overall_sentiment = Column(String, nullable=True)
    risk_level = Column(String, nullable=True)  # low, medium, high

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "company_name": self.company_name,
            "company_context": self.company_context,
            "audio_path": self.audio_path,
            "chart_paths": self.chart_paths,
            "status": self.status,
            "progress": self.progress,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "overall_confidence": self.overall_confidence,
            "overall_sentiment": self.overall_sentiment,
            "risk_level": self.risk_level,
        }

    def get_full_results(self):
        """Get complete results including all analysis data"""
        return {
            **self.to_dict(),
            "transcript": self.transcript,
            "audio_features": self.audio_features,
            "sentiment_analysis": self.sentiment_analysis,
            "chart_analysis": self.chart_analysis,
            "fusion_results": self.fusion_results,
            "claude_analysis": self.claude_analysis,
        }
