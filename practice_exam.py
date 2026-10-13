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
        "scenario": "A coordinator agent is tasked with researching 'renewable energy trends in Southeast Asia'. It creates three subagents: one for wind, one for solar, and one for policy. The synthesis report has significant gaps \u2014 entire sub-topics like hydroelectric, geothermal, and energy storage are missing.",
        "question": "What is the most likely root cause?",
        "options": [
            "A. The subagents did not have enough context",
            "B. The coordinator's task decomposition was too narrow, leaving uncovered subtopics",
            "C. The synthesis agent was not powerful enough",
            "D. The subagents ran in parallel instead of sequentially",
        ],
        "answer": "B",
        "explanation": "Overly narrow task decomposition by the coordinator leads to incomplete coverage of broad research topics. The coordinator should partition the full scope across subagents to minimize gaps.",
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
        "question": "A developer resumes a Claude Code session with --resume after modifying several files. What should they do to ensure accurate re-analysis?",
        "options": [
            "A. Nothing \u2014 --resume automatically detects changes",
            "B. Inform the session about specific file changes for targeted re-analysis",
            "C. Delete the old session and start fresh",
            "D. Run /compact to clear the old context",
        ],
        "answer": "B",
        "explanation": "The agent should be informed about specific file changes when resuming after code modifications. This enables targeted re-analysis rather than requiring full re-exploration of unchanged areas.",
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
        "question": "Which built-in tool should be used to find all callers of a function named 'calculateTotal' across a codebase?",
        "options": [
            "A. Glob \u2014 for file path pattern matching",
            "B. Grep \u2014 for searching content within files",
            "C. Read \u2014 for reading file contents",
            "D. Edit \u2014 for targeted modifications",
        ],
        "answer": "B",
        "explanation": "Grep searches content within files, making it ideal for finding function callers, error messages, or import statements. Glob is for file path pattern matching.",
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
        "question": "What does context: fork do in a skill's SKILL.md frontmatter?",
        "options": [
            "A. Creates a fork of the repository",
            "B. Runs the skill in an isolated sub-agent context, preventing skill outputs from polluting the main conversation",
            "C. Forks the git branch before executing",
            "D. Duplicates the conversation for parallel execution",
        ],
        "answer": "B",
        "explanation": "context: fork runs the skill in an isolated sub-agent context. Useful for skills that produce verbose output (e.g., codebase analysis) or exploratory context.",
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
        "scenario": "A developer repeatedly gets inconsistent output from Claude Code when trying to transform data. Natural language descriptions of the desired transformation do not produce reliable results.",
        "question": "What is the most effective technique to improve consistency?",
        "options": [
            "A. Write a longer, more detailed description",
            "B. Provide 2-3 concrete input/output examples",
            "C. Switch to a more powerful model",
            "D. Use plan mode instead of direct execution",
        ],
        "answer": "B",
        "explanation": "Concrete input/output examples are the most effective way to communicate expected transformations when prose descriptions are interpreted inconsistently. Few-shot examples produce consistently formatted, actionable output.",
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
        "question": "Where are project-scoped slash commands stored so they are shared with the team via version control?",
        "options": [
            "A. ~/.claude/commands/",
            "B. .claude/commands/",
            "C. .claude/skills/",
            "D. The project README",
        ],
        "answer": "B",
        "explanation": "Project-scoped commands in .claude/commands/ are shared via version control. User-scoped commands in ~/.claude/commands/ are personal and not shared.",
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
        "question": "When are retries with error feedback ineffective for extraction?",
        "options": [
            "A. When the schema is too complex",
            "B. When the required information is simply absent from the source document",
            "C. When using the Batch API",
            "D. When there are too many optional fields",
        ],
        "answer": "B",
        "explanation": "Retries are ineffective when the required information is simply absent from the source document. No amount of prompting can extract data that does not exist.",
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
        "scenario": "A developer needs to run a pre-merge code review that must complete before the merge button is enabled.",
        "question": "Which API should they use?",
        "options": [
            "A. Batch API \u2014 for cost savings",
            "B. Synchronous API \u2014 for blocking, latency-sensitive workflows",
            "C. Either \u2014 both support blocking operations",
            "D. Streaming API \u2014 for real-time output",
        ],
        "answer": "B",
        "explanation": "Batch API is inappropriate for blocking workflows like pre-merge checks because it has no guaranteed latency SLA. Use synchronous API for blocking operations.",
    },
    {
        "domain": 4,
        "question": "When using the Batch API, how are individual requests correlated in the response?",
        "options": [
            "A. By the order they were submitted",
            "B. Via custom_id fields",
            "C. By matching request content",
            "D. By timestamp",
        ],
        "answer": "B",
        "explanation": "The custom_id field correlates batch request/response pairs. Failed documents (identified by custom_id) can be resubmitted with appropriate modifications.",
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
    # DOMAIN 5: Context Management & Reliability
    # ═══════════════════════════════════════════════
    {
        "domain": 5,
        "scenario": "After many turns of conversation, an agent starts giving inconsistent answers \u2014 it references 'typical patterns' instead of specific classes discovered earlier.",
        "question": "What is the most likely cause?",
        "options": [
            "A. The model lacks sufficient training data",
            "B. Context degradation \u2014 the model is losing track of findings as context fills up",
            "C. The user's queries are too complex",
            "D. The model was switched mid-session",
        ],
        "answer": "B",
        "explanation": "Context degradation occurs in extended sessions \u2014 models reference 'typical patterns' rather than specific details. Mitigate with scratchpad files, structured summaries, and context management.",
    },
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
        "scenario": "A customer service agent looks up an order and gets 40+ fields, but only 5 are relevant. Over many turns, these verbose results accumulate in context.",
        "question": "What is the best practice for managing this?",
        "options": [
            "A. Ignore it \u2014 context is cheap",
            "B. Trim verbose tool outputs to only relevant fields before they accumulate in context",
            "C. Use a more powerful model with larger context",
            "D. Store all tool results in a database instead of conversation history",
        ],
        "answer": "B",
        "explanation": "Trim verbose tool outputs to only relevant fields before they accumulate in context. Tool results can consume tokens disproportionately to their relevance.",
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
        "question": "When a tool returns multiple customer matches, how should the agent handle this?",
        "options": [
            "A. Select the first match",
            "B. Ask for additional identifiers rather than selecting based on heuristics",
            "C. Return all matches and let the user decide",
            "D. Report an error for ambiguous results",
        ],
        "answer": "B",
        "explanation": "Multiple customer matches require clarification \u2014 request additional identifiers rather than selecting based on heuristics.",
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
