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

| Collection | Folder          | Purpose             |
| :--------- | :-------------- | :------------------ |
| **pages**  | `docs/`         | General pages       |
| **home**   | `docs/index.md` | Homepage only       |
| **jsts**   | `docs/JS-TS/`   | JS-TS section       |
| **ai**     | `docs/AI/`      | AI section articles |

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

### Example Verification Workflow

```bash
# Before adding a command like:
curl -fsSL https://example.com/install | sh

# Verify by:
# 1. Checking official docs at https://example.com/docs
# 2. Checking the install script URL is correct
# 3. Confirming the command works on your test environment
```

### Responsive Videos

Use this pattern to embed YouTube videos responsively (maintains 16:9 aspect ratio):

```markdown
<div>
  <div style="position:relative;padding-top:56.25%;">
    <iframe src="https://www.youtube.com/embed/VIDEO_ID"
            frameborder="0"
            allowfullscreen
            style="position:absolute;top:0;left:0;width:100%;height:100%;">
    </iframe>
  </div>
</div>
```

**Replace `VIDEO_ID`** with the actual YouTube video ID (e.g., `xSqnWcLFd6Y`).

This ensures videos scale properly on all screen sizes while maintaining aspect ratio.

### Responsive Images

Use this pattern for responsive images:

```markdown
![Alt text](/assets/images/image.png){ loading=lazy }
```

**Key points:**

- Use `loading=lazy` for below-the-fold images
- Do NOT lazy-load the first image (hero/LCP image)
- Always specify width/height when possible to prevent layout shift

**First image (hero) - no lazy loading:**

```markdown
![Alt text](/assets/images/hero.png){ width=900 }
```
