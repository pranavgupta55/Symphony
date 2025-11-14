"""
Simple cache test - just check if system prompt is being cached
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.claude_integration import ClaudeIntegrationService

print("Testing if system prompt meets 1024 token threshold for caching...\n")

service = ClaudeIntegrationService()

# Get the system prompt
system_prompt = service._create_system_prompt()

# Rough token count (1 token ≈ 4 characters for English)
char_count = len(system_prompt)
approx_tokens = char_count // 4

print(f"System Prompt Length:")
print(f"  Characters: {char_count}")
print(f"  Estimated tokens: {approx_tokens}")
print(f"  Threshold for caching: 1024 tokens")
print(f"  Will cache: {'✅ YES' if approx_tokens >= 1024 else '❌ NO'}")

if approx_tokens >= 1024:
    print(f"\n✅ System prompt is large enough for caching!")
    print(f"   Expected cache tokens on first call: ~{approx_tokens}")
    print(f"   Expected cache read on second call: ~{approx_tokens}")
else:
    print(f"\n❌ System prompt is too small for caching")
    print(f"   Need at least {1024 - approx_tokens} more tokens")
