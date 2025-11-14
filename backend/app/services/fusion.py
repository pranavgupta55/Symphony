"""
Multi-Modal Fusion Service
Combines audio, text, and chart analysis for unified insights
"""
import numpy as np
from typing import Dict, Any, List


class MultiModalFusionService:
    """Service for fusing multiple analysis modalities"""

    def __init__(self):
        # Weights for different modalities
        self.weights = {
            "audio": 0.35,
            "text": 0.40,
            "chart": 0.25,
        }

    def fuse_modalities(
        self,
        audio_features: Dict[str, Any],
        sentiment_analysis: Dict[str, Any],
        chart_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Fuse multiple modalities into unified analysis

        Args:
            audio_features: Audio feature extraction results
            sentiment_analysis: Sentiment analysis results
            chart_analysis: Chart analysis results

        Returns:
            Dictionary with fusion results
        """
        try:
            print("🔗 Fusing multi-modal data...")

            # Calculate credibility score
            credibility_score = self._calculate_credibility_score(
                audio_features, sentiment_analysis, chart_analysis
            )

            # Detect cross-modal discrepancies
            discrepancies = self._detect_discrepancies(
                audio_features, sentiment_analysis, chart_analysis
            )

            # Calculate risk level
            risk_level = self._calculate_risk_level(
                credibility_score, discrepancies, audio_features, sentiment_analysis
            )

            # Generate fusion insights
            fusion_insights = self._generate_fusion_insights(
                audio_features, sentiment_analysis, chart_analysis, discrepancies
            )

            # Create attention weights showing which modalities were most important
            attention_weights = self._calculate_attention_weights(
                audio_features, sentiment_analysis, chart_analysis
            )

            result = {
                "credibility_score": credibility_score,
                "risk_level": risk_level,
                "discrepancies": discrepancies,
                "fusion_insights": fusion_insights,
                "attention_weights": attention_weights,
            }

            print(f"✅ Fusion complete. Credibility: {credibility_score:.2f}, Risk: {risk_level}")
            return result

        except Exception as e:
            print(f"❌ Fusion error: {e}")
            raise Exception(f"Failed to fuse modalities: {str(e)}")

    def _calculate_credibility_score(
        self,
        audio_features: Dict[str, Any],
        sentiment_analysis: Dict[str, Any],
        chart_analysis: Dict[str, Any],
    ) -> float:
        """
        Calculate unified credibility score using attention-based fusion

        Args:
            audio_features: Audio analysis
            sentiment_analysis: Text analysis
            chart_analysis: Chart analysis

        Returns:
            Credibility score (0-1)
        """
        # Audio credibility (from confidence score)
        audio_conf = audio_features.get("overall_confidence", 0.5)

        # Text credibility (from sentiment)
        sentiment_dist = sentiment_analysis.get("sentiment_distribution", {})
        text_conf = sentiment_dist.get("positive", 0.33) - sentiment_dist.get("negative", 0.33) + 0.5
        text_conf = max(0.0, min(1.0, text_conf))

        # Chart credibility (inverse of inconsistencies)
        num_inconsistencies = len(chart_analysis.get("inconsistencies", []))
        chart_conf = max(0.0, 1.0 - (num_inconsistencies * 0.15))

        # Weighted fusion
        credibility = (
            audio_conf * self.weights["audio"] +
            text_conf * self.weights["text"] +
            chart_conf * self.weights["chart"]
        )

        return round(credibility, 3)

    def _detect_discrepancies(
        self,
        audio_features: Dict[str, Any],
        sentiment_analysis: Dict[str, Any],
        chart_analysis: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Detect discrepancies across modalities

        Args:
            audio_features: Audio analysis
            sentiment_analysis: Text analysis
            chart_analysis: Chart analysis

        Returns:
            List of detected discrepancies
        """
        discrepancies = []

        # Audio-Text discrepancy: Low confidence but positive sentiment
        audio_conf = audio_features.get("overall_confidence", 0.5)
        overall_sentiment = sentiment_analysis.get("overall_sentiment", "neutral")

        if audio_conf < 0.5 and overall_sentiment == "positive":
            discrepancies.append({
                "type": "audio_text_mismatch",
                "severity": "high",
                "description": "Positive verbal statements but low vocal confidence detected",
                "modalities": ["audio", "text"],
                "audio_confidence": audio_conf,
                "text_sentiment": overall_sentiment,
            })

        # Audio-Text discrepancy: High confidence but negative sentiment
        if audio_conf > 0.7 and overall_sentiment == "negative":
            discrepancies.append({
                "type": "audio_text_mismatch",
                "severity": "medium",
                "description": "Negative statements delivered with high confidence - potentially planned bad news",
                "modalities": ["audio", "text"],
                "audio_confidence": audio_conf,
                "text_sentiment": overall_sentiment,
            })

        # Chart inconsistencies
        chart_inconsistencies = chart_analysis.get("inconsistencies", [])
        for incon in chart_inconsistencies:
            discrepancies.append({
                "type": "chart_verbal_mismatch",
                "severity": incon.get("severity", "medium"),
                "description": incon.get("description", "Chart data doesn't match verbal statements"),
                "modalities": ["chart", "text"],
            })

        # Stress indicators with positive sentiment
        stress_indicators = audio_features.get("stress_indicators", [])
        if len(stress_indicators) > 2 and overall_sentiment == "positive":
            discrepancies.append({
                "type": "stress_sentiment_mismatch",
                "severity": "medium",
                "description": f"Detected {len(stress_indicators)} vocal stress indicators despite positive language",
                "modalities": ["audio", "text"],
                "stress_count": len(stress_indicators),
            })

        return discrepancies

    def _calculate_risk_level(
        self,
        credibility_score: float,
        discrepancies: List[Dict[str, Any]],
        audio_features: Dict[str, Any],
        sentiment_analysis: Dict[str, Any],
    ) -> str:
        """
        Calculate overall risk level

        Args:
            credibility_score: Unified credibility score
            discrepancies: Detected discrepancies
            audio_features: Audio analysis
            sentiment_analysis: Text analysis

        Returns:
            Risk level: "low", "medium", or "high"
        """
        risk_score = 0

        # Low credibility increases risk
        if credibility_score < 0.4:
            risk_score += 3
        elif credibility_score < 0.6:
            risk_score += 1

        # Discrepancies increase risk
        high_severity_discrepancies = [d for d in discrepancies if d.get("severity") == "high"]
        risk_score += len(high_severity_discrepancies) * 2
        risk_score += len(discrepancies)

        # Negative sentiment increases risk
        if sentiment_analysis.get("overall_sentiment") == "negative":
            risk_score += 2

        # Many stress indicators increase risk
        stress_count = len(audio_features.get("stress_indicators", []))
        if stress_count > 3:
            risk_score += 2
        elif stress_count > 1:
            risk_score += 1

        # Classify risk
        if risk_score >= 6:
            return "high"
        elif risk_score >= 3:
            return "medium"
        else:
            return "low"

    def _generate_fusion_insights(
        self,
        audio_features: Dict[str, Any],
        sentiment_analysis: Dict[str, Any],
        chart_analysis: Dict[str, Any],
        discrepancies: List[Dict[str, Any]],
    ) -> List[str]:
        """
        Generate human-readable fusion insights

        Args:
            audio_features: Audio analysis
            sentiment_analysis: Text analysis
            chart_analysis: Chart analysis
            discrepancies: Detected discrepancies

        Returns:
            List of insight strings
        """
        insights = []

        # Vocal confidence insights
        audio_conf = audio_features.get("overall_confidence", 0.5)
        if audio_conf > 0.7:
            insights.append("Executive team demonstrated high vocal confidence throughout the call")
        elif audio_conf < 0.4:
            insights.append("Vocal analysis reveals hesitation and uncertainty in delivery")

        # Sentiment insights
        sentiment = sentiment_analysis.get("overall_sentiment", "neutral")
        sentiment_dist = sentiment_analysis.get("sentiment_distribution", {})

        if sentiment == "positive" and sentiment_dist.get("positive", 0) > 0.6:
            insights.append("Overwhelmingly positive language used throughout the call")
        elif sentiment == "negative":
            insights.append("Negative sentiment detected - management acknowledging challenges")

        # Discrepancy insights
        if len(discrepancies) > 0:
            insights.append(f"Found {len(discrepancies)} cross-modal inconsistencies requiring attention")

        # Chart insights
        if chart_analysis.get("chart_descriptions"):
            insights.append(f"Visual data analysis of {len(chart_analysis['chart_descriptions'])} charts completed")

        # Stress insights
        stress_indicators = audio_features.get("stress_indicators", [])
        if len(stress_indicators) > 2:
            insights.append(f"Multiple vocal stress indicators detected: {', '.join([s['type'] for s in stress_indicators[:3]])}")

        return insights

    def _calculate_attention_weights(
        self,
        audio_features: Dict[str, Any],
        sentiment_analysis: Dict[str, Any],
        chart_analysis: Dict[str, Any],
    ) -> Dict[str, float]:
        """
        Calculate attention weights showing modality importance

        Args:
            audio_features: Audio analysis
            sentiment_analysis: Text analysis
            chart_analysis: Chart analysis

        Returns:
            Dictionary of attention weights
        """
        # Simple attention mechanism based on information richness

        weights = {
            "audio": 0.33,
            "text": 0.33,
            "chart": 0.33,
        }

        # Increase weight if modality has rich information
        if len(audio_features.get("stress_indicators", [])) > 2:
            weights["audio"] += 0.1

        if len(sentiment_analysis.get("key_topics", [])) > 3:
            weights["text"] += 0.1

        if len(chart_analysis.get("inconsistencies", [])) > 0:
            weights["chart"] += 0.15

        # Normalize
        total = sum(weights.values())
        weights = {k: round(v / total, 3) for k, v in weights.items()}

        return weights
