# tool_choice.py
# ==============
# SINGLE TOPIC: Tool choice configuration + description design
#
# What you learn:
#   - How tool_choice controls which tool Claude calls
#   - How tool descriptions drive tool selection
#   - Common anti-pattern: ambiguous descriptions causing misrouting
#
# Exam domains covered:
#   Domain 2 — Tool Design & MCP Integration (Subdomains 2.1, 2.3)

# ══════════════════════════════════════════════════════════════════
# PART 1: tool_choice configuration
# ══════════════════════════════════════════════════════════════════

# "auto" — model decides whether to call a tool or return text
tool_choice_auto = {"type": "auto"}

# Forced tool — model MUST call the specified tool (useful when a
# specific tool must run first, e.g., extract metadata before enrichment)
tool_choice_forced = {"type": "tool", "name": "lookup_order"}

# "any" — model must call SOME tool but can choose which one
# Guarantees structured output (no conversational text returned)
tool_choice_any = {"type": "any"}


# ══════════════════════════════════════════════════════════════════
# PART 2: Tool descriptions — the primary selection mechanism
# ══════════════════════════════════════════════════════════════════
#
# LLMs decide which tool to call based primarily on the DESCRIPTION.
# A good description answers four questions:
#   1. WHAT does it do?
#   2. WHEN should I call it?
#   3. WHAT NOT to use it for?
#   4. WHAT does it return?


# ── ANTI-PATTERN: Ambiguous descriptions ─────────────────────────
# These three tools will confuse Claude constantly because their
# descriptions overlap. Claude picks whichever it hits first or
# alternates randomly between search_web and search_documents.

tools_bad = [
    {
        "name": "search_web",
        "description": "Search for information",
    },
    {
        "name": "search_documents",
        "description": "Search documents for information",
    },
    {
        "name": "analyze_content",
        "description": "Analyze and extract information from content",
    },
]


# ── FIX: Clear, differentiated descriptions ──────────────────────
# Each description now explains WHAT, WHEN, WHAT NOT, and WHAT RETURNED.
# Claude can reliably pick the right tool because boundaries are explicit.

tools_good = [
    {
        "name": "search_web",
        "description": (
            "Query live web pages via search engine. Use for current events, "
            "recent publications, URLs not yet in the document corpus. "
            "Input: query string. Returns ranked URLs + snippets. "
            "Do NOT use for documents already loaded into the research corpus."
        ),
    },
    {
        "name": "search_documents",
        "description": (
            "Full-text search across the pre-loaded research corpus (PDFs, "
            "reports, cached articles). Use ONLY for documents already ingested. "
            "Faster and more precise than web search for known sources. "
            "Input: query string + optional doc_id filter. "
            "Do NOT use to find new sources — use search_web for that."
        ),
    },
    {
        "name": "analyze_content",
        "description": (
            "Deep analysis of a specific piece of content already retrieved. "
            "Extracts key claims, identifies contradictions, assesses credibility. "
            "Input: content (string), analysis_type (claims|contradictions|summary). "
            "Use AFTER search_web or search_documents — not as a search tool itself."
        ),
    },
]


# ══════════════════════════════════════════════════════════════════
# PART 3: Tool descriptions in an agent system prompt
# ══════════════════════════════════════════════════════════════════
#
# System prompts can influence tool selection. Be careful:
# keyword-sensitive instructions create unintended tool associations.
# If the system prompt says "search for X", Claude may call search_web
# even when search_documents is more appropriate.

SYSTEM_PROMPT = (
    "You are a customer support assistant. "
    "Your goal is first-contact resolution of returns and refunds. "
    "Tool Use Sequence: "
    "1. Always call get_customer first. "
    "2. Call lookup_order to find the relevant orders."
)


# ══════════════════════════════════════════════════════════════════
# KEY TAKEAWAYS
# ══════════════════════════════════════════════════════════════════
#
# 1. tool_choice "auto" lets the model decide; "any" forces a tool call;
#    forced selection ensures a specific tool runs first.
#
# 2. Tool descriptions are the PRIMARY mechanism for tool selection.
#    Write them carefully: WHAT, WHEN, WHAT NOT, WHAT RETURNED.
#
# 3. Ambiguous/overlapping descriptions cause misrouting.
#    Fix: rename tools and rewrite descriptions to eliminate overlap.
#
# 4. System prompt wording can override well-written descriptions.
#    Review prompts for keyword-sensitive instructions that might
#    create unintended tool associations.
