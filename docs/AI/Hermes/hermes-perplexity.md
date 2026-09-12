---
title: Perplexity via Composio with Hermes
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

<div class="image-wrapper">
  <img src="/assets/images/hermes-perplexity.jpg"
       alt="Perplexity AI via Composio"
       width="1200"
       height="630" />
</div>

This page describes two ways to connect Perplexity through Composio: the
Composio-assisted setup and a direct MCP configuration. The exact tools and
authentication screens may change, so use the current Composio dashboard and
Hermes MCP documentation when they differ from this example.

## Prerequisites

Ensure Hermes is installed and working on your machine or server. Install
Node.js only if the Composio CLI or a selected local MCP server requires it.

!!! warning "Review access before connecting"
    Composio can connect Hermes to external accounts. Read the requested scopes,
    connect only the Perplexity capability you need, and do not paste API keys
    into chat messages or commit them to `config.yaml`.

## CLI Method (Recommended for Personal Use)

1. Install the Composio CLI from the [official Composio setup page](https://composio.dev/hermes),
   or ask Hermes to use that setup link. The current installer command is:

   ```bash
   curl -fsSL https://composio.dev/install | bash
   ```

2. Prompt Hermes: **"Authenticate with Composio"** to link your account.

!!! warning "OAuth required on first use"
    The Composio MCP endpoint uses browser-based OAuth. Complete the first
    authorization in an interactive session; a headless session may require
    the redirect or authorization step to be completed separately.

3. Ask Hermes to connect to Perplexity or request a read-only task such as
   **"Find and summarize the latest official release notes for Zensical"**.
4. Confirm the returned sources and the connected tool name before attempting
   any action that writes to an external service.

After setup, verify the connection with:

```text
hermes mcp list
```

Look for a connected `composio` server and then run a small read-only query.

## MCP Method (For Advanced/Remote Setups)

1. Visit [Connect my agent in the Composio dashboard](https://dashboard.composio.dev/)
   and copy the current MCP connection instructions. Prefer the OAuth setup
   when it is available.
2. Edit Hermes config file (typically `~/.hermes/config.yaml`) with the URL
   and authentication shape supplied by Composio:

```yaml
mcp_servers:
  composio:
    url: "https://connect.composio.dev/mcp"
    auth: oauth
    timeout: 180
    connect_timeout: 60
```

3. Restart Hermes and run `hermes mcp list`.
4. Ask for a read-only Perplexity search, then inspect the returned citations.

## Verification and Tips

!!! tip "Inspect tools and schemas"
    Inspect the connected tools in Hermes before using them. Tool names and
    schemas are supplied by the current Composio connection and may change.

- For cross-app workflows, connect additional apps only when the task needs
  them, and review each requested scope.
- Treat Perplexity answers as research leads: open the cited sources and verify
  important claims independently.

!!! warning "Troubleshooting"
    If issues arise, check `composio dev logs tools` or the [Composio docs](https://docs.composio.dev).

## Verification

- **Last reviewed:** 2026-09-09
- **Primary sources:** [Composio Hermes setup](https://composio.dev/hermes), [Composio Connect MCP with Hermes](https://composio.dev/toolkits/composio_search/framework/hermes-agent), [Hermes MCP documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)
- **Scope:** Installer, OAuth-first setup, Hermes configuration shape, and safety guidance were checked against current primary documentation. Perplexity tool names, account requirements, and Composio dashboard labels may change.
