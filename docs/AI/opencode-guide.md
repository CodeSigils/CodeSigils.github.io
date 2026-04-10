---
title: OpenCode Guide
icon: lucide/terminal
description: Complete guide to OpenCode - the open source AI coding agent for terminal-based development with multi-model support, MCP integration, and slash commands.
keywords:
  - opencode
  - AI coding agent
  - terminal
  - Claude
  - GPT
  - MCP
  - LLM
  - developer tools
---

![OpenCode Screenshot](/assets/images/opencode-screenshot.webp){ width=900 }

The open source AI coding agent for terminal, desktop, and IDE.

## Table of Contents

1. [What is OpenCode?](#what-is-opencode)
2. [Official Links](#official-links)
3. [Installation](#installation)
4. [Core Features](#core-features)
5. [Model Support](#model-support)
6. [Plugins & Extensions](#plugins--extensions)
7. [Most Used Plugins](#most-used-plugins)
8. [Configuration](#configuration)
9. [Interface Options](#interface-options)
10. [Enterprise Features](#enterprise-features)
11. [Use Cases](#use-cases)
12. [Comparison](#comparison)
13. [Troubleshooting](#troubleshooting)
14. [Further Reading](#further-reading)

***

## What is OpenCode?

OpenCode is an **open source AI coding agent** that helps developers write, debug, refactor, and understand code. It operates as a terminal-native interface with optional desktop app and IDE extensions.

<div>
  <div style="position:relative;padding-top:56.25%;">
    <iframe src="https://www.youtube.com/embed/ul7zuyATDqE" 
            frameborder="0" 
            allowfullscreen 
            style="position:absolute;top:0;left:0;width:100%;height:100%;">
    </iframe>
  </div>
</div>

### Key Statistics

| Metric | Value |
| --- | --- |
| **GitHub Stars** | 140K+ |
| **Contributors** | 850+ |
| **Monthly Developers** | 6.5M+ |
| **Commits** | 11,000+ |
| **License** | MIT / Apache 2.0 |

### Core Philosophy

- **100% Open Source** — Complete transparency with MIT license
- **Provider Agnostic** — Works with Claude, OpenAI, Google, or local models
- **Privacy First** — No code or context stored on servers
- **Local-First** — Run locally with optional cloud services

***

## Official Links

- **Website**: https://opencode.ai
- **GitHub**: https://github.com/anomalyco/opencode
- **Documentation**: https://opencode.ai/docs
- **Zen (Curated Models)**: https://opencode.ai/zen
- **Enterprise**: https://opencode.ai/enterprise
- **Discord**: https://opencode.ai/discord
- **Desktop App**: https://opencode.ai/download

***

## Installation

### Prerequisites

!!! tip "Requirements Before You Start"

1. A modern terminal emulator (WezTerm, Alacritty, Ghostty, or Kitty recommended)
2. API keys for your preferred LLM provider(s)
3. Node.js 18+ (required for MCP servers and plugins)

#### Node.js Installation (Common "Foot Guns" to Avoid)

!!! warning "Common Mistakes to Avoid"

| ❌ Don't Do This | ✅ Do This Instead |
| --- | --- |
| `sudo apt install nodejs` (Ubuntu - installs ancient Node) | Use mise, fnm, n, or nvm |
| Rely on `source ~/.nvm/nvm.sh` manually | Use mise or fnm (auto-loads) |
| Assume Node persists across terminals | Test in a NEW terminal |
| Use different Node versions per project | Use a version manager |

#### Recommended: mise (Best for OpenCode Users)

[mise](https://mise.jdx.dev) is a "tool runner" that manages Node, Python, Go, etc. - persistent and project-aware.

```bash
# Install mise (if you have curl or build from source)
curl https://mise.run | sh

# Add to shell config (~/.zshrc or ~/.bashrc):
echo 'eval "$(mise activate zsh)"' >> ~/.zshrc

# Install Node via mise
mise use -g node@lts

# Verify (open NEW terminal)
node --version
```

!!! warning "Distrobox Users"

    If you're using distrobox to develop in a different distribution, be aware that mise-installed packages (like Node.js tools via `mise use -g node@lts`) can sometimes conflict with packages installed in the host distribution's package manager. For example, tools installed globally via `pipx` on the host may not be accessible inside the container, or vice versa. This is because distrobox shares the host's home directory but uses the container's binary paths. If you encounter issues, consider whether you're running tools from the host or the container — consistency is key.

#### Alternative: fnm (Fast Node Manager)

```bash
# Install fnm
curl -fsSL https://fnm.vercel.app/install | bash

# Add to shell config:
echo 'source $(fnm env --shell-only)' >> ~/.zshrc

# Install LTS
fnm install --lts
fnm default lts-latest

# Verify (new terminal)
node --version
```

#### Alternative: pnpm + corepack

If you already use pnpm, enable corepack (comes with Node 18+):

```bash
# Enable corepack (enables pnpm without separate install)
corepack enable

# This gives you pnpm AND the right Node version for pnpm
pnpm --version
```

#### Quick Verification

??? tip "How to Verify"

    1. Open a BRAND NEW terminal (not the same one)
    2. Run:
    
    ```bash
    node --version
    npm --version
    ```
    
    Both should show versions. If errors → Node not persistent.

#### Why This Matters for MCP

MCP servers run as subprocesses. If Node isn't persistent:

- MCP tools fail silently or hang
- `npx` commands don't work
- Plugin loading fails

### Install via Script (Recommended)

!!! tip "Quick Install (Recommended)"

```bash
# Official install script (recommended)
curl -fsSL https://opencode.ai/install.sh | sh

# Alternative URL (also works)
curl -fsSL https://opencode.ai/install | bash
```

### Package Managers

**Using Node.js:**

```bash
npm install -g opencode-ai   # npm
bun install -g opencode-ai   # bun
pnpm install -g opencode-ai  # pnpm
yarn global add opencode-ai  # yarn
```

**Using Homebrew (macOS/Linux):**

```bash
brew install anomalyco/tap/opencode
```

**Using Arch Linux:**

```bash
sudo pacman -S opencode           # Stable
paru -S opencode-bin              # AUR (Latest)
```

**Using Go:**

```bash
# Requires Go 1.21+
go install github.com/anomalyco/opencode@latest
```

### Windows Installation

**Using Chocolatey:**

```bash
choco install opencode
```

**Using Scoop:**

```bash
scoop install opencode
```

**Using Docker:**

```bash
docker run -it --rm ghcr.io/anomalyco/opencode
```

**Using WSL (Recommended):**
OpenCode works best on Windows through WSL (Windows Subsystem for Linux).

### Desktop App

Download the beta for macOS, Windows, and Linux:

- https://opencode.ai/download

***

## Core Features

### 1. Terminal User Interface (TUI)

OpenCode's primary interface is a terminal-based UI with:

- Session management
- File browsing
- Real-time code editing
- Multi-session support
- Theme customization

### 2. Plan and Build Modes

**Plan Mode** (`Tab` key):

- Analyzes and explains code
- Creates implementation plans
- No code changes made
- Perfect for reviewing before building

**Build Mode** (`Tab` key):

- Executes code changes
- Makes file edits
- Runs tests and commands

### 3. LSP Integration

Auto-loads Language Server Protocol servers for:

- Real-time type checking
- Code navigation (Go to Definition, Find References)
- Refactoring tools
- Diagnostics

**Supported Languages:**

- TypeScript/JavaScript (tsserver)
- Python (Pyright, Pylsp)
- Rust (rust-analyzer)
- Go (gopls)
- And many more via custom LSP servers

### 4. Git Integration

**GitHub Integration:**

- Trigger via `/opencode` comments in issues and PRs
- Execute in GitHub Actions runners
- Automatic commit messages

**GitLab Integration:**

- Merge request comments
- CI/CD integration

### 5. Share Sessions

Share conversation links with your team:

```bash
/share
```

Creates a link to the current conversation for collaboration and review.

### 6. Multi-Session

Run parallel agents on the same project:

- Multiple independent sessions
- Shared context when needed
- Share links for each session

### 7. Model Context Protocol (MCP)

Connect to 1,200+ MCP servers for extended capabilities:

- Database access
- External tools
- API integrations
- Browser automation

### 8. File Watching

Auto-reload and respond to file changes:

- Real-time updates
- Build on save
- Test on change

***

## Model Support

### 75+ LLM Providers

OpenCode connects to virtually any LLM via Models.dev:

| Category | Providers |
| --- | --- |
| **Cloud APIs** | OpenAI, Anthropic, Google, Mistral, Cohere |
| **Local Models** | Ollama, LM Studio, LocalAI |
| **Subscriptions** | GitHub Copilot, ChatGPT Plus/Pro |
| **Routers** | OpenRouter, Models.dev |
| **Open Models** | Hugging Face (17+ providers) |

### Hugging Face Integration

OpenCode natively supports **Hugging Face Inference Providers** - giving you access to open models from 17+ providers including Hugging Face, Together AI, Hyperbolic, and more.

#### Quick Setup

```bash
# 1. Create token at huggingface.co/settings/tokens
#    (needs "Make calls to Inference Providers" permission)

# 2. Run auth login
opencode auth login

# 3. Select Hugging Face when prompted
#    Enter your token: hf_...

# 4. Select a model
/models
```

#### Available Models

Access to open models from multiple providers:

- Llama variants
- Qwen
- Phi
- Mistral
- GLM
- And more...

#### Config (Optional)

For organization billing:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "huggingface": {
      "options": {
        "headers": {
          "X-HF-Bill-To": "your-org-name"
        }
      }
    }
  }
}
```

**Resources:**

- [OpenCode + Hugging Face](https://huggingface.co/docs/inference-providers/main/integrations/opencode)
- [OpenCode Providers Docs](https://opencode.ai/docs/providers/)
- [HF Inference Providers](https://huggingface.co/inference-providers)

### Recommended Models

| Model | Best For |
| --- | --- |
| GPT-5.2 | General coding, speed |
| GPT-5.1 Codex | Code-heavy tasks |
| Claude Opus 4.5 | Complex reasoning |
| Claude Sonnet 4.5 | Balanced performance |
| Gemini 3 Pro | Long context tasks |
| Big Pickle | Free tier |

### OpenCode Zen

A curated list of tested and verified models:

- Benchmarked specifically for coding agents
- No performance downgrade or routing to cheaper models
- Pay-as-you-go pricing
- Team workspace management

**Free Models:**

- GLM 4.7 Free
- Big Pickle Free
- MiniMax M2.1 Free

***

## Plugins & Extensions

### Plugin System

OpenCode's plugin system allows hooking into various events and customizing behavior.

#### Loading Plugins

**From local files:**

```bash
.opencode/plugins/      # Project-level
~/.config/opencode/plugins/  # Global plugins
```

**From npm:**

```json
{
  "plugin": ["opencode-helicone-session", "opencode-wakatime", "@my-org/custom-plugin"]
}
```

#### Plugin Events

OpenCode supports 20+ events for plugins:

| Category | Events |
| --- | --- |
| **Command** | `command.executed` |
| **File** | `file.edited`, `file.watcher.updated` |
| **Session** | `session.created`, `session.compacted`, `session.deleted`, `session.diff`, `session.error`, `session.idle` |
| **Tool** | `tool.execute.before`, `tool.execute.after` |
| **LSP** | `lsp.client.diagnostics`, `lsp.updated` |
| **TUI** | `tui.prompt.append`, `tui.command.execute`, `tui.toast.show` |
| **Permission** | `permission.asked`, `permission.replied` |
| **Shell** | `shell.env` |
| **Server** | `server.connected` |
| **Todo** | `todo.updated` |
| **Installation** | `installation.updated` |

### Built-in Tools

| Tool | Description |
| --- | --- |
| `bash` | Execute shell commands |
| `read` | Read files with glob support |
| `edit` | Apply string replacements |
| `write` | Write content to files |
| `grep` | Search file contents |
| `glob` | Find files by pattern |
| `lsp` | Language server queries |
| `apply_patch` | Apply patches |
| `skill` | Load skill documentation |
| `todowrite` | Manage todo lists |
| `webfetch` | Fetch web content |
| `websearch` | Search the web |
| `question` | Ask user questions |

### Custom Tools

Plugins can add custom tools via the `tool` helper:

```typescript
import { tool } from "@opencode-ai/plugin";

export const MyTool = tool({
  name: "my_tool",
  description: "A custom tool",
  parameters: z.object({
    foo: z.string(),
  }),
  execute: async (args, ctx) => {
    return `Hello ${args.foo}`;
  },
});
```

***

## Most Used Plugins

### 1. Oh My OpenCode

**GitHub**: https://github.com/code-yeongyu/oh-my-openagent

Orchestration layer with specialized agents, hooks, MCPs, and workflow automation.

**Features:**

- Planner-Sisyphus agent
- 20+ automation hooks
- Pre-configured Context7 and grep.app MCPs
- LSP defaults

### 2. OpenCode Swarm

**GitHub**: https://github.com/zaxbysauce/opencode-swarm

Architect-centric agentic swarm with 11 specialized agents.

**Features:**

- Hub-and-spoke orchestration
- Gated pipeline (code needs reviewer + test engineer approval)
- 11 specialized agents
- SAST and secrets scanning
- 11 language support
- Free tier available

### 3. opencode-prompts

**GitHub**: https://github.com/minipuft/opencode-prompts

Chain tracking, gate reminders, and state preservation for prompt engineering.

**Features:**

- Gate enforcement
- Chain progress tracking
- State preservation
- Shell verify tracking

### 4. open-reload

**GitHub**: https://github.com/veemex/open-reload

Hot-reload MCP meta-plugin for development.

**Features:**

- Live tool updates without restart
- Plugin development workflow
- Context threading

### 5. opencode-mcp

**GitHub**: https://github.com/AlaeddineMessadi/opencode-mcp

MCP server bridging OpenCode to other AI tools.

**Features:**

- 79 tools
- Multi-project support
- Auto-start capability

### 6. opencode-ecc (Everything Claude Code)

**GitHub**: https://github.com/affaan-m/everything-claude-code

Complete Claude Code compatibility for OpenCode.

**Features:**

- 12 specialized agents
- 24 commands
- 16 skills
- Hook system parity

### 7. Session & Analytics Plugins

| Plugin | Purpose |
| --- | --- |
| `opencode-helicone-session` | Session logging and analytics |
| `opencode-wakatime` | Automatic time tracking |

### 8. MCP Servers (1,200+ Available)

| Category | Popular Servers |
| --- | --- |
| **Browser** | Playwright, Puppeteer |
| **Database** | PostgreSQL, Supabase, SQLite |
| **Search** | Brave Search, Google Search |
| **Communication** | Slack, Discord, Linear, Notion |
| **Cloud** | AWS, GCP, Azure |
| **Development** | GitHub, GitLab, Docker |
| **Memory** | Memory (context persistence) |

**Resources:**

- https://github.com/modelcontextprotocol/servers
- https://github.com/wong2/awesome-mcp-servers
- https://mcp-awesome.com

***

## Configuration

### Configuration Files

| Location | Priority | Purpose |
| --- | --- | --- |
| `./opencode.json` | 1st | Project directory |
| `~/.config/opencode/opencode.json` | 2nd | XDG config directory |
| `~/.opencode.json` | 3rd | Home directory |

**Note**: Config file locations (verified 2026):
- `$HOME/.opencode.json`
- `$XDG_CONFIG_HOME/opencode/.opencode.json`
- `./.opencode.json` (local directory)

### Basic Configuration

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-20250514",
  "permission": {
    "bash": "allow",
    "read": "allow",
    "edit": "allow"
  }
}
```

### Advanced Configuration

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode/gpt-5.1-codex",
  "provider": {
    "openai": {
      "models": {
        "gpt-5": {
          "options": {
            "reasoningEffort": "high",
            "textVerbosity": "low",
          },
        },
      },
    },
  },
  "plugin": ["oh-my-openagent"],
  "mcp": {
    "enabled": true,
  },
  "permission": {
    "bash": "allow",
    "mcp_*": "ask",
  },
}
```

### Provider Setup

Connect to providers using the `/connect` command:

```bash
/opencode
/connect
```

Then:

1. Sign in to your provider
2. Add billing details
3. Copy API key
4. Paste into terminal

***

## Interface Options

### 1. Terminal (TUI)

The primary interface with full features:

- Interactive chat
- Session management
- File editing
- Real-time output

### 2. Desktop App

Beta available for:

- macOS
- Windows
- Linux

Download: https://opencode.ai/download

### 3. IDE Extensions

Available for:

- VS Code
- Cursor
- Zed
- Windsurf
- VSCodium

### 4. Web Interface

Access via browser at:

- https://opencode.ai/go

### 5. ACP (Agent Coding Protocol)

Connect to ACP-compatible editors for deep IDE integration.

***

## Enterprise Features

### Privacy-First Architecture

- No code or context stored on OpenCode servers
- Local-first operation
- Self-hosting options
- BYOK (Bring Your Own Key) model

### Enterprise Deployment

| Feature | Description |
| --- | --- |
| **Self-Hosted** | Run entirely on your infrastructure |
| **Custom Providers** | Use your own LLM infrastructure |
| **Privacy Controls** | Data never leaves your environment |
| **SSO Support** | Enterprise authentication |

### Zen for Teams

- Invite teammates
- Assign roles (Admin, Member)
- Curate model access
- Monthly spending limits
- Shared API keys

***

## Use Cases

OpenCode serves different types of users, from developers to non-programmers.

### Developer Use Cases

#### Code Review and Analysis

```bash
# Review code for security issues
opencode run "Review src/auth.ts for security issues"

# Analyze code architecture
opencode run "Explain the architecture of the middleware system"

# Find all TODO comments in the project
opencode run "Find all TODO comments and create a summary"
```

#### Scaffolding New Features

```bash
# Initialize repository context first
opencode init

# Then scaffold a new feature with handler, validation, and tests
opencode run "Add a new POST /api/widgets endpoint with handler, validation, and tests"
```

#### Large-Scale Refactoring

```bash
# Rename a function across all files
opencode run "Rename getUserProfile to fetchUserProfile and update all imports and docs"
```

#### Test-Driven Development (TDD)

```bash
# Create failing test first, then implement
opencode run "Run npm test. Read the failure. Implement the code in feature.ts to make the test pass"
```

#### Debugging

```bash
# Find and fix bugs
opencode run "Find and fix the memory leak in the application"

# Explain error messages
opencode run "Explain what this error means in context of our codebase"
```

#### Documentation Maintenance

```bash
# Update outdated documentation
opencode run "Read all exported functions in src/api. Update docs/API.md to match the current signatures"
```

#### Language Migration

```bash
# Convert React class components to hooks
opencode run "Read Component.jsx. Rewrite it as a Functional Component using Hooks"
```

### Average User Use Cases (Non-Developers)

#### Content Creation and Marketing

```bash
# White papers, LinkedIn posts, video scripts
opencode run "Write a white paper on [topic] using the style guide in docs/writing-style.md"

# Social media content
opencode run "Create 5 tweet thread concepts for [product launch]"
```

#### Translation Work

```bash
# Translate documents
opencode run "Translate the content in jp/ folder to English following the style in TRANSLATION_NOTES.md"
```

#### Data Analysis and Reporting

```bash
# Analyze data and generate reports
opencode run "Analyze parcel data in data/ and generate summary report with trends"
```

#### File Organization

```bash
# Organize downloads folder
opencode run "Organize the downloads folder: put movies in Movies/, TV shows in TV/"
```

#### Excel and Spreadsheet Work

```bash
# Generate formulas
opencode run "Create a formula in column D that calculates the sum of columns A and B"
```

### Common Real-World Examples

#### Legacy Code Refactoring

```bash
opencode start "Take main.py. Split the database logic into db.py and the utils into utils.py"
```

#### CI/CD Automated Code Review

```yaml
# .github/workflows/opencode-review.yml
name: opencode-review
on: [pull_request]
jobs:
  opencode:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run OpenCode
        uses: anomalyco/opencode/github@latest
        with:
          model: anthropic/claude-sonnet-4-20250514
          prompt: "Code review for the PR changes"
```

#### GitHub Issue Triage

```bash
# In a GitHub issue comment
/opencode explain this issue

# In a GitHub PR comment
/opencode fix this
```

#### Database Operations via MCP

```bash
# Connect to database via MCP
opencode run "Show me the schema for the 'users' table"
```

#### Slack Bot Integration

Connect OpenCode to Slack for team questions like:

- "Where is the retry logic for payment processing?"
- "Summarize what changed in the last sprint"

### Workflow Patterns

#### Plan/Build Pattern (Recommended)

1. Start in Plan mode (`Tab` key) to outline approach
2. Review and refine the plan
3. Switch to Build mode to implement

#### Agent Mode (Autonomous)

```bash
opencode --agent
```

Best for: Project setup, large refactors, debugging, testing, code migration.

***

## Comparison

### OpenCode vs Claude Code

| Feature | **OpenCode** | **Claude Code** |
| --- | --- | --- |
| **GitHub Stars** | 140K+ | 20K+ |
| **License** | MIT | Proprietary |
| **Provider Support** | 75+ providers | Anthropic only |
| **Plugin System** | 20+ events | 3 phases |
| **Interface** | TUI, Desktop, IDE | CLI only |
| **Pricing** | Free + optional Zen | Uses Anthropic API |

### OpenCode vs Cursor

| Feature | **OpenCode** | **Cursor** |
| --- | --- | --- |
| **Focus** | Terminal-native | IDE-centric |
| **Model Support** | Any provider | Custom models |
| **Open Source** | Yes | Partial |
| **Price** | Free | $20/mo+ |

### When to Use OpenCode

- You want full control over your models
- You prefer terminal-based workflows
- You need cross-platform consistency
- You value open-source software
- You want to avoid vendor lock-in

***

## Troubleshooting

### Installation Issues

**Verify installation:**

```bash
opencode --version
```

**Update OpenCode:**

```bash
# Re-run install script
curl -fsSL https://opencode.ai/install | bash
```

### Configuration Issues

**Check config syntax:**

```bash
# Config locations checked in priority order:
cat ~/.opencode.json                    # Home directory
cat ~/.config/opencode/opencode.json  # XDG config directory
cat ./opencode.json                # Project directory
```

**Validate JSON:**

```bash
# Use jq to validate any location
cat ~/.opencode.json | jq .
```

### Provider Issues

**Check API key:**

```bash
/opencode
/connect
```

**Test connection:**

```bash
/opencode
/model <model-name>
```

### Plugin Issues

**Verify plugin loading:**

```bash
opencode --version
# Should list loaded plugins
```

**Debug mode:**

```bash
opencode --debug
```

### Performance Issues

**Clear cache:**

```bash
rm -rf ~/.cache/opencode
```

**Check logs:**

```bash
# Default log location
~/.config/opencode/logs/
```

***

## Further Reading

### Official Documentation

- [OpenCode Docs](https://opencode.ai/docs)
- [Configuration Guide](https://opencode.ai/docs/config/)
- [Plugins Guide](https://opencode.ai/docs/plugins/)
- [MCP Servers](https://opencode.ai/docs/mcp-servers/)
- [LSP Configuration](https://opencode.ai/docs/lsp/)

### Model Resources

- [OpenCode Zen](https://opencode.ai/zen)
- [Models.dev](https://models.dev)
- [AI SDK](https://sdk.vercel.ai)

### Community Resources

- [Discord Community](https://opencode.ai/discord)
- [GitHub Discussions](https://github.com/anomalyco/opencode/discussions)

### Plugin Resources

- [Official Plugins](https://opencode.ai/docs/plugins/)
- [Oh My OpenCode](https://ohmyopencode.com)
- [OpenCode Swarm](https://github.com/zaxbysauce/opencode-swarm)
- [Awesome MCP Servers](https://github.com/wong2/awesome-mcp-servers)

### Comparisons

- [OpenCode vs Claude Code](https://opencode.ai/docs/compare/)
- [OpenCode vs Cursor](https://opencode.ai/compare/cursor)

### Research & Reviews

- [AgentWiki OpenCode](https://agentwiki.org/opencode)
- [Ry Walker Research](https://rywalker.com/research/opencode)

***

_Guide last updated: April 2026_
