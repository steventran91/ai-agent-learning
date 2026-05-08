import anthropic

client = anthropic.Anthropic()

# ─────────────────────────────────────────────
# PART 1: Count tokens BEFORE sending a message
# ─────────────────────────────────────────────
# The count_tokens API lets you check token usage without actually calling the model.
# Useful for estimating cost or checking if you're near the context window limit.

messages = [{"role": "user", "content": "What is the capital of France?"}]

token_count = client.messages.count_tokens(
    model="claude-haiku-4-5-20251001",
    messages=messages,
)

print("=== PART 1: Token counting ===")
print(f"Message: '{messages[0]['content']}'")
print(f"Token count: {token_count.input_tokens}")
print()

# Try a longer message and see how the count changes
long_message = [{"role": "user", "content": "What is the capital of France? " * 20}]
long_count = client.messages.count_tokens(
    model="claude-haiku-4-5-20251001",
    messages=long_message,
)
print(f"Same message repeated 20x: {long_count.input_tokens} tokens")
print(f"Ratio: {long_count.input_tokens / token_count.input_tokens:.1f}x — notice it's not exactly 20x")
print()


# ─────────────────────────────────────────────
# PART 2: Temperature in action
# ─────────────────────────────────────────────
# We'll ask Claude a creative question three times:
# once at temperature=0 (deterministic) and twice at temperature=1 (random).
# The temperature=0 responses should be nearly identical.
# The temperature=1 responses should differ.

print("=== PART 2: Temperature ===")

question = "Give me a one-sentence creative name for a coffee shop."

print(f"Question: '{question}'\n")

# temperature=0: predictable, consistent
for i in range(2):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=64,
        temperature=0,   # deterministic
        messages=[{"role": "user", "content": question}]
    )
    print(f"temperature=0, run {i+1}: {response.content[0].text.strip()}")

print()

# temperature=1: creative, varied
for i in range(2):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=64,
        temperature=1,   # more random
        messages=[{"role": "user", "content": question}]
    )
    print(f"temperature=1, run {i+1}: {response.content[0].text.strip()}")

print()


# ─────────────────────────────────────────────
# PART 3: Context window — what happens at the limit
# ─────────────────────────────────────────────
# Claude Haiku has a 200,000-token context window.
# We won't actually hit it (that would cost money), but let's calculate
# how much of the window a typical conversation uses.

print("=== PART 3: Context window math ===")

context_window = 200_000  # tokens

used_tokens = token_count.input_tokens
remaining = context_window - used_tokens
percent_used = (used_tokens / context_window) * 100

print(f"Context window size:  {context_window:,} tokens")
print(f"Our short message:    {used_tokens} tokens")
print(f"Remaining capacity:   {remaining:,} tokens")
print(f"Percent used:         {percent_used:.4f}%")
print()
print("A 300-page novel is roughly 100,000 tokens.")
print("Claude could hold about 2 novels in its context window at once.")
