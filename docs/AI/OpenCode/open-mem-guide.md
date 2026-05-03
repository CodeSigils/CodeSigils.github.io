---
title: Open-Mem Plugin
icon: lucide/brain
description: Persistent memory system for OpenCode - automatic session capture, AI compression, and context injection across coding sessions.
keywords:
  - opencode
  - open-mem
  - memory
  - plugin
  - persistent
  - AI
---

open-mem is a plugin for [OpenCode](https://opencode.ai) that gives your AI assistant memory across sessions. It runs in the background, capturing what you do, compressing it into structured observations, and recalling it next session.

<div class="image-wrapper">
  <img src="/assets/images/opencode-screenshot.webp"
       alt="OpenCode with open-mem plugin" />
</div>

## What It Does

open-mem provides persistent memory for AI coding assistants through a three-phase workflow:

1. **Capture** — When you read files, run commands, or edit code, open-mem captures the outputs
2. **Compress** — During idle time, AI compresses captures into structured observations
3. **Recall** — Next session, a compact summary injects into the system prompt

!!! tip "The Memory Pipeline"
    open-mem captures tool executions automatically, compresses them using AI into typed observations (decision, bugfix, feature, refactor, discovery, change), and stores everything in a local SQLite database. The next session starts with context from where you left off.

---

## Installation

### Quick Start (Recommended)

```bash
npx open-mem
```

This adds `open-mem` to your OpenCode plugin config automatically. It starts capturing from your next session.

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
# Google Gemini — free tier available
export GOOGLE_GENERATIVE_AL_API_KEY=your_key_here
```

Also supports Anthropic, AWS Bedrock, OpenAI, and OpenRouter. Auto-detects from environment variables.

---

## Memory Tools

open-mem provides 9 memory tools for interacting with your project memories:

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

### Progressive Disclosure

A token-budgeted index injects into the system prompt. The agent sees *what* exists and decides *what to fetch*. Typical compression ratio: ~96%.

### Revision Lineage

Observations are immutable. Updates create new revisions that supersede the previous one. Deletes are tombstones with full audit trail.

### Privacy First

All data stored locally in `.open-mem/`. Automatic redaction of API keys, tokens, passwords. Use `<private>` tags to exclude content entirely.

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

Six pages: Timeline, Sessions, Search, Stats, Operations, Settings. The Settings page doubles as a config control plane with live preview and rollback.

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
| **AI providers** | 5 + fallback chain | 1–3 |
| **Search** | FTS5 + Vector + RRF + Graph | FTS5 only |
| **Knowledge graph** | Yes | No |
| **Revision history** | Immutable lineage | No |
| **Dashboard** | Web UI with SSE | No |
| **Data storage** | Project-local | Global |
| **License** | MIT | AGPL / proprietary |

---

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

- **GitHub**: https://github.com/clopca/open-mem
- **npm**: https://www.npmjs.com/package/open-mem
- **Issues**: https://github.com/clopca/open-mem/issues
