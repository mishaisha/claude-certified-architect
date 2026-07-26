import anthropic

client = anthropic.Anthropic()

# fork_session.py
# ===============
# SINGLE TOPIC: Session fork and resume patterns
#
# What you learn:
#   - When to fork a session (explore divergent approaches from shared baseline)
#   - When to resume vs. start fresh with injected summary
#   - Why resuming with stale tool results is an anti-pattern
#
# Exam domain covered:
#   Domain 1 — Agentic Architecture & Orchestration (Subdomain 1.7)
#   "Manage session state, resumption, and forking"


# ══════════════════════════════════════════════════════════════════
# PART 1: Fork session — parallel exploration
# ══════════════════════════════════════════════════════════════════
#
# Use case: You have a baseline codebase analysis. You want to explore
# two different refactoring approaches WITHOUT one contaminating the other.
#
# fork_session creates independent branches from a shared analysis baseline.
# Each fork gets the same starting context but explores independently.

baseline_session_id = "baseline-arch-analysis-001"

# Fork A: explore service layer pattern
fork_a = client.beta.sessions.fork(
    session_id=baseline_session_id,
    system_prompt_addition="Explore refactoring approach A: extract service layer pattern."
)

# Fork B: explore CQRS pattern
fork_b = client.beta.sessions.fork(
    session_id=baseline_session_id,
    system_prompt_addition="Explore refactoring approach B: CQRS pattern."
)

# Both forks run independently:
# - fork_a gets the baseline context + explores service layer
# - fork_b gets the baseline context + explores CQRS
# - Neither contaminates the other
# - Results can be compared side-by-side


# ══════════════════════════════════════════════════════════════════
# PART 2: Resume vs. start fresh
# ══════════════════════════════════════════════════════════════════
#
# PROBLEM: After code changes, a resumed session may contain stale
# tool results. The model references outdated findings as if they
# are current facts.
#
# SOLUTION: Start a new session with a structured summary of prior
# findings, explicitly noting what has changed.

prior_findings_summary = """
PRIOR ANALYSIS SUMMARY (from 2025-03-13):
- Architecture: monolith, Django 4.2, PostgreSQL 14
- Key coupling points: auth and billing share the User model directly
- Identified debt: payment_service.py has 3 untested code paths
- Recommended next steps: extract billing into separate bounded context

NOTE: This summary is from 2 days ago. The codebase has since been updated.
Please treat these as hypotheses to validate, not established facts.
Re-explore the current file structure before acting on these findings.
"""

# Start a fresh session and inject the summary
messages = [
    {
        "role": "user",
        "content": prior_findings_summary + "\n\nNow please begin fresh analysis of the current codebase state."
    }
]


# ══════════════════════════════════════════════════════════════════
# PART 3: When to resume vs. start fresh
# ══════════════════════════════════════════════════════════════════
#
# USE --resume WHEN:
#   - Prior context is mostly still valid
#   - No significant code changes since last session
#   - You need to continue a multi-session investigation
#
# START FRESH WHEN:
#   - Prior tool results are stale (code has changed)
#   - Session context contains outdated information
#   - You want clean separation between analysis phases
#
# ALWAYS:
#   - Inform the agent about specific file changes
#   - Use --resume with session names for named investigations
#   - Include changes since last session in the resume prompt


# ══════════════════════════════════════════════════════════════════
# KEY TAKEAWAYS
# ══════════════════════════════════════════════════════════════════
#
# 1. fork_session creates independent branches from a shared baseline.
#    Use it to compare approaches (e.g., service layer vs. CQRS).
#
# 2. Starting fresh with an injected summary is more reliable than
#    resuming with stale tool results.
#
# 3. When resuming, inform the agent about specific file changes
#    for targeted re-analysis rather than full re-exploration.
#
# 4. Use --resume with session names to continue named investigations
#    across work sessions.
