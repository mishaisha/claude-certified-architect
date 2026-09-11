# CCA-F Learning Notes

Study guide for Claude Certified Architect Foundations exam.

## Learning Sequence

```
STEP  1  api_check.py              API Setup
STEP  2  agent.py                  Agentic Loop
STEP  3  research_summarizer.py    Full Single-Agent
STEP  4  inbuilt_tools.py          Built-in Tools
STEP  5  tool_choice.py            Tool Choice + Descriptions
STEP  6  developer_productivity.py Codebase Exploration
STEP  7  dynamic_decomposition.py  Adaptive Decomposition
STEP  8  multi_agents.py           Coordinator Pattern
STEP  9  subagent_context.py       Context Passing
STEP 10  fork_session.py           Session Management
STEP 11  prompt_chaining           Sequential Chaining
STEP 12  few_shot_examples.py      Few-Shot Prompting
STEP 13  ci_pipeline.sh            CI/CD Integration
STEP 14  capstone_project.py       Multi-Agent Combo
```

---

## Step 1: api_check.py — API Setup

**What it teaches:** How the Anthropic SDK connects to Claude.

### Key Concepts

```python
client = anthropic.Anthropic()
```
- SDK auto-reads `ANTHROPIC_API_KEY` from environment
- Never hardcode keys

```python
model="claude-haiku-4-5"
```
- All course examples pin to `claude-haiku-4-5` (cost + speed)

```python
messages=[{"role": "user", "content": "..."}]
```
- Conversation is a list of dicts
- Two roles: `"user"` (human) and `"assistant"` (Claude)

```python
response.content[0].text
```
- Response contains `content` array of blocks
- Text blocks have `.text`, tool blocks have `.type == "tool_use"`

### Exam Fact
The SDK reads `ANTHROPIC_API_KEY` from environment. Never hardcode.

---

## Step 2: agent.py — The Agentic Loop

**What it teaches:** The core pattern for building agents with Claude.

This is the **most important file** in the course.

### Concept 1: Tool Definition

```python
tools = [{
    "name": "lookup_order",           # Claude calls this
    "description": "Look up...",      # Claude decides WHEN to use it
    "input_schema": { ... }           # JSON Schema for parameters
}]
```

Three fields. Description drives tool selection.

### Concept 2: The Agentic Loop

```python
while iteration < MAX_ITERATIONS:
    response = client.messages.create(...)

    if response.stop_reason == "end_turn":   # Claude is done
        return block.text

    if response.stop_reason == "tool_use":   # Claude wants tools
        # execute tools, append results, loop continues
```

**Two stop reasons:**
- `"end_turn"` → Claude finished → extract text → **exit**
- `"tool_use"` → Claude wants tools → run them → **loop continues**

**`MAX_ITERATIONS` is a safety valve, NOT a stop condition.**

### Concept 3: The Append Order (EXAM FAVORITE)

```python
# APPEND 1: assistant message (Claude's tool request)
messages.append({"role": "assistant", "content": response.content})

# APPEND 2: tool results (role: "user" — data coming INTO Claude)
messages.append({"role": "user", "content": tool_results})
```

**Order matters:**
1. Append assistant message FIRST (contains `tool_use` blocks)
2. Append tool results SECOND (role is `"user"` even though no human typed it)

### Concept 4: Four Error Categories (EXAM CRITICAL)

| Category | Example | isRetryable | Action |
|---|---|---|---|
| `transient` | TimeoutError | `True` | Retry after delay |
| `permission` | PermissionError | `False` | Escalate |
| `validation` | ValueError | `False` | Model self-corrects |
| `internal` | Exception | `False` | Surface to human |

**Memory trick:** T-P-V-I → "Time Passes, Violent Internal"

### Concept 5: Tool Result Shape

```python
return {
    "type": "tool_result",
    "tool_use_id": tool_id,      # links to Claude's request
    "content": json_string,       # result or error
}
```

On error, add `"is_error": True` and structured error metadata.

### Key Exam Facts
1. `stop_reason == "end_turn"` is the ONLY valid primary exit
2. Append order: assistant → tool results (as user)
3. Four error categories with specific retry behavior
4. `MAX_ITERATIONS` is safety valve, not stop condition

---

## Step 3: research_summarizer.py — Full Single-Agent

*Notes coming after review...*

---

## Step 4: inbuilt_tools.py — Built-in Tools

*Notes coming after review...*

---

## Step 5: tool_choice.py — Tool Choice + Descriptions

*Notes coming after review...*

---

## Step 6: developer_productivity.py — Codebase Exploration

*Notes coming after review...*

---

## Step 7: dynamic_decomposition.py — Adaptive Decomposition

*Notes coming after review...*

---

## Step 8: multi_agents.py — Coordinator Pattern

*Notes coming after review...*

---

## Step 9: subagent_context.py — Context Passing

*Notes coming after review...*

---

## Step 10: fork_session.py — Session Management

*Notes coming after review...*

---

## Step 11: prompt_chaining — Sequential Chaining

*Notes coming after review...*

---

## Step 12: few_shot_examples.py — Few-Shot Prompting

*Notes coming after review...*

---

## Step 13: ci_pipeline.sh — CI/CD Integration

*Notes coming after review...*

---

## Step 14: capstone_project.py — Multi-Agent Combo

*Notes coming after review...*
