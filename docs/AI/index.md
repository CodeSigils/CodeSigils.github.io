---
title: AI Tools
icon: lucide/bot
description: Guides and tutorials for AI coding tools - OpenCode, Hermes AI, Dolphin LLM, and more.
keywords:
  - AI
  - OpenCode
  - LLM
  - AI agent
  - coding assistant
  - GPT
  - Claude
---

AI-powered development tools for coding, debugging, and documentation.

## Why Open Source AI Tools?

The AI coding landscape has shifted dramatically. While proprietary tools like Claude Code ($20/mo) and Cursor ($20/mo) dominate discussions, open-source alternatives offer compelling advantages:

!!! tip "Open Source Benefits"

    - **No vendor lock-in**: Use any model (Claude, GPT, Gemini, local) without being tied to one ecosystem
    - **Total cost control**: Pay only for API tokens — use free models like Grok, GLM 4.7, or run locally for $0
    - **Privacy & security**: Your code stays local — critical for enterprise and regulated industries
    - **Transparency**: Audit the code, know exactly what data is sent where
    - **Flexibility**: Switch models mid-session, use custom hooks, self-host for air-gapped environments

| Tool | Type | Cost | Open Source |
| :--- | :--- | :--- | :--- |
| **OpenCode** | Terminal CLI | Free (BYOK) | ✅ Yes (45K+ stars) |
| **Claude Code** | Terminal CLI | $20-200/mo | ❌ No |
| **Cursor** | IDE (VS Code fork) | $20/mo | ❌ No |
| **Cline** | VS Code extension | Free + API | ✅ Yes |

## Linux AI Tools

Running AI locally on Linux gives you privacy, cost savings, and control. Here are the essential tools:

### Model Runners

| Tool | Description |
| :--- | :--- |
| **Ollama** | CLI tool for running LLMs locally (Llama, Qwen, DeepSeek, etc.) |
| **LM Studio** | Desktop GUI for local models with server mode |

??? tip "Installation"
    - Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
    - LM Studio: See [lmstudio.ai](https://lmstudio.ai/)

### Terminal Agents

| Tool | Description |
| :--- | :--- |
| **OpenCode** | Open-source, provider-agnostic terminal agent with 75+ providers |
| **OllamaCode** | Local-first coding assistant with 120+ MCP tools, memory system |
| **Local Coding Assistant** | Ollama-based CLI with git-aware operations |

### IDE Extensions

| Tool | Description |
| :--- | :--- |
| **Cline** | Open-source VS Code extension with multi-model support |
| **Continue** | Open-source AI assistant for any IDE |
| **Void** | Open source AI code editor (Cursor alternative) |

## Open Source vs Proprietary

### When to Choose Open Source

- **Budget-conscious**: Free tool + BYOK = lowest total cost
- **Privacy matters**: Air-gapped environments, regulated industries
- **Flexibility needed**: Switch providers mid-session, use multiple APIs
- **Custom automation**: Hooks system, MCP integrations

### When to Choose Proprietary

- **Quick onboarding**: Cursor's polished UX needs zero setup
- **Tab completions**: Cursor's inline AI suggestions are best-in-class
- **Enterprise support**: Direct vendor support and SLAs

!!! note "Hybrid Approach"
    Many developers use both: OpenCode for complex autonomous tasks, Cursor for quick inline edits. Or run Cline inside Cursor for the best of both worlds.

## Tooling Ecosystem

| Category | Tools |
| :------- | :---- |
| **Terminal Agents** | OpenCode, Claude CLI, OllamaCode |
| **Local Models** | Ollama, LM Studio, Dolphin |
| **Cloud APIs** | OpenAI, Anthropic, Google, Groq |

---

_This section is part of the Code Sigils documentation._
