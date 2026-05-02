---
title: NotebookLM + OpenCode
icon: lucide/book-open
description: Tutorial for combining Google NotebookLM audio overviews with OpenCode - how to use NotebookLM generated audio files in your OpenCode workflow for context.
keywords:
  - NotebookLM
  - OpenCode
  - audio AI
  - Google NotebookLM
  - audio overview
  - tutorial
---

<p><img src="/assets/images/notebooklm-logo.png" alt="NotebookLM by Google" style="max-width:100%;width:400px;height:auto;display:block;margin:1em 0;" /></p>

A comprehensive guide to connecting Google NotebookLM with OpenCode for AI-powered research and development workflows.

## Table of Contents

1. [Quick Start](#quick-start-5-minutes) (5 minutes)
2. [Prerequisites](#prerequisites)
3. [Introduction](#introduction)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Authentication](#authentication)
7. [Tools Reference](#tools-reference)
8. [Usage Patterns](#usage-patterns)
9. [Suggestions & Prompts](#suggestions--prompts)
10. [Use Cases](#use-cases)
11. [Troubleshooting](#troubleshooting)

---

## Quick Start (5 Minutes)

This section gets you up and running fast. For detailed explanations, skip to the relevant sections below.

### Step 1: Install the MCP Server

```bash
# OpenCode - global config
mkdir -p ~/.config/opencode
cat >> ~/.config/opencode/opencode.json << 'EOF'
{
  "mcp": {
    "notebooklm": {
      "type": "local",
      "command": ["npx", "-y", "@pan-sec/notebooklm-mcp@latest"],
      "enabled": true
    }
  }
}
EOF
```

### Step 2: Get a Gemini API Key (Optional but Recommended)

1. Go to https://aistudio.google.com/app/apikey
2. Create a new API key
3. Add it to your config:

```bash
# Update config with API key
# (edit ~/.config/opencode/opencode.json and add GEMINI_API_KEY)
```

### Step 3: Verify Installation

```bash
opencode

# In the terminal, type:
> List my notebooks
```

### Step 4: Authenticate

On first use, Chrome opens automatically:

1. Log into your Google account
2. Done! Close Chrome when logged in

**You're ready!** Continue to [Usage Patterns](#usage-patterns) for how to use this in your workflow.

---

## Prerequisites

Before starting, ensure you have:

| Requirement                   | Version | Check Command              |
| :---------- | :------ | :------------ |
| **Node.js**                   | 18+     | `node --version`           |
| **npm**                       | 9+      | `npm --version`            |
| **Google Chrome**             | Latest  | `chrome --version`         |
| **Google Account**            | -       | -                          |
| **Gemini API Key** (optional) | -       | Get at aistudio.google.com |

!!! tip "Before You Start"

    **This guide assumes you have:**
    
    - OpenCode installed (`curl -fsSL https://opencode.ai/install.sh | sh`)
    - Node.js 18+ persistently installed
    
    **Node.js not working?** See [OpenCode Prerequisites](../opencode-guide.md#prerequisites) for setup.

### Quick Node.js Verification

??? tip "Verify Node.js"

    Open a BRAND NEW terminal, run:
    ```bash
    node --version
    ```
    Should show v18+ or v20+

### Using npx with pnpm/mise

The MCP commands use `npx` because it comes with npm. If you prefer pnpm, use:

```json
{
  "mcp": {
    "notebooklm": {
      "command": ["pnpm", "exec", "@pan-sec/notebooklm-mcp@latest"],
      ...
    }
  }
}
```

**With mise:**

```json
{
  "mcp": {
    "notebooklm": {
      "command": ["mise", "exec", "--", "notebooklm-mcp"],
      ...
    }
  }
}
```

### Platform-Specific Notes

**macOS:**

- Chrome usually pre-installed
- Use Safari-Chrome CDP if Chrome not available

**Linux:**

- Install Chromium: `sudo apt install chromium-browser`
- Or use Google Chrome directly

**Windows:**

- WSL2 recommended for best experience
- Or use Chrome on Windows directly

---

## Introduction

### What is NotebookLM?

Google NotebookLM is an AI-powered research assistant that:

- Reads and understands your uploaded sources (PDFs, Google Docs, URLs, YouTube)
- Generates audio summaries (Audio Overview)
- Creates flashcards, timelines, and infographics
- Answers questions about your specific documents
- Keeps answers grounded in your source material

### Why Integrate with OpenCode?

| Without Integration    | With Integration                   |
| :------------------ | :--------------- |
| Manual document upload | Auto-add sources from terminal     |
| Copy-paste research    | Query notebooks directly           |
| Single-document focus  | Cross-reference multiple notebooks |
| Browser-only access    | CLI automation                     |
| Limited automation     | Scriptable workflows               |

### Architecture Overview

```
┌─────────────┐     MCP      ┌─────────────┐
│  OpenCode   │ ──────────►  │ NotebookLM  │
│  (Terminal) │              │ MCP Server  │
└─────────────┘              └─────────────┘
                                    │
                                    ▼
                            ┌─────────────┐
                            │   Gemini    │
                            │    API      │
                            └─────────────┘
```

### Which Integration Method Should You Choose?

| Method              | Best For               | Difficulty | Security |
| :----- | :------- | :--------- | :------- |
| **MCP Server**      | Most users, enterprise | Easy       | ★★★★★    |
| **OpenCode Plugin** | Plugin developers      | Medium     | ★★★★☆    |
| **Local Build**     | Customization needs    | Hard       | ★★★★★    |

**Recommendation:** Start with MCP Server. Switch only if you need customization.

---

## Installation

### Option 1: Using MCP (Recommended)

The secure MCP server approach with enterprise-grade security.

#### Quick Install

```bash
# For Claude Code/Desktop
claude mcp add notebooklm -- npx @pan-sec/notebooklm-mcp@latest

# For OpenCode - add to opencode.json
{
  "mcp": {
    "notebooklm": {
      "type": "local",
      "command": ["npx", "-y", "@pan-sec/notebooklm-mcp@latest"],
      "enabled": true,
      "environment": {
        "GEMINI_API_KEY": "your-gemini-api-key"
      }
    }
  }
}
```

#### With Authentication + Gemini (Recommended)

```bash
claude mcp add notebooklm \
  --env NLMCP_AUTH_ENABLED=true \
  --env NLMCP_AUTH_TOKEN=$(openssl rand -base64 32) \
  --env GEMINI_API_KEY=your-gemini-api-key
```

### Option 2: OpenCode Plugin

```bash
# Just add to config - OpenCode auto-installs npm plugins at startup
# No need to run 'bun add' manually

# Add to opencode.json
{
  "plugins": ["opencode-plugin-notebooklm"]
}
```

> **Tip:** OpenCode auto-installs plugins from the `plugins` array. You only need `bun add` if developing the plugin locally.

### Option 3: Local Build

```bash
# Clone and build from source
git clone https://github.com/Pantheon-Security/notebooklm-mcp-secure.git
cd notebooklm-mcp-secure
npm install
npm run build

# Add to opencode.json
{
  "mcp": {
    "notebooklm": {
      "type": "local",
      "command": ["node", "dist/index.js"],
      "enabled": true
    }
  }
}
```

---

## Configuration

### Basic Configuration

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "notebooklm": {
      "type": "local",
      "command": ["npx", "-y", "@pan-sec/notebooklm-mcp@latest"],
      "enabled": true
    }
  }
}
```

### Advanced Configuration

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "notebooklm": {
      "type": "local",
      "command": ["npx", "-y", "@pan-sec/notebooklm-mcp@latest"],
      "enabled": true,
      "environment": {
        "GEMINI_API_KEY": "your-gemini-api-key",
        "NOTEBOOKLM_NO_GEMINI": "false",
        "NLMCP_AUTH_ENABLED": "true",
        "NLMCP_AUTH_TOKEN": "your-secure-token"
      }
    }
  }
}
```

### Project-Level MCP

Create `.opencode/` directory in your project:

```bash
mkdir -p .opencode
```

Add `opencode.json` with MCP configuration to your project root.

---

## Authentication

### First-Time Setup

The first time you use any NotebookLM tool, Chrome will open automatically:

1. Chrome opens with NotebookLM
2. Log in to your Google account
3. Done! Chrome can be closed after login
4. Plugin extracts cookies automatically

### Manual Authentication (Fallback)

If auto-auth fails:

```bash
# Get cookies from DevTools
# 1. Open https://notebooklm.google.com in Chrome
# 2. Open DevTools (F12) > Network tab
# 3. Refresh page, click any request
# 4. Copy the Cookie header value

# Save using the tool
save_auth_tokens({ cookies: "your-cookie-header-from-devtools" })
```

### Auth Recovery

When auth expires, the plugin attempts 4-layer recovery:

1. **Refresh CSRF** - Re-extract tokens from page
2. **Disk Reload** - Load cached auth
3. **CDP Auto-refresh** - Auto-launch Chrome
4. **Manual Auth** - Fallback to manual steps

---

## Tools Reference

### Core Tools

| Tool                    | Description                               |
| :--- | :---------- |
| `notebook_query`        | Query your notebook with natural language |
| `notebook_list`         | List all your notebooks                   |
| `notebook_create`       | Create a new notebook                     |
| `notebook_add_source`   | Add sources (URLs, PDFs, Google Drive)    |
| `notebook_get_audio`    | Generate audio overview                   |
| `notebook_get_insights` | Get auto-generated insights               |
| `save_auth_tokens`      | Save cookies (manual auth fallback)       |

### Tool Examples

#### Query a Notebook

```bash
# Ask questions about your sources
notebook_query({
  query: "What are the main security considerations?",
  notebook_id: "optional-notebook-id"
})
```

#### List Notebooks

```bash
notebook_list({})
```

#### Create a Notebook

```bash
notebook_create({
  name: "OpenCode Research",
  description: "Research for project integration"
})
```

#### Add Sources

```bash
# Add a URL
notebook_add_source({
  source: "https://docs.example.com/guide",
  notebook_id: "your-notebook-id"
})

# Add Google Drive file
notebook_add_source({
  source: "gdrive://document-id",
  notebook_id: "your-notebook-id"
})
```

#### Generate Audio Overview

```bash
# Create audio summary
notebook_get_audio({
  notebook_id: "your-notebook-id"
})
```

---

## Usage Patterns

### Pattern 1: Research-First Development

```bash
# Start new task
opencode

# Query research before coding
> Load the API documentation from https://api.example.com/docs and help me understand the authentication flow
```

### Pattern 2: Notebook QA

```bash
# Ask about your documents
> What's in my "Project Research" notebook? Summarize the key findings about authentication
```

### Pattern 3: Cross-Notebook Research

```bash
# Query multiple notebooks
> Compare the security approach in "Security Docs" notebook
  with the implementation in "Code Review" notebook
```

### Pattern 4: Automated Documentation

```bash
# Generate docs from sources
> Create a README.md for the authentication module based on the docs
  in my "API Documentation" notebook
```

### Pattern 5: Debugging with References

```bash
# Get expected behavior from specs
notebook_query({
  query: "What should happen when payment fails?",
  notebook_id: "api-specs"
})

# Then in OpenCode
> Fix the payment error handling to match the spec
```

### Pattern 6: Learning New Codebases

```bash
# Get architecture from docs
notebook_query({
  query: "Explain the system architecture and data flow",
  notebook_id: "architecture"
})

# In OpenCode
> Map this to our codebase - show me the equivalent code
```

---

## Complete Workflow Examples

### Example 1: Implementing a New Feature

This is the most common workflow - research, then implement.

```
# Session 1: Research
> Create a new notebook called "Auth0 Integration"
> Add the Auth0 documentation from https://auth0.com/docs
> What are the steps to implement SSO login?

# Session 2: Implementation (after getting research)
> Implement the auth0-login feature following the steps in my "Auth0 Integration" notebook
```

### Example 2: Code Review with Standards

```
# Session 1: Get standards
> What are our security standards for API keys?

# Session 2: Apply to code
> Review src/api-keys.ts against the security standards in my notebook
```

### Example 3: Bug Fix with Context

```
# Session 1: Get spec
> How should token refresh work according to the API docs?

# Session 2: Fix
> Fix the token refresh logic - it's not handling expiry correctly
```

---

## Suggestions & Prompts

### Research Prompts

```
"Search the web for [topic] and add the top 3 results to my [notebook-name] notebook"

"Summarize the key points from [URL] and add it to [notebook-name]"

"What are the latest best practices for [technology name]? Search the web and create a notebook"
```

### Development Prompts

```
"Read my [notebook-name] notebook and help me implement a [feature]"

"Based on the research in [notebook-name], write the code for [component]"

"Review the implementation in [notebook-name] and suggest improvements"
```

### Documentation Prompts

```
"Create documentation for [module] using [notebook-name] as reference"

"Write a README based on the architecture docs in my notebook"

"Generate API documentation from the spec in [notebook]"
```

### Code Review Prompts

```
"Review my code changes against the security guidelines in [notebook-name]"

"Check if my implementation follows the patterns in [notebook-name]"

"Are there any deviations from the standards in [notebook-name]?"
```

### Multi-Notebook Prompts

```
"Compare the authentication approach in [notebook-1] with [notebook-2]"

"What overlapping topics exist across [notebook-1] and [notebook-2]?"

"Create a summary combining insights from all my research notebooks"
```

---

## Use Cases

### 1. Technical Research

**Scenario**: Researching a new technology before implementation

```bash
# Create research notebook
notebook_create({ name: "React Server Components Research" })

# Add sources
notebook_add_source({
  source: "https://react.dev/reference/rsc",
  notebook_id: "your-notebook-id"
})

# Query for implementation guide
notebook_query({
  query: "How do I implement server components? What's the migration path?",
  notebook_id: "your-notebook-id"
})
```

**Result**: Get implementation guidance grounded in official docs.

### 2. Security Review

**Scenario**: Reviewing code against security standards

```bash
# Query secure coding guidelines
notebook_query({
  query: "What are the OWASP security guidelines for authentication?",
  notebook_id: "security-guidelines"
})

# Then in OpenCode
> Review src/auth.ts against these guidelines
```

### 3. Architecture Decision

**Scenario**: Making informed architecture decisions

```bash
# Research options
notebook_query({
  query: "Compare REST vs GraphQL vs tRPC for a real-time chat application",
  notebook_id: "architecture-research"
})

# Get Gemini-powered analysis
notebook_query({
  query: "What's the recommended approach for our use case?",
  notebook_id: "architecture-research"
})
```

### 4. API Integration

**Scenario**: Integrating with third-party APIs

```bash
# Research API
notebook_query({
  query: "What are the rate limits and authentication requirements?",
  notebook_id: "api-docs"
})

# In OpenCode
> Implement the API client following these requirements
```

### 5. Debugging with Context

**Scenario**: Debugging with relevant docs in context

```bash
# Get relevant documentation
notebook_query({
  query: "How does error handling work in the payment API?",
  notebook_id: "api-docs"
})

# In OpenCode
> Fix the payment error handling based on the API docs
```

### 6. Learning New Codebases

**Scenario**: Understanding unfamiliar code

```bash
# Get architecture overview
notebook_query({
  query: "What's the overall architecture and data flow?",
  notebook_id: "architecture-docs"
})

# In OpenCode
> Explain the authentication flow in this codebase
```

### 7. Writing Documentation

**Scenario**: Creating accurate documentation

```bash
# Get technical details
notebook_query({
  query: "What are all the configuration options and their defaults?",
  notebook_id: "technical-specs"
})

# In OpenCode
> Write API documentation based on this specification
```

### 8. Bug Investigation

**Scenario**: Investigating bugs with reference docs

```bash
# Get expected behavior
notebook_query({
  query: "What should happen when a token expires during a request?",
  notebook_id: "specs"
})

# In OpenCode
> The current implementation doesn't match the spec. Fix it.
```

### 9. Automated Reports

**Scenario**: Generating status reports

```bash
# Query current state
notebook_query({
  query: "What's the current project status and blockers?",
  notebook_id: "project-status"
})
```

### 10. Knowledge Management

**Scenario**: Managing team knowledge

```bash
# Add new learnings
notebook_add_source({
  source: "https://engineering.example.com/post",
  notebook_id: "team-knowledge"
})

# Query for decision-making
notebook_query({
  query: "What's our standard approach for database migrations?",
  notebook_id: "team-knowledge"
})
```

---

## Troubleshooting

### MCP Server Not Starting

```bash
# Check if npx works
npx @pan-sec/notebooklm-mcp@latest --help

# Try running directly
node dist/index.js
```

### Authentication Issues

```bash
# Re-authenticate
# 1. Close all Chrome windows
# 2. Run any NotebookLM tool
# 3. Complete auth in browser

# Manual fallback
save_auth_tokens({ cookies: "your-cookies" })
```

### Timeout Issues

Increase timeout in config:

```json
{
  "mcp": {
    "notebooklm": {
      "timeout": 120000
    }
  }
}
```

### Rate Limiting

If hitting rate limits:

1. Add your Gemini API key for higher limits
2. Use `NOTEBOOKLM_NO_GEMINI=false` (default)

```json
{
  "environment": {
    "GEMINI_API_KEY": "your-key"
  }
}
```

### Notebook Not Found

Auto-infer notebook from context:

```
# Set context first
# No need to specify notebook_id if context is set

notebook_query({ query: "What are the main topics?" })
```

---

## FAQ - Frequently Asked Questions

### General Questions

**Q: Is NotebookLM free?**
A: Yes, the base features are free. Audio Overview is free for under 90 minutes/week.

**Q: Do I need a Gemini API key?**
A: No, but it gives you higher rate limits and better answers. Get one at aistudio.google.com

**Q: Can I use this with any NotebookLM notebook?**
A: Yes, if you have access to it in your Google account, you can query it.

**Q: How is this different from using NotebookLM in browser?**
A: You get CLI automation, can script workflows, and integrate into your dev process.

### Technical Questions

**Q: Why does Chrome open?**
A: The MCP uses Chrome DevTools Protocol (CDP) to authenticate and interact with NotebookLM's web interface.

**Q: My auth keeps expiring - what do I do?**
A: The 4-layer recovery should handle this. If not, try logging out and back in via the browser that opens.

**Q: Can I use this without Chrome?**
A: No, CDP requires Chrome. Alternatively, use the OpenCode plugin with manual token management.

**Q: Does this store my data?**
A: No. All data stays on Google's servers. The MCP just queries your notebooks.

### Troubleshooting Questions

**Q: "MCP server not found" error**
A: Try running: `npx @pan-sec/notebooklm-mcp@latest --version` to verify installation.

**Q: "Not authenticated" but I logged in**
A: Close Chrome completely, then try again. The CDP session may be stale.

**Q: Rate limit errors**
A: Add your Gemini API key for higher limits, or wait and retry.

---

## Newcomer Guide

### If You're New to OpenCode

1. **Install OpenCode first:**

   ```bash
   curl -fsSL https://opencode.ai/install.sh | sh
   ```

2. **Connect a model:**

   ```bash
   opencode
   /connect
   ```

3. **Test with a simple question:**

   ```bash
   > Hello! What can you help me with?
   ```

4. **Then add MCP:**
   - Edit `~/.config/opencode/opencode.json`
   - Add the MCP config from [Quick Start](#quick-start-5-minutes)

### If You're New to NotebookLM

1. **Go to notebooklm.google.com**
2. **Create your first notebook** - click "+ New notebook"
3. **Add a source** - paste a URL, upload a PDF, or add a Google Doc
4. **Ask a question** - type in the chat at the bottom
5. **Try Audio Overview** - click "Generate" to hear a podcast summary

Then come back here to connect it with OpenCode!

### Quick Command Reference

```
# In OpenCode terminal
/notebooklm          # List available tools
/notebooklm query    # Query a notebook
/notebooklm list     # List notebooks
/notebooklm create   # Create notebook
/notebooklm add      # Add source
```

---

## Resources

### Official Documentation

- [NotebookLM MCP Server](https://github.com/Pantheon-Security/notebooklm-mcp-secure)
- [OpenCode Plugin](https://github.com/nghyane/opencode-plugin-notebooklm)
- [OpenCode MCP Docs](https://opencode-tutorial.com/en/docs/mcp-servers)
- [OpenCode Download](https://opencode.ai/download)

### NotebookLM Resources

- [NotebookLM Official](https://notebooklm.google.com)
- [NotebookLM Help](https://support.google.com/notebooklm)
- [Audio Overview Guide](https://support.google.com/notebooklm/answer/151189)

### Community

- [OpenCode Discord](https://opencode.ai/discord)
- [MCP Server Issues](https://github.com/Pantheon-Security/notebooklm-mcp-secure/issues)

---

## Changelog

| Version | Date       | Changes                                    |
| :------ | :--- | :------ |
| 1.0     | April 2026 | Initial tutorial                           |
| 1.1     | April 2026 | Added Quick Start, FAQ, Newcomer Guide     |
| 1.2     | April 2026 | Added workflow examples, improved patterns |

---

_Tutorial last updated: April 2026_
