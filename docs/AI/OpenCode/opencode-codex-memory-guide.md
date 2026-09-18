---
title: OpenCode Codex Memory for OpenCode
description: A guide to opencode-codex-memory, a local-first persistent memory plugin for OpenCode that ports OpenAI Codex's memory system without a Codex subscription.
keywords:
  - opencode
  - memory
  - plugin
  - codex
  - persistent
  - local-first
  - sqlite
  - markdown
  - AI
---

There is a particular kind of frustration in a long coding project: you explain
the same decision to an assistant again because the useful context stayed in a
previous session. [opencode-codex-memory](https://github.com/moritzfl/opencode-codex-memory)
is a community plugin for [OpenCode](https://opencode.ai) that closes that loop.
It reviews finished sessions in the background, keeps what is durable — your
conventions, how a repo is built, what worked and what did not — and puts that
context back in front of the agent in later conversations.

Despite the name, **no Codex subscription or OpenAI account is needed**. The
plugin is a faithful port of the memory system in OpenAI's Codex, and it works
out of the box with zero extra configuration, using whatever models you already
have configured in OpenCode.

!!! warning "Memory is still data"

    Past sessions can contain commands, file excerpts, and decisions you would
    not normally share. This plugin stores everything locally and redacts
    secrets (see [Privacy and safety](#privacy-and-safety)), but review what it
    learns with `memory_inspect` and treat recalled context as a suggestion to
    verify, not as unquestioned truth.

## How the memory pipeline works

The plugin implements the same two-phase pipeline as Codex:

1. **Extract** — Once a session has been idle long enough (default 6 hours), a
   background pass summarizes it into raw memories using your `small_model`.
2. **Consolidate** — A second pass (using your main model) merges durable raw
   memories into a compact summary index.

During later sessions a token-budgeted summary is injected into the system
prompt, and dedicated tools let the agent fetch details on demand:

| Tool | Purpose |
| :--- | :------ |
| `memory_read` | Read a specific memory entry |
| `memory_search` | Search memory by query |
| `memory_list` | List recent or filtered memories |
| `memory_add_note` | Save an explicit note ("remember that ...") |
| `memory_inspect` | Show effective options, jobs, and health |
| `memory_reset` | Wipe memory and start over |
| `memory_mode` | Turn background learning or injection on/off |

!!! tip "The mental model"
    Think of it as learning, remembering, and forgetting. The project explains
    the design in
    [How OpenCode Codex Memory works](https://github.com/moritzfl/opencode-codex-memory/blob/main/docs/how-ai-memory-works.md).

---

## Installation

### Quick Start

Add the pinned plugin to your OpenCode config at `~/.config/opencode/opencode.json`:

```json
{
  "plugin": ["opencode-codex-memory@0.7.2"]
}
```

That is it. The memory workspace is created on first use and background
learning starts immediately. Requires **OpenCode 1.18 or newer**.

!!! tip "Pin the version"

    OpenCode installs a plugin spec once and never re-resolves it, so a bare
    `"opencode-codex-memory"` is not "always latest". Pin an explicit version
    and check [npm](https://www.npmjs.com/package/opencode-codex-memory) when
    you bump it.

### Optional model tuning

To set options, turn the plugin entry into a `[name, options]` pair. For
example, to make extraction use a specific cheap model and shorten the idle
wait for testing:

```json
{
  "plugin": [
    ["opencode-codex-memory@0.7.2", { "extract_model": "opencode-zen/big-pickle", "min_rollout_idle_hours": 1 }]
  ]
}
```

Model precedence per phase: plugin option (`extract_model` / `consolidation_model`)
→ OpenCode config (`small_model` / `model`) → a `model` on your own
`memorize-extract`/`memorize` agent definition, if you overrode one → the
provider's default model.

---

## Where your data lives

Everything is stored under OpenCode's own data directory —
`$XDG_DATA_HOME/opencode`, otherwise `~/.local/share/opencode`:

```
~/.local/share/opencode/
├── memory.db                       # the plugin's own SQLite database
└── memories/
    ├── memory_summary.md           # compact summary injected into the system prompt
    ├── MEMORY.md                   # searchable index of everything learned
    ├── rollout_summaries/          # one recap per past session
    ├── skills/                     # reusable procedures discovered over time
    └── extensions/ad_hoc/notes/    # things you explicitly asked it to remember
```

!!! note "Local-first by design"

    Memory is plain markdown files plus a small SQLite database on your own
    machine. There is no memory service, no MCP server, no separate process,
    and no sync. You can read it, grep it, edit it, or delete it like anything
    else you own. Nothing leaves your machine beyond the model calls OpenCode
    already makes.

---

## Privacy and safety

- **Local only.** There is no remote storage option to enable. Storage goes
  through a backend interface whose only implementation is the local
  filesystem. The plugin holds no API keys of its own.
- **Secrets are redacted** — API keys, tokens, private keys, and passwords are
  stripped from session transcripts and extracted memories before anything is
  written or sent to a model. Notes you explicitly dictate are stored as you
  said them.
- **Learning agents are sandboxed.** The extraction agent cannot touch your
  filesystem; the consolidation agent gets only file tools plus access to the
  memory folder. Shell, network, IDE, and MCP tools are denied for both.
- **Reset is safe.** `memory_reset` refuses to run if the memory folder is a
  symlink, so it cannot be tricked into deleting something else.
- **Web/MCP sessions:** by default, sessions that used web search, fetch, or
  MCP tools are still eligible for memory. To exclude them — so scraped or
  external content cannot enter memory — set `disable_on_external_context: true`.

---

## Configuration

All options are optional and have sensible defaults; names match Codex's
`[memories]` config so the two stay easy to compare:

| Option | Default | Meaning |
| :----- | :------ | :------ |
| `generate_memories` | `true` | Turn the background learning pipeline on/off |
| `use_memories` | `true` | Inject the memory summary into the system prompt |
| `dedicated_tools` | `true` | Expose the `memory_read`/`memory_search`/`memory_list`/`memory_add_note` tools |
| `disable_on_external_context` | `false` | Exclude sessions that used web/MCP tools from memory |
| `extract_model` | OpenCode `small_model` | Model used for per-session extraction |
| `consolidation_model` | OpenCode `model` | Model used for consolidation |
| `max_raw_memories_for_consolidation` | `256` | How many raw memories feed each consolidation pass |
| `max_rollout_age_days` | `10` | Ignore sessions older than this for extraction |
| `min_rollout_idle_hours` | `6` | How long a session must be idle before it is eligible |
| `max_rollouts_per_startup` | `2` | Max sessions extracted per pass |
| `max_unused_days` | `30` | Prune memories unused for this long |

Numeric options are clamped to Codex's valid ranges. The plugin never
hard-fails on bad options — run `memory_inspect` to see what actually took
effect (it echoes effective options after clamping and warns about unknown or
malformed keys).

---

## Backing up

Back up the whole OpenCode data directory **while OpenCode is stopped**. The
SQLite database and `memories/` workspace are a pair — restoring only one can
leave job state, Git baseline, and memory files out of sync. Include hidden
files (especially `memories/.git/`) and SQLite sidecars (`memory.db-wal`,
`memory.db-shm`) when present. Restore by replacing the data directory with
the backup copy, never by copying single files into a running instance.

---

## Troubleshooting

When memory does not seem to build, ask the agent to run **`memory_inspect`**.
It reports stage-1 job counts and failure classes, provider quota backoffs,
phase-2 status, effective options, and an eligibility reminder.

| Symptom | Likely cause |
| :------ | :----------- |
| No stage-1 outputs yet | Sessions must stay idle at least `min_rollout_idle_hours` (default 6). For a quick local check, set `"min_rollout_idle_hours": 1`. |
| Discovery failed | Host API unavailable; inspect shows the error. Retry after restarting OpenCode. |
| Pin stuck on old version | OpenCode freezes bare package specs; pin an explicit version and bump it. |
| Consolidation never runs | Check `phase2_status` and `phase2_last_error`; failed artifacts keep the workspace diff for the next run. |
| `stage1_error` mentions usage/rate limit | Temporary provider quota; jobs retry automatically once quota returns. |

---

## Why one global memory?

There is a single store for everything you do, not one per project. Codex
started with per-project memory and deliberately removed it in early 2026:
scope boundaries are hard to draw (which project does "prefers table-driven
tests" belong to?), and the most valuable lessons — about how you work — belong
to no project at all. Memories carry the project they came from, and the
consolidator keeps per-project detail separable as soft hints rather than hard
partitions. The cost is that an unrelated project's details can surface in the
summary; the plugin mirrors Codex's judgment that this is cheaper than the
alternative.

---

## Why not a memory plugin that writes into the repo?

Some memory plugins for agent tools generate context blocks and write them
straight into committed files such as `AGENTS.md` or `README.md`. That pattern
is fragile: formatters can corrupt the injected tables, the blocks accumulate
duplicated session state, and a repo's governance documents get consumed by
machine-generated noise. This plugin deliberately keeps **all** memory in
`~/.local/share/opencode/` — outside any project — and injects context through
the system prompt instead of editing your files. Your committed documentation
stays exactly what you wrote.

---

!!! note "Review status"

    Last editorial review: 2026-09-18. Installation, options, and behavior
    reflect opencode-codex-memory v0.7.2; verify against the plugin's current
    release before relying on a particular workflow.

## Further Reading

- [Changelog](https://github.com/moritzfl/opencode-codex-memory/blob/main/CHANGELOG.md)
- [How OpenCode Codex Memory works](https://github.com/moritzfl/opencode-codex-memory/blob/main/docs/how-ai-memory-works.md)
- [OpenCode 2 notes](https://github.com/moritzfl/opencode-codex-memory/blob/main/docs/opencode2.md)
- [Architecture](https://github.com/moritzfl/opencode-codex-memory/blob/main/ARCHITECTURE.md)
- [OpenCode plugin docs](https://opencode.ai/docs/plugins/)

---

## Official Links

- [GitHub repository](https://github.com/moritzfl/opencode-codex-memory)
- [npm package](https://www.npmjs.com/package/opencode-codex-memory)
- [OpenCode](https://opencode.ai)
- [OpenAI Codex](https://github.com/openai/codex)