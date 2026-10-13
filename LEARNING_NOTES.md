# CCAR-F Learning Notes

Study guide for the Claude Certified Architect (Foundations) exam.
Aligned to Exam Guide v1.0 (July 2026) via claudecertificationguide.com.

## Official Exam Facts

- 60 questions, 120 minutes (2 min/question pace), Pearson VUE (online proctored or test centre)
- Weighted scoring out of 1000; pass mark 720. $125 USD. Credential valid 12 months.
- Real exam requires an answer to every question before advancing.
- Domain weights: D1 Agentic Architecture 27% | D2 Tool Design & MCP 18% |
  D3 Claude Code 20% | D4 Prompt Engineering 20% | D5 Context Management 15%
- 30 task statements total (7 + 5 + 6 + 6 + 6 across the five domains).

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
| `transient` | TimeoutError | `True` | Resend as-is after delay |
| `permission` | PermissionError | `False` | Escalate to someone with access |
| `validation` | ValueError | `False` | Model corrects input, new call |
| `business` | Policy violation | `False` | Take an alternative path |

**Memory trick:** T-P-V-B → "Transient Passes, Violations Blocked"

Official guide (Exam Guide v1.0): only `transient` is retryable — the flag asks
whether resending *this* call can work. "Not found" is deliberately NOT a
category: a search returning 0 results is a valid empty result, not an error.
The metadata rides inside the result `content`; the MCP envelope itself only
defines `content`, `structuredContent` and `isError`.

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
3. Same error handling as Step 2 (transient/permission/validation/business)
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

**What it teaches:** How tool_choice controls selection + how descriptions drive tool selection.

### Part 1: tool_choice Configuration

| Value | Behavior | Use when |
|---|---|---|
| `"auto"` | Model decides tool or text | Default — most common |
| `"any"` | Model must call SOME tool | Guarantee structured output |
| `{"type": "tool", "name": "..."}` | Force specific tool | Tool must run first |

### Part 2: Description Design (EXAM CRITICAL)

**Anti-pattern — ambiguous descriptions:**
```python
{"name": "search_web", "description": "Search for information"}
{"name": "search_documents", "description": "Search documents for information"}
# Claude picks randomly — descriptions overlap
```

**Fix — clear, differentiated descriptions:**
```python
{"name": "search_web", "description": "Query live web pages... Do NOT use for documents already loaded."}
{"name": "search_documents", "description": "Full-text search across pre-loaded corpus... Do NOT use to find new sources."}
```

### Part 3: System Prompt Interaction

System prompt wording can override well-written descriptions. If prompt says "search for X", Claude may call `search_web` even when `search_documents` is better.

### Key Exam Facts
1. `tool_choice: "auto"` = model decides. `"any"` = must call a tool. Forced = specific tool.
2. Descriptions are the PRIMARY selection mechanism: WHAT, WHEN, WHAT NOT, WHAT RETURNED.
3. Ambiguous descriptions cause misrouting. Fix by renaming + rewriting.
4. System prompts can override descriptions — review for keyword-sensitive instructions.

---

## Step 6: developer_productivity.py — Codebase Exploration

**What it teaches:** How to incrementally build understanding using Grep → Read → Grep → Read.

### Pattern 1: Incremental Exploration

```
WRONG: Read all 30 files hoping to find the refund flow.
RIGHT: Grep for entry point, follow the call chain.
```

```
Step 1: grep(pattern="def process_refund")  → src/billing/refunds.py:15
Step 2: read("src/billing/refunds.py")      → reveals validate_customer()
Step 3: grep(pattern="def validate_customer") → src/auth/customer_validator.py:8
Step 4: read("src/auth/customer_validator.py") → full flow understood
```

**Result: 2 files loaded, not 30.**

### Pattern 2: Multi-Phase Exploration

```
Phase 1: Discovery   → Glob (find files) + Grep (find entry point)
Phase 2: Understanding → Read key files + trace dependencies
Phase 3: Action       → Write new code
Phase 4: Fix          → Edit existing code
```

