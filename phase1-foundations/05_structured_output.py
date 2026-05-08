import anthropic
import json

client = anthropic.Anthropic()


# Helper defined up top so all parts can use it.
# Strips markdown code fences before parsing — Claude often adds these even when told not to.
def parse_json_response(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


# ─────────────────────────────────────────────
# PART 1: Asking for JSON — the naive way
# ─────────────────────────────────────────────
# Just asking "respond in JSON" works sometimes, but it's unreliable.
# Claude might add explanation text before/after the JSON, breaking your parser.

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    messages=[
        {"role": "user", "content": "Extract the name, age, and city from this text and return JSON:\n\n'Hi, I'm Maria. I'm 34 years old and I live in Austin.'"}
    ]
)

print("=== PART 1: Naive JSON request ===")
raw = response.content[0].text.strip()
print(f"Raw response:\n{raw}")
print()


# ─────────────────────────────────────────────
# PART 2: Reliable JSON with a strong system prompt
# ─────────────────────────────────────────────
# Two techniques that make JSON output reliable:
# 1. Tell Claude in the system prompt to ONLY return JSON, nothing else
# 2. Show the exact schema you expect using a few-shot example

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    system="You are a data extraction assistant. "
           "You ONLY respond with valid JSON. "
           "No explanation, no markdown, no code fences. Raw JSON only.",
    messages=[
        {"role": "user", "content": "Extract the name, age, and city from this text:\n\n'Hi, I'm Maria. I'm 34 years old and I live in Austin.'"}
    ]
)

print("=== PART 2: JSON with system prompt ===")
raw = response.content[0].text.strip()
print(f"Raw response: {raw}")

# Now we can safely parse it (handles code fences if present)
data = parse_json_response(raw)
print(f"Parsed name: {data['name']}")
print(f"Parsed age:  {data['age']}")
print(f"Parsed city: {data['city']}")
print()


# ─────────────────────────────────────────────
# PART 3: Specifying exact schema with few-shot
# ─────────────────────────────────────────────
# When you need a specific structure, show Claude exactly what you want
# using an example input → output pair in the prompt.

system = "You are a data extraction assistant. Respond with raw JSON only. No explanation."

prompt = """Extract product information from reviews. Use exactly this schema:
{"product": "", "rating": 0, "pros": [], "cons": [], "would_recommend": true}

Example:
Review: "The AirPods Pro are amazing for calls but expensive."
Output: {"product": "AirPods Pro", "rating": 4, "pros": ["great for calls"], "cons": ["expensive"], "would_recommend": true}

Now extract from this review:
Review: "The Kindle Paperwhite has a beautiful screen and long battery life, but the setup process was confusing and it feels a bit heavy." """

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    system=system,
    messages=[{"role": "user", "content": prompt}]
)

print("=== PART 3: Exact schema with few-shot ===")
raw = response.content[0].text.strip()
data = parse_json_response(raw)

# Now we can use the structured data programmatically
print(f"Product:          {data['product']}")
print(f"Rating:           {data['rating']}/5")
print(f"Pros:             {', '.join(data['pros'])}")
print(f"Cons:             {', '.join(data['cons'])}")
print(f"Would recommend:  {data['would_recommend']}")
print()


# ─────────────────────────────────────────────
# PART 4: Handling JSON parse failures gracefully
# ─────────────────────────────────────────────
# Even with good prompts, JSON can fail — Claude might wrap it in ```json fences.
# This helper strips common wrappers before parsing.

def parse_json_response(text: str) -> dict:
    text = text.strip()
    # Remove markdown code fences if present (```json ... ``` or ``` ... ```)
    if text.startswith("```"):
        text = text.split("```")[1]         # get content between first pair of fences
        if text.startswith("json"):
            text = text[4:]                  # strip the "json" language tag
    return json.loads(text.strip())

# Test it on a response that has code fences
fenced_json = '```json\n{"name": "Alex", "age": 28}\n```'
result = parse_json_response(fenced_json)
print("=== PART 4: Robust parser ===")
print(f"Input:  {fenced_json}")
print(f"Parsed: {result}")
