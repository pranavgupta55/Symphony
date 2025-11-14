"""
Debug test to see exact cache behavior
"""
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Create a large system prompt (needs to be 1024+ tokens for caching)
large_system_prompt = """You are a world-class financial analyst specializing in earnings call analysis. You have been provided with a multi-modal analysis of an earnings call.

Your task is to synthesize insights from multiple data sources and provide a comprehensive investment analysis.

## YOUR ANALYSIS FRAMEWORK

You will receive data from the following sources:
1. **Company Context**: Background information about the company
2. **Audio Analysis (Vocal Biomarkers)**: Confidence scores, stress indicators, speech patterns
3. **Text Sentiment Analysis**: Overall sentiment, distribution, key topics, financial metrics
4. **Transcript**: The actual spoken content from the earnings call
5. **Chart Analysis**: Visual data presentations and any inconsistencies detected
6. **Multi-Modal Fusion Results**: Unified credibility score and cross-modal discrepancies

## OUTPUT FORMAT

You MUST provide your analysis in the following structured format:

### EXECUTIVE SUMMARY
[2-3 paragraphs summarizing the key takeaways from this earnings call. What should investors know?]

### RISK INDICATORS
[List 3-5 specific risks identified from the analysis. Consider vocal stress, negative sentiment, inconsistencies, etc.]
- Risk 1: [Description]
- Risk 2: [Description]
...

### OPPORTUNITIES
[List 3-5 opportunities or positive signals. Consider confident delivery, positive sentiment, strong metrics, etc.]
- Opportunity 1: [Description]
- Opportunity 2: [Description]
...

### RED FLAGS
[List any major concerns that warrant immediate attention. These are severe issues.]
- Red Flag 1: [Description] (or "None identified" if no major concerns)
...

### CONFIDENCE ASSESSMENT
[Assess the overall confidence and credibility of management's statements. Use insights from vocal biomarkers, sentiment, and cross-modal consistency.]

### OVERALL RECOMMENDATION
[Provide a clear investment perspective: Bullish, Bearish, or Neutral, with reasoning]

---

## ANALYSIS GUIDELINES

1. **Focus on unique insights**: Emphasize findings that come from the combination of vocal stress detection, sentiment analysis, and chart verification
2. **Be specific**: Reference concrete data points from the analysis
3. **Consider contradictions**: When audio signals (stress, hesitation) contradict positive language, flag this
4. **Quantify risk**: Use the confidence scores and credibility metrics provided
5. **Actionable insights**: Every point should help investors make better decisions

## DETAILED METHODOLOGY

When analyzing vocal biomarkers:
- F0 (pitch) stability indicates confidence
- Energy consistency shows engagement
- Speech rate variations may signal uncertainty
- Hesitation patterns reveal stress points
- Voice quality (HNR) reflects emotional state

When analyzing sentiment:
- Overall sentiment provides broad market reaction
- Topic-specific sentiment reveals nuanced concerns
- Financial metric mentions indicate focus areas
- Sentiment shifts during Q&A highlight sensitive topics

When analyzing charts:
- Look for inconsistencies between verbal claims and visual data
- Verify that trends match management statements
- Check for selective data presentation
- Identify missing or abbreviated time periods

When fusing modalities:
- High audio stress + positive language = potential deception
- Low sentiment + high vocal confidence = contrarian opportunity
- Chart inconsistencies + verbal emphasis = red flag
- Aligned modalities = higher credibility

Now, analyze the data provided in the user message."""

print("Testing cache behavior with detailed debug output\n")
print("="*70)

# Test #1: First call (should create cache)
print("\n📞 Call #1: Creating cache...\n")

response1 = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=500,
    system=[
        {
            "type": "text",
            "text": large_system_prompt,
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "Analyze Company A with revenue of $1B."
        }
    ]
)

print(f"Full Usage Object: {response1.usage}")
print(f"\nDetailed breakdown:")
print(f"  input_tokens: {response1.usage.input_tokens}")
print(f"  cache_creation_input_tokens: {response1.usage.cache_creation_input_tokens}")
print(f"  cache_read_input_tokens: {response1.usage.cache_read_input_tokens}")
print(f"  output_tokens: {response1.usage.output_tokens}")

if hasattr(response1.usage, 'cache_creation'):
    print(f"\nCache Creation Object: {response1.usage.cache_creation}")
    if response1.usage.cache_creation:
        print(f"  ephemeral_1h: {response1.usage.cache_creation.ephemeral_1h_input_tokens}")
        print(f"  ephemeral_5m: {response1.usage.cache_creation.ephemeral_5m_input_tokens}")

# Wait a moment, then test #2
import time
time.sleep(1)

print("\n" + "="*70)
print("\n📞 Call #2: Reading from cache...\n")

response2 = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=500,
    system=[
        {
            "type": "text",
            "text": large_system_prompt,
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "Analyze Company B with revenue of $2B."
        }
    ]
)

print(f"Full Usage Object: {response2.usage}")
print(f"\nDetailed breakdown:")
print(f"  input_tokens: {response2.usage.input_tokens}")
print(f"  cache_creation_input_tokens: {response2.usage.cache_creation_input_tokens}")
print(f"  cache_read_input_tokens: {response2.usage.cache_read_input_tokens}")
print(f"  output_tokens: {response2.usage.output_tokens}")

if hasattr(response2.usage, 'cache_creation'):
    print(f"\nCache Creation Object: {response2.usage.cache_creation}")
    if response2.usage.cache_creation:
        print(f"  ephemeral_1h: {response2.usage.cache_creation.ephemeral_1h_input_tokens}")
        print(f"  ephemeral_5m: {response2.usage.cache_creation.ephemeral_5m_input_tokens}")

print("\n" + "="*70)
print("\n💰 Cost Comparison:\n")

cost_per_1k_input = 3.0  # $3 per million = $0.003 per 1k
cost_per_1k_cached = 0.3  # $0.30 per million = $0.0003 per 1k

call1_cost = (response1.usage.input_tokens / 1000) * cost_per_1k_input
call2_cost_without_cache = (response2.usage.input_tokens / 1000) * cost_per_1k_input
call2_cost_with_cache = (response2.usage.input_tokens / 1000) * cost_per_1k_input + \
                        (response2.usage.cache_read_input_tokens / 1000) * cost_per_1k_cached

print(f"Call #1 (creating cache): ${call1_cost:.6f}")
print(f"Call #2 (without cache):  ${call2_cost_without_cache:.6f}")
print(f"Call #2 (with cache):     ${call2_cost_with_cache:.6f}")

if response2.usage.cache_read_input_tokens > 0:
    savings = call2_cost_without_cache - call2_cost_with_cache
    savings_pct = (savings / call2_cost_without_cache) * 100
    print(f"\n✅ Savings: ${savings:.6f} ({savings_pct:.1f}%)")
    print(f"✅ Cache is working!")
else:
    print(f"\n⚠️  No cache hits detected")
    print(f"Possible reasons:")
    print(f"  - System prompt may be below minimum threshold (1024 tokens)")
    print(f"  - Cache may not have been created properly")
    print(f"  - Model may not support caching")
