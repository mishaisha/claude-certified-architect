# subagent_context.py
# ====================
# SINGLE TOPIC: Structured context passing between agents
#
# What you learn:
#   - Why context must be explicitly passed (subagents don't inherit it)
#   - How to pass structured findings (objects, not prose)
#   - How to preserve claim-source mappings through synthesis
#   - How to handle conflicting sources
#   - Why CASE_FACTS block prevents critical data from being summarized away
#
# Exam domain covered:
#   Domain 5 — Context Management & Reliability (Subdomains 5.1, 5.6)
#   Domain 1 — Agentic Architecture (Subdomain 1.3)

import json


# ══════════════════════════════════════════════════════════════════
# PART 1: The case facts pattern
# ══════════════════════════════════════════════════════════════════
#
# PROBLEM: In long conversations, models compress numerical values,
# dates, and customer expectations into vague summaries. A $149.99
# refund becomes "a refund" — and the agent loses track of critical
# details like "day 29 of 30-day policy window."
#
# SOLUTION: Extract transactional facts into a persistent CASE_FACTS
# block included in each prompt, OUTSIDE summarized history.

CASE_FACTS = {
    "customer_id":        "CUST-7823",
    "order_id":           "ORD-12345",   # needed to process the refund
    "item":               "Blue Wireless Headphones",
    "refund_amount":      149.99,         # exact — never summarize amounts
    "order_date":         "2026-05-03",
    "policy_window_days": 30,
    "days_since_order":   29,             # CRITICAL: day 29 of 30 — expiring soon
    "customer_request":   "full_refund",
    "verified":           True
}

# WHY THIS MATTERS:
# - refund_amount stays 149.99 (not "approximately $150")
# - days_since_order stays 29 (not "recently")
# - customer_request stays "full_refund" (not "wants their money back")
# These facts survive progressive summarization because they're injected
# fresh each turn, not compressed from prior turns.


# ══════════════════════════════════════════════════════════════════
# PART 2: Structured findings between subagents
# ══════════════════════════════════════════════════════════════════
#
# Subagents do NOT inherit the coordinator's conversation history.
# Context must be EXPLICITLY provided in the prompt.
# Pass structured objects, not prose summaries.

research_findings = [
    {
        "finding": "Claude's tool_use stop_reason requires the full assistant message to be appended before tool results.",
        "source_url": "https://docs.anthropic.com/agents/tool-use",
        "source_title": "Anthropic Tool Use Documentation",
        "page_number": None,
        "retrieved_at": "2025-03-15T09:12:00Z",
        "confidence": "high"
    },
    {
        "finding": "Using an iteration cap as a primary stop condition is an anti-pattern.",
        "source_url": "https://docs.anthropic.com/agents/loops",
        "source_title": "Agentic Loop Best Practices",
        "page_number": None,
        "retrieved_at": "2025-03-15T09:14:00Z",
        "confidence": "high"
    }
]


# ── Build the synthesis prompt with full context ─────────────────
# The downstream agent receives the COMPLETE findings object.
# Never extract just "claims" and drop "sources" — the next agent
# needs both to produce accurate output.

synthesis_prompt = f"""
You are a synthesis agent. Your task is to produce a structured research report.

FINDINGS TO SYNTHESIZE:
{json.dumps(research_findings, indent=2)}

Requirements:
- Every claim in the report MUST cite its source_url
- Preserve the retrieved_at date for temporal accuracy
- Flag any conflicting findings with both sources annotated
- Output format: JSON with keys: summary, claims[], conflicts[]
"""


# ── Pass to subagent via Task tool ──────────────────────────────
task_call = {
    "type": "tool_use",
    "name": "Task",
    "input": {
        "description": "Synthesize research findings into structured report",
        "prompt": synthesis_prompt
    }
}


# ══════════════════════════════════════════════════════════════════
# PART 3: Claim-source mappings
# ══════════════════════════════════════════════════════════════════
#
# Every synthesis step must output claim-source pairs.
# Source attribution is lost during summarization when findings are
# compressed without preserving claim-source mappings.

intermediate_output = {
    "claims": [
        {
            "claim_id": "c001",
            "text": "Subagents do not inherit coordinator conversation history.",
            "source_id": "src_001",       # links back to source object
            "confidence": "high"
        },
        {
            "claim_id": "c002",
            "text": "Parallel subagents require multiple Task calls in one coordinator response.",
            "source_id": "src_002",
            "confidence": "high"
        }
    ],
    "sources": [
        {
            "source_id": "src_001",
            "url": "https://docs.anthropic.com/multi-agent",
            "title": "Multi-Agent Architecture Guide",
            "retrieved_at": "2025-03-15T09:12:00Z"
        },
        {
            "source_id": "src_002",
            "url": "https://docs.anthropic.com/task-tool",
            "title": "Task Tool Reference",
            "retrieved_at": "2025-03-15T09:14:00Z"
        }
    ],
    "conflicts": []  # if two sources say different things, both go here
}

# KEY RULE: When passing to the next agent, pass the WHOLE object.
# Never extract just "claims" and drop "sources".
# The next agent needs both to produce accurate output.


# ══════════════════════════════════════════════════════════════════
# PART 4: Handling conflicting sources
# ══════════════════════════════════════════════════════════════════
#
# When two credible sources conflict:
# - Annotate with source attribution (don't arbitrarily select one)
# - Include publication dates (temporal differences ≠ contradictions)
# - Let the coordinator decide how to reconcile

conflict = {
    "conflict_id": "conf_001",
    "topic": "parallel subagent invocation",
    "claim_a": {
        "text": "Multiple Task calls in one response run in parallel.",
        "source_id": "src_002"
    },
    "claim_b": {
        "text": "Task calls are always sequential regardless of placement.",
        "source_id": "src_003"
    },
    "resolution": "unresolved"  # coordinator must decide
}


# ══════════════════════════════════════════════════════════════════
# KEY TAKEAWAYS
# ══════════════════════════════════════════════════════════════════
#
# 1. Subagents do NOT inherit parent context. Always pass findings
#    explicitly in the subagent's prompt.
#
# 2. Use CASE_FACTS to persist critical data outside summarization.
#    Amounts, dates, IDs, and customer requests must survive turns.
#
# 3. Pass structured objects (dicts), not prose summaries.
#    Include source URLs, dates, and confidence scores.
#
# 4. Preserve claim-source mappings through synthesis steps.
#    Never drop sources when passing findings downstream.
#
# 5. Handle conflicts by annotating with attribution, not by
#    arbitrarily selecting one value. Include publication dates
#    to distinguish temporal differences from true contradictions.
