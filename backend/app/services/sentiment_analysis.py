"""
Financial Sentiment Analysis Service using FinBERT
"""
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import re
from typing import List, Dict, Any
from ..core.config import settings


class SentimentAnalysisService:
    """Service for financial sentiment analysis using FinBERT"""

    def __init__(self):
        print("📊 Loading FinBERT model...")
        self.tokenizer = AutoTokenizer.from_pretrained(settings.FINBERT_MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(settings.FINBERT_MODEL)

        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if torch.cuda.is_available() else -1
        )

        self.label_map = {
            "positive": "positive",
            "negative": "negative",
            "neutral": "neutral",
        }

        print("✅ FinBERT model loaded successfully")

    def analyze_transcript(self, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze sentiment of transcript segments

        Args:
            segments: List of transcript segments with text and timing

        Returns:
            Dictionary with sentiment analysis results
        """
        try:
            print(f"🔍 Analyzing sentiment for {len(segments)} segments...")

            analyzed_segments = []
            sentiment_scores = {"positive": 0, "negative": 0, "neutral": 0}

            for segment in segments:
                text = segment.get("text", "").strip()
                if not text:
                    continue

                # Analyze sentiment
                sentiment_result = self._analyze_text(text)

                # Add sentiment to segment
                segment_with_sentiment = {
                    **segment,
                    "sentiment": sentiment_result["label"],
                    "sentiment_score": sentiment_result["score"],
                }
                analyzed_segments.append(segment_with_sentiment)

                # Update distribution
                sentiment_scores[sentiment_result["label"]] += 1

            # Calculate distribution
            total = len(analyzed_segments) if analyzed_segments else 1
            sentiment_distribution = {
                label: count / total
                for label, count in sentiment_scores.items()
            }

            # Determine overall sentiment
            overall_sentiment = max(sentiment_scores, key=sentiment_scores.get)

            # Extract key topics and financial metrics
            full_text = " ".join([s.get("text", "") for s in segments])
            key_topics = self._extract_key_topics(full_text)
            financial_metrics = self._extract_financial_metrics(full_text)

            result = {
                "segments": analyzed_segments,
                "overall_sentiment": overall_sentiment,
                "sentiment_distribution": sentiment_distribution,
                "key_topics": key_topics,
                "financial_metrics": financial_metrics,
            }

            print(f"✅ Sentiment analysis complete. Overall: {overall_sentiment}")
            return result

        except Exception as e:
            print(f"❌ Sentiment analysis error: {e}")
            raise Exception(f"Failed to analyze sentiment: {str(e)}")

    def _analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of a single text segment

        Args:
            text: Text to analyze

        Returns:
            Dictionary with label and score
        """
        # Truncate if too long
        max_length = 512
        if len(text.split()) > max_length:
            text = " ".join(text.split()[:max_length])

        try:
            result = self.sentiment_pipeline(text)[0]
            label = result["label"].lower()
            score = result["score"]

            return {
                "label": self.label_map.get(label, "neutral"),
                "score": round(score, 3),
            }
        except Exception as e:
            print(f"Warning: Failed to analyze text segment: {e}")
            return {"label": "neutral", "score": 0.5}

    def _extract_key_topics(self, text: str) -> List[str]:
        """
        Extract key financial topics from text
        Simple keyword-based extraction
        """
        topics = []

        # Common financial topics
        topic_keywords = {
            "Revenue Growth": ["revenue", "sales", "top line", "growth"],
            "Profitability": ["profit", "margin", "earnings", "ebitda", "bottom line"],
            "Guidance": ["guidance", "outlook", "forecast", "expect", "project"],
            "Market Share": ["market share", "competition", "competitive"],
            "Innovation": ["innovation", "new product", "r&d", "development"],
            "Cost Management": ["cost", "expense", "efficiency", "savings"],
            "Customer Acquisition": ["customer", "client", "acquisition", "retention"],
            "Debt & Financing": ["debt", "leverage", "financing", "capital"],
        }

        text_lower = text.lower()

        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)

        return topics[:5]  # Return top 5

    def _extract_financial_metrics(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract financial metrics mentioned in text
        """
        metrics = []

        # Patterns for common metrics
        patterns = {
            "revenue": r"revenue\s+(?:of\s+)?\$?([\d.]+)\s*(billion|million|thousand)?",
            "eps": r"(?:eps|earnings per share)\s+(?:of\s+)?\$?([\d.]+)",
            "growth": r"([\d.]+)%?\s+growth",
            "margin": r"([\d.]+)%?\s+margin",
        }

        for metric_name, pattern in patterns.items():
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                value = match.group(1)
                unit = match.group(2) if len(match.groups()) > 1 else ""

                metrics.append({
                    "metric": metric_name,
                    "value": value,
                    "unit": unit,
                    "context": match.group(0),
                })

        return metrics[:10]  # Return top 10

    def separate_prepared_vs_qa(self, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze sentiment differences between prepared statements and Q&A
        """
        prepared = [s for s in segments if s.get("segment_type") == "prepared_statement"]
        qa = [s for s in segments if s.get("segment_type") == "qa"]

        def calculate_sentiment_stats(segs):
            if not segs:
                return {"positive": 0, "negative": 0, "neutral": 0}

            sentiments = [s.get("sentiment", "neutral") for s in segs]
            total = len(sentiments)
            return {
                "positive": sentiments.count("positive") / total,
                "negative": sentiments.count("negative") / total,
                "neutral": sentiments.count("neutral") / total,
            }

        return {
            "prepared_sentiment": calculate_sentiment_stats(prepared),
            "qa_sentiment": calculate_sentiment_stats(qa),
            "sentiment_shift": self._calculate_sentiment_shift(
                calculate_sentiment_stats(prepared),
                calculate_sentiment_stats(qa)
            ),
        }

    def _calculate_sentiment_shift(self, prepared: Dict, qa: Dict) -> str:
        """
        Calculate shift in sentiment from prepared to Q&A
        """
        prepared_score = prepared.get("positive", 0) - prepared.get("negative", 0)
        qa_score = qa.get("positive", 0) - qa.get("negative", 0)

        diff = qa_score - prepared_score

        if diff < -0.1:
            return "more_negative"
        elif diff > 0.1:
            return "more_positive"
        else:
            return "stable"
