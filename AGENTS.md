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
uv run zensical build

# Clean build (removes old artifacts first)
uv run zensical build --clean

# Local development server
uv run zensical serve
```

**Important**: Build output goes to `./site/` directory, which is gitignored. Do not edit files in `site/` - edit source in `docs/` instead.

**Current dependencies**: `pyproject.toml` declares direct dependencies and the committed `uv.lock` resolves the complete graph. Use `uv sync --locked`; CI uses the same lockfile.

## Content Structure

The site uses top-level categories under `docs/`. A main category, such as
`AI/`, may contain multiple subcategories; articles live in the appropriate
existing category or subcategory:

```
docs/
├── <category>/          # Top-level section or collection (e.g. AI/, JS-TS/)
│   ├── index.md         # Section landing page
│   ├── *.md             # Articles directly in this section
│   └── <subcategory>/   # Optional nested section (e.g. OpenCode/)
│       └── *.md         # Articles in this subsection
├── admin/
│   └── config.yml       # Sveltia CMS collections
└── assets/images/       # Images (deployed to /assets/images/)
```

For an exact listing of all articles, run: `find docs/ -name '*.md' | sort`

New top-level categories or subcategories require a matching collection in
`docs/admin/config.yml`. New articles are `.md` files inside the appropriate
existing category or subcategory.

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

1. Trigger: Push to `master` or `main` with changes to `docs/**`,
   `zensical.toml`, `pyproject.toml`, `uv.lock`, `.python-version`, or
   `.github/workflows/docs.yml`
2. Non-site files (README.md, AGENTS.md, LICENSE, .gitignore, etc.) do **not** trigger a build
3. Steps: `uv sync --locked` → `uv run zensical build --clean` → Deploy to GitHub Pages
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

These pages are authored Code Sigils blog articles, not search-result summaries
or a single uniform documentation template. A useful page should explain the
author’s recommendation, interpretation, or observation—not only repeat vendor
documentation or collect links. Choose the article’s natural form: guide, field
note, explainer, comparison, experiment report, essay, or visual note. Variation
is expected; repeated headings and identical openings are a quality problem.

Lead with a recognizable reader problem, question, observation, or tension.
Explain why before how when context is needed, include a concrete scenario or
experiment where appropriate, and close with a practical takeaway or reflection.
Research and citations support the article’s judgment; they do not replace it.
Community advice must be attributed and separated from official facts or locally
reproduced practice.

For the editorial rationale and flexible article forms, read
`/home/sand/projects/digital-basement/docs/blog-editorial-charter.md`.

After factual verification, perform a developmental editing pass for human
flow, transitions, examples, pacing, and a clear beginning, middle, and ending.
Do not invent personal experience or opinions. If the author’s perspective is
needed but missing, leave an explicit author note for review.

For a tool or project evaluation, make the reader’s decision explicit. Put a
measured recommendation near that decision, explain the trade-off, and give a
safe next step. Do not bury the article’s judgment under a feature catalogue.
Use a concrete situation or observation to carry the reader into the technical
details; vary the structure when the article’s natural form calls for it.

Use creative technical writing where it helps: open with a real reader problem,
choose a concrete analogy or example, vary the rhythm, and leave the reader
with a memorable practical insight. Creativity changes presentation, not the
facts. Never invent anecdotes, outcomes, sources, or certainty to make prose
more engaging.

SEO is supporting infrastructure, not the purpose of an article. Use accurate
titles, descriptions, headings, internal links, and alt text to help readers
find and understand a page. Never add keywords, headings, FAQs, statistics, or
claims only to satisfy search algorithms. Preserve nuance and the author’s
recommendation even when search-oriented phrasing suggests a simpler “best”
answer.

### Agent and skill use

Agents editing articles should behave as bounded research assistants and
developmental editors. They may inspect current sources, challenge claims,
improve structure and flow, and suggest changes. The maintainer supplies
personal context and judgment and approves substantive edits before publishing.

Prefer the project’s eventual article-review skill when it exists. Until then,
use the repository guidelines directly. External documentation-style,
technical-blog-writing, AI-writing-review, or SEO skills may inform a review,
but they are references—not automatic dependencies—and none may override the
author’s voice or the site’s evidence policy.

Before adding a section, search the repository for an existing explanation,
link, admonition, or article covering the same concern. Consolidate or
cross-link where appropriate instead of creating parallel guidance that can
drift. For volatile topics, record the source and review date in the article
or its verification notes.

Accumulate small article suggestions instead of creating a commit for each one.
Group related observations until they justify a coherent change in scope,
structure, voice, or factual accuracy, then edit and publish one logical batch.

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
| **keywords**    | Optional discovery hints where useful | opencode, AI coding agent, terminal  |
| **icon**        | Lucide icon name           | lucide/terminal                      |

> **Discoverability guidance**
> - Use a clear, unique `title` and an accurate `description` when the page's
>   content warrants them. Metadata helps readers and search engines understand
>   a page; it does not replace useful, well-structured content.
> - Do not force keywords, a fixed keyword count, headings, FAQs, or structured
>   data into an article for ranking purposes. Add keywords only when they are
>   meaningful metadata under the site's existing convention.
> - Keep headings, link text, alt text, and visible body content descriptive.
>   Accessibility is a reader-quality practice, not an SEO shortcut.

### Analytics and indexing decisions

The site declares its canonical URL in `zensical.toml` and its sitemap in
`docs/robots.txt`. Treat Google Search Console, sitemap submission, analytics,
cookie consent, and privacy-policy changes as maintainer decisions: inspect the
deployed output and current provider documentation before proposing a change.

Do not add Google Analytics, third-party tracking, consent banners, or custom
analytics JavaScript merely because Zensical supports them. Add analytics only
for a stated measurement question, with explicit authorization and appropriate
privacy review. Search Console is the lower-burden first step for discovery and
indexing questions.

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

Use admonitions to highlight information that benefits from a visible signpost:
important safety boundaries, practical tips, definitions, decisions, exceptions,
or optional detail. Every article does not need the same number or type. Do not
turn ordinary prose or every feature into a callout; keep each one concise and
useful when scanned on its own.

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

Use content tabs for multi-language examples, alternative package managers, or
platform-specific instructions. They are especially useful for keeping
equivalent npm, pnpm, Yarn, and Python commands compact. When alternatives are
genuinely parallel, check for a tabbed presentation before creating repeated
subsections. Do not hide important prerequisites, warnings, or differences in a
tab without explaining them in the surrounding text:

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
