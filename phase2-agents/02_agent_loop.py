import anthropic
import json
import math

client = anthropic.Anthropic()


# ─────────────────────────────────────────────
# The tools — Python functions + JSON descriptions
# ─────────────────────────────────────────────

def calculator(operation: str, a: float, b: float) -> dict:
    """Performs basic math operations."""
    ops = {
        "add":      a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide":   a / b if b != 0 else "Error: division by zero",
        "power":    a ** b,
        "sqrt":     math.sqrt(a),   # b is ignored for sqrt
    }
    result = ops.get(operation, f"Error: unknown operation '{operation}'")
    return {"operation": operation, "a": a, "b": b, "result": result}


def get_word_count(text: str) -> dict:
    """Counts words, characters, and sentences in a piece of text."""
    words = len(text.split())
    chars = len(text)
    sentences = text.count('.') + text.count('!') + text.count('?')
    return {"words": words, "characters": chars, "sentences": sentences}


# JSON tool descriptions
tools = [
    {
        "name": "calculator",
        "description": "Perform math calculations. Use this for any arithmetic, including add, subtract, multiply, divide, power, and sqrt.",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide", "power", "sqrt"],
                    "description": "The math operation to perform."
                },
                "a": {"type": "number", "description": "First number."},
                "b": {"type": "number", "description": "Second number (not used for sqrt)."}
            },
            "required": ["operation", "a", "b"]
        }
    },
    {
        "name": "get_word_count",
        "description": "Count the words, characters, and sentences in a piece of text.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The text to analyze."}
            },
            "required": ["text"]
        }
    }
]

# Maps tool names to the actual Python functions
TOOL_FUNCTIONS = {
    "calculator": calculator,
    "get_word_count": get_word_count,
}


# ─────────────────────────────────────────────
# The agent loop
# ─────────────────────────────────────────────
# This function handles the full observe → think → act cycle automatically.
# It keeps looping until Claude stops requesting tools.

def run_agent(user_message: str):
    print(f"\nUser: {user_message}")
    print("-" * 50)

    # The messages list grows each iteration — this is the agent's short-term memory
    messages = [{"role": "user", "content": user_message}]

    iteration = 0

    while True:
        iteration += 1
        print(f"[Loop iteration {iteration}]")

        # Ask Claude what to do next
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            tools=tools,
            messages=messages,
        )

        print(f"  Stop reason: {response.stop_reason}")

        # If Claude is done, print the final answer and exit the loop
        if response.stop_reason == "end_turn":
            final_text = next(
                (block.text for block in response.content if hasattr(block, "text")), ""
            )
            print(f"\nFinal answer: {final_text}")
            break

        # Claude wants to use one or more tools — process each tool call
        if response.stop_reason == "tool_use":
            # Add Claude's response (which contains the tool call) to message history
            messages.append({"role": "assistant", "content": response.content})

            # Collect results for all tool calls in this response
            # (Claude can request multiple tools in a single response)
            tool_results = []

            for block in response.content:
                if block.type != "tool_use":
                    continue

                print(f"  Tool call: {block.name}({block.input})")

                # Look up and run the Python function
                fn = TOOL_FUNCTIONS[block.name]
                result = fn(**block.input)

                print(f"  Tool result: {result}")

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,      # ties result back to the specific request
                    "content": json.dumps(result)
                })

            # Add all tool results to the message history and loop again
            messages.append({"role": "user", "content": tool_results})

    return messages   # return full history so we can inspect it


# ─────────────────────────────────────────────
# Test 1: single tool call
# ─────────────────────────────────────────────
print("=" * 50)
print("TEST 1: Single tool call")
run_agent("What is 347 multiplied by 19?")

# ─────────────────────────────────────────────
# Test 2: multiple tool calls in sequence
# ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("TEST 2: Multiple tool calls")
run_agent("What is 15 squared? Then take the square root of that result.")

# ─────────────────────────────────────────────
# Test 3: agent picks the right tool on its own
# ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("TEST 3: Agent chooses the right tool")
run_agent("How many words are in this sentence: 'The quick brown fox jumps over the lazy dog'? Then tell me what 10% of that word count is.")


# ─────────────────────────────────────────────
# Inspect the raw message history
# ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("RAW MESSAGE HISTORY")
history = run_agent("What is 347 multiplied by 19?")
print("\n--- Full message history ---")
print(json.dumps(history, indent=2, default=str))
print("\n--- Full message history ---")
print(json.dumps(history, indent=2, default=str))
