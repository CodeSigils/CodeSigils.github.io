---
title: When an AI Agent Signs Your Commits
description: A field note on finding non-consensual AI attribution in a blog's git history, what GitHub's contributor caches hide, and the layered cleanup that cleared it.
keywords:
  - AI attribution
  - Co-authored-by
  - git history
  - GitHub contributors
  - agent hygiene
  - commit provenance
---

The contributors widget on a GitHub repository looks like a plain statement of
fact: avatars, names, a count. When this blog's repository started listing an
AI agent next to my own account, the first question was whether the widget was
simply wrong. It was not wrong, exactly. Two commits in the history carried
attribution I had never agreed to: a `Co-authored-by` trailer naming an AI
agent, and a branding line at the bottom of a commit message reading
`Ultraworked with [Sisyphus](https://github.com/...)`.

The question I kept coming back to was simple: who authorised this, and what is
the remedy when nobody agrees it should be there?

## What the history actually contained

The trailers were small. One documentation commit ended with
`Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>`; another ended with the
branding line above. Both were added by agent tooling during an ordinary
work session, the way these frameworks credit the tool that produced the
change. GitHub parses commit messages at render time, so a trailer written
months ago can change a widget today ([GitHub's co-author
documentation](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-commits-with-co-authored-attributions)
explains the format and how GitHub turns trailers into credits).

