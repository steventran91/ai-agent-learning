import anthropic

client = anthropic.Anthropic()


# ─────────────────────────────────────────────
# PART 1: Seeing hallucination happen
# ─────────────────────────────────────────────
# Ask about something obscure or fictional — the model may invent facts.

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=128,
    messages=[{"role": "user", "content": "What were the key findings of the 2019 Stanford study on AI productivity by Dr. James Whitfield?"}]
)

print("=== PART 1: Hallucination-prone question ===")
print(response.content[0].text.strip())
print()


# ─────────────────────────────────────────────
# PART 2: Fix #1 — tell Claude it's okay to say "I don't know"
# ─────────────────────────────────────────────
# By default, Claude tries to be helpful and may fill gaps with plausible-sounding
# information. Explicitly giving it permission to say "I don't know" reduces this.

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=128,
    system="You are a helpful assistant. If you are not certain about a fact, say 'I don't know' rather than guessing. Never make up names, dates, studies, or citations.",
    messages=[{"role": "user", "content": "What were the key findings of the 2019 Stanford study on AI productivity by Dr. James Whitfield?"}]
)

print("=== PART 2: With 'I don't know' permission ===")
print(response.content[0].text.strip())
print()


# ─────────────────────────────────────────────
# PART 3: Fix #2 — ground answers in a provided document (RAG pattern)
# ─────────────────────────────────────────────
# The most reliable way to prevent hallucination is to give Claude
# the source material and tell it to answer ONLY from that document.
# This is called RAG (Retrieval-Augmented Generation) — you'll use it
# heavily in the Phase 1 milestone project.

document = """
Quarterly Sales Report — Q3 2024

Total revenue: $4.2 million
Units sold: 12,400
Top product: Model X Pro (38% of sales)
Worst performer: Model Z Lite (4% of sales)
New customers acquired: 310
Customer churn rate: 6.2%
"""

prompt = f"""<instructions>
Answer the question using ONLY the information in the document below.
If the answer is not in the document, say exactly: "That information is not in the report."
Do not use any outside knowledge.
</instructions>

<document>
{document}
</document>

<question>
What was the churn rate and which product performed worst?
</question>"""

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=128,
    messages=[{"role": "user", "content": prompt}]
)

print("=== PART 3: Grounded answer (in-document question) ===")
print(response.content[0].text.strip())
print()

# Now ask something NOT in the document — Claude should refuse to answer
prompt_out_of_scope = f"""<instructions>
Answer the question using ONLY the information in the document below.
If the answer is not in the document, say exactly: "That information is not in the report."
Do not use any outside knowledge.
</instructions>

<document>
{document}
</document>

<question>
Who is the CEO of this company?
</question>"""

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=64,
    messages=[{"role": "user", "content": prompt_out_of_scope}]
)

print("=== PART 3b: Grounded answer (out-of-document question) ===")
print(response.content[0].text.strip())
print()


# ─────────────────────────────────────────────
# PART 4: Fix #3 — ask Claude to flag uncertainty
# ─────────────────────────────────────────────
# Instead of binary know/don't-know, ask Claude to express its confidence level.
# Useful when you want an answer but also want to know how much to trust it.

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=192,
    system="When answering questions, always end your response with a confidence rating: [High confidence], [Medium confidence], or [Low confidence — verify this]. Use low confidence whenever you are recalling specific facts, dates, names, or statistics from memory.",
    messages=[{"role": "user", "content": "When was the Eiffel Tower built, and how tall is it?"}]
)

print("=== PART 4: Confidence flagging ===")
print(response.content[0].text.strip())
print()


# ─────────────────────────────────────────────
# PART 5: Summary — the three techniques
# ─────────────────────────────────────────────
print("=== PART 5: Anti-hallucination techniques ===")
print("1. Permission to decline  — tell Claude it's okay to say 'I don't know'")
print("2. Document grounding     — provide the source, answer only from it (RAG)")
print("3. Confidence flagging    — ask Claude to rate its own certainty")
print()
print("In production, technique #2 (RAG) is the gold standard.")
print("The Phase 1 milestone project uses it to build a reliable Document Q&A system.")
