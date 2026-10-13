import anthropic

client = anthropic.Anthropic()

TOOLS = [
    {
        "name": "lookup_term",
        "description": "Looks up keyword terms and matches them with definitions. Use when a user wants a definition from the glossary. It returns the definition to Claude as text for the user. If the term is not found, the tool will send back not found",
        "input_schema": {
            "type": "object",
            "properties": {
                "term": {
                    "type": "string",
                    "description": "The term to look up, in lowercase, like 'orchestrator'",
                }
            },
            "required": ["term"],
        },
    }
]

GLOSSARY = {
    "agent": "An AI agent is a software entity that uses artificial intelligence to perform tasks autonomously or semi-autonomously, often interacting with users or other systems.",
    "orchestrator": "An agent that breaks a big task into pieces, hands each piece to worker agents, and combines what they send back.",
    "stop_reason": "Stop when the answer is complete, the max_tokens are at the required limit, Claude stops with tool_use to ask for a tool and Claude finishes sending back results.",
}

def lookup_term(term):
    return GLOSSARY.get(term, "not found")

messages = [
    {"role": "user", "content": "What does orchestrator mean?"}
]

while True:
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=500,
        tools=TOOLS,
        messages=messages,
    )
    print("stop_reason:", response.stop_reason)

    if response.stop_reason != "tool_use":
        break

    messages.append({"role": "assistant", "content": response.content})

    for block in response.content:
        if block.type == "tool_use":
            result = lookup_term(block.input["term"])
            print("tool result:", result)
            messages.append({
                "role": "user",
                "content": [
                    {"type": "tool_result", "tool_use_id": block.id, "content": result}
                ]
            })

for block in response.content:
    if block.type == "text":
        print(block.text)