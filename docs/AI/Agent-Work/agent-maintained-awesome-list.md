---
title: What Keeps an Awesome List Honest
description: How a curated list turned into a governed one. It has hard gates, soft advisories, two state files, and freshness reporting against a real git history.
keywords: [agents, awesome list, maintenance, drift, CI, freshness, license, url rot]
---

An awesome list makes a quiet promise. A reader follows a link, takes a
project seriously, and may build a decision around it months after the entry
was added. If the repository has vanished, gone quiet, or lost the licence
that made it usable, the list has misled that reader. No one necessarily sends
a correction. The entry simply becomes less true over time.

I keep an awesome list about agent trust and identity
([awesome-agent-trust](https://github.com/CodeSigils/awesome-agent-trust)).
Writing it was the easy part. Keeping it honest took a few months of small
failures, a validation pipeline, and a maintenance routine that keeps finding
things I would otherwise miss. This is a field note about that machinery and
the real commit history that gave each part a reason to exist.

## A list becomes a governed list

For the first weeks it was a README with categories, much like any other
awesome list. Then the failures arrived: dead links, archived repositories,
and entries whose sources no longer resolved. The useful change was not a
cleverer description of the list. It was giving the same questions a place to
be checked every time.

The repository grew a criteria file that says what belongs and what cannot be
merged ([CRITERIA.md](https://github.com/CodeSigils/awesome-agent-trust/blob/main/CRITERIA.md)),
a validator that checks every entry, and regression tests for the validator.
The list is still a document for readers. For maintainers, it is also a small
system with stated promises and evidence about whether those promises hold.

## The git log is full of small deaths

The history explains why the rules exist. It is full of modest failures:

- a project we added disappeared entirely, and its source had to be
  removed as unavailable ([#28](https://github.com/CodeSigils/awesome-agent-trust/commit/0cac0dd9db9c5c2066e384669a3dce2fe63a53df))
- an upstream organisation deleted its repositories, taking several
  entries with them ([#23](https://github.com/CodeSigils/awesome-agent-trust/commit/9baf5a5))
- a linked project stopped being maintained and had to be dropped
  ([#29](https://github.com/CodeSigils/awesome-agent-trust/commit/b97e271ca5a9f7712df8f5a00ec30ba59aa169a7))
- a contributor's name was misspelled in the credits and needed its
  own fixup commit ([#24](https://github.com/CodeSigils/awesome-agent-trust/commit/1c90bf2))
- our own test suite accumulated lint findings that had to be cleaned
  ([#20](https://github.com/CodeSigils/awesome-agent-trust/commit/919631a)).

None of these failures was dramatic. Each was easy to dismiss as a one-off
maintenance task. Together they described the real risk: links rot, sources
vanish, metadata drifts, and the maintainer cannot be the only person or
process expected to notice.

## Hard failures and soft advisories

The first design decision was to separate problems that disprove an entry's
minimum claim from problems that need a human judgment.

A hard failure means the repository is missing, archived, or cannot be
validated reliably. When the validator finds one, CI fails and the pull request
cannot merge
([validate.yml](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/workflows/validate.yml)).

A soft advisory is a reason to look closer, not a verdict. A low star count,
no detected licence, long inactivity, or a weak description can all be useful
signals without proving that a project does not belong. These findings do not
block a pull request. They are recorded in a dated baseline and surfaced for a
maintainer to triage ([advisory-baseline.json](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/advisory-baseline.json)).

This split matters because a gate should enforce a promise the list can explain.
If stars blocked inclusion, small but useful projects would disappear from
consideration. If every missing machine-detected licence blocked a change,
the repository would confuse a review task with a proof that a project has no
licence at all. The gate protects the minimum claim that an entry exists and is
what it says it is. The rest is evidence for a person to weigh.

!!! tip "Let the gate enforce the promise, not the taste"
    If a check blocks a merge, someone must be able to explain which
    promise of the list it protects. If the explanation is "quality",
    the check probably belongs in the advisory pile instead.

## The license criterion keeps the list open

One advisory still changed the contribution policy: licensing. An awesome list
about trust should not treat any public landing page as if it were inspectable
software. New software submissions normally need an open-source licence and a
public repository on a recognised code host. Standards and specifications have
a narrower documented path because public review and implementation matter
more than a conventional source layout ([#32](https://github.com/CodeSigils/awesome-agent-trust/commit/342e890aebce93e8d1f8af9c2afea8d13b58df33)).

The change also closed a loophole the criteria had been carrying: an
old clause allowed "a public repository or documentation site", which
meant a landing page with no code could in principle qualify. That is
gone. Landing pages never qualify on their own.

The validator still reports a missing detected licence as an advisory. That
keeps existing entries visible for review without pretending that an automated
lookup settles every licensing question. It also marks non-GitHub code hosts
and other external destinations explicitly. GitHub-specific checks cannot run
there, so a maintainer must confirm the destination, licence, and activity by
hand ([#31](https://github.com/CodeSigils/awesome-agent-trust/commit/7e8327f1b7f300526dfcd32aadf02be879f3459d)).

## URL rot, and the silent-skip lesson

The most instructive bug involved URL rot of a second kind. The validator
extracts GitHub repository URLs from the README and checks them against the
GitHub API. That part worked well. The blind spot was everything that was not a
GitHub link.

Entries pointing at websites or other code hosts skipped every
validation gate without anyone noticing. No warning, no advisory, no
trace. The validator only knew how to doubt GitHub, so everywhere
else entered the list on faith. The fix ([#31](https://github.com/CodeSigils/awesome-agent-trust/commit/7e8327f1b7f300526dfcd32aadf02be879f3459d))
added a whitelist of recognised hosts and turned everything else into
an explicit `UNVALIDATED_HOST` or `UNVALIDATED_LINK` advisory, so a
silent pass became a visible question.

The general lesson is simple. A checker that quietly skips what it does not
understand creates confidence it has not earned. The skip must become a visible
question.

For non-GitHub links (documentation sites, specification
pages, project homes), a separate reporter checks every external link
and labels it ok, redirect, broken, or unknown, degrading from HEAD to
GET requests before giving up ([report-external-links.py](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/scripts/report-external-links.py)).
Because the network is fallible, a link the reporter cannot reach is labelled
unknown rather than broken. An API or network error is not evidence of
deletion. The gate applies the same caution: when a GitHub API call fails, the
validation run fails instead of treating a transient timeout as evidence about
an entry. Someone can then decide what the incomplete evidence means.

## Submitting a pull request to a governed list

For a contributor, the pull request is where the policy becomes practical.
Branch protection requires the three validation jobs for every merge, including
administrator changes. The repository has one maintainer and no approving-review
requirement, so those checks carry much of the repeatable part of the review.
The validation workflow also runs on pushes to `main`, every Monday, and on
manual dispatch.

Before a proposal reaches that pipeline, the criteria file provides a useful
checklist. The repository must exist and not be archived. A software entry
normally needs an open-source licence on a recognised code host. Its description
must say more than the title, and it must sit in the right category and
alphabetical position. The pipeline refuses what it cannot verify. Softer
signals remain visible for a reviewer instead of being mistaken for automatic
rejections.

Stars are advisory and never decide eligibility. A contributor can add context
such as independent verification, documented adoption, foundation governance,
or a recognised standards process when it would help a reviewer understand a
small project ([contributing.md](https://github.com/CodeSigils/awesome-agent-trust/blob/main/contributing.md)).
That context is optional, and a low-star entry does not need an exception
request. Exceptions are different: they are maintainer-owned records for a
specific reviewed waiver, with the affected checks, a reason, and a future
review date.

The human work sits on top of the same machine. The contribution guide and pull
request template explain what a submission should contain ([pull request
template](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/pull_request_template.md)).
The local routine runs `npm ci`, `npm run lint`, `npm test`, and the two Python
validators before the proposal is opened. That does not replace review. It
means the review can begin with the project and its evidence rather than a
formatting surprise.

## Two state files that never mix

The advisory machinery uses two files. Their separation matters because they
answer different questions.

[`advisory-baseline.json`](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/advisory-baseline.json)
is a dated snapshot of known soft flags. At the 2026-10-17 review it recorded
two inactive projects, 39 low-star entries, 19 entries with no detected
licence, and four external links requiring review. It is monitoring state. It
records what the list knows. It does not approve anything.

[`repo-exceptions.json`](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/repo-exceptions.json)
is the only place a soft advisory can be waived. Each entry names the exact
checks being waived, the reason, and a future review date. Exceptions expire.
An expired exception is a configuration error, not a reminder that can be
ignored. The pipeline refuses to treat a stale waiver as a current decision,
so a maintainer has to decide again.

Mixing the two would be drift dressed up as automation. One file says
"we know", the other says "we decided". The list is honest only while
those two sentences stay in separate drawers.

## Freshness as reporting, not gating

The other half of the machinery is a weekly freshness ritual
([dependency-freshness.yml](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/workflows/dependency-freshness.yml)).
Every Monday it appends four reports to the workflow summary:

- whether pinned GitHub Actions still match their latest tags
  ([report-action-freshness.py](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/scripts/report-action-freshness.py))
- how the advisory baseline has changed, including new, known, resolved, and
  accepted signals ([validate-repos.py](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/scripts/validate-repos.py))
- the health of every non-GitHub link in the README
- a triage report of exceptions and their review dates, flagging any
  that are overdue ([report-advisory-triage.py](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/scripts/report-advisory-triage.py)).

The freshness workflow does not gate pull requests, and ordinary advisory
findings remain non-blocking. It does fail when validation finds a hard problem
or cannot complete, because a partial report should not look trustworthy. The
summary gives a maintainer a weekly view of upstream rot without turning a
remote outage into an automatic removal. It also does not replace Dependabot:
dependency maintenance and repository maintenance are different jobs.

The weekly report supports a slower maintenance cadence. New and overdue
advisories are triaged monthly, and the low-star baseline receives a quarterly
audit. Each entry is classified as resolved, still below the threshold, or
unavailable before it is cleared. A temporary star increase alone is not a
resolution.

## A small CI on purpose

The gate stays deliberately small. One job lints the list and checks
repository-relative Markdown links offline. One runs the validator against the
live API and fails on hard errors. One scans the full Git history for leaked
secrets with a SHA-pinned gitleaks action and an allow-list. Each job answers a
different question, which makes a failed run easier to interpret.

The restraint is as deliberate as the checks. I do not add a Python formatter
or type checker to CI. The scripts are stdlib-only, typed, and covered by
regression tests, so the upkeep would outweigh the benefit for now. A check
added simply because it is easy to add teaches a pipeline to cry wolf. The lint
pass also runs periodically as a maintainer ritual rather than another gate
([#20](https://github.com/CodeSigils/awesome-agent-trust/commit/919631a)).

The workflow permissions are lean: read-only contents access and a token scoped
to the validator's API calls. The secret scan is the exception that needs full
history. A token committed three revisions ago is still exposed.

## The paperwork is part of the machine

Underneath the automation sits the part many awesome lists never write: a
maintenance guide and a roadmap that are read like contracts
([MAINTENANCE.md](https://github.com/CodeSigils/awesome-agent-trust/blob/main/docs/MAINTENANCE.md),
[ROADMAP.md](https://github.com/CodeSigils/awesome-agent-trust/blob/main/docs/ROADMAP.md)).
The guide is revisited before and after every relevant action, including a
merge, an exception, or a criteria change. If it and the roadmap disagree, that
is drift to resolve before treating the action as complete.

The repository also gives agents an explicit starting point before they change
anything ([#35](https://github.com/CodeSigils/awesome-agent-trust/commit/bb404bb982415f45dcd2c46d301334798f8e5e0f)).
An automated contributor begins with the same maintenance contract as the
maintainer. Auto-merge can handle eligible internal work, while an external
pull request still receives a human decision
([#38](https://github.com/CodeSigils/awesome-agent-trust/commit/d1a6186f875ea09cb47b150bdce739f7ecba99ee)).

## What I look for now

When I assess a project that calls itself maintained, I start with three
questions. Does a check fail visibly when it cannot answer? Do its state files
separate observation from a recorded decision? Does its maintenance routine
report change before it turns it into a gate?

Those questions do not make an awesome list timeless. They make decay visible
while there is still someone who can interpret it and act.

The same concern appears in the longer notes on [when agent instructions start
to drift](agent-instruction-drift.md) and [where an agent's memory actually
lives](agent-memory-surfaces.md). In each case, the difficult part is not
adding another document or check. It is making the right responsibility visible.

## Related reading

- [awesome-agent-trust](https://github.com/CodeSigils/awesome-agent-trust) - every check and file mentioned above is real and visible there.
- [CRITERIA.md](https://github.com/CodeSigils/awesome-agent-trust/blob/main/CRITERIA.md) - the gate contract covering hard failures, soft advisories, and the licence rule.
- [MAINTENANCE.md](https://github.com/CodeSigils/awesome-agent-trust/blob/main/docs/MAINTENANCE.md) - three automation layers, review cadence, and handover procedure.
- [validate-repos.py](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/scripts/validate-repos.py) - eight-worker API checking, hard/soft signals, and the quarterly baseline audit.
- [dependency-freshness.yml](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/workflows/dependency-freshness.yml) - the weekly freshness ritual.
- [commit #31](https://github.com/CodeSigils/awesome-agent-trust/commit/7e8327f1b7f300526dfcd32aadf02be879f3459d) - the silent-skip fix was the most instructive bug in the project.
