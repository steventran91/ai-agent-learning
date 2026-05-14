import anthropic
import json

client = anthropic.Anthropic()


# ─────────────────────────────────────────────
# Tools (same as before)
# ─────────────────────────────────────────────

def search_web(query: str) -> dict:
    """Fake web search — returns made-up results for learning purposes."""
    fake_results = {
        "Python salary 2024":        {"results": ["Average Python developer salary: $115,000/yr", "Senior Python dev: $145,000/yr", "Entry level: $75,000/yr"]},
        "JavaScript salary 2024":    {"results": ["Average JS developer salary: $110,000/yr", "Senior JS dev: $140,000/yr", "Entry level: $70,000/yr"]},
        "remote work statistics":    {"results": ["32% of US workers work remotely full-time", "65% work hybrid", "Remote jobs increased 44% since 2020"]},
        "best programming languages":{"results": ["1. Python", "2. JavaScript", "3. TypeScript", "4. Rust", "5. Go"]},
    }
    return fake_results.get(query, {"results": ["No results found for: " + query]})


def calculate(expression: str) -> dict:
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"expression": expression, "error": str(e)}


TOOL_FUNCTIONS = {"search_web": search_web, "calculate": calculate}

tools = [
    {
        "name": "search_web",
        "description": "Search the web for information. Use this to look up facts, statistics, or current information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculate",
        "description": "Evaluate a math expression.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression, e.g. '115000 * 0.8'"}
            },
            "required": ["expression"]
        }
    }
]


# ─────────────────────────────────────────────
# PART 1: Agent WITHOUT ReAct
# ─────────────────────────────────────────────
# Tools get called but you have no visibility into why.
# Fine for simple tasks — but when something goes wrong, hard to debug.

def run_agent(user_message: str, system: str = ""):
    # message history
    messages = [{"role": "user", "content": user_message}]
    while True:
        # this is the payload for the api call. 
        # if system prompt provided, insert system to the arg
        kwargs = {"model": "claude-haiku-4-5-20251001", "max_tokens": 1024, "tools": tools, "messages": messages}
        if system:
            kwargs["system"] = system
            # api call 
        response = client.messages.create(**kwargs)

        if response.stop_reason == "end_turn":
            return next((b.text for b in response.content if hasattr(b, "text")), "")

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                print(f"  [tool call] {block.name}({block.input})")
                result = TOOL_FUNCTIONS[block.name](**block.input)
                tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)})
            messages.append({"role": "user", "content": tool_results})


# ─────────────────────────────────────────────
# PART 2: Agent WITH ReAct
# ─────────────────────────────────────────────
# The system prompt instructs Claude to think through its plan before acting.
# The key format: Thought → Action → Observation → repeat → Final Answer

REACT_SYSTEM = """You are a research assistant that thinks step by step before acting.

For every step, follow this format:
Thought: [explain what you know, what you need to find out, and why you're choosing this action]
Action: [the tool you'll call]

After receiving tool results, continue with:
Observation: [what you learned from the result]
Thought: [what to do next, or that you have enough info]

End with:
Final Answer: [your complete answer to the user's question]

Never skip the Thought step. Always explain your reasoning before calling a tool."""


def run_react_agent(user_message: str):
    messages = [{"role": "user", "content": user_message}]
    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=REACT_SYSTEM,
            tools=tools,
            messages=messages,
        )

        # Print any text Claude generated (its reasoning/thoughts)
        for block in response.content:
            if hasattr(block, "text") and block.text.strip():
                print(block.text.strip())
                print()

        if response.stop_reason == "end_turn":
            break

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                print(f"[Running tool: {block.name}({block.input})]")
                result = TOOL_FUNCTIONS[block.name](**block.input)
                print(f"[Result: {result}]\n")
                tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)})
            messages.append({"role": "user", "content": tool_results})


# ─────────────────────────────────────────────
# Run both agents on the same question — compare the output
# ─────────────────────────────────────────────

question = "If I'm a Python developer making the average salary, how much do I take home after 20% tax?"

print("=" * 60)
print("WITHOUT ReAct:")
print("=" * 60)
answer = run_agent(question)
print(f"Answer: {answer}")

print("\n" + "=" * 60)
print("WITH ReAct:")
print("=" * 60)
run_react_agent(question)
