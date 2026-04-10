# AGENTS.md

## Repository Overview

This is a **Zensical** (Python static site generator) personal documentation site hosted on GitHub Pages with Sveltia CMS for admin interface.

- **Site URL**: https://codesigils.github.io/
- **Repo**: CodeSigils/CodeSigils.github.io
- **Author**: Tom Geo
- **Stack**: Zensical + Sveltia CMS + GitHub Pages

## Build Commands

```bash
# Build the site (outputs to ./site/)
zensical build

# Clean build (removes old artifacts first)
zensical build --clean

# Local development server
zensical serve
```

**Important**: Build output goes to `./site/` directory, which is gitignored. Do not edit files in `site/` - edit source in `docs/` instead.

## Content Structure

```
docs/
├── index.md              # Homepage
├── markdown.md          # Markdown authoring reference
├── AI/                 # AI tools articles
│   ├── opencode-guide.md
│   ├── oh-my-opencode-guide.md
│   ├── dolphin-llm-guide.md
│   ├── hermes-ai-guide.md
│   ├── hermes-vs-opencode.md
│   ├── free-ai-models.md
│   └── notebooklm-opencode-tutorial.md
├── JS-TS/              # JavaScript/TypeScript articles
│   ├── index.md
│   └── oxc-formatting.md
├── admin/
│   └── config.yml      # Sveltia CMS configuration
└── assets/images/     # Images (deployed to /assets/images/)
```

## Content Collections (via Sveltia CMS)

Configured in `docs/admin/config.yml`:

| Collection | Folder | Purpose |
|------------|--------|---------|
| **pages** | `docs/` | General pages |
| **home** | `docs/index.md` | Homepage only |
| **jsts** | `docs/JS-TS/` | JS-TS section |
| **ai** | `docs/AI/` | AI section articles |

Front matter fields: `title`, `icon` (Lucide icon name, e.g., `lucide/rocket`), `body` (markdown).

## Deployment

GitHub Actions workflow in `.github/workflows/docs.yml`:

1. Trigger: Push to `master` or `main`
2. Steps: `pip install zensical` → `zensical build --clean` → Deploy to GitHub Pages
3. No manual build step needed - changes pushed to `docs/` auto-deploy

## Zensical Configuration

`zensical.toml` contains:

- Site metadata (name, URL, author, copyright)
- Theme settings (Modern variant, dark/light mode toggle)
- 60+ feature toggles enabled (instant navigation, search, code blocks, etc.)
- Font: JetBrains Mono for code
- Language: English

## Adding New Articles

1. Create new `.md` file in appropriate section folder (`docs/AI/`, `docs/JS-TS/`, etc.)
2. Add front matter with title and icon:

   ```markdown
   ---
   title: My Article Title
   icon: lucide/rocket
   ---
   ```

3. Commit and push - CI will build automatically

## Images

- Source: `docs/assets/images/`
- Deployed to: `/assets/images/`
- Reference in markdown: `/assets/images/filename.ext`

## Environment

- `.env` contains GitHub OAuth token - do not commit
- `.venv/` - Python virtual environment (gitignored)

## Local Development

```bash
# Activate virtual environment
source .venv/bin/activate

# Run local server with hot reload
zensical serve

# Build for production
zensical build --clean
```