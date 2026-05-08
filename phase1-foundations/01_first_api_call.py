import anthropic

# Create a client — it automatically reads your ANTHROPIC_API_KEY environment variable
client = anthropic.Anthropic()

# Send a message to Claude
# - model: which version of Claude to use (claude-haiku-4-5 is fast and cheap, great for learning)
# - max_tokens: the maximum length of the response (1 token ≈ ¾ of a word)
# - messages: the conversation so far, as a list of role/content pairs
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    messages=[
        {"role": "user", "content": "Say hello and tell me one interesting fact about AI in one sentence."}
    ]
)

# The response object contains a lot of info — let's print the part we care about
print("Claude says:")
print(response.content[0].text)

# Let's also inspect some useful metadata
print("\n--- Response metadata ---")
print(f"Model used:        {response.model}")
print(f"Input tokens:      {response.usage.input_tokens}")   # tokens you sent
print(f"Output tokens:     {response.usage.output_tokens}")  # tokens Claude replied with
print(f"Stop reason:       {response.stop_reason}")          # why Claude stopped (usually "end_turn")