What made this easy to miss is that `git log`'s default view shows subjects,
not bodies. The trailers sat several lines down in messages I had no reason to
reopen. The same experience shows up well beyond this repository: a
[claude-code
discussion](https://github.com/anthropics/claude-code/issues/83813) describes
an attribution trailer sitting 123 commits deep before anyone noticed, with
tags, open pull requests, and uncollected garbage keeping the old objects
reachable long after the author had decided to remove it.

## The same complaint, filed by hundreds

My trailer came from an agent framework rather than an IDE plugin, but the
pattern is not one tool's fault. Claude Code is the most documented case: its
commit workflow appends `Co-Authored-By: Claude <noreply@anthropic.com>` by
default, and a long trail of issues in the
[claude-code](https://github.com/anthropics/claude-code/issues) tracker asks
for that default to change.

- [Issue #48145](https://github.com/anthropics/claude-code/issues/48145),
  titled "should be opt-in", reports a user finding the trailer on every
  public commit they had pushed and arguing that documentation buried in a
  system prompt is not consent.
- [Issue #7422](https://github.com/anthropics/claude-code/issues/7422)
  records the trailer being added even when the project's `CLAUDE.md` says,
  in those words, "DO NOT put this in the commit message".
- [Issue #53259](https://github.com/anthropics/claude-code/issues/53259)
  catalogues the failed escape hatches: `settings.json`, `CLAUDE.md`, custom
  skills, and explicit in-session instructions, with different commit code
  paths in the same session disagreeing about whether to honour them. A
  maintainer in [issue #79909](https://github.com/anthropics/claude-code/issues/79909)
  states that an empty `attribution.commit` setting is the supported switch
  and verifies it, while other reporters say the same key did nothing for
  them; even that disagreement is part of the problem.
- [Issue #64019](https://github.com/anthropics/claude-code/issues/64019)
  describes the same repair I ended up running here: a full `filter-branch`
  pass and force push across the whole history. The reporter in #79909 got
  there too, after a trailer reached a private organisation repository and
  needed `git commit --amend` plus `--force-with-lease`.

The complaint is ethical as much as technical. One recurring theme across
those threads is that the trailer presents the tool as a co-author of the
user's work, in the user's name, without anything the user would recognise
as an approval step.

Codex, by contrast, has so far followed the cleaner practice. Its CLI does
not append a co-author trailer by default: a January 2026 analysis on
OpenAI's community forum, examining a dataset of AI-assisted commits, found
no commit-level attribution or metadata in Codex-associated commits at all
([community analysis](https://community.openai.com/t/does-openai-codex-add-any-default-commit-level-metadata-in-git-workflows/1371947)).
When the option exists, it sits behind an opt-in feature flag
(`codex_git_commit`, with `commit_attribution = ""` disabling even that),
merged in early 2026 rather than assumed at install time
([issue #19799](https://github.com/openai/codex/issues/19799) tracks the
remaining documentation ambiguity). The request threads run in the opposite
direction from Claude's: [discussion #2807](https://github.com/openai/codex/discussions/2807)
and [issue #938](https://github.com/openai/codex/issues/938) ask Codex to
*add* a trailer for teams that want disclosure, as parity with Claude Code.
Nobody in those threads is trying to get attribution out of their history.

One more sign that this has become a genre rather than an incident: purpose
built scrubbers now exist. The
[git-attribution](https://github.com/Londopy/git-attribution) tool scans
history for trailers from seven known agents, rewrites them out, and
installs a pre-push guard so they do not come back. A tool category for
removing a default is its own verdict on the default.

## Two caches, two answers

The first cleanup pass rewrote the three affected commit messages, and the
file contents stayed byte-identical (verified with `git diff` against a backup
ref before the backup was removed). Then the surfaces started disagreeing:

- The REST `/contributors` endpoint returned exactly one account, mine.
- The homepage sidebar widget still credited the AI agent.
- The Insights contributors graph had already forgotten it after the
  force-push.

That split is the finding worth keeping. The best measurements I found come
from [declaudify](https://github.com/ParkerrDev/declaudify), a tool built
precisely to flush this kind of stale attribution. Its author tested the
behaviour rather than assuming it: GitHub renders contributors from two
separate caches, a force-push clears the Insights graph but not the homepage
sidebar, extra commits do not help, and archive/unarchive does nothing.
Toggling the default branch is what clears the sidebar, in his measurements
between 60 and 81 seconds across three trials. The REST `/contributors`
endpoint omits co-authors entirely, which is why an API check can look clean
while the widget still names an AI account.

Community reports match the shape of that problem:

- [Discussion #205858](https://github.com/orgs/community/discussions/205858)
  includes a staff reply: "I've refreshed the contributors list, so it should
  be up to date now." Several other affected repositories are listed by their
  owners in the same thread.
- [Discussion #201982](https://github.com/orgs/community/discussions/201982)
  reports a stale contributor list lasting more than a month, with a checklist
  of nudges: empty commit, edit the repository description, check tags and
  branches for the old SHA, verify in a logged-out window.
- [Discussions #205779](https://github.com/orgs/community/discussions/205779),
  [#204093](https://github.com/orgs/community/discussions/204093), and
  [#202538](https://github.com/orgs/community/discussions/202538) show the
  same pattern: REST and Insights clean, sidebar still crediting an AI account.
- [Discussions #202540](https://github.com/orgs/community/discussions/202540)
  and [#198886](https://github.com/orgs/community/discussions/198886) report
  sidebar staleness measured in weeks.

| Surface | What it reads | How it actually refreshed |
| :--- | :--- | :--- |
| Insights graph | the rewritten history | force-push (per declaudify's tests) |
| REST `/contributors` | commit authorship, no co-authors | updated with the rewrite |
| Homepage sidebar widget | its own cache of parsed trailers | default-branch toggle, staff refresh, or the documented wait |

I also found a cheap way to check the widget's real data source without a
browser: GitHub's JSON payload for the repository route. A `GET` on the
repository page with `Accept: application/json` returns the rendered route,
and the same header on the `/_sidebar` path returns the widget's feed
directly:

```bash
curl -s -H "Accept: application/json" \
  https://github.com/CodeSigils/CodeSigils.github.io/_sidebar
```

After the flush, that feed reported `contributorCount: 1`. Checking the data
source rather than the rendered page settled the question in one request.

## The cleanup, step by step

Nothing about the remediation is complicated individually. The difficulty is
that no single document lists the sequence.

**1. Rewrite the messages, not the tree.** A `git filter-branch` pass with a
message filter over the affected range strips the offending lines while
leaving every file byte-identical:

```bash
git filter-branch -f --msg-filter \
  "grep -v -e '^Co-authored-by: ' -e '^Ultraworked with '" \
  3deab8c..master
```

[filter-repo](https://github.com/newren/filter-repo) is the more modern tool
for the same job; I used `filter-branch` for a three-commit range where the
surgical fix was smaller than the migration.

**2. Push the rewrite and purge the remnants.** `git push --force-with-lease`
updates the remote, then the local backup refs, `ORIG_HEAD`, and reflogs have
to go (`git reflog expire --expire=now --all && git gc --prune=now`), or the
old SHAs stay alive locally and the cleanup looks incomplete to the next
`git fsck`.

**3. Re-queue GitHub's metadata refresh.** An empty commit with a mundane
message (`chore: refresh repository metadata`) gives GitHub's jobs something
new to index. This alone does not clear the sidebar.

**4. The drastic part: toggle the default branch.** This is the sequence that
actually flushed the widget cache:

```bash
gh auth status
git push origin master:refresh/sidebar-flush
gh api -X PATCH /repos/CodeSigils/CodeSigils.github.io -f default_branch=refresh/sidebar-flush
sleep 90
gh api -X PATCH /repos/CodeSigils/CodeSigils.github.io -f default_branch=master
git push origin --delete refresh/sidebar-flush
```

What each line does: `gh auth status` confirms the token carries admin rights,
because changing the default branch is an administrative operation. The second
line pushes `master` to a temporary branch name without touching local state.
The first `PATCH` makes that branch the repository's default, which forces
GitHub to recompute the repository's route data, sidebar included. `sleep 90`
covers the 60-to-81-second window declaudify measured, with margin. The second
`PATCH` restores `master` as the default, and the last line deletes the
temporary branch. No content changes at any point; the repository ends exactly
where it started, minus the stale cache.

!!! warning "Flush only after the index is clean"

    The author of [declaude](https://github.com/ediiloupatty/declaude) warns
    that flushing caches while GitHub still serves the old commit index can
    rebuild the graph from the old history and re-insert the AI credit. Verify
    through the API and commit search that the remote history is clean first,
    then flush, then verify again, retrying up to three times if the widget
    comes back wrong.

One residual worth knowing: rewritten commits remain reachable by their old
SHA and through `refs/pull/N/head` if pull requests existed. Neither surface
feeds the contributor widgets, but in the claude-code discussion above, one
reporter's old commits stayed alive through three open pull requests and
required GitHub Support to delete them, over two rounds of tickets. This
repository had no pull requests holding the old objects, so the purge was
clean.

## Why I consider the default unethical

I consider non-consensual AI attribution in commit messages an unethical
practice, and the cleanup is what convinced me.

A commit trailer is an assertion of authorship. When tooling writes that
assertion in my commits by default, it forges a provenance claim I never
approved: it presents an AI agent as a co-author of my writing, under my name,
in a public record. Consent is absent at every step. The addition is
automatic, the display is asynchronous, and the person credited with the
mistake is the one who has to undo it.

What makes it worse is the response on the other side. I found no official
guidance addressing unwanted attribution from agent tooling. GitHub's
documentation explains how to add co-authors and how to remove one from a
commit before it is shared; once the commit is pushed and the caches have
eaten it, the published remedy for stale contributor data amounts to "wait up
to 24 hours, then contact Support," as quoted by staff in
[discussion #205858](https://github.com/orgs/community/discussions/205858).
There is no button, no API, no documented procedure for the person whose
repository is misrepresenting authorship. The working knowledge lives in
community threads where affected owners compare notes and occasionally
persuade a staff member to refresh a list by hand.

So the burden sits entirely with the author: discover the problem, learn that
the widget and the API disagree, find a tool author's measurement of which
cache clears how, rewrite history, and toggle a branch switch as a cache
flush. That asymmetry is the ethical failure in one sentence: a practice that
creates a false authorship claim, with no concern from the tooling that adds
it and no clear remedy on the platform that displays it.

## What keeps it from happening again

The lesson I took is that attribution has to be enforced by machinery at more
than one layer, because instructions alone demonstrably lose. The
claude-code discussion is the clearest evidence: one reporter's
`attribution` settings were configured to suppress commits and pull-request
credits, and the trailer appeared anyway; the conclusion reached in that
thread was that only a command-level hook inspecting tool calls before they
run, plus a CI gate failing on attribution patterns, can be trusted.

What exists in this repository now:

- **A written policy.** This repository's `AGENTS.md` carries a Git Commit
  Policy section: no `Co-authored-by:` trailers of any kind, no bot accounts,
  no agent branding lines, no `--no-verify`. My local agent instructions
  carry the same rule.
- **A local `commit-msg` hook** rejecting forbidden trailers and branding
  lines, built on [pre-commit](https://pre-commit.com/) with a pygrep rule.
  It fires on `commit`, `commit --amend`, and interactive reword. It does not
  fire on cherry-picks, and `--no-verify` walks past it — which is why it is
  the first layer, not the only one. The other candidates I evaluated:
  [gitlint](https://jorisroovers.com/gitlint/) has been dormant since its
  2023 release and offers no must-not-match rule at all, and
  [commitlint](https://commitlint.js.org/) would need a custom plugin for a
  deny rule.
- **A CI backstop** that scans pushed commit messages and fails the build on
  the same patterns. A hook can be skipped with `--no-verify`, which my
  policy treats as a violation in itself; a CI check cannot be skipped from
  a laptop. It cannot refuse the push itself — on a push event it can only
  flag what has already landed — but a red run on `master` is a signal that
  triggers the rewrite procedure above.

## What I took from it

Rendered summaries are caches with opinions. The widget was neither lying nor
telling the whole truth; it was serving a different index than the API I
checked first, and trusting the first clean answer would have ended the
investigation one layer too early. Since then I read the data source before I
believe the page, and I treat every claim my history makes about authorship
as something I am responsible for. An agent can write the commit. It does not
get to sign it.

## Sources and discussions

**Incidents and community reports**

- [Community discussion #205858](https://github.com/orgs/community/discussions/205858)
  — staff refresh reply, 24-hour guidance quoted, multiple affected repositories.
- [Community discussion #201982](https://github.com/orgs/community/discussions/201982)
  — stale beyond a month, nudge checklist.
- [Discussions #205779](https://github.com/orgs/community/discussions/205779),
  [#204093](https://github.com/orgs/community/discussions/204093),
  [#202538](https://github.com/orgs/community/discussions/202538),
  [#202540](https://github.com/orgs/community/discussions/202540),
  [#198886](https://github.com/orgs/community/discussions/198886) — sidebar
  staleness and API/widget disagreement.
- [anthropics/claude-code issue #83813](https://github.com/anthropics/claude-code/issues/83813)
  — instruction-level attribution settings losing, deep-trailer incident,
  PR-held objects, machine-enforcement conclusion.

**Other agents' defaults**

- [claude-code #48145](https://github.com/anthropics/claude-code/issues/48145)
  — "this should be opt-in", consent argument.
- [claude-code #7422](https://github.com/anthropics/claude-code/issues/7422)
  — trailer added against explicit `CLAUDE.md` instructions.
- [claude-code #53259](https://github.com/anthropics/claude-code/issues/53259)
  — catalogue of failed overrides and code-path inconsistency.
- [claude-code #79909](https://github.com/anthropics/claude-code/issues/79909)
  — recurrence after in-conversation instruction; maintainer's supported
  `attribution.commit` switch.
- [claude-code #64019](https://github.com/anthropics/claude-code/issues/64019)
  — full-history `filter-branch` cleanup account.
- [OpenAI community analysis of AI-assisted commits](https://community.openai.com/t/does-openai-codex-add-any-default-commit-level-metadata-in-git-workflows/1371947)
  — no commit-level metadata found in Codex commits (January 2026).
- [openai/codex #19799](https://github.com/openai/codex/issues/19799) —
  attribution behaviour documentation gap.
- [openai/codex discussion #2807](https://github.com/openai/codex/discussions/2807)
  and [#938](https://github.com/openai/codex/issues/938) — requests to add
  a trailer, not remove one.
- [Londopy/git-attribution](https://github.com/Londopy/git-attribution) —
  multi-agent trailer scanner, rewriter, and pre-push guard.

**Tools and measurements**

- [ParkerrDev/declaudify](https://github.com/ParkerrDev/declaudify) —
  two-cache model, default-branch toggle timings, REST endpoint behaviour.
- [ediiloupatty/declaude](https://github.com/ediiloupatty/declaude) — flush
  ordering caution and retry guidance.
- [newren/filter-repo](https://github.com/newren/filter-repo) — history
  rewriting.

**Official documentation**

- [Creating commits with co-authored
  attributions](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-commits-with-co-authored-attributions)
  — GitHub's format and rendering rules.
- [pre-commit](https://pre-commit.com/), [gitlint](https://jorisroovers.com/gitlint/),
  [commitlint](https://commitlint.js.org/) — candidate enforcement frameworks.

**On this site**

- [When Agent Instructions Start to Drift](./agent-instruction-drift.md) —
  the maintenance problem that duplicated rules create.
- [Agent Memory Is a Surface, Not an Archive](./agent-memory-surfaces.md) —
  what agent-side persistence actually keeps.

Links were reachable when this article was written in October 2026.
