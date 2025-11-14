"""
Test script to verify API key has access to Claude Sonnet 4.5
"""
import anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("❌ No ANTHROPIC_API_KEY found in .env file")
    exit(1)

print(f"🔑 Testing API key: {api_key[:20]}...")

# Initialize client
client = anthropic.Anthropic(api_key=api_key)

# Test models in order of preference
test_models = [
    "claude-sonnet-4-5-20250929",
    "claude-sonnet-4-5",
    "claude-3-5-sonnet-20241022",
    "claude-3-haiku-20240307"
]

print("\n🧪 Testing model access...\n")

for model in test_models:
    try:
        print(f"Testing {model}...", end=" ")
        response = client.messages.create(
            model=model,
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Hello' if you can read this."
                }
            ]
        )
        print(f"✅ SUCCESS")
        print(f"   Response: {response.content[0].text[:50]}")
        print(f"   Usage: {response.usage}")

        # If we found Sonnet 4.5, test caching
        if "sonnet-4" in model or "sonnet-3-5" in model:
            print(f"\n🎯 Found working Sonnet model: {model}")
            print(f"\n🧪 Testing prompt caching with {model}...\n")

            try:
                cache_response = client.messages.create(
                    model=model,
                    max_tokens=100,
                    system=[
                        {
                            "type": "text",
                            "text": "You are a financial analyst.",
                            "cache_control": {"type": "ephemeral"}
                        }
                    ],
                    messages=[
                        {
                            "role": "user",
                            "content": "What is 2+2?"
                        }
                    ]
                )
                print(f"✅ CACHE TEST SUCCESS")
                print(f"   Response: {cache_response.content[0].text[:50]}")
                print(f"   Usage: {cache_response.usage}")

                if hasattr(cache_response.usage, 'cache_creation_input_tokens'):
                    print(f"   ✅ Cache support confirmed!")
                    print(f"   Cache creation tokens: {cache_response.usage.cache_creation_input_tokens}")
                else:
                    print(f"   ⚠️  No cache tokens in response (may still work)")

            except Exception as cache_error:
                print(f"❌ CACHE TEST FAILED: {cache_error}")

            break

    except anthropic.NotFoundError as e:
        print(f"❌ NOT FOUND (404)")
    except Exception as e:
        print(f"❌ ERROR: {e}")

print("\n" + "="*60)
print("Test complete!")
