# Learning Journal

---

## Phase 1 — LLM & Prompt Engineering Foundations
**Completed:** 2026-05-07

### What I built

| File | What it taught |
|------|----------------|
| 01_first_api_call.py | Basic API call — model, max_tokens, messages structure |
| 02_tokens.py | Token counting, context windows, temperature |
| 03_system_prompts.py | System prompts, personas, multi-turn conversation |
| 04_prompting_techniques.py | Zero-shot, few-shot, chain-of-thought |
| 05_structured_output.py | JSON output, defensive parsing for code fences |
| 06_xml_tags.py | XML tags, prompt injection defense |
| 07_prompt_testing.py | A/B testing prompts, edge cases, iteration cycle |
| 08_hallucination.py | Hallucination causes and 3 ways to reduce it |
| 09_document_qa.py | Milestone: interactive Document Q&A system |

### Key things I learned

- A token is roughly ¾ of a word. You pay per token (input + output).
- The context window is how much Claude can "see" at once — 200K tokens for Haiku.
- Temperature 0 = deterministic. Temperature 1 = creative/varied.
- System prompts set behavior for the whole conversation. The user never sees them.
- Few-shot examples are more reliable than describing the format in words.
- Chain-of-thought (asking Claude to think step by step) reduces reasoning errors.
- Claude often adds markdown code fences even when told not to — always use a defensive JSON parser.
- XML tags (`<instructions>`, `<document>`, `<question>`) clearly separate instructions from content.
- The most reliable way to prevent hallucination is document grounding: answer only from provided text.
- Conversation history is just a list you build up — there's no magic memory, you send it all every time.

### Gotchas to remember

- `pip` and `pip3` may point to different Python environments — use `python3 -m pip` to be safe.
- Claude Code's shell may use a different Python than your terminal.
- System prompts are instructions, not guarantees — defensive code is always needed for parsing.

---

## Phase 2 — Agent Architecture & Tool Use
*(not started)*

---

## Phase 3 — MCP, Claude.md & Skills
*(not started)*

---

## Phase 4 — Real Agents & Portfolio Projects
*(not started)*
