import anthropic
import json

client = anthropic.Anthropic()


def parse_json_response(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


# ─────────────────────────────────────────────
# PART 1: Testing consistency with temperature=0
# ─────────────────────────────────────────────
# A good prompt should return the same answer every time for the same input.
# We run it 3 times and check if results match.

prompt = "Is this review positive or negative? Reply with one word only.\n\nReview: 'The food was cold and the service was slow.'"

print("=== PART 1: Consistency test (temperature=0) ===")
results = []
for i in range(3):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=16,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.content[0].text.strip()
    results.append(result)
    print(f"Run {i+1}: '{result}'")

all_same = len(set(results)) == 1  # set() removes duplicates — if length is 1, all match
print(f"Consistent: {all_same}\n")


# ─────────────────────────────────────────────
# PART 2: A/B testing two prompt versions
# ─────────────────────────────────────────────
# The core of prompt testing: run two versions against the same inputs
# and compare which one performs better.

test_reviews = [
    "Absolutely love this product, works perfectly!",
    "Terrible quality, broke after one day.",
    "It's okay, nothing special but gets the job done.",
    "Best purchase of the year, highly recommend!",
    "Don't waste your money, completely useless.",
]

# Version A — vague instruction
prompt_a = "What is the sentiment? Reply with one word."

# Version B — specific instruction with format enforcement
prompt_b = "Classify the sentiment of this product review. Reply with exactly one word: Positive, Negative, or Neutral."

print("=== PART 2: A/B prompt comparison ===")
print(f"{'Review':<45} {'Version A':<15} {'Version B':<15}")
print("-" * 75)

for review in test_reviews:
    response_a = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=16,
        temperature=0,
        messages=[{"role": "user", "content": f"{prompt_a}\n\nReview: '{review}'"}]
    )
    response_b = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=16,
        temperature=0,
        messages=[{"role": "user", "content": f"{prompt_b}\n\nReview: '{review}'"}]
    )

    a = response_a.content[0].text.strip()
    b = response_b.content[0].text.strip()
    short_review = review[:42] + "..." if len(review) > 42 else review
    print(f"{short_review:<45} {a:<15} {b:<15}")

print()


# ─────────────────────────────────────────────
# PART 3: Testing edge cases
# ─────────────────────────────────────────────
# Edge cases break prompts. Always test inputs that are ambiguous,
# empty, or outside your expected range.

print("=== PART 3: Edge case testing ===")

edge_cases = [
    ("Normal input",    "The product works great!"),
    ("Mixed sentiment", "Love the design but hate the price."),
    ("Empty review",    ""),
    ("Off-topic",       "I don't know what to say about this."),
    ("Sarcasm",         "Oh sure, TOTALLY works as advertised. *eye roll*"),
]

system = "You are a sentiment classifier. Reply with one word: Positive, Negative, or Neutral."

for label, review in edge_cases:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=32,
        temperature=0,
        system=system,
        messages=[{"role": "user", "content": f"Review: '{review}'"}]
    )
    result = response.content[0].text.strip()
    print(f"{label:<20} | Input: '{review[:40]}' → {result}")

print()


# ─────────────────────────────────────────────
# PART 4: Iterating on a broken prompt
# ─────────────────────────────────────────────
# Walk through one prompt improvement cycle: identify the failure,
# fix it, verify the fix works.

print("=== PART 4: Prompt iteration ===")

# Broken prompt — asks for JSON but doesn't enforce it
broken_prompt = "Extract the name and email from this text and return it as JSON.\n\nText: 'Contact Sarah at sarah@example.com for details.'"

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=128,
    messages=[{"role": "user", "content": broken_prompt}]
)
raw = response.content[0].text.strip()
print(f"Broken prompt output:\n{raw}\n")

# Try to parse it — this may fail
try:
    json.loads(raw)
    print("Parse result: SUCCESS")
except json.JSONDecodeError:
    print("Parse result: FAILED — response has extra text or fences\n")

# Fixed prompt — system prompt enforces raw JSON, schema is explicit
fixed_system = "You extract structured data. Respond with raw JSON only. No explanation, no code fences."
fixed_prompt = """<instructions>
Extract the name and email from the text. Return exactly: {"name": "", "email": ""}
</instructions>

<text>
Contact Sarah at sarah@example.com for details.
</text>"""

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=64,
    system=fixed_system,
    messages=[{"role": "user", "content": fixed_prompt}]
)
raw = response.content[0].text.strip()
print(f"Fixed prompt output:\n{raw}\n")

# Always use defensive parsing — Claude may still add fences despite instructions
try:
    data = parse_json_response(raw)
    print(f"Parse result: SUCCESS → name='{data['name']}', email='{data['email']}'")
except json.JSONDecodeError:
    print("Parse result: FAILED")