### Key Exam Facts
1. Start with Grep to find entry points — don't read files blindly.
2. Follow the call chain: Grep → Read → Grep → Read.
3. Glob = file discovery (name patterns). Grep = content search (code patterns).
4. For larger tasks: Discovery → Understanding → Action → Fix.

---

## Step 7: dynamic_decomposition.py — Adaptive Decomposition

**What it teaches:** When subtasks should be generated dynamically based on discoveries.

### Fixed vs Dynamic Decomposition

| Approach | When to use | Example |
|---|---|---|
| Fixed (prompt chaining) | Predictable multi-step tasks | Code review: per-file → cross-file → summary |
| Dynamic (adaptive) | Open-ended investigation | Incident response: findings determine next step |

### Dynamic Decomposition Pattern

```python
system = """
You are investigating a production incident.
Start with error logs. Based on what you find,
decide your next investigation step.
Generate subtasks dynamically — next steps depend on findings.
"""
```

**Sequence emerges from work — NOT predictable upfront:**
```
Turn 1: read_logs     → finds DB timeout errors
Turn 2: query_db      → finds unindexed query
Turn 3: check_config  → confirms missing index
Turn 4: end_turn      → root cause + remediation
```

### Key Exam Facts
1. Fixed decomposition = predictable tasks. Dynamic = open-ended investigation.
2. Dynamic: model generates subtasks based on intermediate findings.
3. Fixed: prompt chaining with predetermined steps.
4. Use dynamic when you can't predict the investigation path upfront.

---

## Step 8: multi_agents.py — Coordinator Pattern

**What it teaches:** How a coordinator delegates to subagents via the Task tool.

### Coordinator Configuration

```python
coordinator_config = {
    "tools": [{"type": "task", "name": "Task"}],
    "allowedTools": ["Task", "compile_report"]  # MUST include "Task"
}
```

### Task Tool (AgentDefinition)

```python
{
    "type": "tool_use",
    "name": "Task",
    "input": {
        "description": "Web Search Specialist",
        "prompt": "Research goal: Find papers on...",
        "allowed_tools": ["web_search", "read_url"],  # NO Task here
        "model": "claude-haiku-4-5"
    }
}
```

### Parallel Spawning (EXAM FAVORITE)

```python
# ALL THREE in same content array = PARALLEL execution
"content": [
    {"type": "tool_use", "name": "Task", "input": {"description": "Env Researcher", ...}},
    {"type": "tool_use", "name": "Task", "input": {"description": "Econ Researcher", ...}},
    {"type": "tool_use", "name": "Task", "input": {"description": "Policy Analyst", ...}},
]
# Separate turns = sequential ANTI-PATTERN
```

### Key Exam Facts
1. Coordinator uses Task tool to spawn subagents.
2. `allowedTools` MUST include `"Task"` for coordinator.
3. Subagent gets NO Task tool — scoped to its role.
4. Multiple Task calls in one response = parallel. Separate turns = sequential.

---

## Step 9: subagent_context.py — Context Passing

**What it teaches:** Why context must be explicitly passed + how to preserve claim-source mappings.

### Problem: Critical Data Gets Summarized Away

```
$149.99 → "approximately $150" → "a refund"
day 29 of 30 → "recently" → "some time ago"
```

### Solution: CASE_FACTS Pattern

```python
CASE_FACTS = {
    "refund_amount": 149.99,      # exact — never summarize
    "days_since_order": 29,        # CRITICAL: day 29 of 30
    "customer_request": "full_refund",
}
# Injected fresh each turn — survives summarization
```

### Structured Findings (Not Prose)

```python
# WRONG: "The first agent found that subagents don't inherit context."
# RIGHT:
{
    "finding": "Subagents do not inherit coordinator conversation history.",
    "source_url": "https://docs.anthropic.com/...",
    "retrieved_at": "2025-03-15T09:12:00Z",
    "confidence": "high"
}
```

### Claim-Source Mappings

