---
title: Open-Mem for OpenCode
description: A cautious guide to evaluating open-mem, a community memory plugin for OpenCode that captures and recalls project context.
keywords:
  - opencode
  - open-mem
  - memory
  - plugin
  - persistent
  - AI
---

There is a particular kind of frustration in a long coding project: you explain
the same decision to an assistant again because the useful context stayed in a
previous session. [open-mem](https://github.com/clopca/open-mem) is a community
plugin for [OpenCode](https://opencode.ai) that tries to address that gap by
capturing activity, compressing it into observations, and recalling selected
context later.

That convenience is also the reason to be careful. A memory plugin may see
commands, file contents, and prompts that you would not normally store. I would
test it on a small, non-sensitive project first and keep it only if the recalled
context is more useful than the review and privacy burden.

Its capture, compression, storage, and configuration behavior can change
between releases; verify the current plugin documentation before enabling it on
an important project.

!!! warning "Review captured data"

    Treat captured commands, file contents, and summaries as potentially
    sensitive. Inspect the plugin configuration and local database location
    before using it in a repository containing credentials or private data.

<div class="image-wrapper">
  <img src="/assets/images/opencode-screenshot.webp"
       alt="OpenCode with open-mem plugin"
       width="1200"
       height="978"
       loading="lazy" />
</div>

## How the memory pipeline works

open-mem describes a three-phase workflow:

1. **Capture** — When you read files, run commands, or edit code, it captures outputs.
2. **Compress** — During idle time, it turns captures into structured observations.
3. **Recall** — In a later session, a compact index can be injected into the prompt.

!!! tip "The Memory Pipeline"
    The project stores its observations in SQLite and supports types such as
    decisions, discoveries, bug fixes, features, refactors, and changes. Treat
    recalled context as a suggestion to inspect, not as unquestioned truth.

---

## Installation

### Quick Start (Recommended)

```bash
npx open-mem
```

This adds `open-mem` to your OpenCode plugin config automatically. It starts capturing from your next session.

!!! tip "Make the first run reversible"

    Try the plugin in a disposable repository, add `.open-mem/` to that
    repository's `.gitignore`, and inspect what it records before connecting an
    AI compression provider. A memory system is only useful when you trust what
    it remembers.

### Manual Installation

```bash
bun add open-mem
```

Then add to your OpenCode config at `~/.config/opencode/opencode.json`:

```json
{
  "plugin": ["open-mem"]
}
```

### AI Compression (Optional)

By default, open-mem uses a basic metadata extractor. For semantic compression, add an AI provider:

```bash
# Google Gemini (optional)
export GOOGLE_GENERATIVE_AI_API_KEY=your_key_here
```

Also supports Anthropic, AWS Bedrock, OpenAI, and OpenRouter. Auto-detects from environment variables.

---

## Memory Tools

open-mem provides tools for interacting with project memories:

| Tool | Purpose |
| :--- | :------ |
| `mem-find` | Search by query |
| `mem-create` | Save observations |
| `mem-history` | Browse session timeline |
| `mem-get` | Fetch full details |
| `mem-revise` | Update outdated memories |
| `mem-remove` | Remove obsolete memories |
| `mem-export` | Backup as JSON |
| `mem-import` | Restore from JSON |
| `mem-help` | Show guidance |

### Finding Memories

Search past memories by query:

```
mem-find({ query: "authentication bug", limit: 5 })
```

Returns matching observations with IDs and summaries. Use `mem-get` to fetch full details.

### Creating Memories

Save important observations:

```
mem-create({
  title: "Auth bypass vulnerability in login",
  type: "bugfix",
  narrative: "The login endpoint wasn't validating token expiration...",
  concepts: ["jwt", "authentication", "security"],
  importance: 10
})
```

### Memory Types

| Type | Use Case |
| :--- | :------- |
| `decision` | Architectural choices with rationale |
| `discovery` | Non-obvious findings, gotchas, constraints |
| `bugfix` | Bug root causes and fixes |
| `feature` | Feature implementations |
| `refactor` | Refactoring rationale |
| `change` | General changes |

### Browsing History

View session timeline:

```
mem-history({ limit: 10 })
```

Drill into specific sessions using `sessionId` from the results.

---

## Features

### Hybrid Search

Combines FTS5 full-text search, vector embeddings (via sqlite-vec), knowledge graph traversal, and Reciprocal Rank Fusion. No external vector database needed.

### Knowledge Graph

Automatic entity extraction with relationships. Graph-augmented search finds connections across sessions that keyword search would miss.

### Progressive disclosure

A token-budgeted index can be injected into the system prompt. The agent sees
*what* exists and decides *what to fetch*, reducing the need to load every
observation at once.

### Revision Lineage

Observations are immutable. Updates create new revisions that supersede the previous one. Deletes are tombstones with full audit trail.

### Privacy and retention

The project documents local storage in `.open-mem/` and redaction or exclusion
options. Verify those guarantees in the installed release, add the directory
to `.gitignore`, and inspect the database before sharing a repository. Local
storage does not by itself prevent a configured AI provider from receiving data
for compression.

!!! warning "Sensitive Data"
    Wrap sensitive content in `<private>` tags to exclude from memory entirely:
    ```
mem-create({
      narrative: "Used <private>API_KEY_123</private> for testing"
    })
    ```

---

## Multi-Platform Support

open-mem isn't limited to OpenCode. Dedicated adapters bring the same capabilities to other tools:

| Platform | Integration |
| :------- | :---------- |
| **OpenCode** | Native plugin (hooks + tools) |
| **Claude Code** | `bunx open-mem-claude-code --project /path/to/project` |
| **Cursor** | `bunx open-mem-cursor --project /path/to/project` |
| **Any MCP client** | `bunx open-mem-mcp --project /path/to/project` |

---

## Dashboard

Enable the web dashboard:

```bash
export OPEN_MEM_DASHBOARD=true
# Access at http://localhost:3737
```

The dashboard includes timeline, session, search, statistics, operations, and
settings views. Treat its controls as release-dependent and verify the current
documentation before relying on a particular workflow.

---

## Configuration

### Environment Variables

| Variable | Purpose |
| :------- | :------ |
| `OPEN_MEM_PROJECT` | Project directory path |
| `OPEN_MEM_DASHBOARD` | Enable dashboard |
| `GOOGLE_GENERATIVE_AI_API_KEY` | Google Gemini for compression |
| `ANTHROPIC_API_KEY` | Anthropic Claude |
| `OPENAI_API_KEY` | OpenAI GPT models |

### Custom Storage Location

```bash
export OPEN_MEM_PROJECT=/path/to/custom/project
```

---

## Troubleshooting

### Safe Database Reset

If you encounter database issues, use the maintenance CLI:

```bash
# Non-destructive WAL checkpoint
bunx open-mem-maintenance sqlite checkpoint --project /path/to/project --mode PASSIVE

# Non-destructive integrity check
bunx open-mem-maintenance sqlite integrity --project /path/to/project --max-errors 10

# Safe reset (blocked when active processes detected)
bunx open-mem-maintenance reset-db --project /path/to/project
```

!!! warning "Force Reset"
    Only use `--force` after stopping daemon and platform workers. This is destructive.

### Checking Health

For platform workers, check the queue mode:

```
{"command":"health"}
```

Returns `status.queue.mode`:

- `enqueue-only`: daemon healthy, worker signals `PROCESS_NOW`
- `in-process`: fallback mode when daemon unavailable

---

## Comparison with Alternatives

| Feature | open-mem | Typical Alternatives |
| :------ | :------- | :------------------- |
| **Vector search** | Embedded (sqlite-vec) | External service |
| **AI providers** | Multiple providers and fallback options | Varies |
| **Search** | FTS5 + Vector + RRF + Graph | FTS5 only |
| **Knowledge graph** | Yes | No |
| **Revision history** | Immutable lineage | No |
| **Dashboard** | Web UI with SSE | No |
| **Data storage** | Project-local | Global |
| **License** | MIT | AGPL / proprietary |

---

!!! note "Review status"

    Last editorial review: 2026-09-09. The installation and feature examples
    still require verification against the plugin's current release.

## Further Reading

- [Getting Started](https://github.com/clopca/open-mem/blob/main/docs/getting-started.md)
- [Architecture](https://github.com/clopca/open-mem/blob/main/docs/architecture.md)
- [Memory Tools Reference](https://github.com/clopca/open-mem/blob/main/docs/tools.md)
- [Search Documentation](https://github.com/clopca/open-mem/blob/main/docs/search.md)
- [Configuration](https://github.com/clopca/open-mem/blob/main/docs/configuration.md)
- [Privacy & Security](https://github.com/clopca/open-mem/blob/main/docs/privacy.md)
- [Platform Adapters](https://github.com/clopca/open-mem/blob/main/docs/platforms.md)
- [Troubleshooting](https://github.com/clopca/open-mem/blob/main/docs/troubleshooting.md)

---

## Official Links

- [GitHub repository](https://github.com/clopca/open-mem)
- [npm package](https://www.npmjs.com/package/open-mem)
- [Issue tracker](https://github.com/clopca/open-mem/issues)
