"""
Audio Feature Extraction Service - Extract paralinguistic features using librosa
"""
import librosa
import numpy as np
from pathlib import Path
from typing import Dict, List, Any
from ..core.config import settings


class AudioFeatureExtractor:
    """Extract vocal biomarkers and paralinguistic features from audio"""

    def __init__(self):
        self.sample_rate = settings.SAMPLE_RATE
        self.hop_length = settings.HOP_LENGTH
        self.n_mfcc = settings.N_MFCC

    def _ensure_json_serializable(self, obj):
        """
        Convert numpy types to JSON-serializable Python types

        Args:
            obj: Object to convert (can be dict, list, numpy type, or native type)

        Returns:
            JSON-serializable version of the object
        """
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, dict):
            return {k: self._ensure_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._ensure_json_serializable(item) for item in obj]
        return obj

    def extract_features(self, audio_path: str) -> Dict[str, Any]:
        """
        Extract comprehensive audio features

        Args:
            audio_path: Path to audio file

        Returns:
            Dictionary with all extracted features
        """
        try:
            print(f"🎵 Extracting audio features from: {Path(audio_path).name}")

            # Load audio
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            duration = librosa.get_duration(y=y, sr=sr)

            # Extract all features
            mfccs = self._extract_mfccs(y, sr)
            pitch_features = self._extract_pitch(y, sr)
            energy_features = self._extract_energy(y, sr)
            voice_quality = self._extract_voice_quality(y, sr)
            prosodic_features = self._extract_prosodic_features(y, sr)

            # Compute confidence timeline with time-windowed analysis
            confidence_timeline = self._compute_confidence_timeline_windowed(
                y, sr, duration
            )

            # Detect stress indicators
            stress_indicators = self._detect_stress_indicators(
                pitch_features, energy_features, voice_quality, duration
            )

            # Calculate overall confidence score using 6-factor model
            overall_confidence = self._calculate_overall_confidence_6factor(
                confidence_timeline, pitch_features, energy_features,
                voice_quality, prosodic_features, stress_indicators
            )

            result = {
                "mfccs": mfccs,
                "pitch": pitch_features,
                "energy": energy_features,
                "voice_quality": voice_quality,
                "prosodic": prosodic_features,
                "confidence_timeline": confidence_timeline,
                "stress_indicators": stress_indicators,
                "overall_confidence": overall_confidence,
                "duration": duration,
            }

            # Ensure all numpy types are converted to JSON-serializable Python types
            result = self._ensure_json_serializable(result)

            print(f"✅ Feature extraction complete. Confidence: {overall_confidence:.2f}")
            return result

        except Exception as e:
            print(f"❌ Feature extraction error: {e}")
            raise Exception(f"Failed to extract audio features: {str(e)}")

    def _extract_mfccs(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Extract Mel-frequency cepstral coefficients with deltas"""
        mfccs = librosa.feature.mfcc(
            y=y, sr=sr, n_mfcc=self.n_mfcc, hop_length=self.hop_length
        )

        # Compute delta (first derivative) and delta-delta (second derivative)
        mfcc_delta = librosa.feature.delta(mfccs)
        mfcc_delta2 = librosa.feature.delta(mfccs, order=2)

        return {
            "mean": mfccs.mean(axis=1).tolist(),
            "std": mfccs.std(axis=1).tolist(),
            "shape": list(mfccs.shape),
            "delta_mean": mfcc_delta.mean(axis=1).tolist(),
            "delta_std": mfcc_delta.std(axis=1).tolist(),
            "delta2_mean": mfcc_delta2.mean(axis=1).tolist(),
            "delta2_std": mfcc_delta2.std(axis=1).tolist(),
        }

    def _extract_pitch(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Extract pitch (F0) using pyin algorithm"""
        f0, voiced_flag, voiced_probs = librosa.pyin(
            y,
            fmin=librosa.note_to_hz('C2'),
            fmax=librosa.note_to_hz('C7'),
            sr=sr,
            hop_length=self.hop_length
        )

        # Remove NaN values
        f0_clean = f0[~np.isnan(f0)]

        if len(f0_clean) == 0:
            return {
                "mean": 0.0,
                "std": 0.0,
                "min": 0.0,
                "max": 0.0,
                "variation": 0.0,
                "voiced_percentage": 0.0,
            }

        return {
            "mean": float(np.mean(f0_clean)),
            "std": float(np.std(f0_clean)),
            "min": float(np.min(f0_clean)),
            "max": float(np.max(f0_clean)),
            "variation": float(np.std(f0_clean) / np.mean(f0_clean)) if np.mean(f0_clean) > 0 else 0.0,
            "voiced_percentage": float(np.sum(voiced_flag) / len(voiced_flag) * 100),
        }

    def _extract_energy(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Extract energy/intensity features"""
        # RMS energy
        rms = librosa.feature.rms(y=y, hop_length=self.hop_length)[0]

        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y, hop_length=self.hop_length)[0]

        return {
            "rms_mean": float(np.mean(rms)),
            "rms_std": float(np.std(rms)),
            "zcr_mean": float(np.mean(zcr)),
            "zcr_std": float(np.std(zcr)),
        }

    def _extract_voice_quality(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """
        Extract voice quality metrics (jitter, shimmer, HNR)
        """
        # Spectral features as proxies for voice quality
        spectral_centroid = librosa.feature.spectral_centroid(
            y=y, sr=sr, hop_length=self.hop_length
        )[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(
            y=y, sr=sr, hop_length=self.hop_length
        )[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(
            y=y, sr=sr, hop_length=self.hop_length
        )[0]

        # Spectral contrast across 6 frequency bands (from paper)
        spectral_contrast = librosa.feature.spectral_contrast(
            y=y, sr=sr, hop_length=self.hop_length, n_bands=6
        )

        # Jitter approximation (pitch variation)
        f0, _, _ = librosa.pyin(
            y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'),
            sr=sr, hop_length=self.hop_length
        )
        f0_clean = f0[~np.isnan(f0)]
        jitter = float(np.std(np.diff(f0_clean))) if len(f0_clean) > 1 else 0.0

        # Shimmer approximation (amplitude variation)
        rms = librosa.feature.rms(y=y, hop_length=self.hop_length)[0]
        shimmer = float(np.std(np.diff(rms))) if len(rms) > 1 else 0.0

        # HNR (Harmonics-to-Noise Ratio) using HPSS
        try:
            harmonic, percussive = librosa.effects.hpss(y)
            harmonic_energy = np.sum(harmonic**2)
            percussive_energy = np.sum(percussive**2)
            # Calculate HNR in dB
            if percussive_energy > 0:
                hnr = 10 * np.log10(harmonic_energy / percussive_energy)
            else:
                hnr = 40.0  # Very high HNR if no noise
        except:
            hnr = 20.0  # Default moderate HNR

        return {
            "jitter": jitter,
            "shimmer": shimmer,
            "hnr": float(hnr),
            "spectral_centroid_mean": float(np.mean(spectral_centroid)),
            "spectral_rolloff_mean": float(np.mean(spectral_rolloff)),
            "spectral_bandwidth_mean": float(np.mean(spectral_bandwidth)),
            "spectral_contrast_mean": spectral_contrast.mean(axis=1).tolist(),
            "spectral_contrast_std": spectral_contrast.std(axis=1).tolist(),
        }

    def _extract_prosodic_features(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Extract prosodic features (speech rate, pauses)"""
        # Detect speech/silence using energy threshold
        rms = librosa.feature.rms(y=y, hop_length=self.hop_length)[0]
        threshold = np.mean(rms) * 0.2

        # Count speech segments (rough speech rate)
        speech_frames = rms > threshold
        speech_segments = np.diff(speech_frames.astype(int))
        speech_onsets = np.sum(speech_segments == 1)

        # Calculate speech rate (segments per second)
        duration = librosa.get_duration(y=y, sr=sr)
        speech_rate = speech_onsets / duration if duration > 0 else 0.0

        # Pause detection
        silence_frames = np.sum(~speech_frames)
        pause_percentage = (silence_frames / len(speech_frames) * 100) if len(speech_frames) > 0 else 0.0

        return {
            "speech_rate": float(speech_rate),
            "pause_percentage": float(pause_percentage),
            "speech_segments": int(speech_onsets),
        }

    def _compute_confidence_timeline_windowed(
        self, y: np.ndarray, sr: int, duration: float
    ) -> List[Dict[str, Any]]:
        """
        Compute confidence score timeline with ACTUAL time-windowed analysis.
        Each 1-second window is analyzed independently.
        """
        window_size = 1.0  # 1 second windows
        num_intervals = max(int(duration), 1)
        timeline = []

        for i in range(num_intervals):
            # Extract audio segment for this 1-second window
            start_sample = int(i * window_size * sr)
            end_sample = int((i + 1) * window_size * sr)
            y_window = y[start_sample:end_sample]

            if len(y_window) < sr // 10:  # Skip if less than 0.1 seconds
                continue

            # Analyze THIS window
            try:
                # Pitch analysis for window
                f0, voiced_flag, _ = librosa.pyin(
                    y_window, fmin=65, fmax=400, sr=sr, hop_length=self.hop_length
                )
                f0_clean = f0[~np.isnan(f0)]

                if len(f0_clean) > 0:
                    pitch_mean = np.mean(f0_clean)
                    pitch_std = np.std(f0_clean)
                    pitch_variation = pitch_std / pitch_mean if pitch_mean > 0 else 0.5
                    pitch_stability = max(0, 1.0 - pitch_variation)
                else:
                    pitch_stability = 0.5

                # Energy for window
                rms = librosa.feature.rms(y=y_window, hop_length=self.hop_length)[0]
                energy_level = min(np.mean(rms) / 0.1, 1.0)

                # Voice quality for window
                try:
                    harmonic, percussive = librosa.effects.hpss(y_window)
                    h_energy = np.sum(harmonic**2)
                    p_energy = np.sum(percussive**2)
                    hnr = 10 * np.log10(h_energy / p_energy) if p_energy > 0 else 20
                    voice_stability = min(max(hnr / 40, 0), 1.0)  # Normalize HNR to 0-1
                except:
                    voice_stability = 0.5

                # Calculate window confidence
                confidence = (
                    pitch_stability * 0.4 +
                    energy_level * 0.3 +
                    voice_stability * 0.3
                )
                confidence = max(0.0, min(1.0, confidence))

                timeline.append({
                    "time": i + 0.5,  # Middle of interval
                    "confidence": round(confidence, 3),
                    "pitch_stability": round(pitch_stability, 3),
                    "energy_level": round(energy_level, 3),
                    "voice_quality": round(voice_stability, 3),
                })

            except Exception as e:
                # Fallback for problematic windows
                timeline.append({
                    "time": i + 0.5,
                    "confidence": 0.5,
                    "pitch_stability": 0.5,
                    "energy_level": 0.5,
                    "voice_quality": 0.5,
                })

        return timeline

    def _compute_confidence_timeline(
        self,
        pitch: Dict[str, Any],
        energy: Dict[str, Any],
        voice_quality: Dict[str, Any],
        duration: float
    ) -> List[Dict[str, Any]]:
        """
        OLD METHOD - kept for compatibility
        Compute confidence score timeline
        """
        # Create timeline with 1-second intervals
        num_intervals = max(int(duration), 1)
        timeline = []

        for i in range(num_intervals):
            time = i + 0.5  # Middle of interval

            # Simplified confidence calculation
            # High confidence: stable pitch, high energy, low jitter
            pitch_stability = 1.0 - min(pitch.get("variation", 0.5), 1.0)
            energy_level = min(energy.get("rms_mean", 0.01) / 0.1, 1.0)
            voice_stability = 1.0 - min(voice_quality.get("jitter", 10) / 20, 1.0)

            confidence = (pitch_stability * 0.4 + energy_level * 0.3 + voice_stability * 0.3)
            confidence = max(0.0, min(1.0, confidence))  # Clamp to [0, 1]

            timeline.append({
                "time": time,
                "confidence": round(confidence, 3),
                "pitch_stability": round(pitch_stability, 3),
                "energy_level": round(energy_level, 3),
            })

        return timeline

    def _detect_stress_indicators(
        self,
        pitch: Dict[str, Any],
        energy: Dict[str, Any],
        voice_quality: Dict[str, Any],
        duration: float
    ) -> List[Dict[str, Any]]:
        """
        Detect stress and hesitation indicators
        """
        indicators = []

        # High pitch variation -> stress
        if pitch.get("variation", 0) > 0.15:
            indicators.append({
                "type": "high_pitch_variation",
                "severity": "medium",
                "description": "Elevated pitch variation may indicate stress or uncertainty",
                "metric": pitch.get("variation", 0),
            })

        # High jitter -> vocal tension
        if voice_quality.get("jitter", 0) > 10:
            indicators.append({
                "type": "vocal_tension",
                "severity": "medium",
                "description": "High jitter suggests vocal tension or nervousness",
                "metric": voice_quality.get("jitter", 0),
            })

        # Low energy -> lack of confidence
        if energy.get("rms_mean", 0) < 0.02:
            indicators.append({
                "type": "low_energy",
                "severity": "low",
                "description": "Low vocal energy may indicate hesitation",
                "metric": energy.get("rms_mean", 0),
            })

        return indicators

    def _calculate_overall_confidence_6factor(
        self,
        timeline: List[Dict[str, Any]],
        pitch: Dict[str, Any],
        energy: Dict[str, Any],
        voice_quality: Dict[str, Any],
        prosodic: Dict[str, Any],
        stress_indicators: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate overall confidence using 6-factor model from paper:
        - F0 stability (25% weight) - lower variation = higher confidence
        - Energy consistency (20% weight)
        - Speech rate (15% weight) - optimal around 155 WPM (2.6 segments/sec)
        - Hesitation rate (20% weight) - low pause % = higher confidence
        - Pitch range (10% weight) - optimal 100-150 Hz
        - Voice quality HNR (10% weight)
        """

        # Factor 1: F0 Stability (25% weight)
        # Lower coefficient of variation indicates higher confidence
        pitch_variation = pitch.get("variation", 0.5)
        f0_stability = max(0, 1.0 - pitch_variation)

        # Factor 2: Energy Consistency (20% weight)
        # Lower standard deviation relative to mean = more consistent
        rms_mean = energy.get("rms_mean", 0.05)
        rms_std = energy.get("rms_std", 0.02)
        energy_consistency = max(0, 1.0 - (rms_std / rms_mean if rms_mean > 0 else 0.5))

        # Factor 3: Speech Rate (15% weight)
        # Optimal around 155 WPM ~= 2.6 segments/second
        speech_rate = prosodic.get("speech_rate", 2.0)
        # Gaussian-like scoring: peak at 2.6, falls off on either side
        optimal_rate = 2.6
        rate_deviation = abs(speech_rate - optimal_rate) / optimal_rate
        speech_rate_score = max(0, 1.0 - rate_deviation)

        # Factor 4: Hesitation Rate (20% weight)
        # Lower pause percentage = higher confidence
        pause_pct = prosodic.get("pause_percentage", 20)
        hesitation_score = max(0, 1.0 - (pause_pct / 50))  # Normalize to 0-1

        # Factor 5: Pitch Range (10% weight)
        # Optimal range 100-150 Hz
        pitch_mean = pitch.get("mean", 125)
        if 100 <= pitch_mean <= 150:
            pitch_range_score = 1.0
        elif pitch_mean < 100:
            pitch_range_score = max(0, pitch_mean / 100)
        else:  # > 150
            pitch_range_score = max(0, 1.0 - (pitch_mean - 150) / 150)

        # Factor 6: Voice Quality HNR (10% weight)
        # Higher HNR = better voice quality
        hnr = voice_quality.get("hnr", 20)
        # Normalize HNR (typical range 10-40 dB)
        hnr_score = min(max((hnr - 10) / 30, 0), 1.0)

        # Weighted combination according to paper
        overall_confidence = (
            f0_stability * 0.25 +
            energy_consistency * 0.20 +
            speech_rate_score * 0.15 +
            hesitation_score * 0.20 +
            pitch_range_score * 0.10 +
            hnr_score * 0.10
        )

        # Penalty for stress indicators
        penalty = len(stress_indicators) * 0.03
        overall_confidence = max(0.0, min(1.0, overall_confidence - penalty))

        return round(overall_confidence, 3)

    def _calculate_overall_confidence(
        self,
        timeline: List[Dict[str, Any]],
        stress_indicators: List[Dict[str, Any]]
    ) -> float:
        """
        OLD METHOD - Calculate overall confidence score
        """
        if not timeline:
            return 0.5

        # Average confidence from timeline
        avg_confidence = np.mean([t["confidence"] for t in timeline])

        # Penalize for stress indicators
        penalty = len(stress_indicators) * 0.05

        overall = max(0.0, min(1.0, avg_confidence - penalty))
        return round(overall, 3)
