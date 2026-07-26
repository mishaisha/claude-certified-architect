# developer_productivity.py
# =========================
# SINGLE TOPIC: Codebase exploration patterns
#
# What you learn:
#   - How to incrementally build understanding using Grep → Read → Grep → Read
#   - Why reading only relevant files is better than reading everything upfront
#   - How to trace function usage across a codebase efficiently
#
# Exam domain covered:
#   Domain 2 — Tool Design & MCP Integration (Subdomain 2.5)
#   "Building codebase understanding incrementally: starting with Grep to
#    find entry points, then using Read to follow imports and trace flows,
#    rather than reading all files upfront."

# ══════════════════════════════════════════════════════════════════
# PATTERN: Incremental codebase exploration
# ══════════════════════════════════════════════════════════════════
#
# WRONG: Read all 30 Python files hoping to find the refund flow.
# RIGHT: Grep for the entry point, then follow the call chain.

# ── Step 1: Find the entry point ────────────────────────────────
# Grep searches content — perfect for finding function definitions.
grep(pattern="def process_refund", path="./src")
# → Found: src/billing/refunds.py:15

# ── Step 2: Read only that file ─────────────────────────────────
# Read loads the full file into context — targeted, not wasteful.
read(file_path="src/billing/refunds.py")
# → Reveals it calls validate_customer() from auth module

# ── Step 3: Trace the dependency ────────────────────────────────
# Grep again to find the next function in the call chain.
grep(pattern="def validate_customer", path="./src")
# → Found: src/auth/customer_validator.py:8

# ── Step 4: Read only what you need ─────────────────────────────
read(file_path="src/auth/customer_validator.py")
# → Now we understand the full flow: refund → validate → auth

# ── Result ──────────────────────────────────────────────────────
# Total files loaded: 2 (not 30)
# Context window: efficient
# Understanding: deep and targeted


# ══════════════════════════════════════════════════════════════════
# PATTERN: Multi-phase exploration
# ══════════════════════════════════════════════════════════════════
#
# For larger tasks, split exploration into phases:
#   Phase 1 — Discovery: What files exist?
#   Phase 2 — Understanding: Read the key files
#   Phase 3 — Action: Generate or modify code

# ── Phase 1: Discovery ──────────────────────────────────────────
# Glob finds files by name pattern — perfect for discovering structure.
glob(pattern="src/orders/**/*.py")
# → returns list of 12 files

# Grep narrows down to the specific entry point.
grep(pattern="class OrderProcessor", path="./src/orders")
# → src/orders/processor.py:1

# ── Phase 2: Understanding ──────────────────────────────────────
read(file_path="src/orders/processor.py")
# → Shows it uses STATUS_CODES dict, calls notify_customer()

# Trace the dependency
grep(pattern="STATUS_CODES", path="./src/orders")
# → src/orders/constants.py:5

read(file_path="src/orders/constants.py")
# → Reveals legacy numeric status codes (1,2,3) not descriptive strings

# ── Phase 3: Action ─────────────────────────────────────────────
# Now that we understand the structure, we can generate or modify code.
write(
    file_path="src/orders/routes/order_status.py",
    content="""
from src.orders.constants import STATUS_CODES
from src.orders.processor import OrderProcessor

class OrderStatusEndpoint:
    # Generated endpoint using discovered constants and patterns
    ...
"""
)

# ── Phase 4: Fix ────────────────────────────────────────────────
# Targeted edit using unique anchor text from what we read.
edit(
    file_path="src/orders/constants.py",
    old_string="STATUS_CODES = {1: 'pending', 2: 'processing', 3: 'complete'}",
    new_string="STATUS_CODES = {1: 'pending', 2: 'processing', 3: 'complete', 'PENDING': 1, 'PROCESSING': 2, 'COMPLETE': 3}"
)


# ══════════════════════════════════════════════════════════════════
# KEY TAKEAWAYS
# ══════════════════════════════════════════════════════════════════
#
# 1. Start with Grep to find entry points — don't read files blindly.
#
# 2. Follow the call chain: Grep → Read → Grep → Read.
#    Each step loads only what's needed.
#
# 3. Glob is for file discovery (finding files by name).
#    Grep is for content search (finding code patterns).
#
# 4. For larger tasks, split into phases:
#    Discovery → Understanding → Action → Fix
#
# 5. This approach is exam-critical: it demonstrates efficient use
#    of built-in tools for codebase navigation.
