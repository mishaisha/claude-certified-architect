# CCAR-F Practice Exam — 60 Questions, all 5 domains
# Run: python practice_exam.py
# Aligned to the official Exam Guide v1.0 (July 2026) via claudecertificationguide.com.
# Domain weights: D1 27% | D2 18% | D3 20% | D4 20% | D5 15% (approx).

import random
import time
from typing import List, Dict, Tuple

DOMAINS = {
    1: "Agentic Architecture & Orchestration",
    2: "Tool Design & MCP Integration",
    3: "Claude Code Configuration & Workflows",
    4: "Prompt Engineering & Structured Output",
    5: "Context Management & Reliability",
}

# Official exam weights (Exam Guide v1.0) — shown in results for comparison.
WEIGHTS = {1: 27, 2: 18, 3: 20, 4: 20, 5: 15}

QUESTIONS: List[Dict] = [
    # ═══════════════════════════════════════════════
    # DOMAIN 1: Agentic Architecture & Orchestration
    # ═══════════════════════════════════════════════
    {
        "domain": 1,
        "scenario": "A developer implements an agentic loop. The loop runs for 10 iterations, then returns whatever Claude last said. Some queries return incomplete results because Claude was mid-analysis.",
        "question": "What is the primary problem with this implementation?",
        "options": [
            "A. MAX_ITERATIONS should be higher",
            "B. The loop should exit on stop_reason == 'end_turn', using MAX_ITERATIONS only as a safety valve",
            "C. The developer should check for text content in the response",
            "D. The loop should always run at least 20 iterations",
        ],
        "answer": "B",
        "explanation": "stop_reason == 'end_turn' is the only valid primary exit. MAX_ITERATIONS is a safety valve, not a stop condition. Checking text content or setting arbitrary caps are anti-patterns.",
    },
    {
        "domain": 1,
        "scenario": "An agent calls a database tool and gets a TimeoutError because the database is under heavy load.",
        "question": "Which error category should the tool return?",
        "options": [
            "A. permission \u2014 access may be restricted during high load",
            "B. validation \u2014 the query parameters were probably wrong",
            "C. transient \u2014 infrastructure hiccup, retryable after a delay",
            "D. business \u2014 policy violation, take an alternative path",
        ],
        "answer": "C",
        "explanation": "Timeouts are transient errors \u2014 infrastructure issues that may resolve on retry (isRetryable True, resend as-is). The four exam categories are transient | validation | business | permission; only transient is retryable.",
    },
    {
        "domain": 1,
        "question": "In a coordinator-subagent pattern, how does the coordinator invoke subagents?",
        "options": [
            "A. By importing the subagent Python module directly",
            "B. Via the built-in Task tool, with allowedTools including 'Task'",
            "C. By sending HTTP requests to subagent API endpoints",
            "D. Via the Batch API for parallel execution",
        ],
        "answer": "B",
        "explanation": "The Task tool is the mechanism for spawning subagents. The coordinator must have 'Task' in its allowedTools. Subagents are defined via AgentDefinition with description, system prompt, and tool restrictions.",
    },
    {
        "domain": 1,
        "question": "How should a coordinator pass findings from one subagent to another?",
        "options": [
            "A. Store results in a shared database that all agents access",
            "B. Include the complete findings directly in the downstream subagent's prompt",
            "C. Use environment variables to pass data between agents",
            "D. Subagents automatically inherit the coordinator's conversation history",
        ],
        "answer": "B",
        "explanation": "Subagent context must be explicitly provided in the prompt \u2014 subagents do NOT automatically inherit parent context or share memory. Complete findings from prior agents should be passed directly in the subagent's prompt.",
    },
    {
        "domain": 1,
        "scenario": "A coordinator spawns three research subagents. The developer wants them to run simultaneously to reduce total execution time.",
        "question": "How should the coordinator spawn the subagents?",
        "options": [
            "A. Use three sequential Task tool calls across separate turns",
            "B. Emit multiple Task tool calls in a single coordinator response",
            "C. Use the Batch API to run them in parallel",
            "D. Fork the session three times and run each subagent independently",
        ],
        "answer": "B",
        "explanation": "Claude can emit multiple tool_use blocks within the same response content array, launching multiple subagents in parallel. The coordinator handles this naturally in one turn.",
    },
    {
        "domain": 1,
        "question": "When should programmatic enforcement (e.g., hooks, prerequisite gates) be preferred over prompt-based guidance for workflow ordering?",
        "options": [
            "A. Always \u2014 programs are always better than prompts",
            "B. When deterministic compliance is required, such as identity verification before financial operations",
            "C. Only when the developer does not trust the model",
            "D. Programmatic enforcement is never needed if prompts are well-written",
        ],
        "answer": "B",
        "explanation": "When deterministic compliance is required (e.g., identity verification before financial operations), prompt instructions alone have a non-zero failure rate. Programmatic prerequisites block downstream tool calls until prerequisite steps complete.",
    },
    {
        "domain": 1,
        "question": "What is the PostToolUse hook pattern used for?",
        "options": [
            "A. Logging tool calls for audit purposes only",
            "B. Intercepting tool results for transformation before the model processes them",
            "C. Preventing any tool from being called more than once",
            "D. Automatically retrying failed tool calls",
        ],
        "answer": "B",
        "explanation": "PostToolUse hooks intercept tool results for transformation before the model processes them \u2014 e.g., normalizing heterogeneous data formats like Unix timestamps, ISO 8601 dates, and numeric status codes from different MCP tools.",
    },
    {
        "domain": 1,
        "scenario": "A developer uses tool call interception hooks to block refunds exceeding $500 and redirect to human escalation.",
        "question": "Why is this approach better than prompting 'never refund more than $500'?",
        "options": [
            "A. It is not better \u2014 prompt instructions are sufficient",
            "B. Hooks provide deterministic guarantees, while prompt instructions are probabilistic",
            "C. Hooks are cheaper than prompt-based enforcement",
            "D. Prompt instructions only work for amounts under $100",
        ],
        "answer": "B",
        "explanation": "Hooks provide deterministic guarantees for business rules (e.g., refund limits), while prompt-based enforcement is probabilistic with a non-zero failure rate. Choose hooks when guaranteed compliance is required.",
    },
    {
        "domain": 1,
        "scenario": "A developer needs a workflow that reviews each file individually for local issues, then does a cross-file pass to check integration consistency.",
        "question": "Which decomposition pattern is most appropriate?",
        "options": [
            "A. Dynamic adaptive decomposition based on intermediate findings",
            "B. Fixed sequential pipeline (prompt chaining) \u2014 per-file analysis then cross-file integration",
            "C. Parallel subagent execution for all files simultaneously",
            "D. Single agent with all files in one prompt",
        ],
        "answer": "B",
        "explanation": "Fixed sequential pipelines (prompt chaining) are appropriate for predictable multi-aspect reviews. Split into per-file local analysis passes plus a separate cross-file integration pass to avoid attention dilution.",
    },
    {
        "domain": 1,
        "question": "When should dynamic adaptive decomposition be used instead of prompt chaining?",
        "options": [
            "A. For simple, well-understood tasks with fixed steps",
            "B. For open-ended investigation tasks where subtasks should be generated based on what is discovered",
            "C. Dynamic decomposition is always better than prompt chaining",
            "D. Only when using the Task tool",
        ],
        "answer": "B",
        "explanation": "Dynamic adaptive decomposition works well for open-ended tasks like 'add comprehensive tests to a legacy codebase' \u2014 first map structure, identify high-impact areas, then create a prioritized plan that adapts as dependencies are discovered.",
    },
    {
        "domain": 1,
        "question": "When should a developer choose to start a new session with a structured summary rather than use --resume?",
        "options": [
            "A. When the prior context is mostly valid",
            "B. When prior tool results are stale and the session context contains outdated information",
            "C. Always \u2014 new sessions are always better",
            "D. When the session name is unknown",
        ],
        "answer": "B",
        "explanation": "Starting fresh with injected summaries is more reliable when prior tool results are stale. Use --resume when prior context is mostly still valid.",
    },
    {
        "domain": 1,
        "scenario": "An agent cannot complete a customer request and must hand the case to a human support specialist.",
        "question": "What must the structured handoff include?",
        "options": [
            "A. A generic error message and the full conversation transcript",
            "B. Customer ID, factual summary of what happened, root cause, and recommended action",
            "C. The agent's confidence score and the customer's sentiment rating",
            "D. Only the recommended action \u2014 the human can re-investigate the rest",
        ],
        "answer": "B",
        "explanation": "The exam-tested handoff format is: Customer ID (who), Summary (what, factual), Root cause (why), Recommended action (what next). Never silently fail with a generic error. Self-reported confidence and sentiment are unreliable and do not belong in the handoff.",
    },
    {
        "domain": 1,
        "scenario": "A team wants the full session transcript archived to a log every time Claude Code compacts the conversation, before the summary discards detail.",
        "question": "Which hook mechanism supports this?",
        "options": [
            "A. A PostToolUse hook on the compact tool",
            "B. A PreCompact hook \u2014 it receives the transcript path and trigger (manual matcher for /compact, auto for the context window), and exit code 2 blocks compaction",
            "C. A PreToolUse hook denying all tool calls during compaction",
            "D. A system-prompt instruction to save transcripts before compacting",
        ],
        "answer": "B",
        "explanation": "PreCompact fires immediately before compaction with the transcript path, trigger, and custom /compact instructions, so it can archive detail first. Same pattern as tool hooks: a Pre event can inspect and block (exit code 2), a Post event only observes. Prompt instructions are probabilistic and cannot guarantee archival.",
    },
    {
        "domain": 1,
        "scenario": "An agent must analyse a large dataset under two competing hypotheses \u2014 statistical modelling vs machine learning \u2014 without either exploration polluting the other's context.",
        "question": "Which session mechanism fits, and why?",
        "options": [
            "A. --resume \u2014 continue the same session twice, once per hypothesis",
            "B. fork_session \u2014 branch two independent explorations from one shared baseline context",
            "C. /compact between hypotheses \u2014 summarise the first before starting the second",
            "D. A single longer session covering both hypotheses sequentially",
        ],
        "answer": "B",
        "explanation": "fork_session branches divergent explorations from a shared baseline so each hypothesis gets clean context. Resume continues one line; compacting between them leaks the first hypothesis into the second; one long session cross-contaminates both.",
    },
    {
        "domain": 1,
        "scenario": "A moderation agent auto-removes posts. Review finds 3% of removed posts were legitimate, while clearly violating posts sometimes stay up for hours.",
        "question": "What routing design fixes both failure modes?",
        "options": [
            "A. Escalate every borderline case to humans and auto-remove the rest",
            "B. Tiered confidence routing \u2014 high-confidence violations actioned, high-confidence safe passed, uncertain cases to human review",
            "C. Route by the agent's self-reported confidence score alone",
            "D. Lower the removal threshold until nothing violating stays up",
        ],
        "answer": "B",
        "explanation": "Tiered routing matches action to certainty: act where confident, escalate where uncertain. Self-reported confidence is poorly calibrated and not a valid trigger \u2014 but per-category classifier scores are. Blanket escalation or threshold-shifting fixes one failure mode by worsening the other.",
    },
    # ═══════════════════════════════════════════════
    # DOMAIN 2: Tool Design & MCP Integration
    # ═══════════════════════════════════════════════
    {
        "domain": 2,
        "question": "What is the primary mechanism LLMs use to decide which tool to call?",
        "options": [
            "A. The tool name length",
            "B. The tool description",
            "C. The order tools are listed in the array",
            "D. The number of input parameters",
        ],
        "answer": "B",
        "explanation": "Tool descriptions are the primary mechanism LLMs use for tool selection. Minimal or ambiguous descriptions lead to unreliable selection among similar tools.",
    },
    {
        "domain": 2,
        "scenario": "Claude keeps calling the wrong tool. The team must diagnose before fixing.",
        "question": "How does the correct remedy depend on the diagnosis?",
        "options": [
            "A. Few lookalike tools in a small set \u2014 sharpen the descriptions; different jobs across many tools \u2014 split by role into focused agents; variations on one job sharing a shape \u2014 consolidate into one parameterised tool",
            "B. Always rewrite all tool descriptions first, regardless of toolkit size",
            "C. Always add few-shot examples showing correct tool selection",
            "D. Always split into more agents until each agent has exactly one tool",
        ],
        "answer": "A",
        "explanation": "Count the tools before picking the remedy. Descriptions are the first fix only when the toolkit is already workable (~4-5 tools); past that, selection degrades on decision complexity alone. Few-shot examples are NOT a sanctioned remedy for misselection.",
    },
    {
        "domain": 2,
        "scenario": "An MCP tool always returns 'Operation failed' for every error \u2014 timeout, invalid input, and permission denied all produce the same message.",
        "question": "What is the consequence of this uniform error response?",
        "options": [
            "A. None \u2014 the agent will retry all failures equally",
            "B. The agent cannot make appropriate recovery decisions because it cannot distinguish error types",
            "C. The agent will always escalate to a human",
            "D. The tool will be automatically disabled",
        ],
        "answer": "B",
        "explanation": "Uniform errors hide the category the agent needs: transient (retry as-is, isRetryable true), validation (correct input, new call), business (alternative path), permission (escalate). Structured metadata (errorCategory, isRetryable, description) rides inside the result content \u2014 the MCP envelope itself only defines content, structuredContent and isError. 'Not found' is deliberately absent: an empty search result is valid data, not an error.",
    },
    {
        "domain": 2,
        "scenario": "A coordinator agent has access to 18 tools including web_search, document_parser, code_analyzer, database_query, and many others. The agent frequently calls the wrong tool for the task.",
        "question": "What is the most likely cause?",
        "options": [
            "A. The model is not powerful enough",
            "B. Too many tools (18) degrades tool selection reliability by increasing decision complexity",
            "C. The tool input schemas are too complex",
            "D. The tools lack proper error handling",
        ],
        "answer": "B",
        "explanation": "Giving an agent access to too many tools (e.g., 18 instead of 4-5) degrades tool selection reliability. Agents should only have the tools needed for their specialization.",
    },
    {
        "domain": 2,
        "question": "When should tool_choice: 'any' be used?",
        "options": [
            "A. When the model must return a text response",
            "B. When the model must call a tool but can choose which one",
            "C. When forcing a specific tool to be called first",
            "D. When the model should decide between calling a tool or returning text",
        ],
        "answer": "B",
        "explanation": "tool_choice: 'any' guarantees the model calls a tool rather than returning conversational text, but allows it to choose which tool. Use forced selection to ensure a specific tool runs first.",
    },
    {
        "domain": 2,
        "question": "Where should shared team MCP servers be configured?",
        "options": [
            "A. ~/.claude.json \u2014 user-level config for personal access",
            "B. .mcp.json \u2014 project-level config shared via version control",
            "C. CLAUDE.md \u2014 described in natural language",
            "D. The MCP server's own configuration file",
        ],
        "answer": "B",
        "explanation": "Project-level .mcp.json (checked into version control) is for shared team tooling. User-level ~/.claude.json is for personal or experimental servers.",
    },
    {
        "domain": 2,
        "question": "What is the purpose of MCP resources?",
        "options": [
            "A. To replace tools with static data",
            "B. To expose content catalogs (e.g., issue summaries, documentation hierarchies) to reduce exploratory tool calls",
            "C. To store compiled binary resources for tools",
            "D. To provide authentication credentials to MCP servers",
        ],
        "answer": "B",
        "explanation": "MCP resources expose content catalogs like issue summaries, documentation hierarchies, or database schemas \u2014 no list_tables + describe_table per table. Resources are application-controlled: the server lists them but the client decides when to attach one (Claude Code via @server:resource). Resources show what data is available; tools let the agent act on it.",
    },
    {
        "domain": 2,
        "question": "When Edit fails due to non-unique text matches, what is the correct fallback?",
        "options": [
            "A. Retry Edit with the same text \u2014 it might work the second time",
            "B. Use Read to load the full file, then Write to overwrite with updated content",
            "C. Switch to Bash sed commands",
            "D. Delete the file and recreate it",
        ],
        "answer": "B",
        "explanation": "When Edit cannot find unique anchor text, the fallback is to Read the full file contents, modify them, and Write the updated version. This is the documented graceful fallback pattern.",
    },
    {
        "domain": 2,
        "scenario": "Every invoice must be extracted into one exact schema via an extract_invoice tool, with no variation and no text responses.",
        "question": "Which tool_choice mode guarantees this?",
        "options": [
            "A. tool_choice: 'auto' \u2014 the model will learn to prefer extract_invoice",
            "B. tool_choice: 'any' \u2014 a tool call is guaranteed and the model picks extract_invoice",
            "C. Forced tool_choice: { type: 'tool', name: 'extract_invoice' } \u2014 the specific tool must be called every time",
            "D. Omitting tool_choice \u2014 fewer constraints mean more reliable output",
        ],
        "answer": "C",
        "explanation": "Forced tool_choice guarantees one specific structure every time. 'any' guarantees a tool call but lets the model choose which \u2014 correct when the document type is unknown and several schemas could apply. 'auto' (the agentic-loop default) lets the model answer with text. Scope agents to 4-5 role-focused tools so selection stays reliable.",
    },
    # ═══════════════════════════════════════════════
    {
        "domain": 2,
        "scenario": "An 'InvalidStateTransition' error is logged somewhere in a large codebase. The developer does not know which files define the state machine.",
        "question": "What is the correct tool sequence?",
        "options": [
            "A. Read every file in the repository until the state machine is found",
            "B. Grep for 'InvalidStateTransition' to locate occurrences, then Read only the relevant files",
            "C. Glob for *state* files, then Edit them directly",
            "D. Ask the model to guess the file from the error name",
        ],
        "answer": "B",
        "explanation": "Grep-then-Read is the discovery sequence: Grep finds content across unknown files, Read loads only what matched. Reading everything wastes context; Glob matches paths not content; guessing skips grounding entirely.",
    },
    {
        "domain": 2,
        "scenario": "A rename touches 'userData' in 12 places across one file. The developer reaches for Edit.",
        "question": "What is the most efficient correct approach?",
        "options": [
            "A. Twelve separate Edit calls, one per occurrence",
            "B. Read the file, then Write the whole file with all renames applied",
            "C. One Edit call with replace_all for the non-unique match",
            "D. A Bash sed command across the repository",
        ],
        "answer": "C",
        "explanation": "Edit with replace_all handles non-unique matches in a single operation. Read + Write is the fallback when a unique anchor cannot be constructed \u2014 not the first resort for a uniform rename. Twelve calls waste turns; sed bypasses the specialised tool.",
    },
    # DOMAIN 3: Claude Code Configuration & Workflows
    # ═══════════════════════════════════════════════
    {
        "domain": 3,
        "question": "A team member cannot see project instructions that others on the team can see. What is the most likely cause?",
        "options": [
            "A. Their API key is invalid",
            "B. The instructions are in ~/.claude/CLAUDE.md (user-level) rather than a project-level CLAUDE.md",
            "C. Their Claude Code version is outdated",
            "D. The instructions are in a subdirectory CLAUDE.md",
        ],
        "answer": "B",
        "explanation": "User-level ~/.claude/CLAUDE.md applies only to that user and is not shared via version control. Project-level .claude/CLAUDE.md or root CLAUDE.md is shared with teammates.",
    },
    {
        "domain": 3,
        "question": "How do you reference an external standards file from a project CLAUDE.md to keep it modular?",
        "options": [
            "A. With an @import keyword, e.g. @import ./standards/naming.md",
            "B. With @ followed by a path on its own line, e.g. @./standards/naming.md \u2014 there is no @import keyword",
            "C. By listing the file under an imports: key in YAML frontmatter",
            "D. By adding the file to .claude/rules/ with a paths: pattern",
        ],
        "answer": "B",
        "explanation": "Modular CLAUDE.md files use @ plus a path inlined at load time. There is no @import keyword. Each @<path> line is expanded inline \u2014 it organises source files but does not reduce per-session context; use .claude/rules/ with paths: frontmatter for conditional loading.",
    },
    {
        "domain": 3,
        "question": "What is the advantage of splitting a large CLAUDE.md into multiple files in .claude/rules/?",
        "options": [
            "A. It runs faster",
            "B. Each file can have YAML frontmatter with path patterns for conditional activation, reducing irrelevant context",
            "C. It allows multiple team members to edit simultaneously",
            "D. It bypasses the CLAUDE.md size limit",
        ],
        "answer": "B",
        "explanation": ".claude/rules/ files with YAML frontmatter paths fields containing glob patterns enable conditional rule activation. Rules load only when editing matching files, reducing irrelevant context and token usage.",
    },

    {
        "domain": 3,
        "question": "When should plan mode be selected over direct execution?",
        "options": [
            "A. For all tasks to ensure safety",
            "B. For simple, well-scoped changes like a single-file bug fix with a clear stack trace",
            "C. For complex tasks involving large-scale changes, architectural decisions, and multiple valid approaches",
            "D. Only when explicitly requested by the user",
        ],
        "answer": "C",
        "explanation": "Plan mode is for complex tasks with architectural implications. Direct execution is for well-understood, clearly scoped changes.",
    },

    {
        "domain": 3,
        "question": "What is the -p (--print) flag used for in Claude Code CLI?",
        "options": [
            "A. Printing formatted output to the console",
            "B. Running Claude Code in non-interactive mode for automated pipelines",
            "C. Printing the current configuration",
            "D. Pretty-printing JSON responses",
        ],
        "answer": "B",
        "explanation": "The -p (--print) flag runs Claude Code in non-interactive mode, preventing interactive input hangs in automated CI/CD pipelines.",
    },
    {
        "domain": 3,
        "scenario": "A developer runs Claude Code in CI to review pull requests. After a new commit, they want to re-run the review without getting duplicate comments.",
        "question": "What is the best approach?",
        "options": [
            "A. Use --resume to continue the previous review session",
            "B. Include prior review findings in context, instructing Claude to report only new or still-unaddressed issues",
            "C. Clear all previous comments and re-run the full review",
            "D. Run reviews only on the diff of the new commit",
        ],
        "answer": "B",
        "explanation": "Including prior review findings in context when re-running reviews after new commits allows Claude to report only new or still-unaddressed issues, avoiding duplicate comments.",
    },

    {
        "domain": 3,
        "scenario": "A project CLAUDE.md says 'use tabs' and a directory CLAUDE.md says 'use spaces'. A developer asks which rule wins.",
        "question": "What is the correct answer?",
        "options": [
            "A. The directory-level rule wins \u2014 more specific scope overrides",
            "B. The project-level rule wins \u2014 broader scope takes precedence",
            "C. Neither is guaranteed \u2014 CLAUDE.md files are concatenated into context, not overridden, and contradictions may resolve arbitrarily; move must-hold rules to settings.json or a hook",
            "D. The user-level ~/.claude/CLAUDE.md breaks the tie",
        ],
        "answer": "C",
        "explanation": "CLAUDE.md has a documented load order (broadest to most specific) but NO precedence chain \u2014 every applicable file loads together. 'More specific wins' and 'user overrides project' are classic distractors. settings.json is the strict chain (managed policy > local > project > user); hooks fire deterministically at lifecycle events.",
    },
    {
        "domain": 3,
        "scenario": "A CI job needs extra review instructions for one run without losing Claude Code's default tool guidance and safety behaviour.",
        "question": "Which flag is correct?",
        "options": [
            "A. --system-prompt \"<text>\" \u2014 replaces the whole default prompt",
            "B. --append-system-prompt \"<text>\" \u2014 adds to the default prompt and keeps tool guidance and safety instructions",
            "C. --bare \u2014 adds instructions while skipping hooks and memory",
            "D. --max-turns 1 \u2014 constrains the prompt to a single turn",
        ],
        "answer": "B",
        "explanation": "--append-system-prompt adds and keeps the defaults; --system-prompt replaces everything (you then own all safety/tool guidance). --bare is the opposite need: a fast scripted run skipping hooks, skills, plugins, MCP, memory and CLAUDE.md. The *-file variants load the same text from a file.",
    },
    {
        "domain": 3,
        "question": "How do project slash commands differ from project skills?",
        "options": [
            "A. A command is a single flat .md file in .claude/commands/ (a prompt template, $ARGUMENTS supported); a skill is a directory with a SKILL.md entrypoint plus supporting files and frontmatter",
            "B. A flat .md file placed directly inside .claude/skills/ creates a command",
            "C. Commands run in forked context; skills run in the main conversation",
            "D. There is no difference \u2014 the systems were merged into one",
        ],
        "answer": "A",
        "explanation": "Commands and skills were merged so both surface as /commands, but the shapes differ: command = flat .md prompt template; skill = directory with SKILL.md, supporting files, frontmatter (e.g. allowed-tools, context: fork) and automatic invocation when relevant. A flat file inside .claude/skills/ does NOT create a command.",
    },
    # ═══════════════════════════════════════════════
    {
        "domain": 3,
        "scenario": "A developer asks Claude to 'explain the order processing pipeline'. It spans 15 classes across 4 packages with deep inheritance. Claude reads 3 files and returns a superficial summary that misses key flows.",
        "question": "What is the correct fix?",
        "options": [
            "A. Ask Claude to read more files in the same session",
            "B. Delegate to an Explore subagent for thorough reference-tracing discovery across the codebase",
            "C. Switch to plan mode and re-ask the same question",
            "D. Increase max_tokens so the summary can be longer",
        ],
        "answer": "B",
        "explanation": "The Explore subagent exists for thorough multi-hop codebase discovery \u2014 tracing references across classes and packages. More files in-session dilutes attention; plan mode structures approach but does not deepen discovery; longer output cannot contain flows never read.",
    },
    {
        "domain": 3,
        "scenario": "Three Claude instances work in one repo: two extracting services, one updating shared libraries. Their commits keep conflicting.",
        "question": "How should the parallel work be isolated and coordinated?",
        "options": [
            "A. All three work on main and resolve conflicts after each commit",
            "B. git worktree \u2014 an isolated directory + branch per instance; sequence shared-file edits (one merges, the other rebases) to avoid conflicts",
            "C. Clone the repository three times and merge at the end",
            "D. Run the instances sequentially instead of in parallel",
        ],
        "answer": "B",
        "explanation": "git worktree gives each instance an isolated working directory on its own branch without full re-clones. Shared files still need sequencing \u2014 merge-then-rebase \u2014 because isolation prevents clobbering, not logical conflicts.",
    },
    {
        "domain": 3,
        "scenario": "A scheduled workflow uses anthropics/claude-code-action with a valid API key but no prompt input. The team expects an automated summary of yesterday's commits.",
        "question": "What actually happens, and what is missing?",
        "options": [
            "A. It runs the summary \u2014 the key alone is sufficient for automation",
            "B. Nothing automated: with no prompt the action waits in interactive mode for an @claude mention or trigger_phrase; automation mode requires prompt input",
            "C. It fails immediately \u2014 scheduled workflows cannot use the action",
            "D. It summarises but cannot open issues without extra permissions",
        ],
        "answer": "B",
        "explanation": "No prompt = interactive mode (waits for @claude/trigger_phrase); prompt = automation mode. Related trap: workflow permissions are not Claude tools \u2014 a plain-text prompt starts with no tools, so scheduled jobs needing repo access must allowlist the GitHub MCP tools.",
    },
    # DOMAIN 4: Prompt Engineering & Structured Output
    # ═══════════════════════════════════════════════
    {
        "domain": 4,
        "scenario": "A review prompt says 'be conservative and only report high-confidence findings'. Reviewers still report many false positives, and developers stop trusting the results.",
        "question": "What is the most effective fix?",
        "options": [
            "A. Increase the confidence threshold",
            "B. Replace vague instructions with specific categorical criteria defining which issues to report vs skip",
            "C. Add more examples of acceptable code",
            "D. Switch to a different model",
        ],
        "answer": "B",
        "explanation": "General instructions like 'be conservative' fail to improve precision compared to specific categorical criteria. Write specific review criteria defining which issues to report (bugs, security) versus skip.",
    },
    {
        "domain": 4,
        "question": "What is the most reliable approach for guaranteed schema-compliant structured output from Claude?",
        "options": [
            "A. JSON mode in the system prompt",
            "B. Tool use (tool_use) with JSON schemas",
            "C. Few-shot examples of the desired JSON format",
            "D. Post-processing with JSON.parse and retry",
        ],
        "answer": "B",
        "explanation": "Tool use with JSON schemas is the most reliable approach for guaranteed schema-compliant structured output, eliminating JSON syntax errors.",
    },
    {
        "domain": 4,
        "question": "Strict JSON schemas via tool use eliminate syntax errors. What type of errors can still occur?",
        "options": [
            "A. No errors \u2014 JSON schemas guarantee perfect output",
            "B. Semantic errors \u2014 e.g., line items that don't sum to total, values in wrong fields",
            "C. Connection timeout errors",
            "D. Schema validation errors",
        ],
        "answer": "B",
        "explanation": "While JSON schemas eliminate syntax errors, they do not prevent semantic errors such as line items that don't sum to the total or values placed in wrong fields.",
    },
    {
        "domain": 4,
        "question": "When designing an extraction schema, when should a field be made optional (nullable)?",
        "options": [
            "A. Never \u2014 all fields should be required",
            "B. When source documents may not contain the information, to prevent the model from fabricating values",
            "C. Only for numeric fields",
            "D. When the field is used for filtering",
        ],
        "answer": "B",
        "explanation": "Fields should be optional when source documents may not contain the information. Required fields can cause the model to fabricate values to satisfy the schema.",
    },
    {
        "domain": 4,
        "question": "How should validation errors be handled in an extraction retry flow?",
        "options": [
            "A. Restart from scratch with a blank prompt",
            "B. Append specific validation errors to the prompt on retry to guide the model toward correction",
            "C. Keep retrying with the exact same prompt",
            "D. Switch to a different model for the retry",
        ],
        "answer": "B",
        "explanation": "Retry-with-error-feedback appends specific validation errors to the prompt on retry, guiding the model toward correction. Ineffective when required info is absent from source.",
    },

    {
        "domain": 4,
        "question": "What is the primary benefit of the Batch API (Message Batches API)?",
        "options": [
            "A. Lower latency than the synchronous API",
            "B. 50% cost savings with up to 24-hour processing window",
            "C. Support for real-time streaming responses",
            "D. Higher rate limits",
        ],
        "answer": "B",
        "explanation": "The Batch API offers 50% cost savings with up to a 24-hour processing window. No guaranteed latency SLA \u2014 appropriate for non-blocking, latency-tolerant workloads. Never for real-time or user-facing requests.",
    },


    {
        "domain": 4,
        "question": "Why is a model less effective at reviewing its own generated code in the same session?",
        "options": [
            "A. It does not understand the code it wrote",
            "B. It retains reasoning context from generation, making it less likely to question its own decisions",
            "C. The code is not saved to disk yet",
            "D. Self-review requires a different API",
        ],
        "answer": "B",
        "explanation": "A model retains reasoning context from generation, making it less likely to question its own decisions. Independent review instances are more effective at catching subtle issues.",
    },
    {
        "domain": 4,
        "scenario": "An extraction schema marks contract_value as required, but half the source documents contain no contract value. The model keeps inventing plausible dollar amounts.",
        "question": "What is the correct schema fix?",
        "options": [
            "A. Add more few-shot examples showing contract values",
            "B. Make the field nullable with a union type {\"type\": [\"string\", \"null\"]} and leave it out of the parent object's required array, so the model may return null",
            "C. Mark the field nullable: true in the input_schema",
            "D. Add required: true on the property itself to strengthen the constraint",
        ],
        "answer": "B",
        "explanation": "Required fields CAUSE fabrication when data is missing \u2014 give the model permission to return null. Note the syntax: nullable: true is OpenAPI, not JSON Schema, and required is an array on the parent object, never a per-property boolean. Schemas kill syntax errors, never semantic ones (wrong-field values, line items not summing).",
    },
    {
        "domain": 4,
        "scenario": "Detailed prose instructions produce inconsistently formatted classifications. The team adds few-shot examples and quality jumps; they consider adding 10 more examples to push further.",
        "question": "What should they do?",
        "options": [
            "A. Add all 10 \u2014 more examples always improve quality",
            "B. Stop at 2-4 examples covering severity levels and edge cases with Input \u2192 Reasoning \u2192 Output; 0\u21922 has the largest impact and returns diminish after ~4",
            "C. Move the examples out of the system prompt into every user message",
            "D. Replace the examples with stricter prose rules",
        ],
        "answer": "B",
        "explanation": "Few-shot is the most effective fix when instructions alone fail, but 2-4 is the sweet spot \u2014 include reasoning, cover edge cases, show SKIP alongside REPORT to cut false positives. Keep examples in the system prompt for prompt-caching benefits; per-request variation belongs in the user message.",
    },
    # ═══════════════════════════════════════════════
    {
        "domain": 4,
        "scenario": "A tool named 'check_security' exists, and the system prompt says 'check the security of each function'. The model writes text analyses instead of calling the tool.",
        "question": "What is the root cause and fix?",
        "options": [
            "A. The tool description is too short \u2014 lengthen it",
            "B. Keyword overlap: prompt phrasing mirroring the tool name reads as a general instruction \u2014 reword the instruction so it unambiguously directs the tool call",
            "C. The model needs few-shot examples of tool selection",
            "D. tool_choice must be set to 'any' on every request",
        ],
        "answer": "B",
        "explanation": "When instruction wording mirrors a tool name, the model treats it as prose guidance and answers in text. Reword so the instruction clearly demands the tool call. Few-shot is not a sanctioned misselection fix; forcing tool_choice on every turn removes the model's legitimate text responses.",
    },
    {
        "domain": 4,
        "scenario": "A multi-step prompt chain (extract \u2192 validate \u2192 format \u2192 synthesise) occasionally produces confident final reports built on a corrupted extraction in step 1.",
        "question": "What structural fix prevents the cascade?",
        "options": [
            "A. Merge all steps into one larger prompt to avoid handoff loss",
            "B. Inter-step validation \u2014 validate each step's focused output before the next step consumes it",
            "C. Add more few-shot examples to the final synthesis step",
            "D. Run the whole chain twice and average the reports",
        ],
        "answer": "B",
        "explanation": "Each chained step has a small focused prompt whose output can be checked mechanically before downstream steps build on it \u2014 this stops cascading failures and lets single steps retry without rerunning the chain. Merging reintroduces attention dilution; examples at the end cannot repair a corrupted start.",
    },
    {
        "domain": 4,
        "scenario": "Extracting 2,000 contracts requires calling lookup_counterparty mid-extraction, reading the result, then finishing. The team wants the Batch API's 50% saving.",
        "question": "Can they use it?",
        "options": [
            "A. Yes \u2014 Batch supports the full agentic loop including tool calls",
            "B. No \u2014 the Batch API has no multi-turn tool calling; run synchronously and forfeit the saving",
            "C. Yes \u2014 by polling processing_status until 'ended' mid-extraction",
            "D. Yes \u2014 by splitting each contract into its own batch",
        ],
        "answer": "B",
        "explanation": "Batch is fire-and-forget bulk inference: no tool calls, no mid-run interaction (polling only tells you when results are ready). Any workflow needing model \u2192 tool \u2192 model turns must run synchronously. Related: on batch failures, identify by custom_id and resubmit only those, chunking oversized docs \u2014 never resubmit the whole batch.",
    },
    # DOMAIN 5: Context Management & Reliability
    # ═══════════════════════════════════════════════

    {
        "domain": 5,
        "question": "What is the 'lost in the middle' effect?",
        "options": [
            "A. Files in the middle of a directory listing are skipped",
            "B. Models reliably process info at the beginning and end of long inputs but may omit middle sections",
            "C. Tools listed in the middle of the tools array are called less often",
            "D. Only the middle of a conversation is retained in context",
        ],
        "answer": "B",
        "explanation": "The 'lost in the middle' effect means models reliably process information at the beginning and end of long inputs but may miss content in the middle section.",
    },

    {
        "domain": 5,
        "question": "When should an agent escalate to a human agent?",
        "options": [
            "A. Whenever the agent is unsure",
            "B. Only when the agent's confidence drops below 50%",
            "C. When customer explicitly requests human, policy is ambiguous, or agent cannot make meaningful progress",
            "D. Never \u2014 agents should always resolve issues autonomously",
        ],
        "answer": "C",
        "explanation": "Appropriate escalation triggers: customer explicitly requests a human, policy exceptions or gaps, and inability to make meaningful progress. Sentiment and confidence scores are unreliable proxies.",
    },
    {
        "domain": 5,
        "scenario": "A customer expresses frustration: 'This is ridiculous, I want to talk to a real person.' The agent can resolve the issue easily in one more step.",
        "question": "What should the agent do?",
        "options": [
            "A. Immediately escalate without further action",
            "B. Acknowledge frustration, offer to resolve, escalate only if customer reiterates preference for human",
            "C. Ignore the request and continue with resolution",
            "D. Apologize and close the conversation",
        ],
        "answer": "B",
        "explanation": "Acknowledge frustration while offering resolution when the issue is within the agent's capability. Escalate only if the customer reiterates their preference for a human.",
    },
    {
        "domain": 5,
        "scenario": "An MCP server times out during a search from a research subagent. The subagent tries again and succeeds on the second attempt.",
        "question": "How should this be handled in a multi-agent system?",
        "options": [
            "A. Return the timeout error to the coordinator",
            "B. Subagent implements local recovery for transient failures, propagates only errors it cannot resolve",
            "C. Silently return empty results",
            "D. Terminate the entire workflow",
        ],
        "answer": "B",
        "explanation": "Subagents should implement local recovery for transient failures and only propagate errors they cannot resolve, including what was attempted and partial results.",
    },
    {
        "domain": 5,
        "question": "What is the difference between an access failure and a valid empty result?",
        "options": [
            "A. There is no difference \u2014 both mean 'no data found'",
            "B. Access failures need retry decisions, while empty results are successful queries with no matches",
            "C. Both should be treated as errors",
            "D. Access failures are always permanent",
        ],
        "answer": "B",
        "explanation": "Access failures (timeouts) need retry decisions as transient errors. Valid empty results represent successful queries that found no matches \u2014 they are not errors.",
    },
    {
        "domain": 5,
        "scenario": "A knowledge base search has 97% overall accuracy, but financial documents have 82% accuracy while technical docs have 99%. Errors on financial documents go unnoticed for weeks.",
        "question": "What went wrong with quality monitoring?",
        "options": [
            "A. Nothing \u2014 97% overall is acceptable",
            "B. Aggregate metrics mask poor performance on specific types. Validate accuracy by document type and field segment.",
            "C. The model needs retraining on financial documents",
            "D. The review threshold was set too high",
        ],
        "answer": "B",
        "explanation": "Aggregate accuracy metrics may mask poor performance on specific document types. Implement stratified random sampling to measure error rates across segments.",
    },
    {
        "domain": 5,
        "question": "Why is source attribution lost during multi-step summarization?",
        "options": [
            "A. The model intentionally removes citations to save tokens",
            "B. Findings are compressed without preserving claim-source mappings",
            "C. Source URLs are too long for the context window",
            "D. Attribution is only possible in the first summarization step",
        ],
        "answer": "B",
        "explanation": "Source attribution is lost when findings are compressed without preserving claim-source mappings. Require structured claim-source mappings preserved through synthesis.",
    },
    {
        "domain": 5,
        "scenario": "A long-running exploration may exceed the context window, and intermediate findings must survive a context reset or crash.",
        "question": "What design pattern supports this recovery?",
        "options": [
            "A. Re-run all agents from the beginning",
            "B. Scratchpad files \u2014 write findings to disk as discovered; at context boundaries read the scratchpad back to restore state",
            "C. Ask the model to progressively summarise the conversation as it grows",
            "D. Log all agent outputs to a file for manual review only",
        ],
        "answer": "B",
        "explanation": "Scratchpads are external persistence (files on disk) \u2014 they survive any context reset, unlike conversation history. Progressive summarisation loses specifics (names, numbers, quotes); /compact summarises while project CLAUDE.md is re-read from disk, but nested CLAUDE.md files and path-scoped rules only return on next matching read.",
    },

    {
        "domain": 5,
        "scenario": "Context budget is 200k tokens: system prompt 8k, conversation history 120k, one tool result 65k. The model now gives thin, rushed responses.",
        "question": "What is the arithmetic and the fix?",
        "options": [
            "A. 193k consumed leaves 7k for the response \u2014 trim history and verbose tool outputs to free response room",
            "B. The budget only counts the response \u2014 raise max_tokens",
            "C. 200k minus 8k leaves plenty \u2014 history and tool results use a separate budget",
            "D. Switch models \u2014 the budget math differs per model",
        ],
        "answer": "A",
        "explanation": "The budget is shared: system + history + tool results + response all draw from the same 200k. 8k + 120k + 65k = 193k leaves ~7k for output. Trim stale history and verbose tool fields before they accumulate \u2014 the fix is subtraction, not a bigger model.",
    },
    {
        "domain": 5,
        "scenario": "A research subagent's academic-DB search hits a 403. The subagent catches the error and returns an empty result marked successful. The coordinator reports 'no relevant papers found'.",
        "question": "What went wrong?",
        "options": [
            "A. Nothing \u2014 empty results are valid and the coordinator handled them",
            "B. Silent suppression: an access failure was masked as a valid empty result, so the coordinator believed a failed search succeeded with zero hits \u2014 propagate the 403 explicitly with what was attempted",
            "C. The subagent should have retried the 403 until it succeeded",
            "D. The coordinator should distrust all empty results from subagents",
        ],
        "answer": "B",
        "explanation": "The worst propagation anti-pattern: converting an error into fake success. Empty-from-success (valid) and empty-from-failure (403) look identical downstream but demand opposite responses. Propagate failures explicitly with structured error context; only genuinely empty successes count as 'no matches'.",
    },
]

