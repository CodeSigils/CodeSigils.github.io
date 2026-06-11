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
       alt="Perplexity AI via Composio" />
</div>

Perplexity via Composio is straightforward using either the CLI or MCP method. Both handle authentication securely and enable tasks like AI search, summarization, and multi-turn queries.

## Prerequisites

Install Node.js (v18+) and ensure Hermes is set up on your machine or server.

!!! tip "Security"
    Composio is SOC 2 Type 2 compliant, encrypting all credentials at rest and in transit.

## CLI Method (Recommended for Personal Use)

1. Install Composio CLI by running the install script or pasting `https://composio.dev/hermes` into Hermes chat — it handles installation automatically.
2. Prompt Hermes: **"Authenticate with Composio"** to link your account.

!!! warning "OAuth required on first use"
    The Composio MCP endpoint uses OAuth 2.1 PKCE. On first connection, you'll need to run `hermes mcp test composio` in an interactive terminal to complete the browser-based authorization flow. This cannot be done from a non-interactive session.

3. Ask Hermes: **"Connect to Perplexity"** or request a Perplexity task (e.g., "Summarize latest AI news via Perplexity") — it prompts OAuth authentication.
4. Test with a query like **"Generate a story about space travel using Perplexity"** — Hermes now accesses Perplexity tools natively via CLI commands.

Then Hermes will report after finishing setup:

```text
Here's what I've done and where things stand:

    Done:
    - Added composio MCP server to ~/.hermes/config.yaml at https://connect.composio.dev/MCP with OAuth auth
    - Server is enabled and listed in hermes mcp list

    The OAuth hurdle:

    The Composio MCP endpoint requires OAuth 2.1 PKCE authorization on first use. The MCP SDK tries to open a browser for the login flow, which can't complete in a non-interactive environment like this. The connection fails with "Session terminated" because the OAuth redirect can't be handled without browser interaction.

    To complete setup, run this once in an interactive terminal:


    hermes mcp test composio


    This will:
    1. Open a browser window for Composio OAuth login
    2. After you authorize, it'll show all available Composio tools (1000+ integrations)
    3. From there you can select which apps you want to connect

    What Composio gives you: 1000+ tool integrations including Gmail, GitHub, HubSpot, Salesforce, Slack, Linear, Notion, Airtable, Stripe, and many more. Since you've been working with GitHub and productivity tools, Composio would let you manage those directly through tool calls rather than browser automation.

    Want me to save this as a skill so we can revisit it, or would you prefer to run the interactive OAuth step now?
```

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

!!! tip "Inspect tools and schemas"
    Run `composio tools info perplexityai` in terminal to inspect tools and schemas. This shows the exact parameters available for Perplexity queries.

- For cross-app workflows, connect more apps via Composio (e.g., Slack, Notion).
- Provide feedback to Hermes for better adaptation.

!!! warning "Troubleshooting"
    If issues arise, check `composio dev logs tools` or the [Composio docs](https://docs.composio.dev).