```python
{
    "claims": [{"claim_id": "c001", "text": "...", "source_id": "src_001"}],
    "sources": [{"source_id": "src_001", "url": "...", "retrieved_at": "..."}],
    "conflicts": []  # annotate conflicts, don't select one
}
```

### Key Exam Facts
1. Subagents do NOT inherit parent context. Always pass explicitly.
2. CASE_FACTS persists critical data outside summarization.
3. Pass structured objects, not prose summaries.
4. Preserve claim-source mappings through synthesis.
5. Annotate conflicts with attribution — don't arbitrarily select one.

---

## Step 10: fork_session.py — Session Management

**What it teaches:** When to fork vs. resume vs. start fresh.

### Fork Session — Parallel Exploration

```python
fork_a = client.beta.sessions.fork(
    session_id=baseline_session_id,
    system_prompt_addition="Explore approach A: service layer pattern."
)
fork_b = client.beta.sessions.fork(
    session_id=baseline_session_id,
    system_prompt_addition="Explore approach B: CQRS pattern."
)
# Both get same baseline, explore independently, don't contaminate each other
```

### Resume vs. Start Fresh

| Scenario | Use |
|---|---|
| Prior context still valid, no code changes | `--resume` with session name |
| Code has changed, stale tool results | Start fresh + inject summary |

### Start Fresh with Summary

```python
prior_findings_summary = """
PRIOR ANALYSIS SUMMARY (from 2025-03-13):
- Architecture: monolith, Django 4.2
- Key coupling: auth and billing share User model
NOTE: Codebase has changed since. Treat as hypotheses to validate.
"""
# Inject into fresh session — not resumed stale session
```

### Key Exam Facts
1. `fork_session` = independent branches from shared baseline.
2. Starting fresh with injected summary > resuming with stale results.
3. When resuming, inform agent about specific file changes.
4. Use `--resume` with session names for named investigations.

---

## Step 11: prompt_chaining — Sequential Chaining

**What it teaches:** Fixed sequential pipelines for predictable multi-step tasks.

### The Pattern

```
Step 1: Per-file review → focused scope per changed file
Step 2: Cross-file integration → look at how changes interact
Step 3: Final summary → severity-ranked report
```

```python
# Step 1: Per-file review
for file in changed_files:
    review = claude(prompt=f"Review {file}", context=read_file(file))
    file_reviews.append(review)

# Step 2: Cross-file integration (output of Step 1 as input)
integration_issues = claude(
    prompt="Identify cross-cutting concerns",
    context="\n".join(file_reviews)
)

# Step 3: Final summary (output of Step 2 as input)
final_report = claude(
    prompt="Generate PR review summary, rank by severity",
    context=integration_issues
)
```

### Fixed vs Dynamic (Review from Step 7)

| Fixed (this file) | Dynamic (Step 7) |
|---|---|
| Predictable steps | Findings determine next step |
| Code review: per-file → cross-file → summary | Incident response: logs → query → config → root cause |
| Each step's input is previous step's output | Each step's input depends on discoveries |

### Key Exam Facts
1. Fixed chains: each step's output feeds next step's input.
2. Use for predictable multi-aspect tasks (code review, document processing).
3. Avoids attention dilution by splitting large tasks into focused passes.
4. Different from dynamic decomposition (which adapts based on findings).

---

## Step 12: few_shot_examples.py — Few-Shot Prompting

**What it teaches:** How examples improve output consistency and reduce false positives.

### Pattern 1: Classification Examples

```python
EXAMPLE 1 — CRITICAL:
Code:      if not verify_token(token): pass
Reasoning: Auth check silently bypassed. Direct security control failure.
Severity:  CRITICAL

EXAMPLE 2 — HIGH:
Code:      user_data = json.loads(request.body)  # no try/except
Reasoning: Malformed JSON causes unhandled exception. Availability impact.
Severity:  HIGH

EXAMPLE 3 — MEDIUM:
Code:      log.debug(f"Processing user {user_id}")
Reasoning: Debug logging in production — minor perf impact.
Severity:  MEDIUM
```

**Each example shows: Input → Reasoning → Output**

