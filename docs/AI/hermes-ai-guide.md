---
title: Hermes AI Agent Guide
icon: lucide/cpu
---

![Hermes AI Agent](/assets/images/hermes-banner.png){ width=900 }

The self-improving AI agent built by Nous Research — the only AI agent with a built-in learning loop.

## What is Hermes AI Agent?

Hermes AI Agent is an autonomous AI assistant that goes beyond simple chatbots. It learns from your interactions, creates skills from experience, persists knowledge across sessions, and builds a deepening model of who you are over time.

Unlike traditional AI coding assistants tethered to an IDE, Hermes runs anywhere — from your local terminal to a $5 VPS, Docker container, or serverless infrastructure.

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

### Built-in Learning
- **Memory System** — MEMORY.md and USER.md persist context across sessions
- **Skills Creation** — Auto-generates reusable skills from complex tasks
- **Skill Self-Improvement** — Skills improve during use
- **Cross-Session Recall** — FTS5 search with LLM summarization

### 47 Built-in Tools
| Category | Tools |
|----------|-------|
| Web | `web_search`, `web_extract` |
| Terminal | `terminal`, `process`, `file` ops |
| Browser | `browser_navigate`, `browser_snapshot`, `browser_vision` |
| Vision | `vision_analyze`, `image_generate` |
| Memory | `memory`, `session_search` |
| Automation | `cronjob`, `send_message` |
| Delegation | Delegate subagents |

### Research Ready
- **Batch Trajectory Generation** — Generate training data at scale
- **Atropos RL** — Reinforcement learning environments
- **MCP Integration** — Connect any MCP server
- **Tool-calling Training** — Export to ShareGPT format

<iframe width="100%" height="450" src="https://www.youtube.com/embed/YtfROZK1BDM" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

After installation:

```bash
source ~/.bashrc  # or source ~/.zshrc
hermes  # Start chatting!
```

## Quick Start

```bash
# Interactive CLI
hermes

# Choose your model provider
hermes model

# Configure toolsets
hermes tools

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
- 200+ models via OpenRouter
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

# Options: Nous Portal, OpenRouter, OpenAI, Kimi, MiniMax, custom
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

## Resources

- [Official Documentation](https://hermes-agent.nousresearch.com/docs/)
- [GitHub Repository](https://github.com/NousResearch/hermes-agent)
- [Discord Community](https://discord.gg/NousResearch)
- [Skills Hub](https://agentskills.io)

---

> **Last Updated:** April 2026