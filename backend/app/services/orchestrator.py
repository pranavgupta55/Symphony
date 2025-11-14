"""
Analysis Orchestrator - Coordinates all processing steps
"""
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import traceback

from ..models import AnalysisJob
from .audio_transcription import AudioTranscriptionService
from .audio_features import AudioFeatureExtractor
from .sentiment_analysis import SentimentAnalysisService
from .chart_analysis import ChartAnalysisService
from .fusion import MultiModalFusionService
from .claude_integration import ClaudeIntegrationService


class AnalysisOrchestrator:
    """Orchestrates the complete analysis pipeline"""

    def __init__(self):
        print("🎵 Initializing Symphony AI Orchestrator...")

        # Initialize all services
        self.transcription_service = AudioTranscriptionService()
        self.audio_feature_extractor = AudioFeatureExtractor()
        self.sentiment_service = SentimentAnalysisService()
        self.chart_service = ChartAnalysisService()
        self.fusion_service = MultiModalFusionService()
        self.claude_service = ClaudeIntegrationService()

        print("✅ All services initialized")

    def process_job(self, job_id: str):
        """
        Process a complete analysis job

        Args:
            job_id: Job ID to process
        """
        # Create a new session for this thread
        from ..models import SessionLocal
        db = SessionLocal()

        try:
            job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()
            if not job:
                print(f"❌ Job {job_id} not found")
                return

            print(f"\n{'='*60}")
            print(f"🎬 Starting analysis for job: {job_id}")
            print(f"{'='*60}\n")

            # Update job status
            job.status = "processing"
            job.started_at = datetime.utcnow()
            job.progress = 0.0
            db.commit()

            # Step 1: Transcribe audio (20% progress)
            print("\n[1/7] 🎤 Audio Transcription...")
            transcript_result = self.transcription_service.transcribe_audio(job.audio_path)

            # Add speaker identification
            transcript_result["segments"] = self.transcription_service.identify_speakers(
                transcript_result["segments"]
            )

            job.transcript = transcript_result
            job.progress = 20.0
            db.commit()
            print(f"✅ Transcription complete ({len(transcript_result['segments'])} segments)")

            # Step 2: Extract audio features (35% progress)
            print("\n[2/7] 🎵 Audio Feature Extraction...")
            audio_features = self.audio_feature_extractor.extract_features(job.audio_path)
            job.audio_features = audio_features
            job.progress = 35.0
            db.commit()
            print(f"✅ Audio features extracted (Confidence: {audio_features.get('overall_confidence', 0):.2f})")

            # Step 3: Sentiment analysis (50% progress)
            print("\n[3/7] 📊 Financial Sentiment Analysis...")
            sentiment_results = self.sentiment_service.analyze_transcript(
                transcript_result["segments"]
            )

            # Also analyze prepared vs Q&A
            discourse_analysis = self.sentiment_service.separate_prepared_vs_qa(
                sentiment_results["segments"]
            )
            sentiment_results["discourse_analysis"] = discourse_analysis

            job.sentiment_analysis = sentiment_results
            job.progress = 50.0
            db.commit()
            print(f"✅ Sentiment analysis complete (Overall: {sentiment_results.get('overall_sentiment', 'neutral')})")

            # Step 4: Chart analysis (65% progress)
            print("\n[4/7] 📈 Chart Analysis...")
            chart_results = {"chart_descriptions": [], "extracted_data": [], "inconsistencies": []}

            if job.chart_paths:
                chart_results = self.chart_service.analyze_charts(
                    job.chart_paths,
                    transcript_result.get("full_text", ""),
                    job.company_context or ""
                )

            job.chart_analysis = chart_results
            job.progress = 65.0
            db.commit()
            print(f"✅ Chart analysis complete ({len(chart_results.get('chart_descriptions', []))} charts)")

            # Step 5: Multi-modal fusion (75% progress)
            print("\n[5/7] 🔗 Multi-Modal Fusion...")
            fusion_results = self.fusion_service.fuse_modalities(
                audio_features,
                sentiment_results,
                chart_results
            )

            job.fusion_results = fusion_results
            job.overall_confidence = audio_features.get("overall_confidence")
            job.overall_sentiment = sentiment_results.get("overall_sentiment")
            job.risk_level = fusion_results.get("risk_level")
            job.progress = 75.0
            db.commit()
            print(f"✅ Fusion complete (Credibility: {fusion_results.get('credibility_score', 0):.2f})")

            # Step 6: Claude AI analysis (90% progress)
            print("\n[6/7] 🤖 Claude AI Comprehensive Analysis...")
            try:
                claude_results = self.claude_service.generate_comprehensive_analysis(
                    job.company_name or "Unknown Company",
                    job.company_context or "",
                    transcript_result,
                    audio_features,
                    sentiment_results,
                    chart_results,
                    fusion_results
                )
                print("✅ Claude analysis complete")
            except Exception as e:
                import traceback
                print(f"❌ Claude API Error: {str(e)}")
                print(f"Full traceback:\n{traceback.format_exc()}")
                # Provide fallback analysis based on fusion results
                claude_results = {
                    "executive_summary": f"Multi-modal analysis complete for {job.company_name or 'the company'}. Overall credibility score: {fusion_results.get('credibility_score', 0):.2f}. Risk level: {fusion_results.get('risk_level', 'unknown')}. Claude AI deep analysis failed: {str(e)[:200]}",
                    "risk_indicators": [d.get('description', '') for d in fusion_results.get('discrepancies', [])[:3]],
                    "opportunities": [],
                    "red_flags": [],
                    "confidence_assessment": f"Multi-modal credibility: {fusion_results.get('credibility_score', 0):.2f}/1.0, Audio confidence: {audio_features.get('overall_confidence', 0):.2f}/1.0, Sentiment: {sentiment_results.get('overall_sentiment', 'unknown')}",
                    "overall_recommendation": "Review detailed multi-modal analysis sections for insights.",
                }

            job.claude_analysis = claude_results
            job.progress = 90.0
            db.commit()

            # Step 7: Finalize (100% progress)
            print("\n[7/7] ✨ Finalizing...")
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            job.progress = 100.0
            db.commit()

            duration = (job.completed_at - job.started_at).total_seconds()
            print(f"\n{'='*60}")
            print(f"🎉 Analysis complete in {duration:.1f} seconds!")
            print(f"{'='*60}\n")

        except Exception as e:
            print(f"\n❌ Error processing job {job_id}: {e}")
            print(traceback.format_exc())

            # Update job with error
            try:
                job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()
                if job:
                    job.status = "failed"
                    job.error_message = str(e)
                    job.completed_at = datetime.utcnow()
                    db.commit()
            except Exception as db_error:
                print(f"Failed to update job error status: {db_error}")

        finally:
            db.close()
