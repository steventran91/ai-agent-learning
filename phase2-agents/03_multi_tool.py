import anthropic
import json
import datetime

client = anthropic.Anthropic()


# ─────────────────────────────────────────────
# A personal assistant agent with 4 tools.
# The point: Claude picks the right tool (or combination) for each request.
# ─────────────────────────────────────────────

def get_weather(city: str) -> dict:
    fake_data = {
        "San Francisco": {"temp": 18, "condition": "foggy"},
        "New York":      {"temp": 24, "condition": "sunny"},
        "London":        {"temp": 12, "condition": "rainy"},
        "Tokyo":         {"temp": 28, "condition": "humid"},
    }
    data = fake_data.get(city, {"temp": 20, "condition": "unknown"})
    return {"city": city, **data}


def search_calendar(date: str) -> dict:
    """Fake calendar — returns events for a given date (YYYY-MM-DD)."""
    fake_calendar = {
        "2026-05-13": ["9am: Team standup", "2pm: Design review", "5pm: Gym"],
        "2026-05-14": ["10am: Client call", "12pm: Lunch with Sarah"],
        "2026-05-15": ["All day: Company offsite"],
    }
    events = fake_calendar.get(date, [])
    return {"date": date, "events": events, "count": len(events)}


def send_reminder(message: str, time: str) -> dict:
    """Fake reminder — in a real app this would schedule a notification."""
    return {"status": "Reminder set", "message": message, "time": time}


def calculate(expression: str) -> dict:
    """Safely evaluate a math expression like '15 * 4 + 10'."""
    try:
        # eval is dangerous with untrusted input — in production use a proper math parser
        result = eval(expression, {"__builtins__": {}}, {})
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"expression": expression, "error": str(e)}


TOOL_FUNCTIONS = {
    "get_weather":     get_weather,
    "search_calendar": search_calendar,
    "send_reminder":   send_reminder,
    "calculate":       calculate,
}

tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city. Use when the user asks about weather or temperature.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name, e.g. 'London'"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "search_calendar",
        "description": "Look up calendar events for a specific date. Use when the user asks about their schedule, meetings, or plans.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Date in YYYY-MM-DD format"}
            },
            "required": ["date"]
        }
    },
    {
        "name": "send_reminder",
        "description": "Set a reminder with a message and time. Use when the user asks to be reminded about something.",
        "input_schema": {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "What to remind the user about"},
                "time":    {"type": "string", "description": "When to send the reminder, e.g. '3pm' or '9am tomorrow'"}
            },
            "required": ["message", "time"]
        }
    },
    {
        "name": "calculate",
        "description": "Evaluate a math expression. Use when the user asks for a calculation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression to evaluate, e.g. '15 * 4 + 10'"}
            },
            "required": ["expression"]
        }
    }
]


# ─────────────────────────────────────────────
# Reusable agent loop (same pattern as before)
# ─────────────────────────────────────────────

def run_agent(user_message: str, system: str = ""):
    print(f"\nUser: {user_message}")
    print("-" * 50)

    messages = [{"role": "user", "content": user_message}]

    while True:
        kwargs = {"model": "claude-haiku-4-5-20251001", "max_tokens": 1024, "tools": tools, "messages": messages}
        if system:
            kwargs["system"] = system

        response = client.messages.create(**kwargs)

        if response.stop_reason == "end_turn":
            final = next((b.text for b in response.content if hasattr(b, "text")), "")
            print(f"Answer: {final}")
            break

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []

            for block in response.content:
                if block.type != "tool_use":
                    continue
                print(f"  → {block.name}({block.input})")
                result = TOOL_FUNCTIONS[block.name](**block.input)
                print(f"    {result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result)
                })

            messages.append({"role": "user", "content": tool_results})


# ─────────────────────────────────────────────
# Tests — each one requires a different tool or combination
# ─────────────────────────────────────────────

system_prompt = "You are a helpful personal assistant. Today's date is 2026-05-13."

print("=" * 50)
print("TEST 1: Single tool — weather")
run_agent("What's the weather like in Tokyo?", system_prompt)

print("\n" + "=" * 50)
print("TEST 2: Single tool — calendar")
run_agent("What do I have on my schedule tomorrow?", system_prompt)

print("\n" + "=" * 50)
print("TEST 3: Single tool — reminder")
run_agent("Remind me to send the project report at 4pm.", system_prompt)

print("\n" + "=" * 50)
print("TEST 4: Two tools — weather + calendar")
run_agent("Should I bring an umbrella to my 2pm meeting today? Check the weather in San Francisco and my calendar.", system_prompt)

print("\n" + "=" * 50)
print("TEST 5: No tool needed")
run_agent("What's the capital of Japan?", system_prompt)

print("\n" + "=" * 50)
print("TEST 6: Calculate tool")
run_agent("What is 100 times 34? then divide that by 6. What's the result?", system_prompt)