### Pattern 2: Ambiguous Case Handling

```python
EXAMPLE 1 — Structured table:
Document: | Amount | USD 45,000 | Start Date | March 1, 2025 |
Reasoning: Explicit table — values directly stated, no inference.
Output: contract_value: EXTRACTED | USD 45,000

EXAMPLE 2 — Prose paragraph:
Document: "total engagement fee of forty-five thousand dollars..."
Reasoning: Stated in prose — EXTRACTED. Date says "anticipated" — INFERRED.
Output: effective_date: INFERRED | Q1 2025 (projected)
```

### When to Use Few-Shot

| Situation | Use few-shot? |
|---|---|
| Detailed instructions produce inconsistent output | Yes |
| Ambiguous cases need reasoning chains | Yes |
| Need to reduce false positives | Yes |
| Simple, well-defined task | No — instructions sufficient |

### Key Exam Facts
1. Few-shot = MOST EFFECTIVE technique for consistent output.
2. Include 2-4 examples with Input → Reasoning → Output.
3. Show reasoning for ambiguous cases — model generalizes judgment.
4. Include SKIP examples alongside REPORT examples to reduce false positives.

---

## Step 13: ci_pipeline.sh — CI/CD Integration

**What it teaches:** How to run Claude Code in CI/CD pipelines for automated code review.

### The Pipeline

```yaml
steps:
  1. Load prior review findings (dedup)
  2. Run Claude review (-p flag, structured output)
  3. Block merge on critical findings
```

### Key CLI Flags

| Flag | Purpose |
|---|---|
| `-p` / `--print` | Non-interactive mode (no hanging on input) |
| `--output-format json` | Machine-parseable output |
| `--json-schema` | Enforce structured output schema |

### Dedup Pattern

```bash
# Load prior findings
PRIOR=$(cat prior_findings.txt)

# Include in prompt — Claude skips already-reported issues
claude -p "Review the PR. Existing issues (skip): ${PRIOR}" \
  --output-format json > findings.json
```

### Block Merge on Critical

```bash
CRITICAL=$(jq '.findings | map(select(.severity=="critical")) | length' findings.json)
[ "$CRITICAL" -eq 0 ] || exit 1  # fail if critical findings exist
```

### Key Exam Facts
1. `-p` flag = non-interactive mode for CI (prevents input hangs).
2. `--output-format json` + `--json-schema` = structured output.
3. Include prior findings to avoid duplicate comments.
4. CLAUDE.md loaded automatically — provides project context.
5. Fresh session each run — don't review own changes (self-review limitation).

---

## Step 14: capstone_project.py — Multi-Agent Combo

**What it teaches:** Everything combined — loop, coordinator, hooks, escalation.

This is the **integration file**. It connects Steps 1-13 into one working system.

### What's Covered

| Concept | From Step | In This File |
|---|---|---|
| Agentic loop | Step 2 | `run_agentic_loop()` |
| Tool definitions | Step 5 | `TOOLS` array with 4 tools |
| Error categories | Step 2 | `handle_tool_call()` with T-P-V-I |
| Coordinator pattern | Step 8 | `coordinator()` decomposes + delegates |
| Context passing | Step 9 | Structured findings passed between subagents |
| Few-shot prompting | Step 12 | System prompt with resolve/escalate examples |
| PreToolUse hooks | NEW | `prerequisite_gate()`, `enforce_refund_policy()` |
| PostToolUse hooks | NEW | `normalize_order_result()`, `update_verification_state()` |
| Escalation | NEW | `escalate_to_human()` tool |

### PreToolUse Hooks (NEW — not in earlier steps)

```python
def prerequisite_gate(tool_name, tool_params):
    """Block refund/lookup until customer verified."""
    if tool_name in ("process_refund", "lookup_order"):
        if not session["customer_verified"]:
            return {"allowed": False, "reason": "Call get_customer first."}
    return {"allowed": True}

def enforce_refund_policy(tool_name, tool_params):
    """Block refunds above $500 agent limit."""
    if tool_name == "process_refund" and tool_params.get("amount", 0) > 500:
        return {"allowed": False, "reason": "Exceeds $500 limit.", "action_required": "escalate_to_human"}
    return {"allowed": True}
```

