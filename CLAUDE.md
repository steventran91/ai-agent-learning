# AI Agent Learning Project

## About this file
Claude Code reads this file automatically at the start of every session. It defines your
learning goals, current progress, project structure, and how Claude should behave as your
coding mentor throughout this project.

---

## Who you are
You are a beginner learning to build AI agents using Claude. Your goal is to become
job-ready in agentic AI development. You have basic familiarity with Python but are new
to LLMs, the Anthropic API, MCP, and agent architecture.

## How Claude should behave in this project
- Act as a **patient coding mentor**, not just a code generator
- Always **explain what you're doing and why** before writing code
- When introducing a new concept, give a **one-paragraph plain-English explanation first**
- Write **heavily commented code** — every non-obvious line should have a comment
- If something could be done multiple ways, **show the simplest way first**, then mention alternatives
- After completing a task, always suggest **what to try next** to deepen understanding
- If I make a mistake or have a misconception, **correct it gently with an explanation**
- Keep responses **focused and practical** — working code over theory

---

## Learning roadmap

### Phase 1 — LLM & prompt engineering foundations (Weeks 1–2)
**Goal:** Understand how LLMs work and write reliable prompts

Topics to cover:
- [x] Tokens, context windows, and temperature
- [x] System prompts vs user messages
- [x] Zero-shot, few-shot, and chain-of-thought prompting
- [x] Getting structured JSON output reliably
- [x] XML tags in prompts (`<instructions>`, `<examples>`, `<context>`)
- [x] Prompt testing and iteration
- [x] Hallucination and how to reduce it

Milestone project: **Document Q&A system** — paste any document, ask questions about it
reliably without hallucination.

### Phase 2 — Agent architecture & tool use (Weeks 3–4)
**Goal:** Build your first real agent loop

Topics to cover:
- [ ] What an agent loop is (observe → think → act → repeat)
- [ ] Tool/function definitions (JSON schema)
- [ ] How Claude decides when to call a tool
- [ ] Handling tool results and multi-turn conversations
- [ ] ReAct pattern (Reasoning + Acting)
- [ ] Memory: short-term (context) vs long-term (files/databases)
- [ ] Error handling in agents

Milestone project: **Research agent** — give it a question, it searches the web, reads
pages, and writes a summary report.

### Phase 3 — MCP, Claude.md & skills (Weeks 5–6)
**Goal:** Understand the Claude Code ecosystem and extend it

Topics to cover:
- [ ] What MCP (Model Context Protocol) is and why it exists
- [ ] Building a simple MCP server in Python
- [ ] Connecting an MCP server to Claude Code
- [ ] What CLAUDE.md files do (you are reading one right now!)
- [ ] Writing effective CLAUDE.md files for different project types
- [ ] What "skills" are and how they work
- [ ] Claude Code slash commands and workflows

Milestone project: **Custom MCP server** — build a server that exposes a local SQLite
database as tools Claude can query and write to.

### Phase 4 — Real agents & portfolio projects (Weeks 7–8)
**Goal:** Build things you can show employers

Topics to cover:
- [ ] Multi-agent systems (orchestrator + subagents)
- [ ] Agentic coding with Claude Code
- [ ] Handling long-running tasks safely
- [ ] Evaluation and testing agents
- [ ] Deploying a simple agent as an API

Milestone projects (pick one or more):
- **Coding agent** — reviews a codebase, finds bugs, writes fixes
- **Customer support agent** — handles questions with memory of past conversations
- **Data analyst agent** — given a CSV, answers questions and generates charts

---

## Current progress

Update this section as you complete topics. Claude will use it to know where you are.

```
Phase 1: [ ] Not started
Phase 2: [ ] Not started
Phase 3: [ ] Not started  ← you are here (reading this file = first step of Phase 3!)
Phase 4: [ ] Not started

Last session: Getting set up, exploring CLAUDE.md
Next task:    Start Phase 1 — understand tokens and make your first API call
```

---

## Project structure

```
ai-learning/
├── CLAUDE.md                  ← this file (Claude reads it every session)
├── README.md                  ← project overview for GitHub
│
├── phase1-foundations/
│   ├── 01_first_api_call.py   ← hello world with the Anthropic SDK
│   ├── 02_tokens.py           ← exploring tokenization
│   ├── 03_system_prompts.py   ← experimenting with system prompts
│   ├── 04_structured_output.py← getting reliable JSON back
│   └── 05_document_qa.py      ← Phase 1 milestone project
│
├── phase2-agents/
│   ├── 01_tool_definition.py  ← defining your first tool
│   ├── 02_agent_loop.py       ← the core observe-think-act loop
│   ├── 03_multi_tool.py       ← agent with multiple tools
│   └── 04_research_agent.py   ← Phase 2 milestone project
│
├── phase3-mcp/
│   ├── 01_mcp_server.py       ← minimal MCP server
│   ├── 02_sqlite_tools.py     ← database-backed MCP tools
│   └── mcp_config.json        ← MCP server config for Claude Code
│
├── phase4-portfolio/
│   └── (your chosen project)
│
└── notes/
    └── learnings.md           ← your personal notes (update as you go)
```

---

## How to start each session

When you open Claude Code, just say one of:
- `"Let's continue Phase 1"` — Claude will check progress and pick up where you left off
- `"Explain [concept] then let's code it"` — dive into a specific topic
- `"Review my code in phase1-foundations/"` — get feedback on what you've written
- `"I'm stuck on [thing]"` — debugging and help

You don't need to re-explain your background — Claude reads this file and knows your context.

---

## Key concepts reference

A quick-reference glossary. Claude can expand on any of these on request.

| Term | One-line definition |
|------|---------------------|
| Token | The unit LLMs process — roughly ¾ of a word on average |
| Context window | How much text the model can "see" at once (e.g. 200K tokens) |
| System prompt | Hidden instructions that shape the model's behavior |
| Temperature | Randomness knob: 0 = deterministic, 1 = creative |
| Tool/function call | How you give the model access to external actions |
| Agent loop | Observe → think → act → observe → ... until task done |
| ReAct | Reasoning + Acting — model explains its thinking before each action |
| MCP | Model Context Protocol — standard for connecting AI to external tools |
| CLAUDE.md | This file — persistent context Claude Code reads every session |
| RAG | Retrieval-Augmented Generation — giving the model relevant docs to answer from |

---

## Setup checklist

Complete these before starting Phase 1:

- [x] Python 3.10+ installed (`python --version`)
- [x] Anthropic SDK installed (`pip install anthropic`)
- [x] API key set as environment variable (`export ANTHROPIC_API_KEY=sk-ant-...`)
- [x] Claude Code installed (`npm install -g @anthropic-ai/claude-code`)
- [x] This project folder open in Claude Code
- [x] `notes/learnings.md` created (write one thing you learn each session)

To verify setup, ask Claude: `"Run my first API call and show me the output"`

---

## Resources

- Anthropic docs: https://docs.anthropic.com
- Prompt engineering guide: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- MCP documentation: https://modelcontextprotocol.io
- Claude Code docs: https://docs.anthropic.com/en/docs/claude-code
- Anthropic cookbook (code examples): https://github.com/anthropics/anthropic-cookbook

---

## Notes from past sessions

*(Claude will help you update this section as you learn. Treat it as a learning journal.)*

- Session 1: Created this CLAUDE.md file. Understanding how Claude Code uses project context.

---

*Last updated: May 2026*
