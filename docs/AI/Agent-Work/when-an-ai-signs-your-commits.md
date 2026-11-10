---
title: When an AI Agent Signs Your Commits
description: A field note on finding non-consensual AI attribution in a blog's git history, why GitHub contributor surfaces can disagree, and the layered cleanup that cleared it.
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

An AI account appeared beside mine in this repository's GitHub contributors
widget. I had not added it as a co-author. The explanation was in two old
commit messages. One carried a `Co-authored-by` trailer for an AI agent. The
other ended with `Ultraworked with [Sisyphus](https://github.com/...)`.

The files in those commits were not the problem. Their public provenance was.
I needed to remove the unwanted lines without changing the trees, then make
the same surprise less likely for the next commit.
It led to [ai-repo-sanitize](https://github.com/CodeSigils/ai-repo-sanitize),
a small tool that checks, previews, and safely rewrites known AI-attribution
lines. This field note records the incident, the limits of GitHub's contributor
views, and the safeguards I now use.

## What the history contained

The trailers were easy to overlook. One documentation commit ended with
`Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>`. Another ended with the
branding line above. Both were added by agent tooling during an ordinary
work session. GitHub recognises co-author trailers in commit messages, so a
trailer can become a visible credit ([GitHub's co-author documentation](https://docs.github.com/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors)
describes the format and how it is rendered).

`git log`'s default view shows subjects, not bodies. These lines sat several
lines down in messages I had no reason to reopen. The problem is not unique to
this repository: a
[claude-code
discussion](https://github.com/anthropics/claude-code/issues/83813) describes
an attribution trailer sitting 123 commits deep before anyone noticed, with
tags, open pull requests, and uncollected garbage keeping the old objects
reachable long after the author had decided to remove it.

## Reports across tools

My incident came from one agent framework. Users report similar problems
across several tools. Claude Code has the largest public issue trail I found.
Those reports describe commit workflows adding
`Co-Authored-By: Claude <noreply@anthropic.com>` and ask for an opt-in default.
They are reports from affected users, not a substitute for a current product contract.

Three recurring points matter here:

- [Issues #48145](https://github.com/anthropics/claude-code/issues/48145),
  [#7422](https://github.com/anthropics/claude-code/issues/7422), and
  [#5458](https://github.com/anthropics/claude-code/issues/5458) describe
  trailers appearing despite users asking for opt-in behavior or explicit
  project instructions.
- [Issues #53259](https://github.com/anthropics/claude-code/issues/53259) and
  [#79909](https://github.com/anthropics/claude-code/issues/79909) record
  conflicting reports about configuration and instruction-based suppression.
  A setting reported as supported by one maintainer did not work for every
  reporter.
- [Issue #64019](https://github.com/anthropics/claude-code/issues/64019)
  shows the cost of discovering the trailer after publication. The reported
  recovery involved rewriting history and force-pushing it.

The technical problem is small. The provenance decision is not. A trailer
presents a tool as a co-author of work published in the user's name. That
choice belongs to the author, before the commit is created.

My observations of Codex point in a different direction: I have not seen it
append a co-author trailer in this work, and a January 2026 community analysis
reported the same result in its sample
([community analysis](https://community.openai.com/t/does-openai-codex-add-any-default-commit-level-metadata-in-git-workflows/1371947)).
That is a dated observation, not a permanent product guarantee. The current
official CLI reference does not establish the configuration details that were
previously described here. Teams that want attribution or want to prohibit it
should set and enforce their own repository policy rather than infer a durable
default from an issue thread.

Purpose-built scrubbers now exist. The
[git-attribution](https://github.com/Londopy/git-attribution) tool scans
history for trailers from known agents, rewrites them out, and installs a
pre-push guard. Its existence is useful evidence that some teams want a way to
remove or prevent this metadata.

I later built
[ai-repo-sanitize](https://github.com/CodeSigils/ai-repo-sanitize). It turns
the recovery into a checked process: `check` scans reachable local and fetched
history, `preview` identifies matching messages, and `rewrite` removes only
matching attribution lines. The rewrite verifies that the resulting tree is
unchanged, creates a mirror backup, and never pushes unless the maintainer adds
`--push`. The scanner also provides a read-only CI check.

That does not replace policy or owner review. It makes the technical boundary
enforceable: human co-author trailers remain intact, matching AI attribution is
removed line by line, and a history rewrite cannot quietly become a remote
change.

## GitHub's contributor views can disagree

The cleanup rewrote three commit messages while leaving their file contents
byte-identical. I compared the rewritten tree with a backup ref before
removing it. GitHub then gave me three different answers:

- The REST `/contributors` result listed my account as the only contributor.
- The homepage sidebar still credited the AI agent.
- The Insights contributors graph no longer showed the agent after the
  force-push.

The closest comparison I found is
[declaudify](https://github.com/ParkerrDev/declaudify), a tool built for stale
attribution. Its author observed that the Insights graph, REST endpoint, and
homepage sidebar can update on different schedules. A force-push cleared the
Insights graph in those tests but did not immediately change the sidebar. That
matches my result, but it is not a documented model of GitHub's internal
caches. The REST `/contributors` endpoint does not audit trailers, so a clean
API response cannot settle what the sidebar will show.

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

| Surface | What it reads | What the evidence can show |
| :--- | :--- | :--- |
| Insights graph | the rewritten history | a force-push updated it in this case |
| REST `/contributors` | author-email contributor counts | it can be cached for hours and is not a trailer audit |
| Homepage sidebar widget | an undocumented contributor view | it can disagree with the API. GitHub documents no cache-refresh control |

The REST endpoint is useful as one signal, not a verdict. GitHub documents it
as an author-email-based contributor count and warns that the response can be
cached for hours.

### A read-only look at the widget

During this incident, GitHub served an undocumented sidebar payload at
`/_sidebar` when asked for JSON:

```bash
curl -s -H "Accept: application/json" \
  https://github.com/CodeSigils/CodeSigils.github.io/_sidebar
```

This `GET` does not clear or repair a cache. It exposed `contributorCount: 1`
before the visible widget caught up. Treat it as a complementary diagnostic
beside the REST endpoint and rendered sidebar, not as a stable interface or an
automated fix.

## A safer recovery process

The original repair used a one-off `filter-branch` pass. Git now warns about
that command's safety and performance limits and recommends
[filter-repo](https://github.com/newren/filter-repo) for new work. I would use
`ai-repo-sanitize`, which wraps `filter-repo`, for the same situation now.

1. Run `check` and `preview` first. They are read-only and establish which
   reachable commits match the attribution pattern.
2. Run `rewrite` against a fresh working clone with its required backup
   location. It changes message lines only, then verifies that the tree before
   and after the rewrite is identical.
3. Inspect the rewritten messages and the affected refs. The remote remains
   unchanged unless the maintainer separately chooses the explicit push option.
4. If the rewrite is approved, publish with the tool's `--force-with-lease`
   path. Then inspect the normal GitHub contributor surfaces and allow time for
   their documented caching behaviour.

The process does not claim to clear GitHub's homepage widget. GitHub documents
that its contributors API may be cached for hours, and I found no supported API
or CLI command that flushes the sidebar. A default-branch change is an
administrative repository change, not a documented cache remedy. It should not
be used as routine cleanup.

Rewritten commits can remain reachable by their old SHA and through
`refs/pull/N/head` when pull requests exist. Those refs need inspection when
deciding whether the unwanted message remains accessible. In the Claude Code
discussion above, old commits stayed alive through open pull requests and
required GitHub Support to remove them. This repository had no pull requests
holding the old objects, so that particular concern did not apply here.

## Why consent belongs in the workflow

I consider non-consensual AI attribution in commit messages unethical. The
cleanup made the reason concrete.

A commit trailer makes a public claim about authorship. When tooling writes
that claim into my commits by default, it assigns a co-author to work published
in my name without my approval. The author then has to discover and remove it.

I found no official guidance addressing unwanted attribution from agent
tooling. GitHub's
documentation explains how to add co-authors and how to remove one from a
commit before it is shared. Once the commit is pushed and the caches have
not yet caught up, the published remedy for stale contributor data amounts to "wait up
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

## The safeguards I now use

Settings and written instructions state the policy. They do not enforce it. I
use three layers instead:

1. Write the repository policy in the instructions that agents and maintainers
   actually read. In this repository, that means no agent attribution trailers,
   branding lines, or bypassing the normal commit checks.
2. Reject a matching message locally with a `commit-msg` hook. This gives the
   person making the commit a clear failure before the history changes.
3. Run `ai-repo-sanitize check` in CI against the reachable history. CI cannot
   prevent a push, but it gives the repository an independent result and makes
   a bypass visible for review.

The local hook and CI check should share a documented policy boundary.
Otherwise a message can pass one layer and fail another because each tool
describes AI attribution differently. `ai-repo-sanitize` keeps its scanner and
rewriter on one pattern definition. Its defaults preserve human co-author
trailers and only remove the known agent trailers or branding lines that match
the policy.

This repository deliberately blocks `dependabot[bot]`, but that is a
maintainer choice, not a universal conclusion. Dependabot is GitHub's
dependency-update automation: it opens security and version-update pull
requests rather than asserting co-authorship of a human-directed change. A
maintainer may reasonably allow it while still rejecting AI attribution. The
important part is deciding which automated identities may enter the history,
then making the hook and CI rule match that decision.

## Signing is useful, but it answers a different question

Commit signing is a useful companion to these checks, but it solves a different
problem. A signature lets GitHub verify that the person holding a configured
GPG, SSH, or S/MIME key created the commit. It does not make an AI trailer true
or settle who wrote the change. It proves control of a key at the time of the
commit.

The placeholder in `user.signingkey` is not one universal value: Git reads it
through the selected signing format. After adding the public SSH key to GitHub
as a signing key, the complete SSH default setup is:

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

Start with the commit messages. GitHub's REST result, Insights graph, and
sidebar are separate diagnostics that can update at different times. If you
need a repair, use a tool that previews its scope, verifies a message-only
rewrite, keeps a backup, and requires an explicit push decision. A contributor
widget is not an authorship audit.

## Sources and discussions

**Incidents and community reports**

- [Community discussion #205858](https://github.com/orgs/community/discussions/205858):
  staff refresh reply, 24-hour guidance quoted, multiple affected repositories.
- [Community discussion #201982](https://github.com/orgs/community/discussions/201982):
  stale beyond a month, nudge checklist.
- [Discussions #205779](https://github.com/orgs/community/discussions/205779),
  [#204093](https://github.com/orgs/community/discussions/204093),
  [#202538](https://github.com/orgs/community/discussions/202538),
  [#202540](https://github.com/orgs/community/discussions/202540),
  [#198886](https://github.com/orgs/community/discussions/198886): sidebar
  staleness and API/widget disagreement.
- [anthropics/claude-code issue #83813](https://github.com/anthropics/claude-code/issues/83813)
  instruction-level attribution settings losing, deep-trailer incident,
  PR-held objects, machine-enforcement conclusion.

**Other agents' defaults**

- [claude-code #48145](https://github.com/anthropics/claude-code/issues/48145):
  "this should be opt-in", consent argument.
- [claude-code #7422](https://github.com/anthropics/claude-code/issues/7422):
  trailer added against explicit `CLAUDE.md` instructions.
- [claude-code #53259](https://github.com/anthropics/claude-code/issues/53259):
  catalogue of failed overrides and code-path inconsistency.
- [claude-code #79909](https://github.com/anthropics/claude-code/issues/79909):
  recurrence after in-conversation instruction. Maintainer's supported
  `attribution.commit` switch.
- [claude-code #64019](https://github.com/anthropics/claude-code/issues/64019):
  full-history `filter-branch` cleanup account.
- [OpenAI community analysis of AI-assisted commits](https://community.openai.com/t/does-openai-codex-add-any-default-commit-level-metadata-in-git-workflows/1371947)
  dated observation of no commit-level metadata in Codex commits (January 2026).
- [Londopy/git-attribution](https://github.com/Londopy/git-attribution):
  multi-agent trailer scanner, rewriter, and pre-push guard.
- [CodeSigils/ai-repo-sanitize](https://github.com/CodeSigils/ai-repo-sanitize):
  checked scanner, preview, message-only rewrite, backup, verification, and
  opt-in push for known AI attribution patterns.

**Tools and measurements**

- [ParkerrDev/declaudify](https://github.com/ParkerrDev/declaudify):
  two-cache model, default-branch toggle timings, REST endpoint behaviour.
- [ediiloupatty/declaude](https://github.com/ediiloupatty/declaude): flush
  ordering caution and retry guidance.
- [newren/filter-repo](https://github.com/newren/filter-repo): history
  rewriting.

**Official documentation**

- [Creating commits with co-authored
  attributions](https://docs.github.com/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors)
  GitHub's format and rendering rules.
- [Git hooks](https://git-scm.com/docs/githooks): which commands invoke the
  `commit-msg` hook and how `--no-verify` bypasses it.
- [Git history rewriting](https://git-scm.com/docs/git-filter-branch): the
  warning against new `filter-branch` use and its recommendation of
  `filter-repo`.
- [GitHub repository API](https://docs.github.com/en/rest/repos/repos):
  default-branch updates and cached contributor responses.
- [GitHub commit signing](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)
  signing defaults and verification.
- [Dependabot version updates](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-version-updates)
  GitHub's automated dependency-update pull requests.
- [pre-commit](https://pre-commit.com/), [gitlint](https://jorisroovers.com/gitlint/),
  [commitlint](https://commitlint.js.org/): candidate enforcement frameworks.

**On this site**

- [When Agent Instructions Start to Drift](./agent-instruction-drift.md):
  the maintenance problem that duplicated rules create.
- [Agent Memory Is a Surface, Not an Archive](./agent-memory-surfaces.md):
  what agent-side persistence actually keeps.

Links were reachable when this article was written in October 2026.