**Order matters: prerequisite gate BEFORE business rule check.**

### PostToolUse Hooks (NEW — not in earlier steps)

```python
def normalize_order_result(tool_name, raw_result):
    """Convert raw DB fields to readable format."""
    # status code → string, Unix ts → date, cents → dollars
    # Runs AFTER tool returns, BEFORE model sees result

def update_verification_state(tool_name, raw_result):
    """Flip session flag when get_customer succeeds."""
    # Must be PostToolUse — only know success after tool runs
```

### Escalation Triggers

| Trigger | Action |
|---|---|
| Customer explicitly asks for human | Escalate immediately |
| Refund exceeds $500 limit | Hook blocks → escalate |
| Verification fails | Return error, don't escalate |
| Repeated failures | Escalate with context |

### Key Exam Facts
1. PreToolUse hooks = policy gates BEFORE tool execution.
2. PostToolUse hooks = data normalization AFTER tool execution.
3. Hook order matters: prerequisites before business rules.
4. Escalate immediately when customer explicitly requests human.
5. This file combines ALL concepts from Steps 1-13.

---

## CONGRATULATIONS — All 14 Steps Complete!

### Quick Reference Card

| Step | File | One-Liner |
|---|---|---|
| 1 | api_check.py | SDK connects via env var |
| 2 | agent.py | Loop: end_turn exit, tool_use continue, 4 error categories |
| 3 | research_summarizer.py | 2-tool pattern: search → fetch |
| 4 | inbuilt_tools.py | Grep=content, Glob=paths, Edit fallback=Read+Write |
| 5 | tool_choice.py | auto/any/forced. Descriptions: WHAT/WHEN/NOT/RETURNED |
| 6 | developer_productivity.py | Grep→Read→Grep→Read. Phases: Discover→Understand→Act |
| 7 | dynamic_decomposition.py | Fixed=predictable. Dynamic=findings determine next step |
| 8 | multi_agents.py | Task tool spawns subagents. Multiple calls=parallel |
| 9 | subagent_context.py | CASE_FACTS. Structured objects. Claim-source mappings |
| 10 | fork_session.py | Fork=branches. Fresh+summary > stale resume |
| 11 | prompt_chaining | Sequential: output of step N = input of step N+1 |
| 12 | few_shot_examples.py | 2-4 examples. Input→Reasoning→Output. Ambiguous cases |
| 13 | ci_pipeline.sh | -p flag, --output-format json, dedup prior findings |
| 14 | capstone_project.py | Everything: loop+coordinator+hooks+escalation |
| — | mcp_integration.py | Host⊃Client↔Server, .mcp.json vs ~/.claude.json, ${VAR}, resources |

---

## APPENDIX: Official-Guide Alignment (Exam Guide v1.0)

Condensed from claudecertificationguide.com quick-reference sheets.
These are the exact wordings and distinctions the exam keys on.

### Corrections to older notes

1. Error categories are `transient | validation | business | permission`
   — NOT `internal`. Only `transient` is retryable.
2. There is NO `@import` keyword — modular CLAUDE.md uses `@` + path.
3. The bulk API is called **Batch API** on the exam (50% cheaper, up to 24h).
4. Prompt chaining is keyed as Domain 1 (TS 1.6, fixed vs dynamic), not Domain 4.

### Domain 1 extras (27%)

- Exam `stop_reason` values: `end_turn` (done) + `tool_use` (continue).
  Production adds `pause_turn`, `max_tokens`, `stop_sequence`, `refusal`,
  `model_context_window_exceeded` — handle them in real loops.
- Five orchestration patterns: Sequential, Parallel, Pipeline,
  Dynamic Adaptive, Hub-and-Spoke (coordinator + specialists).
- AgentDefinition = description + system prompt + `tools` field (small,
  role-focused: 4–5, not 18). Coordinator needs `"Task"` (aka `"Agent"`)
  in `allowedTools` or it cannot spawn subagents. No shared memory, ever.
