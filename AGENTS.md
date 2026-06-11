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

**Current dependency**: zensical 0.0.45 (CI pins `==0.0.45`, `.venv/` uses `>=0.0.45,<0.0.46`)

## Content Structure

The site uses a flat category convention -- articles live in one-level subfolders under `docs/`:

```
docs/
├── <category>/          # Section or collection (e.g. AI/, JS-TS/)
│   ├── index.md         # Section landing page
│   └── *.md             # Articles in this section
├── admin/
│   └── config.yml       # Sveltia CMS collections
└── assets/images/       # Images (deployed to /assets/images/)
```

For an exact listing of all articles, run: `find docs/ -name '*.md' | sort`

New categories = new folder under `docs/` + new collection in `docs/admin/config.yml`.
New articles = new `.md` file inside an existing category folder.

## Content Collections (via Sveltia CMS)

Configured in `docs/admin/config.yml`. Each category folder under `docs/` maps to a collection entry. For current collections, read `docs/admin/config.yml` directly -- or run:

```bash
grep -E '^\s+- name:|^\s+  label:|^\s+  folder:' docs/admin/config.yml
```

Front matter fields: `title`, `icon` (Lucide icon name, e.g., `lucide/rocket`), `body` (markdown).

> **Warning: Adding a new category**
> When creating a new folder under `docs/`, add a matching collection to `docs/admin/config.yml` so Sveltia CMS can manage its articles.

## Deployment

GitHub Actions workflow in `.github/workflows/docs.yml`:

1. Trigger: Push to `master` or `main` with changes to `docs/**`, `zensical.toml`, or `.github/workflows/docs.yml`
2. Non-site files (README.md, AGENTS.md, LICENSE, .gitignore, etc.) do **not** trigger a build
3. Steps: `pip install zensical` → `zensical build --clean` → Deploy to GitHub Pages
4. No manual build step needed - changes pushed to `docs/` auto-deploy

## Adding New Articles

1. Create new `.md` file in the appropriate category folder under `docs/`
2. Add front matter with title (and icon for category indexes only):

   ```markdown
   ---
   title: My Article Title
   icon: lucide/rocket
   ---
   ```

3. Commit and push - CI will build automatically

> **Warning: Changing content structure**
> When adding, moving, or renaming folders under `docs/`, update `docs/admin/config.yml` to match. See [Content Collections](#content-collections-via-sveltia-cms) above.

## Content Guidelines

### No Local Article Links in Index Pages

Index pages (section landing pages like `docs/AI/index.md`, `docs/JS-TS/index.md`) **must not** contain links to local articles — this prevents duplicate listings in the sidebar navigation. Let the navigation handle article links.

## Images

- Source: `docs/assets/images/`
- Deployed to: `/assets/images/`
- Reference in markdown: `/assets/images/filename.ext`

## Front Matter SEO Fields

| Field           | Purpose                       | Example                                |
| :---- | :------ | :------ |
| **title**       | Page title                 | OpenCode Guide                        |
| **description** | Meta description (~150 chars) | Complete guide to OpenCode...        |
| **keywords**    | SEO keywords (comma-separated) | opencode, AI coding agent, terminal  |
| **icon**        | Lucide icon name           | lucide/terminal                      |

> **SEO Best Practices**
> - Always add a unique `description` for each article
> - Include primary keyword in title and description
> - Use 3-5 relevant keywords, avoid keyword stuffing
> - Description appears in search results and social previews

## Local Development

```bash
# Activate virtual environment
source .venv/bin/activate

# Run local server with hot reload
zensical serve

# OAuth proxy for Sveltia CMS admin authentication
python oauth-proxy.py       # requires GITHUB_CLIENT_ID + GITHUB_CLIENT_SECRET

# Build and verify before pushing
zensical build --clean
```

> **Test before push**
> Always run `zensical build --clean` locally to catch link errors and warnings.

## Environment

- `.env` - GitHub OAuth token (gitignored)
- `.venv/` - Python virtual environment (gitignored)
- `.open-mem/` - Agent memory data (gitignored)

## Markdown Standards

These standards **MUST** be followed for all articles in this repo:

### Admonitions (Important Notes)

Always use admonitions to highlight important information, warnings, tips, and key takeaways. Every article should use them where relevant — they make content scannable and visually distinct.

Supported admonition types in Zensical:

| Type | Usage |
| :--- | :---- |
| note, tip, warning, danger, success, failure | `!!! type "Title"` |
| question, info, bug, example, quote | Followed by indented content body |

### Collapsible Sections

Use collapsible blocks for content that is optional or secondary — setup details, alternative methods, troubleshooting notes:

```markdown
??? tip "Click to expand"

    Hidden content here.  The blank line and 4-space indent are required.
```

### Content Tabs

Use content tabs for multi-language examples, alternative package managers, or platform-specific instructions:

```markdown
=== "Python"

    ```python
    print("Hello!")
    ```

=== "Rust"

    ```rust
    println!("Hello!");
    ```
```

Content tabs work without blank lines between them. Each tab body must be indented 4 spaces.

### Icons in Front Matter

Use Lucide icons:

```markdown
---
title: My Article Title
icon: lucide/rocket
---
```

Common icons: `lucide/terminal`, `lucide/box`, `lucide/fish`, `lucide/cpu`, `lucide/book-open`, `lucide/bot`, `lucide/rocket`

## Verification Standards

Use the same `image-wrapper` / `youtube-video-wrapper` CSS wrappers from existing articles for images and videos.
MD033 (no inline HTML) is **disabled** in `.markdownlint.json` for this repo.
