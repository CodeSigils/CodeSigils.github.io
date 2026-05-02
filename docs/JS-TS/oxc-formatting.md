---
title: OXC Formatter Guide
icon: simple/typescript
description: Guide to OXC formatter - the next-generation JavaScript/TypeScript code formatter written in Rust. Fast, configurable, and modern.
keywords:
  - OXC
  - formatter
  - JavaScript
  - TypeScript
  - Rust
  - code formatting
---

# The OXC tools

<p><img src="/assets/images/oxc-logo.svg" alt="OXC Logo" style="max-width:100%;width:200px;height:auto;display:block;margin:1em auto;" /></p>

[OXC](https://oxc.rs/) is a collection of JavaScript/TypeScript tooling written in Rust.
The OXC formatter is a fast, configurable code formatter for JavaScript, TypeScript, JSX, and JSON.
It represents a new generation of high-performance tools for the JavaScript ecosystem.

## How The OXC Formatter Works

OXC formatter parses your JavaScript/TypeScript source code into an Abstract Syntax Tree (AST), then applies formatting rules to generate consistently styled output. Because it's written in Rust, it avoids the overhead of Node.js and achieves near-native performance.

### Use Cases

- **Large Codebases**: Format thousands of files in seconds during CI/CD pipelines
- **Monorepos**: Handle multiple packages with different configurations efficiently
- **Pre-commit Hooks**: Instant formatting without waiting for slower alternatives
- **IDE Integration**: Real-time formatting as you type with minimal latency
- **Migration Projects**: Drop-in replacement for Prettier with compatible output

## Why OXC Formatter?

!!! success "Performance"

    OXC formatter is written in Rust and is significantly faster than other JavaScript formatters.
    It can format large codebases in milliseconds.

!!! tip "Compatibility"

    OXC aims to be compatible with Prettier's formatting rules, making migration easy.

## Installation

```sh
npm install --save-dev oxc
```

Or using other package managers:

=== "pnpm"

```sh
    pnpm add -D oxc
```

=== "yarn"

```sh
    yarn add -D oxc
```

=== "bun"

```sh
    bun add -D oxc
```

### Standalone Formatter (oxcfmt)

You can also install the standalone formatter package [`oxcfmt`](https://www.npmjs.com/package/oxcfmt) directly:

=== "pnpm"

```sh
    pnpm add -D oxcfmt
```

=== "npm"

```sh
    npm install --save-dev oxcfmt
```

=== "yarn"

```sh
    yarn add -D oxcfmt
```

## Basic Usage

### CLI Commands

```sh
# Format all files
npx oxc format .

# Format specific files
npx oxc format src/**/*.ts

# Check formatting without writing
npx oxc format . --check
```

## Configuration

Create an [`oxc.config.json`](https://oxc.rs/docs/guide/usage/linter-config.html) file in your project root:

```json
{
  "formatter": {
    "enabled": true,
    "indentStyle": "tab",
    "indentWidth": 2,
    "lineEnding": "lf",
    "printWidth": 80,
    "quoteStyle": "double"
  }
}
```

### Configuration Options

| Option        | Type                     | Default    | Description                            |
| :----- | :--- | :------ | :---------- |
| `enabled`     | boolean                  | `true`     | Enable/disable formatter               |
| `indentStyle` | `"tab" \| "space"`       | `"tab"`    | Indentation style                      |
| `indentWidth` | number                   | `2`        | Number of spaces per indentation level |
| `lineEnding`  | `"lf" \| "crlf" \| "cr"` | `"lf"`     | Line ending character                  |
| `printWidth`  | number                   | `80`       | Maximum line length                    |
| `quoteStyle`  | `"single" \| "double"`   | `"double"` | Quote style for strings                |

## Formatting Examples

### Before Formatting

```js
function greet(name, age) {
  const message = "Hello, " + name + "! You are " + age + " years old.";
  console.log(message);
  return { message: message, timestamp: Date.now() };
}
```

### After Formatting

```js
function greet(name, age) {
  const message = "Hello, " + name + "! You are " + age + " years old.";
  console.log(message);
  return { message: message, timestamp: Date.now() };
}
```

## Supported Languages

- :white_check_mark: JavaScript (`.js`, `.mjs`, `.cjs`)
- :white_check_mark: TypeScript (`.ts`, `.mts`, `.cts`)
- :white_check_mark: JSX (`.jsx`)
- :white_check_mark: TSX (`.tsx`)
- :white_check_mark: JSON (`.json`)
- :white_check_mark: JSONC (`.jsonc`)

## Integration

### With VS Code

Install the [OXC VS Code extension](https://marketplace.visualstudio.com/items?itemName=oxc.oxc-vscode):

```json
{
  "editor.defaultFormatter": "oxc.oxc-vscode",
  "editor.formatOnSave": true
}
```

## VS Code Extension

The [OXC VS Code extension](https://marketplace.visualstudio.com/items?itemName=oxc.oxc-vscode) provides first-class integration with your editor.

### Features

- **Format on Save**: Automatically format files when you save them
- **Format on Type**: Format code as you type (configurable)
- **Format Selection**: Format only the selected code block
- **Error Reporting**: Shows parsing errors and formatting issues inline
- **Configuration Support**: Reads your `oxc.config.json` automatically

### Extension installation

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Search for "OXC"
4. Click **Install** on the OXC extension

Or install via CLI:

```sh
code --install-extension oxc.oxc-vscode
```

### Recommended Settings

```json
{
  "editor.defaultFormatter": "oxc.oxc-vscode",
  "editor.formatOnSave": true,
  "editor.formatOnType": false,
  "[javascript]": {
    "editor.defaultFormatter": "oxc.oxc-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "oxc.oxc-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "oxc.oxc-vscode"
  }
}
```

### With LazyVim

LazyVim includes OXC support as an extra. Enable it in your configuration:

```lua
-- In your LazyVim config (e.g., lua/plugins/oxc.lua)
{ import = "lazyvim.plugins.extras.lang.typescript.oxc" }
```

For more details, see the [LazyVim OXC documentation](https://www.lazyvim.org/extras/lang/typescript/oxc).

### With Pre-commit Hooks

Add to your [`.pre-commit-config.yaml`](https://pre-commit.com/):

```yaml
repos:
  - repo: local
    hooks:
      - id: oxc-format
        name: OXC Format
        entry: npx oxc format
        language: system
        files: \.(js|ts|jsx|tsx|json)$
```

## Migration from Prettier

!!! warning "Check your config"

    Before migrating, review your Prettier configuration and map the equivalent options in OXC.

Migration steps:

1. [ ] Install OXC: `npm install --save-dev oxc`
2. [ ] Create `oxc.config.json` with your preferred settings
3. [ ] Run formatter: `npx oxc format .`
4. [ ] Compare output with your Prettier-formatted code
5. [ ] Update CI/CD pipelines to use OXC
6. [ ] Remove Prettier (optional)

## Performance Comparison

```text
Benchmark: Formatting 1000 files

OXC:        ~50ms
Prettier:   ~2000ms

Speedup: 40x faster
```

## Resources

- [OXC Official Website](https://oxc.rs/)
- [GitHub Repository](https://github.com/oxc-project/oxc)
- [Configuration Documentation](https://oxc.rs/docs/guide/usage/linter-config.html)

---
