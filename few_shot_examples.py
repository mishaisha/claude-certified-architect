# few_shot_examples.py
# =====================
# SINGLE TOPIC: Few-shot prompting for consistent output
#
# What you learn:
#   - How few-shot examples improve output consistency and quality
#   - How to handle ambiguous cases with reasoning chains
#   - How to reduce false positives with concrete examples
#   - The right number of examples (2-4 is usually enough)
#
# Exam domain covered:
#   Domain 4 — Prompt Engineering & Structured Output (Subdomain 4.2)
#   "Few-shot examples as the most effective technique for achieving
#    consistently formatted, actionable output."


# ══════════════════════════════════════════════════════════════════
# PATTERN: Few-shot classification
# ══════════════════════════════════════════════════════════════════
#
# Give 2-4 examples covering different severity levels and edge cases.
# Each example shows: Input → Reasoning → Output.
# The model learns to generalize from these examples to new inputs.

SYSTEM_PROMPT = """
You are a code reviewer for a CI/CD pipeline.

[REPORT] security vulnerabilities, runtime errors,
         authentication failures, data exposure
[SKIP]   style, naming, formatting, performance hints

Classify each reported issue as CRITICAL, HIGH, or MEDIUM
using the following examples:

EXAMPLE 1 — CRITICAL:
Code:      token = request.headers.get('X-API-Key')
           if not verify_token(token): pass  # TODO: add auth
Reasoning: Authentication check exists but is silently bypassed.
           Any request proceeds regardless of token validity.
           Direct security control failure.
Severity:  CRITICAL

EXAMPLE 2 — HIGH:
Code:      user_data = json.loads(request.body)
           # no try/except around json.loads
Reasoning: Malformed JSON causes unhandled exception. Service
           crashes for that request. No data exposure, but
           availability impact is real.
Severity:  HIGH

EXAMPLE 3 — MEDIUM:
Code:      log.debug(f"Processing user {user_id}")
Reasoning: Debug logging in production — adds noise, minor perf
           impact. Not a security risk. Should be addressed but
           won't cause failures.
Severity:  MEDIUM
"""


# ══════════════════════════════════════════════════════════════════
# PATTERN: Few-shot with ambiguous cases
# ══════════════════════════════════════════════════════════════════
#
# Few-shot examples are most valuable for AMBIGUOUS cases — where the
# model might hesitate or give inconsistent answers. Show reasoning
# for why one action was chosen over plausible alternatives.

EXTRACTION_PROMPT = """
Extract: contract_value, effective_date, payment_terms

EXAMPLE 1 — Structured table format:
Document: | Field      | Value           |
          | Amount     | USD 45,000      |
          | Start Date | March 1, 2025   |
          | Terms      | Net 30          |

Reasoning: Explicit table — values directly stated, no inference.
Output:
  contract_value:   EXTRACTED | USD 45,000
  effective_date:   EXTRACTED | March 1, 2025
  payment_terms:    EXTRACTED | Net 30

EXAMPLE 2 — Prose paragraph format:
Document: "The parties agree to a total engagement fee of forty-five
          thousand dollars, payable within thirty days of each
          milestone completion. The agreement takes effect upon
          final signature, anticipated in Q1 2025."

Reasoning: No explicit table. contract_value is stated in prose as
           'forty-five thousand dollars' — EXTRACTED. payment_terms
           is stated as 'within thirty days' — EXTRACTED. effective_date
           says 'upon final signature' — the Q1 2025 is a projection,
           not a confirmed date — INFERRED.
Output:
  contract_value:   EXTRACTED | USD 45,000
  effective_date:   INFERRED  | Q1 2025 (projected)
  payment_terms:    EXTRACTED | Net 30
"""


# ══════════════════════════════════════════════════════════════════
# KEY TAKEAWAYS
# ══════════════════════════════════════════════════════════════════
#
# 1. Few-shot examples are the MOST EFFECTIVE technique for consistent
#    output when detailed instructions alone produce inconsistent results.
#
# 2. Include 2-4 examples covering different severity levels and edge cases.
#    Each example should show: Input → Reasoning → Output.
#
# 3. Show reasoning for ambiguous cases — the model learns to generalize
#    judgment to novel patterns, not just match pre-specified cases.
#
# 4. Include examples that demonstrate acceptable code patterns (SKIP)
#    alongside genuine issues (REPORT) to reduce false positives.
#
# 5. For extraction tasks, include examples with varied document structures
#    (tables vs prose) to handle real-world input diversity.
