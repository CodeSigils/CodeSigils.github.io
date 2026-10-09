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

<div class="image-wrapper">
  <img src="/assets/images/contributors-01.webp"
       alt="GitHub contributors widget listing CodeSigils, dependabot[bot], and sisyphus-dev-ai"
       width="579"
       height="390" />
</div>

The contributors widget on a GitHub repository looks like a plain statement of
fact: avatars, names, a count. When this blog's repository started listing an
AI agent next to my own account, I checked whether the widget was accurate.
It was: two commits in the history carried
attribution I had never agreed to: a `Co-authored-by` trailer naming an AI
agent, and a branding line at the bottom of a commit message reading
`Ultraworked with [Sisyphus](https://github.com/...)`.

No one had authorised the attribution, and no single source described how to
remove it completely.

## What the history actually contained

The trailers were small. One documentation commit ended with
`Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>`; another ended with the
branding line above. Both were added by agent tooling during an ordinary
work session, the way these frameworks credit the tool that produced the
change. GitHub parses commit messages at render time, so a trailer written
months ago can change a widget today ([GitHub's co-author
documentation](https://docs.github.com/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors)
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

My trailer came from an agent framework. Users have reported the same pattern
across multiple tools. Claude Code is the most documented case: its
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
- [Issue #617](https://github.com/anthropics/claude-code/issues/617) asks for
  a setting to disable the generated-with line and co-author trailer, citing
  an organisation whose one-line commit standard leaves no room for either.
- [Issue #5458](https://github.com/anthropics/claude-code/issues/5458) makes
  the same consent argument directly: the reporter says attribution continued
  despite an explicit instruction not to add it.
- [Issue #24590](https://github.com/anthropics/claude-code/issues/24590)
  documents a separate reliability problem: the co-author trailer named an
  Opus model while the reporter was using Sonnet, strengthening the case for
  a generic tool identity or no automatic trailer at all.
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

The complaint is ethical as much as technical, in my opinion. One recurring theme across
those threads is that the trailer presents the tool as a co-author of the
user's work, in the user's name, without anything the user would recognise
as an approval step.

Codex, by contrast, has so far followed the cleaner practice. Its CLI does
not append a co-author trailer by default: a January 2026 analysis on
OpenAI's community forum, examining a dataset of AI-assisted commits, found
no commit-level attribution or metadata in Codex-associated commits at all
([community analysis](https://community.openai.com/t/does-openai-codex-add-any-default-commit-level-metadata-in-git-workflows/1371947)).
The option is behind an opt-in feature flag
(`codex_git_commit`, with `commit_attribution = ""` disabling even that),
introduced in early 2026
([issue #19799](https://github.com/openai/codex/issues/19799) tracks the
remaining documentation ambiguity). The request threads run in the opposite
direction from Claude's: [discussion #2807](https://github.com/openai/codex/discussions/2807)
and [issue #938](https://github.com/openai/codex/issues/938) ask Codex to
*add* a trailer for teams that want disclosure, as parity with Claude Code.
Nobody in those threads is trying to get attribution out of their history.

Purpose-built scrubbers now exist. The
[git-attribution](https://github.com/Londopy/git-attribution) tool scans
history for trailers from seven known agents, rewrites them out, and
installs a pre-push guard so they do not come back. The existence of a tool
for removing default attribution suggests the default is not serving everyone.

## Two caches, two answers

The first cleanup pass rewrote the three affected commit messages while
leaving the file contents byte-identical (verified with `git diff` against a
backup ref before the backup was removed), but after inspecting the results I
realised the three checks did not agree:

- The REST `/contributors` endpoint returned exactly one account, mine.
- The homepage sidebar widget still credited the AI agent.
- The Insights contributors graph had already forgotten it after the
  force-push.

The best measurements I found come from
[declaudify](https://github.com/ParkerrDev/declaudify), a tool built
precisely to flush this kind of stale attribution. Its author tested the
behaviour: GitHub renders contributors from two
separate caches, a force-push clears the Insights graph but not the homepage
sidebar, extra commits do not help, and archive/unarchive does nothing.
Toggling the default branch cleared the sidebar after a short delay in those
tests. The REST `/contributors`
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

After the flush, that feed reported `contributorCount: 1`. The feed answered
the question in one request.

## The cleanup, step by step

Each step is straightforward, but I could not find one source that put them
in order.

**1. Remove the trailers from commit messages.** A `git filter-branch` pass with a
message filter over the affected range strips the offending lines while
leaving every file byte-identical:

```bash
git filter-branch -f --msg-filter \
  "grep -v -e '^Co-authored-by: ' -e '^Ultraworked with '" \
  3deab8c..master
```

[filter-repo](https://github.com/newren/filter-repo) also supports this job. I
used `filter-branch` for this three-commit range.

**2. Push the rewrite and purge the remnants.** `git push --force-with-lease`
updates the remote, then the local backup refs, `ORIG_HEAD`, and reflogs have
to go (`git reflog expire --expire=now --all && git gc --prune=now`), or the
old SHAs stay alive locally and the cleanup looks incomplete to the next
`git fsck`.

**3. Re-queue GitHub's metadata refresh.** An empty commit with a mundane
message (`chore: refresh repository metadata`) gives GitHub's jobs something
new to index, but this alone does not clear the sidebar.

**4. Toggle the default branch.** This sequence flushed the widget cache:

```bash
gh auth status
git push origin master:refresh/sidebar-flush
gh api -X PATCH /repos/CodeSigils/CodeSigils.github.io -f default_branch=refresh/sidebar-flush
sleep 90
gh api -X PATCH /repos/CodeSigils/CodeSigils.github.io -f default_branch=master
git push origin --delete refresh/sidebar-flush
```

`gh auth status` confirms that the token carries the administrative permission
needed to change the default branch. The commands push `master` to a temporary
branch, make it the default, wait 90 seconds for GitHub to recompute the route
data, restore `master`, and delete the temporary branch without touching the
repo's actual content.

!!! warning "Flush only after the index is clean"

    The author of [declaude](https://github.com/ediiloupatty/declaude) warns
    that flushing caches while GitHub still serves the old commit index can
    rebuild the graph from the old history and re-insert the AI credit. Verify
    through the API and commit search that the remote history is clean first,
    then flush, then verify again, retrying up to three times if the widget
    comes back wrong.

Rewritten commits can remain reachable by their old
SHA and through `refs/pull/N/head` if pull requests existed. Neither surface
feeds the contributor widgets, but in the claude-code discussion above, one
reporter's old commits stayed alive through three open pull requests and
required GitHub Support to delete them, **over two rounds of tickets**. This
repository had no pull requests holding the old objects, so the purge was
clean.

## Why I consider the default unethical

I consider non-consensual AI attribution in commit messages an unethical
practice, and the cleanup is what convinced me.

A commit trailer is an assertion of authorship. Period. When tooling writes that
assertion in my commits by default, it makes a provenance claim I never
approved and presents an AI agent as a co-author of my writing in a public
record. The author must later find and remove that claim.

I found no official guidance addressing unwanted attribution from agent
tooling. GitHub's
documentation explains how to add co-authors and how to remove one from a
commit before it is shared; once the commit is pushed and the caches have
eaten it, the published remedy for stale contributor data amounts to "wait up
to 24 hours, then contact Support," as quoted by staff in
[discussion #205858](https://github.com/orgs/community/discussions/205858).
GitHub provides no documented procedure for the person whose repository is
misrepresenting authorship. The working knowledge lives in
community threads where affected owners compare notes and occasionally
persuade a staff member to refresh a list by hand.

The burden sits with the author, who must discover the problem, determine why
the widget and API disagree, rewrite history, and trigger the cache refresh.
The tooling creates a false authorship claim, while the platform offers no
clear remedy for removing it.

## What keeps it from happening again

Settings and written instructions are useful, but they do not reliably stop
attribution on their own, so the safeguard needs more than one layer. In the
claude-code discussion, one reporter had configured `attribution` to suppress
credits in both commits and pull requests, yet a trailer still appeared. The
discussion's practical conclusion was that a command-level hook, which checks
tool calls before they run, and a CI gate that fails on attribution patterns
are the only reliable backstops.

What exists in this repository now:

- **A written policy.** This repository's `AGENTS.md` carries a Git Commit
  Policy section: no `Co-authored-by:` trailers of any kind, no bot accounts,
  no agent branding lines, no `--no-verify`. My local agent instructions
  carry the same rule.
- **A local `commit-msg` hook** rejecting forbidden trailers and branding
  lines, built on [pre-commit](https://pre-commit.com/) with a pygrep rule.
  It covers `commit`, `commit --amend`, and interactive reword. Cherry-picks
  and `--no-verify` bypass it, so CI supplies a second check. The other
  candidates I evaluated:
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

## Sign the commits you mean to stand behind

Commit signing solves a different problem, but it is a useful companion to
the checks above. A signature lets GitHub verify that the person holding a
configured GPG, SSH, or S/MIME key created the commit. It does not make an AI
trailer true, nor does it settle who wrote the change; it proves control of a
key at the time the commit was made.

The placeholder in `user.signingkey` is not one universal value: Git reads it
through the selected signing format. For SSH, the complete default setup is:

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

For GPG, `openpgp` is the default format and `user.signingkey` is usually the
long key ID. S/MIME uses the `x509` format and its configured signing program.
Drop `--global` when a repository needs a different key. A one-off signed
commit is `git commit -S -m "message"`. GitHub shows a **Verified** badge when
it can validate the signature, while `git log --show-signature -1` is a quick
local check. The precise key setup varies by GPG, SSH, or S/MIME, so I use
GitHub's
[signing commits guide](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)
rather than copying a key recipe from a random terminal snippet.

## A practical takeaway

GitHub's sidebar and API can rely on different indexes. I now check the data
source behind a contributor widget and treat authorship claims in commit
history as my responsibility.

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
  attributions](https://docs.github.com/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors)
  — GitHub's format and rendering rules.
- [pre-commit](https://pre-commit.com/), [gitlint](https://jorisroovers.com/gitlint/),
  [commitlint](https://commitlint.js.org/) — candidate enforcement frameworks.

**On this site**

- [When Agent Instructions Start to Drift](./agent-instruction-drift.md) —
  the maintenance problem that duplicated rules create.
- [Agent Memory Is a Surface, Not an Archive](./agent-memory-surfaces.md) —
  what agent-side persistence actually keeps.

Links were reachable when this article was written in October 2026.
