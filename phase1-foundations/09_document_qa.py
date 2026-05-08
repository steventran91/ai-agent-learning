import anthropic
import json

client = anthropic.Anthropic()

# ─────────────────────────────────────────────
# Phase 1 Milestone: Document Q&A System
#
# Techniques used:
#   - System prompts (sets the assistant's behavior)
#   - XML tags (separates instructions from document content)
#   - Document grounding (answers only from provided text)
#   - Hallucination prevention (refuses out-of-scope questions)
#   - Multi-turn conversation (remembers previous Q&A in the session)
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """You are a precise document analyst.

Your rules:
1. Answer questions using ONLY the information in the document provided.
2. If the answer is not in the document, respond with exactly: "That information is not in the document."
3. Always quote or reference the specific part of the document your answer comes from.
4. Never use outside knowledge, even if you're confident it's correct.
5. Keep answers concise — 1-3 sentences unless the question requires more detail."""


def ask_question(document: str, question: str, history: list) -> str:
    """Send a question about the document and return Claude's answer."""

    # Build the user message using XML tags to clearly separate each part
    user_message = f"""<document>
{document}
</document>

<question>
{question}
</question>"""

    # Add the new question to the conversation history
    # History lets Claude refer back to previous answers in the same session
    history.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=history,
    )

    answer = response.content[0].text.strip()

    # Add Claude's answer to history so the next question has context
    history.append({"role": "assistant", "content": answer})

    return answer


def run_qa_session(document: str):
    """Interactive Q&A loop for a document."""
    history = []  # grows with each turn — this is the short-term memory

    print("\n" + "="*60)
    print("Document Q&A System ready.")
    print("Ask questions about the document. Type 'quit' to exit.")
    print("="*60 + "\n")

    while True:
        question = input("Your question: ").strip()

        if question.lower() in ("quit", "exit", "q"):
            print("Session ended.")
            break

        if not question:
            continue

        print("\nAnswer:", end=" ")
        answer = ask_question(document, question, history)
        print(answer)
        print()


# ─────────────────────────────────────────────
# Sample document — swap this out for any text you want to query
# ─────────────────────────────────────────────

SAMPLE_DOCUMENT = """
The Apollo 11 Mission — Summary

Apollo 11 was the American spaceflight that first landed humans on the Moon.
Commander Neil Armstrong and lunar module pilot Buzz Aldrin landed the Apollo
Lunar Module Eagle on July 20, 1969, at 20:17 UTC. Armstrong became the first
person to step onto the lunar surface six hours and 39 minutes later, on
July 21 at 02:56 UTC. Aldrin joined him 19 minutes later.

The two astronauts spent about two and a quarter hours together outside the
spacecraft and collected 47.5 pounds (21.5 kg) of lunar material to bring back
to Earth. The third member of the mission, command module pilot Michael Collins,
piloted the command spacecraft in lunar orbit until Armstrong and Aldrin returned.

The mission fulfilled a national goal proposed in 1961 by President John F. Kennedy:
to perform a crewed lunar landing and return to Earth before the end of the 1960s.
The mission was declared a success by NASA, and the crew returned safely on
July 24, 1969, splashing down in the Pacific Ocean.
"""


if __name__ == "__main__":
    print("Document loaded:")
    print("-" * 40)
    print(SAMPLE_DOCUMENT.strip())
    print("-" * 40)

    run_qa_session(SAMPLE_DOCUMENT)
