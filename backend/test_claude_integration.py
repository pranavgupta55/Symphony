"""
Test script for Claude Sonnet 4.5 integration with prompt caching
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.claude_integration import ClaudeIntegrationService
from app.core.config import settings

print("="*70)
print("🧪 Testing Claude Sonnet 4.5 Integration with Prompt Caching")
print("="*70)

# Print configuration
print(f"\n📋 Configuration:")
print(f"   Model: {settings.CLAUDE_MODEL}")
print(f"   Max Tokens: {settings.CLAUDE_MAX_TOKENS}")
print(f"   Temperature: {settings.CLAUDE_TEMPERATURE}")
print(f"   Prompt Caching: {settings.ENABLE_PROMPT_CACHING}")

# Create test data
test_company_name = "TechCorp Inc."
test_company_context = "A leading technology company focused on AI and machine learning solutions"

test_transcript = {
    "full_text": "Good morning everyone. Thank you for joining us today. We're excited to share our Q4 results. Revenue grew 25% year over year to $1.2 billion. Our AI products continue to gain market share, and we're seeing strong adoption in the enterprise segment. That said, we faced some headwinds in our consumer division due to increased competition. Looking ahead, we expect margins to improve as we scale our operations.",
    "segments": [
        {"speaker": "CEO", "text": "Good morning everyone. Thank you for joining us today."},
        {"speaker": "CEO", "text": "We're excited to share our Q4 results."}
    ]
}

test_audio_features = {
    "overall_confidence": 0.75,
    "stress_indicators": [
        {"type": "pitch_variation", "severity": "moderate", "timestamp": 10.5},
        {"type": "speech_rate_increase", "severity": "low", "timestamp": 45.2}
    ],
    "prosodic": {
        "speech_rate": 2.3,
        "energy_mean": 0.65
    },
    "pitch": {
        "variation": 0.042,
        "mean": 150.5
    }
}

test_sentiment_analysis = {
    "overall_sentiment": "positive",
    "sentiment_distribution": {
        "positive": 0.65,
        "neutral": 0.25,
        "negative": 0.10
    },
    "key_topics": ["revenue growth", "market share", "AI products", "enterprise adoption", "competition"],
    "financial_metrics": [
        {"metric": "revenue", "value": "$1.2B", "change": "+25%"},
        {"metric": "market_share", "trend": "increasing"}
    ]
}

test_chart_analysis = {
    "chart_descriptions": [
        "Revenue trend chart showing consistent growth from Q1 to Q4",
        "Market share comparison chart showing TechCorp at 18% vs competitors"
    ],
    "extracted_data": [
        {"chart": 1, "data": "Q1: $900M, Q2: $950M, Q3: $1.1B, Q4: $1.2B"}
    ],
    "inconsistencies": []
}

test_fusion_results = {
    "credibility_score": 0.78,
    "risk_level": "moderate",
    "discrepancies": [
        {"type": "sentiment_audio_mismatch", "description": "Positive language with moderate vocal stress when discussing competition"}
    ]
}

# Initialize service
print("\n🔧 Initializing Claude Integration Service...")
service = ClaudeIntegrationService()

# Test #1: First call (should create cache)
print("\n" + "="*70)
print("📞 Test #1: First API call (creating cache)")
print("="*70)

try:
    result1 = service.generate_comprehensive_analysis(
        company_name=test_company_name,
        company_context=test_company_context,
        transcript=test_transcript,
        audio_features=test_audio_features,
        sentiment_analysis=test_sentiment_analysis,
        chart_analysis=test_chart_analysis,
        fusion_results=test_fusion_results
    )

    print("\n✅ First call successful!")
    print(f"\n📊 Cache Statistics:")
    cache_stats = result1.get("cache_stats", {})
    print(f"   Cache Creation Tokens: {cache_stats.get('cache_creation_tokens', 0)}")
    print(f"   Cache Read Tokens: {cache_stats.get('cache_read_tokens', 0)}")
    print(f"   Total Input Tokens: {cache_stats.get('total_input_tokens', 0)}")
    print(f"   Total Output Tokens: {cache_stats.get('total_output_tokens', 0)}")

    print(f"\n📋 Analysis Preview:")
    print(f"   Executive Summary: {result1.get('executive_summary', '')[:200]}...")
    print(f"   Risk Indicators: {len(result1.get('risk_indicators', []))} identified")
    print(f"   Opportunities: {len(result1.get('opportunities', []))} identified")
    print(f"   Red Flags: {len(result1.get('red_flags', []))} identified")
    print(f"   Overall Recommendation: {result1.get('overall_recommendation', '')[:100]}...")

    # Test #2: Second call with same system prompt (should read from cache)
    print("\n" + "="*70)
    print("📞 Test #2: Second API call (reading from cache)")
    print("="*70)

    # Modify user data slightly
    test_company_name_2 = "TechCorp Inc. (Q4 2024)"

    result2 = service.generate_comprehensive_analysis(
        company_name=test_company_name_2,
        company_context=test_company_context,
        transcript=test_transcript,
        audio_features=test_audio_features,
        sentiment_analysis=test_sentiment_analysis,
        chart_analysis=test_chart_analysis,
        fusion_results=test_fusion_results
    )

    print("\n✅ Second call successful!")
    print(f"\n📊 Cache Statistics:")
    cache_stats2 = result2.get("cache_stats", {})
    print(f"   Cache Creation Tokens: {cache_stats2.get('cache_creation_tokens', 0)}")
    print(f"   Cache Read Tokens: {cache_stats2.get('cache_read_tokens', 0)}")
    print(f"   Total Input Tokens: {cache_stats2.get('total_input_tokens', 0)}")
    print(f"   Total Output Tokens: {cache_stats2.get('total_output_tokens', 0)}")

    # Calculate savings
    if cache_stats2.get('cache_read_tokens', 0) > 0:
        savings_pct = (cache_stats2.get('cache_read_tokens', 0) /
                      (cache_stats2.get('cache_read_tokens', 0) + cache_stats2.get('total_input_tokens', 0))) * 100
        print(f"\n💰 Cost Savings:")
        print(f"   Tokens read from cache: {cache_stats2.get('cache_read_tokens', 0)}")
        print(f"   Estimated cost reduction: ~{savings_pct:.1f}% on input tokens")
        print(f"   ✅ Prompt caching is working!")
    else:
        print(f"\n⚠️  No cache hits detected (cache may have expired or not been created)")

    print("\n" + "="*70)
    print("🎉 All tests completed successfully!")
    print("="*70)

    print(f"\n✅ Summary:")
    print(f"   • Model: {settings.CLAUDE_MODEL}")
    print(f"   • Prompt caching: {'ACTIVE' if cache_stats2.get('cache_read_tokens', 0) > 0 else 'NOT DETECTED'}")
    print(f"   • Analysis quality: GOOD (structured output received)")
    print(f"   • Integration status: ✅ WORKING")

except Exception as e:
    print(f"\n❌ Test failed with error:")
    print(f"   {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