- Structured handoff: Customer ID → factual Summary → Root cause →
  Recommended action. Never silently fail.
- PreToolUse returns `permissionDecision` (allow/deny/ask/defer) +
  optional `updatedInput`. PostToolUse returns `updatedToolOutput`.
  PostToolUse can NEVER block — the tool already ran.
- PreCompact (matchers `manual`/`auto`) archives transcripts before
  compaction; exit code 2 blocks it.
- Decision rule: "must always / guaranteed / compliance / audit" → hooks.
  Prompts are probabilistic, hooks deterministic.

### Domain 2 extras (18%)

- Misselection diagnosis: small lookalike set → sharpen descriptions (2.1);
  different jobs → split by role (2.3); one-job variants → consolidate
  into one parameterised tool (2.3). Few-shot is NOT a sanctioned fix.
- MCP: Host ⊃ Client ↔ Server, JSON-RPC 2.0 over stdio/streamable HTTP.
  All tools discovered at connect; servers never talk directly.
- `.mcp.json` (project, committed) vs `~/.claude.json` (personal).
  Remote entry needs `"type": "http"` + url; local needs command + args.
- `${VAR}` for secrets, `${VAR:-default}` for paths with fallback.
- Community MCP servers first — custom builds only for team-specific needs.
- `tool_choice`: `auto` (default, may answer text), `any` (must call ≥1,
  model picks), `tool` forced (one specific schema every time).

### Domain 3 extras (20%)

- CLAUDE.md files are CONCATENATED, not overridden. Load order broadest →
  most specific, but contradictions resolve arbitrarily. "Specific wins" is
  always a distractor. Must-hold rules → `settings.json` or hooks.
- `settings.json` strict chain: managed policy > local > project > user.
- `.claude/rules/` with `paths:` frontmatter loads conditionally (glob).
  Without frontmatter it loads at launch like project CLAUDE.md.
- Exam answer for "which files loaded": `/memory`. At your keyboard also
  check `/context` → Memory files. Neither command LOADS anything.
- Project CLAUDE.md is re-read after `/compact`; nested CLAUDE.md files
  and path-scoped rules return on next matching read.
- Skills = directory + SKILL.md (+ frontmatter, auto-invoke).
  Commands = flat `.md` in `.claude/commands/` (+ `$ARGUMENTS`).
- CLI: `-p` non-interactive; `--output-format json` + `--json-schema`
  (lands in `structured_output`); `--bare` skips hooks/skills/MCP/memory;
  `-c`/`-r` resume; `--max-turns`; `--append-system-prompt` keeps defaults,
  `--system-prompt` replaces them.
- Never review code in the session that wrote it (reasoning bias).

### Domain 4 extras (20%)

- Nullable fields: `{"type": ["string", "null"]}` + omit from parent's
  `required` array. `nullable: true` is OpenAPI, NOT JSON Schema.
  Required-on-missing-data CAUSES fabrication.
- Tool-use schemas kill SYNTAX errors, never SEMANTIC ones
  (wrong field, rows not summing). Pydantic: parsing enforces schema,
  custom validators enforce semantics; feed `ValidationError` into retry.
- Retry-with-error-feedback = original prompt + failed output + specific
  error. Never bare "try again". >2 failures → escalate.
- Few-shot: 2–4 with Input → Reasoning → Output; system prompt placement
  earns prompt-caching; 0→2 matters most.
- Batch API: throughput/cost, NOT speed. Never real-time/user-facing.
  `custom_id` correlates batch responses.
- System prompt structure: role → rules → output format → calibration
  examples. One prompt shapes every request (most cost-effective control).

### Domain 5 extras (15%)

- Progressive summarisation LOSES details — use persistent fact blocks
  copied verbatim, not re-summarised.
- Scratchpad files = external persistence surviving any context reset.
- The API is stateless: every request carries its full history (why the
  window fills). "Lost in the middle": edges beat middles — put critical
  content at beginning/end.
