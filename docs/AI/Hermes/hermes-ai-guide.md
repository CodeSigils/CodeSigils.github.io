---
title: Hermes AI Agent Guide
description: Practical guide to Hermes Agent, including installation, memory, skills, MCP integrations, and cross-session workflows.
keywords:
  - hermes
  - AI agent
  - Nous Research
  - memory
  - MCP
  - autonomous agents
  - open source
---

<div class="image-wrapper">
  <img src="/assets/images/hermes-banner.png"
       alt="Hermes AI Agent"
       width="1145"
       height="196" />
</div>

Hermes is an AI agent built by Nous Research with persistent memory, skills,
and several ways to interact with it.

## What is Hermes AI Agent?

Hermes Agent is an autonomous assistant that can use tools, retain selected
context across sessions, and load reusable skills. These features are useful
when a task spans more than one conversation, but they also make it important
to understand what data is stored and which tools are enabled.

Unlike traditional AI coding assistants tethered to an IDE, Hermes can run in a
local terminal, a container, or a hosted environment.

!!! info "Technical jargon → In plain language"

    **Technical jargon:** MCP (Model Context Protocol) lets Hermes connect to
    tools that run outside the agent itself.

    **In plain language:** You can add a compatible server so Hermes can use a
    browser, database, or other external service.

    **Why it matters:** Each connection expands what Hermes can access, so add
    only the servers and tools needed for the task.

## Key Capabilities

### Multi-Platform Messaging

Access Hermes from multiple platforms:

- CLI (Terminal)
- Telegram
- Discord
- Slack
- WhatsApp
- Signal
- Email
- And more...

### Memory and Skills

- **Memory system** — Selected context can persist across sessions
- **Skills** — Reusable `SKILL.md` instructions can be loaded for specific tasks
- **Cross-session recall** — Stored observations can be searched and summarized

!!! warning "Review what the agent can access"

    Hermes can run terminal commands, read and modify files, use networked
    services, and connect to external MCP servers. Start with the smallest
    useful toolset, keep credentials out of prompts and configuration files,
    and use a separate test project until the workflow is understood.

### Built-in Tools

| Category | Tools |
| :------- | :---- |
| Web | `web_search`, `web_extract` |
| Terminal | `terminal`, `process`, `file` ops |
| Browser | `browser_navigate`, `browser_snapshot`, `browser_vision` |
| Vision | `vision_analyze`, `image_generate` |
| Memory | `memory`, `session_search` |
| Automation | `cronjob`, `send_message` |
| Delegation | Delegate subagents |

### Research and extension surfaces

- **Batch Trajectory Generation** — Generate training data at scale
- **Atropos RL** — Reinforcement learning environments
- **MCP integration** — Connect compatible external tool servers
- **Tool-calling Training** — Export to ShareGPT format

<div class="youtube-video-wrapper">
  <iframe src="https://www.youtube.com/embed/YtfROZK1BDM" title="Hermes Agent overview video" allowfullscreen></iframe>
</div>

## Installation

!!! tip "Quick Install"

    ```bash
    curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
    ```

After installation:

```bash
source ~/.bashrc  # or source ~/.zshrc
hermes  # Start chatting!
```

## Quick Start

```bash
# Interactive setup (recommended first run)
hermes setup --portal

# Interactive CLI
hermes chat

# Choose or change your model provider later
hermes model

# Configure toolsets
hermes tools

# Check the installation and configuration
hermes doctor

# Start messaging gateway
hermes gateway
```

## Use Cases

### For Common Users

**Personal AI Assistant**

- Daily task automation
- Research and summarization
- Writing and editing
- Calendar and schedule management

**Learning Companion**

- Explain complex topics
- Create study guides
- Quiz generation
- Cross-session memory of your learning progress

**Productivity Booster**

- Email drafting
- Meeting summaries
- Content creation
- Automated reminders via cron

### For Researchers

**RL Training**

- Atropos RL environments
- Trajectory generation for model training
- Tool-call data export

**Multi-Model Comparison**

- Mixture of Agents (MOA) routing
- Multiple models via OpenRouter
- Benchmark workflows

**Agent Architecture Research**

- Multi-agent orchestration
- Skill systems (agentskills.io compatible)
- Memory and personality modeling

### For Developers

**Coding Assistant**

- Full terminal access
- Git integration
- File operations
- Browser automation for web testing

**DevOps Automation**

- SSH/Docker/Singularity backends
- Cron scheduling with delivery
- MCP server integration

**Custom Skill Development**

- Create reusable skills
- Skill sharing via agentskills.io
- Plugin system

## Configuration

### Models

Hermes supports multiple providers:

```bash
# Set provider
hermes model

# Provider options change over time; use the interactive list rather than
# relying on a static list in an article.
```

### Toolsets

```bash
# Enable specific toolsets
hermes chat --toolsets "web,terminal,file,browser"

# View all available
hermes tools
```

### Gateway Setup

```bash
# Set up Telegram/Discord/etc
hermes gateway setup
hermes gateway start
```

## Verification

- **Last reviewed:** 2026-09-09
- **Primary sources:** [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs/), [Hermes quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart), [MCP documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)
- **Scope:** Installation, first-run commands, memory/skills wording, and MCP guidance were checked against the current official documentation. Provider names, tool availability, and messaging integrations may change.

## Resources

- [Official Documentation](https://hermes-agent.nousresearch.com/docs/)
- [GitHub Repository](https://github.com/NousResearch/hermes-agent)
- [Discord Community](https://discord.gg/NousResearch)
- [Skills Hub](https://agentskills.io)

---
