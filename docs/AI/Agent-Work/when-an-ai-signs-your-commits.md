---
title: When an AI Agent Signs Your Commits
description: An AI account appeared beside mine in this blog's contributors list. Two commit trailers explained it, and three GitHub surfaces disagreed about the cleanup.
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

I wanted to know why an AI account sat beside mine in this blog's GitHub
contributors widget. The explanation was in two commit messages I had no reason
to reopen, and removing it took a rewrite that left every file in the repository
byte-identical. GitHub then gave me three different answers about whether the
cleanup had worked.

The repair became
[ai-repo-sanitize](https://github.com/CodeSigils/ai-repo-sanitize), a small tool
that checks, previews, and safely rewrites known AI-attribution lines. Here is
what I found, and what I run before the next commit.

## The trailers sat in messages I never reopened

One documentation commit ended with
`Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>`. Another ended with
`Ultraworked with [Sisyphus](https://github.com/...)`. Both were written by agent
tooling during an ordinary work session, and I did not see either line at the
time.

That is the whole reason they lasted. `git log`'s default view shows subjects
only, so the lines sat several lines down in messages I had no reason to open
again. GitHub reads co-author trailers when it renders a commit, which is how a
line I never saw became a visible credit beside my name
([GitHub's co-author documentation](https://docs.github.com/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors)
describes the format and how it is rendered).

The files in those commits were fine; their public provenance was the problem. A
trailer is a claim about who wrote the work, and this one had been published
under my name without my agreeing to it.

My repository is ordinary. A
[claude-code discussion](https://github.com/anthropics/claude-code/issues/83813)
describes an attribution trailer sitting 123 commits deep before anyone noticed,
still reachable afterwards through tags, open pull requests, and uncollected
garbage, long after the author had decided to remove it. The depth is the part I
keep coming back to: no ordinary reading of `git log` would have found it, and
deciding to remove it is the easy half.

## What other people report

My incident came from one agent framework. The largest public trail I found was
Claude Code's, where reporters describe commit workflows adding
`Co-Authored-By: Claude <noreply@anthropic.com>` and ask for an opt-in default. I
read those as reports of what happened to the people who wrote them, and I could
not find a current product contract that settles the default.

Three recurring points mattered to me:

- [Issues #48145](https://github.com/anthropics/claude-code/issues/48145),
  [#7422](https://github.com/anthropics/claude-code/issues/7422), and
  [#5458](https://github.com/anthropics/claude-code/issues/5458) describe
  trailers appearing despite users asking for opt-in behavior or giving explicit
  project instructions.
- [Issues #53259](https://github.com/anthropics/claude-code/issues/53259) and
  [#79909](https://github.com/anthropics/claude-code/issues/79909) record
  conflicting reports about configuration and instruction-based suppression. A
  setting one maintainer described as supported did not work for every reporter.
- [Issue #64019](https://github.com/anthropics/claude-code/issues/64019) shows
  the cost of finding the trailer after publication. The recovery in that report
  was a history rewrite and a force-push.

All three have the same shape. The tooling writes the trailer by default, and
the person who has to undo it finds out afterwards. Removing the lines is
mechanical; deciding who may write them is the part I keep arguing about.

My own observation of Codex points the other way. In this work I have not seen it
append a co-author trailer, and a January 2026 community analysis reported the
same result in its sample
([community analysis](https://community.openai.com/t/does-openai-codex-add-any-default-commit-level-metadata-in-git-workflows/1371947)).
I treat that as a dated observation. The current
official CLI reference leaves unsettled the configuration details that an
earlier version of this note described, so a team that wants attribution, or
wants to prohibit it, should write repository policy and enforce it. A durable
default inferred from an issue thread is how teams get surprised.

Purpose-built scrubbers exist now, and their existence is evidence in itself:
the [git-attribution](https://github.com/Londopy/git-attribution) tool scans
history for trailers from known agents, rewrites them out, and installs a
pre-push guard.

I built [ai-repo-sanitize](https://github.com/CodeSigils/ai-repo-sanitize) after
this incident, because I did not want to repeat the repair by hand. `check` scans
reachable local and fetched history, `preview` names the matching messages, and
`rewrite` removes only the matching attribution lines. It verifies that the
resulting tree is unchanged, writes a mirror backup, and never pushes unless the
maintainer adds `--push`. The same scanner runs as a read-only CI check.

Policy and owner review still carry the decision. The tool adds a checkable
technical boundary: human co-author trailers stay intact, matching agent
attribution goes line by line, and a rewrite cannot quietly become a remote
change.

## Three GitHub surfaces gave three answers

The cleanup rewrote three commit messages while their file contents stayed
byte-identical. I compared the rewritten tree against a backup ref before
deleting it. Then GitHub answered the same question three ways:

- The REST `/contributors` result listed my account as the only contributor.
- The homepage sidebar still credited the AI agent.
- The Insights contributors graph no longer showed the agent after the
  force-push.

The closest comparison I found is
[declaudify](https://github.com/ParkerrDev/declaudify), built for stale
attribution. Its author observed that the Insights graph, the REST endpoint, and
the homepage sidebar can update on different schedules. A force-push cleared the
Insights graph in those tests but did not immediately change the sidebar. That
matches what I saw. I still treat it as an observation: GitHub documents none of
those caches, so I have no model to cite.

The REST endpoint is the surface most likely to be trusted and the least able to
settle this. It counts contributors by author email, warns that the response can
be cached for hours, and does not audit trailers. A clean API response says
nothing certain about what the sidebar will render.

| Surface | What it reads | What the evidence can show |
| :--- | :--- | :--- |
| Insights graph | the rewritten history | a force-push updated it in this case |
| REST `/contributors` | author-email contributor counts | it can be cached for hours and reads author emails only |
| Homepage sidebar widget | an undocumented contributor view | it can disagree with the API. GitHub documents no cache-refresh control |

The community reports read the same way. The thread that ended best needed a
staff member to refresh the list by hand
([Discussion #205858](https://github.com/orgs/community/discussions/205858),
where the reply reads "I've refreshed the contributors list, so it should be up
to date now."). Several other repository owners list themselves in that thread.
[Discussion #201982](https://github.com/orgs/community/discussions/201982)
reports staleness past a month and collects the nudges people try: empty commit,
edit the repository description, check tags and branches for the old SHA, verify
in a logged-out window.
[Discussions #205779](https://github.com/orgs/community/discussions/205779),
[#204093](https://github.com/orgs/community/discussions/204093), and
[#202538](https://github.com/orgs/community/discussions/202538) show the same
split: REST and Insights clean, sidebar still crediting an AI account. Two more,
[#202540](https://github.com/orgs/community/discussions/202540) and
[#198886](https://github.com/orgs/community/discussions/198886), measure the
delay in weeks.

A month of waiting, a manual staff refresh, and a checklist of nudges are what
people do when the platform has no documented way to say that a credit is wrong.
That is the state of the recovery path I found.

### The sidebar payload I could read without repairing it

While the widget was stale, GitHub served an undocumented sidebar payload at
`/_sidebar` when asked for JSON:

```bash
curl -s -H "Accept: application/json" \
  https://github.com/CodeSigils/CodeSigils.github.io/_sidebar
```

It answered with `contributorCount: 1` while the visible widget still listed the
agent. The request is a `GET`, so it clears and repairs nothing. I use it as one
more diagnostic beside the REST endpoint and the rendered page, and I would not
build on it.

## The recovery I would run now

The original repair was a one-off `filter-branch` pass. Git now warns about that
command's safety and performance limits and points new work at
[filter-repo](https://github.com/newren/filter-repo), so I would not repeat it. I
would use `ai-repo-sanitize`, which wraps `filter-repo`, in this order:

1. Run `check` and `preview` first. They are read-only and establish which
   reachable commits match the attribution pattern.
2. Run `rewrite` against a fresh working clone with its required backup
   location. It changes message lines only, then verifies that the tree before
   and after the rewrite is identical.
3. Inspect the rewritten messages and the affected refs. The remote stays
   unchanged unless the maintainer separately chooses the explicit push option.
4. If the rewrite is approved, publish with the tool's `--force-with-lease`
   path. Then look at the normal GitHub contributor surfaces and allow time for
   their documented caching behaviour.

I do not expect that process to clear the homepage widget. GitHub documents that
its contributors API may be cached for hours, and I found no supported API or
CLI command that flushes the sidebar. Changing the default branch is an
administrative change to the repository, and GitHub documents no cache remedy,
so I would not use it as routine cleanup.

Old commits can also survive their own rewrite: they stay reachable by SHA, and
through `refs/pull/N/head` while pull requests hold them. In the Claude Code
discussion above, old objects stayed alive through open pull requests until
GitHub Support removed them. This repository had no pull requests holding the old
objects, so that part of the job did not come up.

## Why I treat this as a consent problem

I consider non-consensual AI attribution in a commit message unethical, and the
cleanup is where that stopped being an abstraction for me.

A commit trailer makes a public claim about authorship. When tooling writes that
claim into my commits by default, it assigns a co-author to work published in my
name and leaves me to discover it. The decision belongs to the author, before the
commit exists.

I went looking for official guidance on unwanted attribution from agent tooling
and did not find any. GitHub's documentation explains how to add co-authors and
how to remove one before a commit is shared. After the push, the published
remedy for stale contributor data is to wait up to 24 hours and then contact
Support, as a staff member says in
[discussion #205858](https://github.com/orgs/community/discussions/205858).
There is no documented procedure for the person whose repository credits someone
who did not write the code. What exists is a set of community threads where
owners compare notes and occasionally persuade a staff member to refresh a list
by hand.

The work lands on the author: notice the trailer, work out why the widget and the
API disagree, rewrite history, then wait for a cache to agree. That is a lot of
work to undo a claim that tooling made on the author's behalf.

## The three layers I use now

Repository settings and written instructions state the policy. Enforcement takes
three layers:

1. Write the policy in the instructions agents and maintainers actually read. In
   this repository that means no agent attribution trailers, no branding lines,
   and no bypassing the normal commit checks.
2. Reject a matching message locally with a `commit-msg` hook. The person
   committing gets a clear failure before the history changes.
3. Run `ai-repo-sanitize check` in CI against the reachable history. CI cannot
   prevent a push, but it gives the repository an independent result and makes a
   bypass visible for review.

The hook and the CI check have to share one documented policy boundary. If they
do not, a message can pass one layer and fail the other because each tool
describes AI attribution differently. `ai-repo-sanitize` keeps its scanner and
rewriter on one pattern definition, preserves human co-author trailers, and
removes only the agent trailers or branding lines that match the policy.

This repository blocks `dependabot[bot]` deliberately, and that is a maintainer
choice for this repository. Dependabot is GitHub's dependency-update automation:
it opens security and version-update pull requests on its own schedule, and the
change inside each one is a dependency bump. A maintainer can reasonably allow
it and still reject AI attribution. What matters is that the decision is written
down and that the hook and the CI rule match it. A policy kept in someone's head
is a policy the next agent will guess wrong.

## What signing does not prove

Commit signing is a useful companion check that answers a different question. A
signature lets GitHub verify that the person holding a configured GPG, SSH, or
S/MIME key created the commit. What it proves is control of a key at the time of
the commit, and a signed commit can still carry a false trailer.

The value in `user.signingkey` follows the selected signing format. After adding
the public SSH key to GitHub as a signing key, the complete SSH default setup is:

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

For GPG, `openpgp` is the default format and `user.signingkey` is usually the
long key ID. S/MIME uses the `x509` format and its configured signing program.
Drop `--global` when a repository needs a different key, and
`git commit -S -m "message"` signs a single commit. GitHub shows a **Verified**
badge when it can validate the signature, while `git log --show-signature -1` is
the quick local check. Because the key setup differs between the three formats, I
follow GitHub's
[signing commits guide](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits).

## What I would do first

Start with the commit messages, then look at the widget. If the trailers are
still in reachable history, no amount of work on GitHub's surfaces will change
what a reader sees.

If the history is clean and the surfaces still disagree, treat them as three
diagnostics on different schedules. The REST endpoint is a count that may be
cached, the Insights graph reads rewritten history, and the sidebar is
undocumented. None of the three verifies what a commit message claims, and a
contributor widget reports who GitHub counts.

If you need a repair, use something that previews its scope, verifies that only
message lines changed, keeps a backup, and requires an explicit push decision.
Doing it by hand is how people end up with a rewritten tree they did not intend.

What I still cannot check is the part I would most like help with: an agent that
writes attribution my pattern set does not know, or a GitHub surface that keeps
disagreeing with the other two after a clean rewrite. If you have either, the
[ai-repo-sanitize](https://github.com/CodeSigils/ai-repo-sanitize) issue tracker
is the first place I would look.

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
