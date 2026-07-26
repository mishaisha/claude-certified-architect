# Claude Certified Architect — Course Project

Demo code for the **Claude Certified Architect** course (Episodes 01–05). Most files are teaching artifacts, not a production app: some are runnable scripts, others are illustrative snippets that won't execute as-is.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

The SDK reads `ANTHROPIC_API_KEY` from the environment — never hardcode keys.

## Learning Sequence

Each file covers ONE topic. Study in this order — concepts build on each other.

### Domain 1: Agentic Architecture & Orchestration

| # | File | Topic | What You Learn |
|---|------|-------|----------------|
| 01 | `api_check.py` | API setup | Smoke test that the API key works |
| 02 | `agent.py` | Agentic loop | The core loop: stop_reason, tool_use, messages array |
| 03 | `research_summarizer.py` | Full single-agent | Complete runnable agent with tools and error handling |

### Domain 2: Tool Design & MCP Integration

| # | File | Topic | What You Learn |
|---|------|-------|----------------|
| 04 | `inbuilt_tools.py` | Built-in tools | Grep, Glob, Read, Write, Edit + fallback pattern |
| 05 | `tool_choice.py` | Tool choice + descriptions | tool_choice config, description design, misrouting prevention |
| 06 | `developer_productivity.py` | Codebase exploration | Grep → Read → Grep → Read incremental discovery |

### Domain 5: Context Management & Reliability

| # | File | Topic | What You Learn |
|---|------|-------|----------------|
| 07 | `dynamic_decomposition.py` | Dynamic decomposition | Adaptive subtask generation based on discoveries |
| 08 | `multi_agents.py` | Coordinator pattern | Task tool, parallel subagent spawning, agent definitions |
| 09 | `subagent_context.py` | Context passing | Structured findings, claim-source mappings, CASE_FACTS pattern |
| 10 | `fork_session.py` | Session management | fork_session, resume vs. start fresh, stale context handling |

### Domain 4: Prompt Engineering & Structured Output

| # | File | Topic | What You Learn |
|---|------|-------|----------------|
| 11 | `prompt_chaining` | Sequential chaining | Per-file review → cross-file integration → final report |
| 12 | `few_shot_examples.py` | Few-shot prompting | Consistent classification, ambiguous case handling |

### Domain 3: Claude Code Configuration & Workflows

| # | File | Topic | What You Learn |
|---|------|-------|----------------|
| 13 | `ci_pipeline.sh` | CI/CD integration | Claude Code in CI with -p flag, structured output, dedup |

### Integration

| # | File | Topic | What You Learn |
|---|------|-------|----------------|
| 14 | `capstone_project.py` | Multi-agent combo | Combines Ep 01-03: loop, coordinator, hooks, escalation |

## File map

**Runnable scripts** (have `if __name__ == "__main__"` or top-level calls):
- `api_check.py` — smoke test that the API key works
- `agent.py` — the canonical single-agent loop with structured error categories (Ep 01)
- `research_summarizer.py` — complete single-agent with search/fetch tools
- `capstone_project.py` — multi-agent demo connecting Ep 01–05
- `fork_session.py` — `client.beta.sessions.fork` example
- `ci_pipeline.sh` — GitHub Actions workflow for Claude Code in CI

**Illustrative snippets** (don't run standalone — embedded code samples for teaching):
- `inbuilt_tools.py` — Grep, Glob, Read, Write, Edit patterns
- `tool_choice.py` — tool_choice config + description design
- `developer_productivity.py` — codebase exploration patterns
- `dynamic_decomposition.py` — adaptive decomposition
- `multi_agents.py` — coordinator pattern with Task tool
- `subagent_context.py` — structured context passing
- `prompt_chaining` — sequential chaining (no `.py` extension on purpose)
- `few_shot_examples.py` — few-shot prompting

When editing snippet files, preserve their pedagogical shape — comments and ordering matter more than executability.

## Conventions

1. **Model pinning**: all examples use `claude-haiku-4-5` deliberately (cost + speed for learners). Don't bump to Sonnet/Opus without asking.
2. **Error categories**: tool errors must use the four-category schema from `agent.py` — `transient`, `permission`, `validation`, `internal`. New tools should follow the same pattern.
3. **Agentic loop exit**: `stop_reason == "end_turn"` is the only valid primary exit. `MAX_ITERATIONS` is a safety valve, not a stop condition.
4. **No real secrets**: mock data only (see `FAKE_DB`, `FAKE_ORDERS` in `capstone_project.py`).

## Reference

Deeper SDK guide (single-agent loop, inbuilt tools, coordinator pattern): `docs/agent-guide.md`.
