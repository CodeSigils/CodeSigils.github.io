---
title: OpenCode Guide
description: "A practical guide to starting safely with OpenCode: install it, connect a provider, choose a model, and add only the integrations a project needs."
keywords:
  - opencode
  - AI coding agent
  - terminal
  - MCP
  - LLM
  - developer tools
---

<div class="image-wrapper">
  <img src="/assets/images/opencode-screenshot.webp"
       alt="OpenCode Screenshot"
       width="1200"
       height="978" />
</div>

OpenCode is worth trying when you want a terminal-based coding agent without
committing a repository to one model provider or a large automation stack. Start
with one repository, one provider, and one repeatable task. That baseline makes
it possible to tell whether a later model, MCP server, or plugin actually
helped.

This is a setup guide for the current OpenCode documentation. Commands, model
availability, and configuration fields change quickly, so use the linked
upstream pages as the authority when a detail here disagrees with your installed
version.

## Table of contents

1. [What OpenCode does](#what-opencode-does)
2. [Start with a small baseline](#start-with-a-small-baseline)
3. [Choose a provider and model](#choose-a-provider-and-model)
4. [Keep configuration small](#keep-configuration-small)
5. [Add MCP servers deliberately](#add-mcp-servers-deliberately)
6. [Treat plugins as code you depend on](#treat-plugins-as-code-you-depend-on)
7. [Automate only after an interactive check](#automate-only-after-an-interactive-check)
8. [Troubleshoot with the built-in commands](#troubleshoot-with-the-built-in-commands)

---

## What OpenCode does

OpenCode is an open-source coding agent with terminal, desktop, and IDE
surfaces. In a normal local setup, its client coordinates a model provider,
your repository, and any tools you enable. The client can run on your machine
while the selected provider still receives prompts or code. Local installation
does not make a provider interaction local by itself.

The useful question is therefore narrower than “is OpenCode private?”: which
provider, credentials, tools, and integrations will this task use? Check those
boundaries before sending sensitive code or adding a remote service.

## Start with a small baseline

The [official installation page](https://opencode.ai/docs/) is the source of
truth for supported installers and the current OpenCode generation. OpenCode 1
and OpenCode 2 use the same default command name, so do not install both side
by side without following the upstream migration guidance.

For a terminal installation, the documented script is:

```bash
curl -fsSL https://opencode.ai/install | bash
opencode --version
```

Windows users should read the current installation page. It recommends WSL for
the terminal workflow and lists package-manager and container alternatives.

Open a small repository and start the interactive interface:

```bash
cd path/to/repository
opencode
```

Ask for an explanation before asking for an edit. A good first task is:

```text
Explain the purpose of this repository, identify its test command, and propose
one small improvement. Do not change files.
```

That gives you a concrete way to judge the selected model and provider before
you grant write permissions or attach additional tools.

!!! tip "Keep the first task review-only"

    Read the proposed plan and inspect the repository yourself. A successful
    first conversation proves only that this provider and model can serve that
    task. It does not prove that automatic edits, CI use, or an MCP integration
    are safe for the project.

## Choose a provider and model

OpenCode's model selector shows enabled models whose providers are available in
the current project. Connect a provider in the interactive interface, then
choose from the models it exposes:

```text
/connect
/models
```

For a one-off command, select a model explicitly:

```bash
opencode run --model provider/model-id "Explain this repository"
```

The exact provider/model identifier matters. Availability can depend on the
provider account, region, subscription, credentials, and project configuration.
Use `/models` or `opencode models`. Model IDs copied from an old article can
already be unavailable. Provider terms and billing remain the provider's
responsibility.

OpenCode can also discover models from supported local runtimes, including
Ollama, LM Studio, and vLLM. A locally reachable model avoids sending prompts
to a cloud model provider, but it does not settle every privacy question. Check
the runtime, any proxy, and the tools the agent can invoke.

## Keep configuration small

Use `opencode.json` or `opencode.jsonc` when a repository needs a stable
default. The current schema supports editor validation and documents the
available keys:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  // Copy an available identifier from /models.
  "model": "provider/model-id"
}
```

Put personal defaults in `~/.config/opencode/opencode.json(c)`. Project
configuration can live in `opencode.json(c)` or
`.opencode/opencode.json(c)`. OpenCode searches from the working directory
toward the filesystem root and merges applicable configuration. Choose one
project convention unless you deliberately need the different precedence of
the two file locations.

Keep credentials out of a repository. The official configuration reference
supports environment- and file-based substitution when a provider needs an API
key, and `/connect` is often the simpler first path. Review the provider's
credential and data-handling documentation before sharing a team configuration.

Permissions are a separate decision. Start with prompts and approvals intact.
Only make a permission rule more permissive after you understand the tool and
repository consequences. `--auto` approves requests that are not explicitly
denied, so it belongs after an interactive check, not before it.

## Add MCP servers deliberately

MCP servers expose external tools, resources, prompts, and instructions to the
agent. They can be useful, but every server expands the trust boundary and its
tools consume model context. Add one only when the first baseline task reveals
a concrete missing capability.

From the project that needs it, the documented command shape is:

```bash
opencode mcp add server-name --url https://server.example/mcp
opencode mcp list
```

Use `--global` only when the server is appropriate in every project. Remote
servers may need OAuth. OpenCode reports that state in the server list and can
complete authentication through its MCP controls. A local server deserves the
same review: inspect the package, its command, its environment variables, and
the data it can read or send before enabling it.

## Treat plugins as code you depend on

Plugins can add tools, hooks, integrations, agents, or interface components.
They are not a harmless preference file. Read their source, release history,
permissions, and compatibility claim before adding one to a working setup.

OpenCode discovers local plugins beneath `.opencode/plugins/` for a project or
`~/.config/opencode/plugins/` globally. It can also install a published plugin
and add it to global configuration:

```bash
opencode plugin add package-name
opencode plugin list
opencode plugin check
```

Pin a plugin version when reproducibility matters, and test the installed
package in a non-critical repository first. The official plugin documentation
also explains how configuration order, local paths, and package updates work.

## Automate only after an interactive check

`opencode run` sends a prompt without opening the full interactive interface.
It is useful for scripts and CI once you have already established a safe model,
provider, prompt, and permission boundary:

```bash
opencode run "Summarize the failing test and suggest the smallest fix"
```

For CI, use a dedicated provider credential stored as a repository secret and
a model ID that you have tested for that job. The official command reference
shows a standalone GitHub Actions example. Keep automated runs review-oriented
at first, preserve ordinary branch protection, and require human review for
changes that affect code, credentials, or deployment.

## Troubleshoot with the built-in commands

Start with the information OpenCode can show about its own environment:

```bash
opencode --help
opencode debug paths
opencode auth list
opencode models
opencode mcp list
opencode plugin list
```

If a model is unavailable, confirm the provider account and then use the exact
identifier shown by the model list. If OpenCode cannot start, consult its logs
or run it with the documented logging option for your installed version. Do
not delete caches, credentials, or configuration as a first troubleshooting
step. Those actions erase useful evidence and can make a smaller problem
harder to identify.

## Further reading

- [OpenCode introduction and installation](https://opencode.ai/docs/)
- [CLI and command reference](https://opencode.ai/docs/cli/commands)
- [Providers](https://opencode.ai/docs/providers)
- [Models](https://opencode.ai/docs/models)
- [Configuration](https://opencode.ai/docs/config)
- [Permissions](https://opencode.ai/docs/en/permissions/)
- [MCP servers](https://opencode.ai/docs/mcp-servers)
- [Plugins](https://opencode.ai/docs/plugins)

_Guide fact-checked: 2026-11-11. OpenCode releases, configuration, provider
availability, pricing, and plugin behavior are release-dependent. Recheck the
linked official documentation before adopting a command or integration in a
production workflow._
