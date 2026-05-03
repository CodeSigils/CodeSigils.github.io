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
│   ├── index.md        # AI section landing
│   ├── OpenCode/      # OpenCode articles
│   │   ├── index.md
│   │   ├── opencode-guide.md
│   │   ├── oh-my-opencode-guide.md
│   │   ├── open-mem-guide.md
│   │   └── notebooklm-opencode-tutorial.md
│   ├── Hermes/        # Hermes articles
│   │   ├── index.md
│   │   ├── hermes-ai-guide.md
│   │   ├── hermes-vs-opencode.md
│   │   ├── browseros-hermes-guide.md
│   │   └── hermes-perplexity.md
│   └── LLMs/          # LLM articles
│       ├── index.md
│       ├── dolphin-llm-guide.md
│       └── free-ai-models.md
├── JS-TS/              # JavaScript/TypeScript articles
│   ├── index.md
│   └── oxc-formatting.md
├── admin/
│   └── config.yml      # Sveltia CMS configuration
└── assets/images/     # Images (deployed to /assets/images/)
```

## Content Collections (via Sveltia CMS)

Configured in `docs/admin/config.yml`:

| Collection | Folder          | Purpose             |
| :--------- | :-------------- | :------------------ |
| **pages**  | `docs/`         | General pages       |
| **home**   | `docs/index.md` | Homepage only       |
| **jsts**   | `docs/JS-TS/`   | JS-TS section       |
| **ai**     | `docs/AI/`      | AI section index    |
| **ai_opencode** | `docs/AI/OpenCode/` | OpenCode articles |
| **ai_hermes**  | `docs/AI/Hermes/`   | Hermes articles   |
| **ai_llms**    | `docs/AI/LLMs/`     | LLM articles    |

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

1. Create new `.md` file in appropriate section folder (`docs/AI/OpenCode/`, `docs/AI/Hermes/`, `docs/AI/LLMs/`, `docs/JS-TS/`, etc.)
2. Add front matter with title (and icon for category indexes only):
3. Commit and push - CI will build automatically

!!! warning "Sveltia CMS"
   When changing content structure (adding/moving/renaming folders), update `docs/admin/config.yml` to add new collections.

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

## OpenCode Settings

This repo uses `open-mem` plugin for persistence.

### Memory Commands

Add important updates to memory:

```bash
memory.store({ content: "Description of what changed" })
```

Search memories:

```bash
memory.find({ query: "search term" })
```

List memories:

```bash
memory.list({ scope: "project", limit: 10 })
```

## Markdown Standards

These standards **MUST** be followed for all articles in this repo:

### Admonitions (Important Notes)

```markdown
!!! tip "Title of the tip"
Important content here.

!!! warning "Title of the warning"
Warning content here.

!!! note "Title of the note"
Note content here.
```

### Collapsible Sections

```markdown
??? tip "Click to expand"

    Hidden content here.
```

### Table Headers

Always use aligned table headers:

```markdown
| Header 1 | Header 2 | Header 3 |
| :------- | :------- | :------- |
| Data     | Data     | Data     |
```

**DO NOT use:**

```markdown
|---|---|---| # WRONG
```

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

These standards **MUST** be followed for all articles in this repo:

### Links and References

- **Double-check all links** before publishing
- Verify external URLs are accessible and point to the correct page
- Check that anchor links within the article work correctly
- Ensure documentation links point to current versions (not outdated)

### Command Verification

When documenting commands for any technology:

1. **Verify against official sources**:
   - Check the official documentation site
   - Check the official GitHub repository
   - Check official installation guides

2. **Verify command syntax**:
   - Ensure correct flags and options
   - Check for version-specific differences
   - Confirm the command exists (not deprecated)

3. **Search for known issues**:
   - Look for common mistakes users might encounter
   - Note any prerequisites or dependencies

4. **Cross-reference multiple times**:
   - If in doubt, search the official docs again
   - Don't rely on a single source for critical commands

5. **Article infoemation validation**:
   - **Check link validity** - Verify each URL returns a valid HTTP response
   - **Investigate content accuracy** - Ensure the linked content matches the article claims
   - **Check for broken links** - Identify 404 errors or domain changes
   - **Validate references** - Confirm citations are from reputable sources

### Example Verification Workflow

```bash
# Before adding a command like:
curl -fsSL https://example.com/install | sh

# Verify by:
# 1. Checking official docs at https://example.com/docs
# 2. Checking the install script URL is correct
# 3. Confirming the command works on your test environment
```

### Responsive Images

Use div with CSS class for responsive images (consistent with YouTube pattern):

```html
<div class="image-wrapper">
  <img src="/assets/images/image.webp"
       alt="Alt text" />
</div>
```

CSS classes available:

| Class | Purpose |
| :------- | :------ |
| `.image-wrapper` | Full-width responsive image |
| `.logo-wrapper` | Small logo/icon |

Image sources live in `docs/assets/images/` and deploy to `/assets/images/`. WebP preferred for screenshots (smaller files). PNG for logos/icons. JPEG for photos.

### Responsive Videos

Always use the YouTube wrapper pattern to maintain 16:9 aspect ratio on all screens:

```markdown
<div class="youtube-video-wrapper">
  <iframe src="https://www.youtube.com/embed/VIDEO_ID"
          allowfullscreen>
  </iframe>
</div>
```

**Replace `VIDEO_ID`** with the actual YouTube video ID (e.g., `xSqnWcLFd6Y`).

### Inline HTML

Inline HTML is **allowed and encouraged** for:

- Embedded videos (YouTube iframes)
- Custom styling not possible with markdown
- Responsive images with CSS wrappers

**Images**: Use standard markdown with `{ width= }` — do **not** use inline HTML for images.

```html
<!-- Responsive image -->
<div class="image-wrapper">
  <img src="/assets/images/screenshot.webp"
       alt="Description" />
</div>
```

MD033 (no inline HTML) is **disabled** in `.markdownlint.json` for this repo.
