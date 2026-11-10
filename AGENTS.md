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

**LLMs.txt**: This repo maintains `/llms.txt` as a curated entrypoint for AI agents. When adding, removing, or reorganizing articles/categories, update `llms.txt` to keep it current.

## Editorial Workflow

Load the `zensical` skill for editorial guidance when creating, drafting, or
editing an article in `docs/`. Apply its article-review checklist during
drafting, not as a post-hoc cleanup pass. Editing means any change a reader
would notice in the prose: a rewritten section, a new opening, a reordered
argument, a claim replaced by a sharper one. A correction limited to a typo, a
broken link, a version number, or formatting does not need the review.

Two authorities apply, and this file is the stricter one:

- `zensical` supplies the review mechanics: how to characterize the voice
  already present, which tell families to walk, and how to report a finding.
- This file and the [Voice model](#voice-model) supply the rules. Where the
  portable checklist allows a load-bearing contrast, an em dash for a genuine
  interruption, or a semicolon between balanced clauses, this blog still
  disallows them. A rule here wins over a general allowance there.

Review once before drafting and once after fixing, and stop there. For an edit
that reaches a reader, say in the change what you checked, including the tell
families that turned up nothing. `zensical build` proves links and rendering
only, so a clean build is not evidence that anyone read the prose.

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

For the editorial rationale and the seven article forms, the maintainer keeps a
charter at `docs/blog-editorial-charter.md` in a separate local project. It is
not part of this repository, so treat the guidance in this file as complete on
its own and the charter as background reading when it happens to be available.

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

### Voice model

The reference register for an authored technical article is Jan Brennenstuhl’s
writing (<https://www.janbrennenstuhl.eu/writing/>). Treat it as a model for how
a field note sounds, not as a template to copy and not as permission to borrow
another writer’s subject matter. What to aim for:

1. **Open with motive, method, and finding in one short dek.** Three clauses:
   what I wanted to know, what I did about it, what I found. Do not warm up with
   a repository inventory or a mission statement.
2. **Use the first person singular in the active voice** for anything the author
   did. “I made the check reject the trailer” reads as a decision; “the trailer
   was rejected” reads as a system description.
3. **Own the author’s own mistakes, not only other people’s reports.** A
   regression the author introduced and then fixed is stronger evidence of a real
   practice than a link to someone else’s bug.
4. **Interpret every number in the same breath as the number.** A count or a
   table cell without a sentence saying what it means is decoration. Say what it
   shows, what it does not show, and what the reader should take from it.
5. **Make hedges orient the reader.** State the limit of the evidence once,
   beside the claim it bounds, and say how much weight to give it. A disclaimer
   after every sentence reads as fear.
6. **State judgment as a decision, a reason, and a consequence.** If the article
   does not rank something, say so, and say what that costs the reader.
7. **Let evidence trail the claim as an aside.** The sentence carries the
   assertion, and the issue number or link is a parenthetical on it. A list of
   sources is not a substitute for the argument that cites them.
8. **Use plain noun-phrase headings, and let some of them carry the argument.**
   “How far the check may go” is a heading; “Additional considerations” is not.
9. **Keep one register throughout:** plain, dry, specific, and occasionally
   self-deprecating. Do not mix audit formality with slang.
10. **Close on what is unfinished and how a reader can help**, with a concrete
    route such as an issue, a page, or a command. A moral is the weaker close.
11. **State the point once, in the affirmative.** The negated contrast is the
    most recognisable AI cadence in prose: “X, not Y”, “this rather than that”,
    “do this instead of that”. Write the claim you mean and let the opposite go
    unstated. Name a possible misreading in a full sentence of its own only when
    a reader could plausibly hold it, and keep “instead” for a literal
    substitution of one action for another.
12. **Write sentences you would say out loud.** The test is a colleague at a
    coffee break: would you tell them this, in these words? A sentence that only
    works on the page is usually doing something a speaker would not do. The
    clearest case is the semicolon. Speech joins two independent clauses with a
    full stop, with “but” or “while”, or with a comma and a conjunction. A
    semicolon in prose drops written register into the middle of an explanation.
    End the sentence and start another one, or name the relation with a word.
    Code, configuration, and quoted source keep their own punctuation.

Four corrections show the shape better than another description:

- `The files in those commits were fine; their public provenance was the
  problem.` becomes `The files in those commits were fine. Their public
  provenance was the problem.`
- `They are reports from affected users, not a substitute for a current product
  contract.` becomes `I read those as reports of what happened to the writer. I
  could not find a current product contract that settles the default.`
- The heading `Additional considerations` becomes `What the recovery cannot
  promise`.
- The close `That does not make an agent infallible. It makes the project easier
  for both the agent and its maintainer to understand next time.` becomes `The
  routing table is the part I reread after every checklist change.`, followed by
  a link a reader can act on.

Rules that keep the model honest:

- **Never manufacture an observation, measurement, or incident.** If the author
  did not run, build, break, or measure the thing, the article does not get a
  first-person scene and the historical record is not adjusted to supply one.
  Write the shorter page the evidence supports, or choose a different question.
- **Do not pad a reference page into an essay.** The model applies to field
  notes, experiment reports, and essays. A page whose real job is retrieval
  stays short and direct.
- **Apply the model to the text being changed.** The older corpus still carries
  semicolons, em dashes, and negated contrasts. Clean an article when you are
  already editing it, or as a pass of its own, and keep that sweep out of an
  unrelated change.

### Technical accuracy protocol

For technology articles, investigate factual claims before presenting them as
settled. This includes product behavior, versions, models, provider limits,
pricing, compatibility, commands, configuration, security, and “works out of
the box” claims.

1. Separate documented facts, local observations, community reports, and
   inferences. Do not present one as another.
2. Use current primary sources for product-dependent claims and reproduce the
   decisive workflow when practical. A package installation, listed model, or
   interactive success alone is not end-to-end evidence.
3. For volatile, version-sensitive, or decision-critical claims, state the
   version and relevant provider/account constraints; retain a source URL and
   review date, and state remaining uncertainty.
4. Replace a broad claim that cannot be verified with a caveat or
   `[AUTHOR NOTE: ...]`. Never invent a test result, compatibility guarantee,
   or personal experience.
5. Perform factual verification as a separate pass before developmental
   editing, then run the site’s normal link and build checks.

`/home/sand/projects/digital-basement/docs/editorial-core.md` is the canonical
editorial and evidence policy. The `/home/sand/projects/zensical-skill`
workflow is for Zensical content and rendering validation; it does not decide
factual accuracy or editorial judgment.

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
## Git Workflow

- **Default branch:** `master` (also accepts `main` in some workflows). Treat it as protected.
- **Changes:** Work on a feature branch, open a pull request, and merge via PR (see `.github/workflows/docs.yml` for deployment triggers). Direct pushes to `master` are discouraged; branch protection may block them.
- **Branch hygiene:** Delete merged branches locally and remotely (e.g. `git branch -d <branch>` and `git push origin --delete <branch>` or enable "Automatically delete head branches" in GitHub settings). Keep only long-lived branches.
- **Commit policy:** See [Git Commit Policy](#git-commit-policy) below. Enforced locally by `.pre-commit-config.yaml` (hook) and in CI by [`.github/workflows/commit-message-guard.yml`](.github/workflows/commit-message-guard.yml).

## Git Commit Policy

**Human-only commits. No bots. No AI attribution. No exceptions.**

This is a personal blog. Every commit must reflect human authorship only, and the
repository history and contributors list must show only @CodeSigils.

**Forbidden in every commit message:**

- Any `Co-authored-by:` trailer — regardless of identity. No AI agents
  (`clio-agent@sisyphuslabs.ai`, `Sisyphus`, ...), no accounts matching the
  `*[bot]` pattern (`github-actions[bot]`, `dependabot[bot]`,
  `renovate[bot]`, ...), no other automation or AI identity. AI contributors
  are forbidden unless explicitly authorised by the repository owner in
  advance — the default is none, and no such authorisation currently exists
  for this blog.
- Any agent branding or signature line: `Ultraworked with ...`,
  `Assisted-by: ...`, `Prompted-by: ...`, `Generated-with: ...`,
  `Tool: ...`, or links to agent/framework repositories in commit messages,
  trailers, or PR descriptions.
- Any attribution appended by tooling, hooks, templates, or `init.templateDir`
  defaults. Tooling must never write trailers of its own accord.

**If a violation lands anyway** (amend, rebase, or cherry-pick reintroduces
one): rewrite it out of history before pushing — amend or
`git rebase` + `git push --force-with-lease`. Never leave it in a pushed
commit. This rule is enforced by a local `commit-msg` hook
(`.pre-commit-config.yaml`, bootstrapped once per clone with
`uvx pre-commit install`) and a CI check
(`.github/workflows/commit-message-guard.yml`); do not bypass them
(`--no-verify` is itself a violation).


