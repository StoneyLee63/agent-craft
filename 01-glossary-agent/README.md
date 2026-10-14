# Glossary Agent

A Claude command-line agent, you ask for a term and it brings back the definition. It searches its own glossary through a tool, finds the definition and outputs the results.

## What it does

```
python 01-glossary-agent/agent.py
Ask the glossary agent: What is an AI agent?            
stop_reason: tool_use
tool result: not found
stop_reason: tool_use
tool result: An AI agent is a software entity that uses artificial intelligence to perform tasks autonomously or semi-autonomously, often interacting with users or other systems.
stop_reason: end_turn
The glossary defines an AI agent as follows:

> A software entity that uses artificial intelligence to perform tasks autonomously or semi-autonomously, often interacting with users or other systems.

The first search, "ai agent", returned no result. The entry was listed under "agent".

In practice, an AI agent usually does more than answer a single prompt. It can pursue a goal, decide what steps to take, use tools such as search, code execution, or APIs, and adjust based on the results. "Semi-autonomous" means a human may still review or approve some steps.

I can look up related terms in the glossary if you'd like, such as "orchestrator."
```

## How it works

1. The typed question is given to Claude along with a tool called `lookup_term`.

2. When Claude stops with `tool_use`, the loop runs `lookup_term` for every term that was asked for and sends everything back in one message.

3. That repeats until Claude stops for any other reason, then at the end the final text prints.

4. A term that isn't in the agent's glossary returns a `not found` instead of crashing so Claude can see its misses and report them.

5. `MAX_TURNS` caps the loop at 5 rounds. 

## How to run it

Python 3, the `anthropic` package, and an Anthropic API key as the `ANTHROPIC_API_KEY` environment variable.

```
git clone https://github.com/StoneyLee63/agent-craft.git
cd agent-craft
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic
export ANTHROPIC_API_KEY=your-key-here
python 01-glossary-agent/agent.py
```

## What it reads and writes

**What it reads**
- The question typed in the prompt
- The glossary, a dictionary defined inside `agent.py`
- The API key from the `ANTHROPIC_API_KEY` environment variable

**What it writes**
- Each `stop_reason`, each tool result, and the final answer, all printed to the terminal
- Writes no files
- Sends the conversation to the Anthropic API over the network

## Why it's built this way

- I made sure **the loop checks** `!= "tool_use"`, **not** `== "end_turn"` because any stop reason that isn't a tool request ends the loop, so it can't spin on something unexpected like `max_tokens`.
- I **batched the tool results** so when Claude asks for several terms at once, all the answers go back in one message.
- I used **`.get`** with `not found`. A missing term comes back as a clear result Claude can read and report, instead of crashing the agent.