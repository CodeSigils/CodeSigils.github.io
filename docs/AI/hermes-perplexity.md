---
title: Perplexity via Composio with Hermes
icon: lucide/search
description: Connect Perplexity AI to Hermes via Composio CLI or MCP — for AI search, summarization, and multi-turn queries.
keywords:
  - hermes
  - perplexity
  - composio
  - MCP
  - AI search
  - Nous Research
  - open source
---

Perplexity via Composio is straightforward using either the CLI or MCP method. Both handle authentication securely and enable tasks like AI search, summarization, and multi-turn queries.

## Prerequisites

Install Node.js (v18+) and ensure Hermes is set up on your machine or server. Composio is SOC 2 Type 2 compliant, encrypting all credentials at rest and in transit.

## CLI Method (Recommended for Personal Use)

1. Install Composio CLI by running the install script or pasting `https://composio.dev/hermes` into Hermes chat — it handles installation automatically.

2. Prompt Hermes: **"Authenticate with Composio"** to link your account.

3. Ask Hermes: **"Connect to Perplexity"** or request a Perplexity task (e.g., "Summarize latest AI news via Perplexity") — it prompts OAuth authentication.

4. Test with a query like **"Generate a story about space travel using Perplexity"** — Hermes now accesses Perplexity tools natively via CLI commands.

## MCP Method (For Advanced/Remote Setups)

1. Visit [dashboard.composio.dev](https://dashboard.composio.dev), copy your Connect MCP URL and API key.

2. Edit Hermes config file (typically `~/.hermes/config.yaml` or via UI) to add the MCP endpoint:

```yaml
mcp_servers:
  - url: "YOUR_MCP_URL"
    api_key: "YOUR_API_KEY"
```

1. Restart Hermes and prompt **"Connect to Perplexity via MCP"** — it discovers and loads Perplexity tools dynamically.

2. Verify with a test: Hermes can now select models, refine queries, and retrieve cited answers and images.

## Verification and Tips

- Run `composio tools info perplexityai` in terminal to inspect tools and schemas.
- For cross-app workflows, connect more apps via Composio (e.g., Slack, Notion).
- Provide feedback to Hermes for better adaptation.
- If issues arise, check `composio dev logs tools` or the [Composio docs](https://docs.composio.dev).