random.seed(42)
random.shuffle(QUESTIONS)
for i, q in enumerate(QUESTIONS, 1):
    q["id"] = i


def get_letter(opt: str) -> str:
    return opt[0]


def run_exam():
    total = len(QUESTIONS)
    score = 0
    start = time.time()
    domain_correct: Dict[int, int] = {d: 0 for d in DOMAINS}
    domain_total: Dict[int, int] = {d: 0 for d in DOMAINS}

    print("=" * 66)
    print("  CCAR-F PRACTICE EXAM \u2014 Claude Certified Architect (Foundations)")
    print(f"  {total} questions  |  120 minutes  |  Pass: 720/1000")
    print("=" * 66)

    for q in QUESTIONS:
        domain_total[q["domain"]] += 1
        domain_name = DOMAINS[q["domain"]]
        print(f"\n{'=' * 66}")
        if q.get("scenario"):
            print(f"\n  SCENARIO ({domain_name}):")
            print(f"  {q['scenario']}")
        print(f"\n  Q{q['id']}. {q['question']}")
        print()
        for opt in q["options"]:
            print(f"     {opt}")
        print()

        valid = {get_letter(o) for o in q["options"]}
        answer = None
        while answer not in valid:
            raw = input(f"  Your answer ({chr(9608)}): ").strip().upper()
            if raw in valid:
                answer = raw
            else:
                print(f"  Invalid. Choose from: {', '.join(sorted(valid))}")

        correct = answer == q["answer"]
        pts = 1000 / total

        if correct:
            score += 1
            domain_correct[q["domain"]] += 1
            print(f"  \u2713 CORRECT  ({pts:.0f}/{pts:.0f} pts)")
        else:
            print(f"  \u2717 INCORRECT  (0/{pts:.0f} pts)")
            print(f"  Correct answer: {q['answer']}")
        print(f"  {q['explanation']}")

    elapsed = time.time() - start
    scaled = int(score * 1000 / total)
    passed = scaled >= 720

    print("\n" + "=" * 66)
    print("  RESULTS")
    print("=" * 66)
    print(f"  Raw:     {score}/{total} correct")
    print(f"  Scaled:  {scaled}/1000")
    print(f"  Time:    {elapsed/60:.1f} minutes")
    if passed:
        print(f"  STATUS:  \u2713 PASS (\u2265720)")
    else:
        print(f"  STATUS:  \u2717 FAIL (<720) \u2014 keep studying!")

    print(f"\n  Domain breakdown (official exam weight in brackets):")
    for d in sorted(DOMAINS):
        c = domain_correct[d]
        t = domain_total[d]
        bar = "\u2588" * int((c / t) * 20) if t else ""
        pct = (c / t) * 100 if t else 0
        print(f"    {d}. {DOMAINS[d][:42]:42s} {c:2d}/{t:2d} ({pct:3.0f}%) [wt {WEIGHTS[d]:2d}%]  {bar}")
    print()


if __name__ == "__main__":
    run_exam()
