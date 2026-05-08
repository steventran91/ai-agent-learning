import anthropic

client = anthropic.Anthropic()

# ─────────────────────────────────────────────
# PART 1: Zero-shot prompting
# ─────────────────────────────────────────────
# Zero-shot = just ask, no examples provided.
# Works well for common tasks the model has seen a lot of during training.

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=128,
    messages=[
        {"role": "user", "content": "Classify the sentiment of this review as positive, negative, or neutral:\n\n'The battery life is decent but the screen is way too dim.'"}
    ]
)

print("=== PART 1: Zero-shot ===")
print(response.content[0].text.strip())
print()


# ─────────────────────────────────────────────
# PART 2: Few-shot prompting
# ─────────────────────────────────────────────
# Few-shot = show examples of input → output BEFORE your actual question.
# This "teaches" the model the exact format and behavior you want.
# Notice we embed examples directly in the user message.

few_shot_prompt = """Classify the sentiment of product reviews. Reply with only one word: Positive, Negative, or Neutral.

Review: "Absolutely love this! Best purchase I've made all year."
Sentiment: Positive

Review: "Stopped working after two days. Total waste of money."
Sentiment: Negative

Review: "It's fine. Does what it says on the box."
Sentiment: Neutral

Review: "The battery life is decent but the screen is way too dim."
Sentiment:"""

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=16,   # we only need one word
    messages=[
        {"role": "user", "content": few_shot_prompt}
    ]
)

print("=== PART 2: Few-shot ===")
print(f"Answer: {response.content[0].text.strip()}")
print("(Compare — same question, but now it follows the exact format we showed it)")
print()


# ─────────────────────────────────────────────
# PART 3: Chain-of-thought prompting
# ─────────────────────────────────────────────
# Chain-of-thought = ask the model to reason step by step before giving a final answer.
# This is especially powerful for math, logic puzzles, and multi-step decisions.
# Without it, the model may jump to a wrong answer confidently.

question = "A store is having a 30% off sale. A jacket costs $85. " \
           "You also have a coupon for an extra $10 off. " \
           "How much do you pay if the coupon applies AFTER the sale discount?"

# Without chain-of-thought — just asks for the answer
response_direct = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=32,
    messages=[
        {"role": "user", "content": f"{question}\n\nJust give me the final dollar amount."}
    ]
)

# With chain-of-thought — asks the model to show its work first
response_cot = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    messages=[
        {"role": "user", "content": f"{question}\n\nThink through this step by step, then give the final answer."}
    ]
)

print("=== PART 3: Chain-of-thought ===")
print(f"Question: {question}\n")
print(f"Direct answer:          {response_direct.content[0].text.strip()}")
print()
print(f"With chain-of-thought:\n{response_cot.content[0].text.strip()}")
print()


# ─────────────────────────────────────────────
# PART 4: Combining techniques
# ─────────────────────────────────────────────
# In real applications you often combine all three:
# a system prompt (sets behavior) + few-shot examples (shows format) +
# chain-of-thought instruction (improves reasoning quality).

system = "You are a helpful math tutor. Always show your work step by step."

few_shot_cot_prompt = """Here are two examples of how to solve word problems:

Problem: A train travels 60 mph for 2 hours. How far does it go?
Solution: Distance = speed × time = 60 × 2 = 120 miles.
Answer: 120 miles

Problem: A recipe needs 3 cups of flour for 12 cookies. How much for 20 cookies?
Solution: Flour per cookie = 3/12 = 0.25 cups. For 20 cookies = 0.25 × 20 = 5 cups.
Answer: 5 cups

Now solve this:
Problem: A car gets 32 miles per gallon. Gas costs $3.50 per gallon. How much does a 200-mile trip cost?"""

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=128,
    system=system,
    messages=[
        {"role": "user", "content": few_shot_cot_prompt}
    ]
)

print("=== PART 4: Combined techniques ===")
print(response.content[0].text.strip())
