"""
Audio Transcription Service using OpenAI Whisper API
"""
import openai
from pathlib import Path
from typing import List, Dict, Any
from ..core.config import settings


class AudioTranscriptionService:
    """Service for transcribing audio using Whisper API"""

    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    def transcribe_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe audio file using Whisper API

        Args:
            audio_path: Path to audio file

        Returns:
            Dictionary with transcript and segments
        """
        try:
            audio_file = Path(audio_path)
            if not audio_file.exists():
                raise FileNotFoundError(f"Audio file not found: {audio_path}")

            print(f"🎤 Transcribing audio: {audio_file.name}")

            # Transcribe with timestamps
            with open(audio_path, "rb") as audio:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )

            # Extract segments with timing
            segments = []
            if hasattr(transcript, 'segments') and transcript.segments:
                for seg in transcript.segments:
                    segments.append({
                        "text": getattr(seg, "text", ""),
                        "start_time": getattr(seg, "start", 0.0),
                        "end_time": getattr(seg, "end", 0.0),
                        "speaker": None,  # Will be filled by diarization
                    })
            else:
                # Fallback: single segment
                segments.append({
                    "text": transcript.text,
                    "start_time": 0.0,
                    "end_time": 0.0,
                    "speaker": None,
                })

            result = {
                "full_text": transcript.text,
                "segments": segments,
                "language": getattr(transcript, 'language', 'en'),
                "duration": getattr(transcript, 'duration', 0.0),
            }

            print(f"✅ Transcription complete: {len(segments)} segments")
            return result

        except Exception as e:
            print(f"❌ Transcription error: {e}")
            raise Exception(f"Failed to transcribe audio: {str(e)}")

    def identify_speakers(self, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Simple speaker identification heuristic
        In a real implementation, this would use speaker diarization models

        Args:
            segments: List of transcript segments

        Returns:
            Segments with speaker labels
        """
        # Simple heuristic: First ~30% is usually CEO, middle is CFO, rest is Q&A
        total_segments = len(segments)

        for i, segment in enumerate(segments):
            progress = i / total_segments

            if progress < 0.3:
                segment["speaker"] = "CEO"
                segment["segment_type"] = "prepared_statement"
            elif progress < 0.5:
                segment["speaker"] = "CFO"
                segment["segment_type"] = "prepared_statement"
            else:
                # Alternate between analyst and executive
                if i % 2 == 0:
                    segment["speaker"] = "Analyst"
                    segment["segment_type"] = "qa"
                else:
                    segment["speaker"] = "Executive"
                    segment["segment_type"] = "qa"

        return segments

    def separate_qa_from_prepared(self, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Separate Q&A section from prepared statements

        Args:
            segments: List of segments with speaker info

        Returns:
            Dictionary with separated sections
        """
        prepared_statements = []
        qa_section = []

        for segment in segments:
            if segment.get("segment_type") == "prepared_statement":
                prepared_statements.append(segment)
            else:
                qa_section.append(segment)

        return {
            "prepared_statements": prepared_statements,
            "qa_section": qa_section,
        }
