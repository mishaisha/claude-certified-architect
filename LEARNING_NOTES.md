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

**What it teaches:** A complete runnable agent — tools, error handling, loop, all in one file.

Reinforces Step 2 with a real use case: searching a document corpus.

### What's New vs Step 2

| Concept | Step 2 (agent.py) | Step 3 (this file) |
|---|---|---|
| Tools | 1 tool (lookup_order) | 2 tools (search_docs + fetch_doc) |
| Tool descriptions | Basic | Detailed: WHAT, WHEN, WHAT NOT, WHAT RETURNED |
| Use case | Single lookup | Multi-step research |

### Tool Design Pattern (EXAM CRITICAL)

Each description answers 4 questions:
1. WHAT does it do?
2. WHEN should I call it?
3. WHAT NOT to use it for?
4. WHAT does it return?

```python
"search_docs": "Call this FIRST to discover which documents exist...
                Do NOT use this to read full contents — use fetch_doc."

"fetch_doc":   "Call this AFTER search_docs to read actual content.
                Do NOT call with a topic keyword."
```

### The Two-Tool Flow

```
User: "Research tool-use loop"
   → Claude calls search_docs(topic="tool-use") → returns [doc-002, doc-005]
   → Claude calls fetch_doc(doc_id="doc-002") → returns full body
   → Claude calls fetch_doc(doc_id="doc-005") → returns full body
   → Claude synthesizes → stop_reason == "end_turn"
```

### Key Exam Facts
1. Tool descriptions drive selection — write them carefully
2. Two-tool pattern: search first → fetch second
3. Same error handling as Step 2 (transient/permission/validation/internal)
4. Same loop pattern — exit on `end_turn`, safety valve on `MAX_ITERATIONS`

---

## Step 4: inbuilt_tools.py — Built-in Tools

**What it teaches:** The 5 tools Claude Code uses to interact with your filesystem.

### The 5 Built-in Tools

| Tool | What it does | Input | Use when |
|---|---|---|---|
| `grep` | Search file **content** | pattern, path, include | Find function calls, error messages, imports |
| `glob` | Search file **paths** | pattern, path | Find files by name/extension |
| `read` | Read full file | file_path | Load file into context |
| `write` | Create/overwrite file | file_path, content | Generate new files |
| `edit` | Targeted replacement | file_path, old_string, new_string | Modify specific lines |

### Grep vs Glob (EXAM FAVORITE)

```
Grep = CONTENT search → "find all callers of process_refund"
Glob = PATH search    → "find all .test.tsx files"
```

Memory trick: Grep = grep (search text). Glob = glob (match patterns).

### The Edit Fallback Pattern (EXAM CRITICAL)

```
Step 1: Edit fails (old_string matches multiple locations)
Step 2: Read the full file
Step 3: Claude modifies in reasoning
Step 4: Write the entire updated file
```

Why: Edit needs unique anchor text. If text appears multiple times, it fails. Fallback: Read + Write.

### Key Exam Facts
1. **Grep** = content search. **Glob** = path search.
2. **Edit** needs unique `old_string`. Non-unique → fails.
3. **Fallback**: Edit fails → Read full file → Write updated version.
4. Don't read all files upfront — use Grep to find entry points first.

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
