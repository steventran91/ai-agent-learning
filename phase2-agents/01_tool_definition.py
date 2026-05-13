import anthropic
import json

client = anthropic.Anthropic()


# ─────────────────────────────────────────────
# PART 1: What a tool definition looks like
# ─────────────────────────────────────────────
# A tool is just a Python function + a JSON description of that function.
# Claude reads the description to decide WHEN to call the tool and WHAT
# arguments to pass. You write the actual logic — Claude decides when to use it.

# Step 1: Write the actual Python function
def get_weather(city: str, unit: str = "celsius") -> dict:
    """Fake weather function — in a real app this would call a weather API."""
    fake_data = {
        "San Francisco": {"temp": 18, "condition": "foggy"},
        "New York":      {"temp": 24, "condition": "sunny"},
        "London":        {"temp": 12, "condition": "rainy"},
    }
    weather = fake_data.get(city, {"temp": 20, "condition": "unknown"})
    temp = weather["temp"] if unit == "celsius" else round(weather["temp"] * 9/5 + 32)
    return {"city": city, "temperature": temp, "unit": unit, "condition": weather["condition"]}


# Step 2: Write the JSON description of that function
# This is what you pass to Claude — it never sees the Python code above,
# only this description. The quality of this description determines how
# well Claude knows when and how to call the tool.
weather_tool = {
    "name": "get_weather",                          # must match your function name
    "description": "Get the current weather for a city. Use this when the user asks about weather, temperature, or conditions in a specific location.",
    "input_schema": {                               # JSON Schema format — describes the arguments
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The name of the city, e.g. 'San Francisco' or 'London'"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],  # enum restricts valid values
                "description": "Temperature unit. Defaults to celsius."
            }
        },
        "required": ["city"]                        # city is required, unit is optional
    }
}

print("=== PART 1: Tool definition ===")
print("Tool name:", weather_tool["name"])
print("Description:", weather_tool["description"])
print("Required args:", weather_tool["input_schema"]["required"])
print()


# ─────────────────────────────────────────────
# PART 2: Claude decides whether to use the tool
# ─────────────────────────────────────────────
# Pass the tool to Claude via the `tools` parameter.
# Claude will call it if it thinks it needs to — or answer directly if it doesn't.

def ask_with_tool(user_message: str):
    print(f"User: {user_message}")

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        tools=[weather_tool],           # give Claude access to the tool
        messages=[{"role": "user", "content": user_message}]
    )

    # stop_reason tells us WHY Claude stopped generating
    # "tool_use"  = Claude wants to call a tool
    # "end_turn"  = Claude answered directly without using a tool
    print(f"Stop reason: {response.stop_reason}")

    if response.stop_reason == "tool_use":
        # Find the tool call in the response content blocks
        tool_use = next(block for block in response.content if block.type == "tool_use")
        print(f"Claude wants to call: {tool_use.name}")
        print(f"With arguments: {json.dumps(tool_use.input, indent=2)}")
    else:
        print(f"Claude answered directly: {response.content[0].text}")
    print()

print("=== PART 2: Does Claude use the tool? ===")
ask_with_tool("What's the weather like in London?")       # should trigger tool
ask_with_tool("What is the capital of France?")           # should NOT trigger tool
ask_with_tool("Is it warm in New York right now?")        # should trigger tool


# ─────────────────────────────────────────────
# PART 3: Completing the tool call (one full round trip)
# ─────────────────────────────────────────────
# When Claude calls a tool, it STOPS and waits for you to run the function
# and send the result back. Then it generates a final response using that result.
# This is the core pattern of every agent.

print("=== PART 3: Full tool call round trip ===")

user_message = "What's the weather in San Francisco in fahrenheit?"

# Turn 1: send the user message
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    tools=[weather_tool],
    messages=[{"role": "user", "content": user_message}]
)

# Claude stopped to request a tool call
tool_use = next(block for block in response.content if block.type == "tool_use")
print(f"1. Claude requested tool: {tool_use.name}({tool_use.input})")

# Run the actual function with the arguments Claude chose
tool_result = get_weather(**tool_use.input)
print(f"2. Tool returned: {tool_result}")

# Turn 2: send the tool result back to Claude
# The messages list now has: user message → assistant tool call → tool result
response2 = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    tools=[weather_tool],
    messages=[
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": response.content},    # Claude's tool call
        {"role": "user", "content": [                          # our tool result
            {
                "type": "tool_result",
                "tool_use_id": tool_use.id,                    # must match the request
                "content": json.dumps(tool_result)
            }
        ]}
    ]
)

print(f"3. Claude's final answer: {response2.content[0].text}")