- Error context needs: failure type + what was attempted + partial results
  + POTENTIAL alternatives (not a retry log).
- Three escalation triggers: explicit human request, policy gap/exception,
  no meaningful progress. Unreliable: sentiment, self-reported confidence
  (but per-category classifier scores ARE valid triggers).
- Policy GAP (silent) → escalate. Policy VIOLATION (forbids) → refuse
  with the policy explanation. Multiple matches → ask for identifiers.
- Stratified validation: aggregate 95% hides per-type 60%. Monitor
  per-type rates; conflicting sources get annotated with provenance +
  dates, never averaged or silently picked.

### Master decision table (all domains)

| Question says... | Answer |
|---|---|
| guaranteed / must always / enforce / compliance | Hooks, not prompts |
| flexibility / adapt / unexpected | Model-driven decisions |
| independent subtasks | Parallel orchestration |
| needs previous output | Sequential / chaining |
| unknown structure | Dynamic adaptive |
| runaway agent | Iteration cap as safety net only |
| share context between agents | Explicit passing, no shared memory |
| wrong tool, small toolkit | Sharpen descriptions |
| wrong tool, 20+ tools | Split by role / consolidate |
| guaranteed schema, one structure | Forced `tool_choice` |
| guaranteed schema, unknown doc type | `tool_choice: any` |
| fabricates missing data | Nullable union + drop required |
| validation failed | Original + failed + specific error |
| bulk cheap / latency-tolerant | Batch API |
| real-time / user-facing / blocking | Synchronous API, never Batch |
| review own output | Separate instance |
| details lost over time | Persistent fact blocks |
| survive context reset | Scratchpad files |
| high overall accuracy, user complaints | Stratified per-type validation |
| sources disagree | Annotate both + dates |
| team config | Project-level, version-controlled |
| personal config | User-level (`~`) |
| path-specific rules | `.claude/rules/` + `paths:` |
| CI / non-interactive | `-p` + `--output-format json` |
| keep defaults + extras | `--append-system-prompt` |

### Real-bank additions (Oct 2026 — from the live mock-exam bank)

12 topics the official bank tests that the steps above under-cover:

1. **fork_session branches (D1)** — parallel hypothesis explorations from one
   shared baseline; resume continues one line, compact leaks across hypotheses.
2. **Tiered confidence routing (D1)** — high-confidence violations actioned,
   high-confidence safe passed, uncertain → human. Self-reported confidence
   is invalid; per-category classifier scores are valid.
3. **Grep → Read sequence (D2)** — Grep locates content in unknown files,
   Read loads only matches. Glob matches paths, not content.
4. **Edit replace_all (D2)** — one op for uniform renames (12 occurrences);
   Read + Write is the fallback when no unique anchor exists, not plan A.
5. **Explore subagent (D3)** — thorough reference-tracing discovery across
   packages; 3-file skims miss key flows. Depth tool, not a longer summary.
6. **git worktree parallelism (D3)** — isolated dir + branch per instance;
   sequence shared-file edits (merge, then rebase). Isolation ≠ no conflicts.
7. **GitHub Action modes (D3)** — no prompt = interactive (waits for
   @claude/trigger_phrase); prompt = automation. Workflow permissions are
   NOT Claude tools — allowlist GitHub MCP tools for repo access.
8. **Keyword overlap (D4)** — instruction wording mirroring a tool name reads
   as prose guidance → text instead of tool call. Reword to demand the call.
9. **Inter-step validation (D4)** — validate each chain step's output before
   the next consumes it; stops cascades, enables single-step retry.
10. **Batch has no tool calling (D4)** — model → tool → model workflows must
    run synchronously. Batch failures: resubmit by custom_id only, chunked.
11. **Token-budget arithmetic (D5)** — system + history + tools + response
    share one budget (8k+120k+65k → ~7k left). Fix by trimming, not models.
12. **Silent suppression (D5)** — 403 masked as empty success is the worst
    propagation anti-pattern; coordinator believes a failed search returned
    zero hits. Propagate failures explicitly, always.
