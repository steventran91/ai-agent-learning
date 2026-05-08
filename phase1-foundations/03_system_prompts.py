import anthropic

client = anthropic.Anthropic()

# ─────────────────────────────────────────────
# PART 1: No system prompt (default behavior)
# ─────────────────────────────────────────────
# Without a system prompt, Claude is a general-purpose assistant.

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=128,
    messages=[
        {"role": "user", "content": "Who are you and what can you help me with?"}
    ]
)

print("=== PART 1: No system prompt ===")
print(response.content[0].text.strip())
print()


# ─────────────────────────────────────────────
# PART 2: With a system prompt
# ─────────────────────────────────────────────
# The system prompt is a special parameter that sits outside the messages list.
# Claude sees it first, before any user message. It shapes behavior for the
# entire conversation — like giving an actor their character brief before the scene.

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=128,
    system="You are a grumpy pirate who reluctantly answers questions. "
           "You always complain before helping. You speak in pirate dialect.",
    messages=[
        {"role": "user", "content": "Who are you and what can you help me with?"}
    ]
)

print("=== PART 2: With a system prompt ===")
print(response.content[0].text.strip())
print()


# ─────────────────────────────────────────────
# PART 3: System prompt for a real use case
# ─────────────────────────────────────────────
# A silly example makes the concept clear, but system prompts are powerful
# for real applications: customer support bots, coding assistants, etc.
# Here's what a professional system prompt looks like.

system_prompt = """You are a helpful customer support agent for a software company.

Your rules:
- Be concise — answer in 2-3 sentences maximum
- If you don't know the answer, say so honestly rather than guessing
- Never make up product names, prices, or features
- Always end your response with: "Is there anything else I can help you with?"
"""

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=128,
    system=system_prompt,
    messages=[
        {"role": "user", "content": "How do I reset my password?"}
    ]
)

print("=== PART 3: Professional system prompt ===")
print(response.content[0].text.strip())
print()


# ─────────────────────────────────────────────
# PART 4: System prompt across multiple turns
# ─────────────────────────────────────────────
# The system prompt applies to the ENTIRE conversation, not just the first message.
# Watch how the pirate persona persists even in a follow-up question.

print("=== PART 4: Persona persists across turns ===")

messages = [
    {"role": "user",      "content": "What's 2 + 2?"},
    {"role": "assistant", "content": "Arrr, ye dare interrupt me treasure countin' for ARITHMETIC? "
                                     "Fine... 'tis 4. Now leave me be!"},
    {"role": "user",      "content": "And what's 4 + 4?"},
]

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=128,
    system="You are a grumpy pirate who reluctantly answers questions. "
           "You always complain before helping. You speak in pirate dialect.",
    messages=messages,
)

print(f"User: {messages[2]['content']}")
print(f"Claude: {response.content[0].text.strip()}")
