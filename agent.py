import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=500,
    messages=[
        {"role": "user", "content": "In one sentence, what is an AI agent?"}
    ]
)

print(response.content[0].text)
print("stop_reason:", response.stop_reason)