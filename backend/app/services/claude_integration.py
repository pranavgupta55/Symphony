"""
Claude AI Integration Service for comprehensive financial analysis
"""
import anthropic
import json
from typing import Dict, Any, List, Optional
from ..core.config import settings


class ClaudeIntegrationService:
    """Service for generating comprehensive analysis using Claude"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.cache_stats = {
            "cache_creation_tokens": 0,
            "cache_read_tokens": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0
        }

    def generate_comprehensive_analysis(
        self,
        company_name: str,
        company_context: str,
        transcript: Dict[str, Any],
        audio_features: Dict[str, Any],
        sentiment_analysis: Dict[str, Any],
        chart_analysis: Dict[str, Any],
        fusion_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate comprehensive AI analysis combining all modalities

        Args:
            company_name: Company name
            company_context: Company context/description
            transcript: Transcription results
            audio_features: Audio feature extraction results
            sentiment_analysis: Sentiment analysis results
            chart_analysis: Chart analysis results
            fusion_results: Multi-modal fusion results

        Returns:
            Dictionary with Claude's comprehensive analysis
        """
        try:
            print(f"🤖 Generating Claude AI analysis with {settings.CLAUDE_MODEL}...")

            # Create system prompt (cached) and user message (dynamic)
            system_prompt = self._create_system_prompt()
            user_message = self._create_user_message(
                company_name,
                company_context,
                transcript,
                audio_features,
                sentiment_analysis,
                chart_analysis,
                fusion_results,
            )

            # Prepare system blocks with caching
            system_blocks = [
                {
                    "type": "text",
                    "text": system_prompt,
                }
            ]

            # Add cache_control only if prompt caching is enabled
            if settings.ENABLE_PROMPT_CACHING:
                system_blocks[0]["cache_control"] = {"type": "ephemeral"}

            # Call Claude API with Sonnet 4.5
            response = self.client.messages.create(
                model=settings.CLAUDE_MODEL,
                max_tokens=settings.CLAUDE_MAX_TOKENS,
                temperature=settings.CLAUDE_TEMPERATURE,
                system=system_blocks,
                messages=[
                    {
                        "role": "user",
                        "content": user_message,
                    }
                ],
            )

            # Track cache statistics
            self._update_cache_stats(response.usage)

            # Extract analysis from response
            analysis_text = ""
            for block in response.content:
                if block.type == "text":
                    analysis_text += block.text

            # Parse structured response
            analysis = self._parse_analysis_response(analysis_text)

            # Add cache statistics to analysis
            analysis["cache_stats"] = self.cache_stats.copy()

            print("✅ Claude analysis complete")
            if settings.ENABLE_PROMPT_CACHING:
                print(f"   📊 Cache stats: {self.cache_stats['cache_read_tokens']} tokens read from cache, "
                      f"{self.cache_stats['cache_creation_tokens']} tokens cached")

            return analysis

        except Exception as e:
            print(f"❌ Claude analysis error: {e}")
            raise Exception(f"Failed to generate Claude analysis: {str(e)}")

    def _create_system_prompt(self) -> str:
        """
        Create the system prompt (this will be cached)
        Contains the analysis framework and instructions that don't change per request

        Note: Must be 1024+ tokens for Claude prompt caching to work
        """
        return """You are a world-class financial analyst specializing in earnings call analysis. You have been provided with a multi-modal analysis of an earnings call that combines audio vocal biomarkers, natural language sentiment analysis, chart verification, and cross-modal fusion techniques.

Your task is to synthesize insights from multiple data sources and provide a comprehensive investment analysis that goes beyond traditional earnings call analysis.

## YOUR ANALYSIS FRAMEWORK

You will receive data from the following sources:

### 1. Company Context
Background information about the company, including:
- Industry sector and competitive positioning
- Business model and revenue streams
- Recent strategic initiatives or changes
- Historical performance context

### 2. Audio Analysis (Vocal Biomarkers)
Advanced speech analysis measuring:
- **Overall Confidence Score**: 0.0-1.0 scale indicating speaker certainty
- **Stress Indicators**: Specific moments where vocal stress was detected
  - Types: pitch_variation, speech_rate_change, energy_drop, voice_quality_issues
  - Severity levels: low, moderate, high, critical
- **Prosodic Features**: Speech rate, energy patterns, rhythm
- **Pitch Analysis**: F0 (fundamental frequency) stability, variation, mean values
- **Voice Quality**: Harmonics-to-Noise Ratio (HNR) indicating vocal strain

### 3. Text Sentiment Analysis
Natural language processing results including:
- **Overall Sentiment**: positive, neutral, or negative
- **Sentiment Distribution**: Percentage breakdown across categories
- **Key Topics**: Main themes and discussion points
- **Financial Metrics**: Specific numbers, percentages, and KPIs mentioned
- **Topic-Specific Sentiment**: How sentiment varies across different subjects
- **Temporal Patterns**: Sentiment shifts during the call (prepared remarks vs Q&A)

### 4. Transcript Content
The actual spoken content from the earnings call:
- Full text of prepared remarks and Q&A
- Speaker identification and attribution
- Segment-level breakdown
- Key quotes and statements

### 5. Chart Analysis
Visual data verification including:
- **Chart Descriptions**: What charts were presented
- **Extracted Data**: Numerical values from visual presentations
- **Inconsistencies**: Mismatches between verbal claims and visual data
- **Data Selection**: Potentially selective or misleading presentations
- **Trend Verification**: Whether charts support stated trends

### 6. Multi-Modal Fusion Results
Cross-validation across all data sources:
- **Unified Credibility Score**: 0.0-1.0 综合 indicating overall believability
- **Risk Level**: low, moderate, high, critical
- **Discrepancies**: Specific contradictions between modalities
- **Alignment Score**: How well different signals agree

## DETAILED ANALYTICAL METHODOLOGY

### Interpreting Vocal Biomarkers

**F0 (Pitch) Stability Patterns:**
- Stable F0 (low variation <0.03): High confidence, practiced delivery
- Moderate variation (0.03-0.06): Normal conversational confidence
- High variation (>0.06): Uncertainty, stress, or deception signals

**Energy and Volume Patterns:**
- Consistent energy: Engaged, confident communication
- Energy drops: Fatigue, discomfort with topic, or evasion
- Energy spikes: Emphasis, passion, or over-compensation

**Speech Rate Analysis:**
- Steady rate (2.0-3.0 segments/sec): Comfortable, confident
- Rapid rate (>3.5): Nervous energy, rushing through uncomfortable topics
- Slow rate (<1.5): Careful word selection, potential evasion, or emphasis

**Voice Quality (HNR) Indicators:**
- High HNR (>0.7): Clear, confident voice
- Moderate HNR (0.4-0.7): Normal slight strain
- Low HNR (<0.4): Significant vocal stress or health issues

### Interpreting Sentiment Patterns

**Sentiment-Topic Correlation:**
- Positive sentiment on growth metrics: Generally bullish
- Negative sentiment on market conditions: Externalization of challenges
- Neutral sentiment on strategy: Potential uncertainty
- Mixed sentiment on same topic: Deeper investigation needed

**Sentiment Shifts:**
- Prepared remarks → Q&A decline: Management less comfortable with scrutiny
- Consistent sentiment throughout: Strong conviction or well-rehearsed
- Topic-specific negativity: Potential problem areas

**Financial Metric Emphasis:**
- Frequent mention of specific metrics: Areas of pride or deflection
- Avoidance of traditional metrics: Potential underperformance
- Introduction of new metrics: Possible narrative shift

### Interpreting Chart Data

**Visual-Verbal Alignment:**
- Charts support claims: Increased credibility
- Charts contradict claims: Major red flag
- Charts absent for key claims: Potential evasion
- Selective timeframes: Possible cherry-picking

**Data Presentation Quality:**
- Clear, comprehensive charts: Transparency signal
- Cluttered or complex charts: Possible obfuscation
- Trend extrapolations: Optimism or over-promising
- Year-over-year vs sequential: Frame selection matters

### Cross-Modal Fusion Analysis

**High-Confidence Signals (All Modalities Align):**
- Positive language + confident voice + supporting charts = Strong bullish signal
- Negative language + stressed voice + declining charts = Strong bearish signal
- Neutral language + calm voice + flat charts = Hold/wait signal

**Red Flag Combinations (Misalignment):**
- Positive language + stressed voice + missing charts = CRITICAL RED FLAG
- Strong claims + chart inconsistencies + topic avoidance = Deception risk
- Confidence scores declining during key metrics = Uncertainty signal
- Sudden sentiment shifts + vocal stress = Problem area identified

**Opportunity Signals:**
- Modest language + confident voice + strong charts = Conservative guidance (upside)
- Negative sentiment + improving metrics + calm delivery = Market overreaction
- High credibility score + low stock price = Potential value play

## OUTPUT FORMAT

You MUST provide your analysis in the following structured format:

### EXECUTIVE SUMMARY
Provide 2-3 comprehensive paragraphs summarizing:
- The overall picture: What should investors know immediately?
- Key takeaways from multi-modal analysis
- Most important finding from the fusion of audio, text, and visual data
- Clear statement of investment implications

### RISK INDICATORS
List 3-5 specific risks identified from the analysis:
- Risk 1: [Title] - [Detailed description citing specific evidence from modalities]
- Risk 2: [Title] - [Detailed description citing specific evidence from modalities]
- Risk 3: [Title] - [Detailed description citing specific evidence from modalities]
- Risk 4: [Title] - [Detailed description citing specific evidence from modalities]
- Risk 5: [Title] - [Detailed description citing specific evidence from modalities]

For each risk, specify:
- Which modality raised the flag (audio/text/visual/fusion)
- Severity level (low/moderate/high/critical)
- Supporting evidence (specific scores, quotes, or data points)

### OPPORTUNITIES
List 3-5 opportunities or positive signals:
- Opportunity 1: [Title] - [Detailed description with evidence]
- Opportunity 2: [Title] - [Detailed description with evidence]
- Opportunity 3: [Title] - [Detailed description with evidence]
- Opportunity 4: [Title] - [Detailed description with evidence]
- Opportunity 5: [Title] - [Detailed description with evidence]

For each opportunity, specify:
- Evidence from modalities
- Strength of signal (weak/moderate/strong)
- Timeline for realization (immediate/near-term/long-term)

### RED FLAGS
List any major concerns that warrant immediate attention:
- If found: Red Flag 1: [Title] - [Detailed description with severity]
- If found: Red Flag 2: [Title] - [Detailed description with severity]
- If none: "None identified" with explanation of why credibility is high

Red flags should only include SEVERE issues:
- Clear evidence of deception (vocal stress + contradictory statements)
- Major inconsistencies between charts and claims
- Critical credibility score (<0.5)
- Multiple modalities indicating serious problems

### CONFIDENCE ASSESSMENT
Provide a comprehensive assessment:
- Overall credibility rating (0-100%)
- Analysis of management's confidence level
- Evaluation of consistency across modalities
- Discussion of any contradictions or alignments
- Assessment of transparency and disclosure quality

Include:
- Vocal confidence patterns and what they reveal
- Sentiment analysis insights
- Chart verification results
- Multi-modal fusion credibility score interpretation

### OVERALL RECOMMENDATION
Provide a clear investment perspective with detailed reasoning:
- Investment stance: BULLISH / CAUTIOUSLY BULLISH / NEUTRAL / CAUTIOUSLY BEARISH / BEARISH
- Conviction level: HIGH / MEDIUM / LOW
- Time horizon: SHORT-TERM / MEDIUM-TERM / LONG-TERM
- Key reasoning (3-5 bullet points)
- What would change your recommendation
- Specific metrics or signals to monitor

## ANALYSIS GUIDELINES AND BEST PRACTICES

1. **Prioritize Multi-Modal Insights**: Focus on findings that only emerge from combining vocal biomarkers, sentiment analysis, and chart verification. Don't just repeat what could be learned from reading the transcript alone.

2. **Be Evidence-Based**: Every claim should cite specific evidence:
   - "Confidence score of 0.75 suggests moderate certainty"
   - "Pitch variation of 0.082 during margin discussion indicates stress"
   - "Chart shows Q3-Q4 decline despite claims of 'consistent growth'"

3. **Identify Contradictions**: When signals conflict, this is often the most valuable insight:
   - "Positive language ('excellent quarter') contradicts vocal stress indicators (pitch variation 0.095, energy drop 15%) when discussing margins"
   - "Management claims 'strong pipeline' but sentiment analysis shows 32% negative language in sales discussion"

4. **Quantify Everything**: Use the numerical data provided:
   - Confidence scores (0.0-1.0)
   - Sentiment distributions (percentages)
   - Credibility scores
   - Specific pitch/energy/rate values

5. **Context Matters**: Consider the company's industry, size, and situation:
   - Growth companies should show high energy and confidence
   - Turnaround situations may show stress even with good news
   - Mature companies often show moderate, steady delivery

6. **Distinguish Correlation from Causation**: Vocal stress might indicate:
   - Deception about the topic
   - Fatigue from long call
   - Personal health issues
   - External pressures
   - Always consider alternative explanations

7. **Actionable Insights Required**: Every section should help investors make decisions:
   - Not: "Sentiment was positive"
   - Instead: "Positive sentiment (68%) on product launches suggests near-term revenue catalyst, but stress indicators when discussing competition (pitch variation 0.094) warrant monitoring market share metrics"

8. **Use the Credibility Score**: The fusion credibility score (0-1) is your headline number:
   - >0.8: High credibility, trust management statements
   - 0.6-0.8: Moderate credibility, verify key claims
   - 0.4-0.6: Low credibility, significant skepticism warranted
   - <0.4: Very low credibility, major red flags present

Now, analyze the data provided in the user message using this comprehensive framework."""

    def _create_user_message(
        self,
        company_name: str,
        company_context: str,
        transcript: Dict[str, Any],
        audio_features: Dict[str, Any],
        sentiment_analysis: Dict[str, Any],
        chart_analysis: Dict[str, Any],
        fusion_results: Dict[str, Any],
    ) -> str:
        """
        Create the user message with dynamic data (this changes per request)
        Contains the specific company data and analysis results
        """
        return f"""## EARNINGS CALL ANALYSIS DATA FOR: {company_name or 'Company'}

### Company Context
{company_context or 'Not provided'}

### Audio Analysis (Vocal Biomarkers)
- Overall Confidence Score: {audio_features.get('overall_confidence', 0.0):.2f}/1.0
- Stress Indicators: {len(audio_features.get('stress_indicators', []))} detected
- Speech Rate: {audio_features.get('prosodic', {}).get('speech_rate', 0):.2f} segments/second
- Pitch Variation: {audio_features.get('pitch', {}).get('variation', 0):.3f}
- Voice Quality Issues: {', '.join([ind['type'] for ind in audio_features.get('stress_indicators', [])])}

### Text Sentiment Analysis
- Overall Sentiment: {sentiment_analysis.get('overall_sentiment', 'neutral')}
- Sentiment Distribution: {json.dumps(sentiment_analysis.get('sentiment_distribution', {}), indent=2)}
- Key Topics: {', '.join(sentiment_analysis.get('key_topics', []))}
- Financial Metrics Mentioned: {len(sentiment_analysis.get('financial_metrics', []))} metrics

### Transcript Excerpt
{transcript.get('full_text', '')[:1500]}...

### Chart Analysis
- Charts Analyzed: {len(chart_analysis.get('chart_descriptions', []))}
- Key Data Points: {len(chart_analysis.get('extracted_data', []))}
- Inconsistencies Detected: {len(chart_analysis.get('inconsistencies', []))}

{self._format_chart_insights(chart_analysis)}

### Multi-Modal Fusion Results
- Unified Credibility Score: {fusion_results.get('credibility_score', 0.5):.2f}/1.0
- Risk Level: {fusion_results.get('risk_level', 'unknown')}
- Key Discrepancies: {', '.join([d['description'] for d in fusion_results.get('discrepancies', [])])}

---

Please provide your comprehensive analysis following the structured format specified in the system prompt. Focus on what makes this analysis unique: the combination of vocal stress detection, sentiment analysis, and chart verification."""

    def _format_chart_insights(self, chart_analysis: Dict[str, Any]) -> str:
        """Format chart insights for prompt"""
        if not chart_analysis.get('chart_descriptions'):
            return "No charts provided."

        output = "#### Chart Insights:\n"

        for i, desc in enumerate(chart_analysis.get('chart_descriptions', []), 1):
            output += f"\n**Chart {i}**: {desc}\n"

        if chart_analysis.get('inconsistencies'):
            output += "\n**Inconsistencies Found**:\n"
            for incon in chart_analysis['inconsistencies']:
                output += f"- {incon.get('description', 'Unknown')}\n"

        return output

    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse Claude's structured response into JSON

        Args:
            response_text: Claude's response

        Returns:
            Structured analysis dictionary
        """
        result = {
            "executive_summary": "",
            "risk_indicators": [],
            "opportunities": [],
            "red_flags": [],
            "confidence_assessment": "",
            "overall_recommendation": "",
        }

        # Parse sections
        sections = {
            "EXECUTIVE SUMMARY": "executive_summary",
            "RISK INDICATORS": "risk_indicators",
            "OPPORTUNITIES": "opportunities",
            "RED FLAGS": "red_flags",
            "CONFIDENCE ASSESSMENT": "confidence_assessment",
            "OVERALL RECOMMENDATION": "overall_recommendation",
        }

        current_section = None
        current_content = []

        lines = response_text.split("\n")

        for line in lines:
            line_stripped = line.strip()

            # Check for section headers
            matched_section = None
            for header, section_key in sections.items():
                if header in line_stripped.upper() and line_stripped.startswith("#"):
                    matched_section = section_key
                    break

            if matched_section:
                # Save previous section
                if current_section:
                    self._save_section_content(result, current_section, current_content)

                # Start new section
                current_section = matched_section
                current_content = []
            else:
                # Accumulate content
                if line_stripped:
                    current_content.append(line_stripped)

        # Save last section
        if current_section:
            self._save_section_content(result, current_section, current_content)

        return result

    def _save_section_content(
        self,
        result: Dict[str, Any],
        section: str,
        content: List[str]
    ):
        """Save parsed section content to result dictionary"""
        if section in ["executive_summary", "confidence_assessment", "overall_recommendation"]:
            # Text sections
            result[section] = "\n".join(content)
        else:
            # List sections (risks, opportunities, red flags)
            items = []
            for line in content:
                if line.startswith("-") or line.startswith("•") or line.startswith("*"):
                    # Extract list item
                    item = line.lstrip("-•*").strip()
                    if item and item.lower() not in ["none", "none identified"]:
                        items.append(item)

            result[section] = items

    def _update_cache_stats(self, usage) -> None:
        """
        Update cache statistics from API response

        Args:
            usage: Usage object from Claude API response
        """
        # Update cache metrics
        self.cache_stats["cache_creation_tokens"] = getattr(usage, 'cache_creation_input_tokens', 0)
        self.cache_stats["cache_read_tokens"] = getattr(usage, 'cache_read_input_tokens', 0)
        self.cache_stats["total_input_tokens"] = getattr(usage, 'input_tokens', 0)
        self.cache_stats["total_output_tokens"] = getattr(usage, 'output_tokens', 0)
