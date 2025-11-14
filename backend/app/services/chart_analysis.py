"""
Chart Analysis Service using Claude Vision API
"""
import anthropic
import base64
from pathlib import Path
from typing import List, Dict, Any
from ..core.config import settings


class ChartAnalysisService:
    """Service for analyzing financial charts using Claude Vision API"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    def analyze_charts(
        self,
        chart_paths: List[str],
        transcript_text: str = "",
        company_context: str = ""
    ) -> Dict[str, Any]:
        """
        Analyze financial charts and compare with verbal statements

        Args:
            chart_paths: List of paths to chart images
            transcript_text: Full transcript text for comparison
            company_context: Additional company context

        Returns:
            Dictionary with chart analysis results
        """
        try:
            if not chart_paths:
                return {
                    "chart_descriptions": [],
                    "extracted_data": [],
                    "inconsistencies": [],
                }

            print(f"📊 Analyzing {len(chart_paths)} charts...")

            chart_descriptions = []
            extracted_data = []
            inconsistencies = []

            for i, chart_path in enumerate(chart_paths):
                print(f"  Analyzing chart {i+1}/{len(chart_paths)}...")

                # Analyze single chart
                analysis = self._analyze_single_chart(
                    chart_path,
                    transcript_text,
                    company_context
                )

                chart_descriptions.append(analysis["description"])
                extracted_data.extend(analysis["data"])

                if analysis.get("inconsistencies"):
                    inconsistencies.extend(analysis["inconsistencies"])

            print(f"✅ Chart analysis complete. Found {len(inconsistencies)} inconsistencies")

            return {
                "chart_descriptions": chart_descriptions,
                "extracted_data": extracted_data,
                "inconsistencies": inconsistencies,
            }

        except Exception as e:
            print(f"❌ Chart analysis error: {e}")
            raise Exception(f"Failed to analyze charts: {str(e)}")

    def _analyze_single_chart(
        self,
        chart_path: str,
        transcript_text: str,
        company_context: str
    ) -> Dict[str, Any]:
        """
        Analyze a single chart image

        Args:
            chart_path: Path to chart image
            transcript_text: Transcript for comparison
            company_context: Company context

        Returns:
            Dictionary with chart analysis
        """
        # Read and encode image
        image_data = self._encode_image(chart_path)

        # Create analysis prompt
        prompt = self._create_chart_analysis_prompt(transcript_text, company_context)

        try:
            # Call Claude Vision API
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": self._get_media_type(chart_path),
                                    "data": image_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt,
                            }
                        ],
                    }
                ],
            )

            # Parse response
            analysis_text = response.content[0].text

            # Extract structured data from response
            result = self._parse_chart_response(analysis_text)

            return result

        except Exception as e:
            print(f"Warning: Failed to analyze chart {chart_path}: {e}")
            return {
                "description": f"Failed to analyze chart: {str(e)}",
                "data": [],
                "inconsistencies": [],
            }

    def _encode_image(self, image_path: str) -> str:
        """
        Encode image to base64

        Args:
            image_path: Path to image

        Returns:
            Base64 encoded image string
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def _get_media_type(self, image_path: str) -> str:
        """
        Get media type from file extension

        Args:
            image_path: Path to image

        Returns:
            Media type string
        """
        ext = Path(image_path).suffix.lower()
        media_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        return media_types.get(ext, "image/jpeg")

    def _create_chart_analysis_prompt(
        self,
        transcript_text: str,
        company_context: str
    ) -> str:
        """
        Create prompt for chart analysis

        Args:
            transcript_text: Transcript text
            company_context: Company context

        Returns:
            Analysis prompt
        """
        prompt = """Analyze this financial chart in detail. Please provide:

1. **Chart Description**: What type of chart is this? (line, bar, pie, etc.) What does it show?

2. **Key Data Points**: Extract specific numbers, trends, and metrics shown in the chart.
   - What are the axes labels?
   - What time periods are covered?
   - What are the key values shown?

3. **Trends & Insights**: What trends or patterns are visible?

4. **Inconsistencies**: If provided with transcript context below, identify any discrepancies between what the chart shows and what was stated verbally.

"""

        if company_context:
            prompt += f"\n**Company Context**: {company_context}\n"

        if transcript_text:
            # Include first 500 words of transcript for context
            transcript_excerpt = " ".join(transcript_text.split()[:500])
            prompt += f"\n**Transcript Excerpt**: {transcript_excerpt}...\n"

        prompt += """
Please structure your response as follows:

DESCRIPTION: [Brief description of the chart]

DATA:
- [Key data point 1]
- [Key data point 2]
...

TRENDS:
- [Trend 1]
- [Trend 2]
...

INCONSISTENCIES:
- [Any inconsistency found, or "None detected"]
"""

        return prompt

    def _parse_chart_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse structured response from Claude

        Args:
            response_text: Claude's response text

        Returns:
            Structured dictionary
        """
        result = {
            "description": "",
            "data": [],
            "inconsistencies": [],
        }

        # Simple parsing logic
        sections = {
            "DESCRIPTION:": "description",
            "DATA:": "data",
            "TRENDS:": "trends",
            "INCONSISTENCIES:": "inconsistencies",
        }

        current_section = None
        lines = response_text.split("\n")

        for line in lines:
            line = line.strip()

            # Check for section headers
            for header, section_name in sections.items():
                if line.startswith(header):
                    current_section = section_name
                    # Extract content after header
                    content = line[len(header):].strip()
                    if content:
                        if section_name == "description":
                            result["description"] = content
                    break
            else:
                # Process content based on current section
                if current_section and line:
                    if line.startswith("-") or line.startswith("•"):
                        # List item
                        content = line.lstrip("-•").strip()
                        if content:
                            if current_section == "data":
                                result["data"].append({
                                    "description": content,
                                    "source": "chart"
                                })
                            elif current_section == "inconsistencies":
                                if content.lower() not in ["none", "none detected", "no inconsistencies"]:
                                    result["inconsistencies"].append({
                                        "type": "chart_verbal_mismatch",
                                        "description": content,
                                        "severity": "medium"
                                    })
                    elif current_section == "description" and not result["description"]:
                        result["description"] = line

        # Default description if none found
        if not result["description"]:
            result["description"] = "Financial chart analysis completed"

        return result
