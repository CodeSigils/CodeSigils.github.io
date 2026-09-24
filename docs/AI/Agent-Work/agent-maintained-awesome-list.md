---
title: What Keeps an Awesome List Honest
description: How a curated list turned into a governed one — hard gates, soft advisories, two state files, and freshness reporting against a real git history.
keywords: [agents, awesome list, maintenance, drift, CI, freshness, license, url rot]
---

An awesome list is a promise. Someone reads it, trusts one of its
links, and builds a decision on top of a project you pointed at last
winter. When that repository has since vanished, gone dark, or quietly
dropped its license, the promise is broken — and nobody sends you a
letter about it. The list just slowly stops being true.

I keep an awesome list about agent trust and identity
([awesome-agent-trust](https://github.com/CodeSigils/awesome-agent-trust)).
Writing it was the easy part. Keeping it honest took a few months of
small failures, a validation pipeline, and a maintenance ritual that
still surprises me with what it catches. This is the story of the
machinery, and of the real commit history that made each piece
necessary.

## A list becomes a governed list

For the first weeks it was just a README with categories, exactly like
every other awesome list. Then the failures started — dead links,
archived repositories, entries whose sources no longer resolved.
What actually fixed it was to stop being the only checker and let the
machine watch the same links.

The repository grew a criteria file that says what belongs and what
cannot be merged ([CRITERIA.md](https://github.com/CodeSigils/awesome-agent-trust/blob/main/CRITERIA.md)),
a validator that checks every entry, and regression tests that keep
the validator honest. The list stopped being a document and became a
small governed system. That distinction is the whole article.

## The git log is full of small deaths

Every rule in that system has a gravestone behind it. The history of
the list reads like an obituary column:

- a project we added disappeared entirely, and its source had to be
  removed as unavailable ([#28](https://github.com/CodeSigils/awesome-agent-trust/commit/0cac0dd9db9c5c2066e384669a3dce2fe63a53df));
- an upstream organisation deleted its repositories, taking several
  entries with them ([#23](https://github.com/CodeSigils/awesome-agent-trust/commit/9baf5a5));
- a linked project stopped being maintained and had to be dropped
  ([#29](https://github.com/CodeSigils/awesome-agent-trust/commit/b97e271ca5a9f7712df8f5a00ec30ba59aa169a7));
- a contributor's name was misspelled in the credits and needed its
  own fixup commit ([#24](https://github.com/CodeSigils/awesome-agent-trust/commit/1c90bf2));
- our own test suite accumulated lint findings that had to be cleaned
  ([#20](https://github.com/CodeSigils/awesome-agent-trust/commit/919631a)).

None of these is dramatic. That is the point. An awesome list does not
fail in one spectacular moment; it fails in a hundred quiet ones, and
each quiet failure looks like a judgement call until you notice the
pattern. The pattern here was: links rot, sources vanish, metadata
drifts, and the maintainer is the only witness.

## Hard failures and soft advisories

The first design decision was to split every possible problem into two
classes: hard failures and soft advisories.

A hard failure means the entry cannot safely be in the list at all —
the repository is missing, it is archived, or it cannot be verified.
When the validator finds one, CI fails and the PR does not merge
([validate.yml](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/workflows/validate.yml)).

A soft advisory is a warning sign, not a verdict: low star count, no
detected license, long inactivity, a weak description. These never
block a pull request. They are recorded in a dated baseline file and
surfaced for a human to triage ([advisory-baseline.json](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/advisory-baseline.json)).

This split matters more than it sounds. If stars blocked inclusion,
small and honest projects would never get in. If license absence
blocked inclusion, the list would shut out many genuinely useful
tools before their authors ever added a license. The gate should only
enforce what the list actually promises — that the thing exists and is
what it claims to be. Everything else is a question, not a verdict.

!!! tip "Let the gate enforce the promise, not the taste"
    If a check blocks a merge, someone must be able to explain which
    promise of the list it protects. If the explanation is "quality",
    the check probably belongs in the advisory pile instead.

## The license criterion keeps the list open

One soft signal turned out to deserve a much firmer role: the license.
An awesome list is only as open as the projects it vouches for, and
"open" has a testable meaning. Over time the criteria hardened into a
plain rule: software entries normally require an open-source license,
and they must live on a recognised code host — GitHub, GitLab,
Codeberg, sr.ht, Bitbucket, or similar ([#32](https://github.com/CodeSigils/awesome-agent-trust/commit/342e890aebce93e8d1f8af9c2afea8d13b58df33)).

The change also closed a loophole the criteria had been carrying: an
old clause allowed "a public repository or documentation site", which
meant a landing page with no code could in principle qualify. That is
gone. Landing pages never qualify on their own.

The validator flags missing licenses as advisories rather than hard
failures, so the list stays inclusive of projects that are still
sorting their licensing out. But the baseline makes the absence
visible, and the recognised-host rule means a non-GitHub entry is
never silently assumed to be fine — the checks that GitHub lets us
automate cannot run there, so a human must confirm existence, license,
and activity by hand ([#31](https://github.com/CodeSigils/awesome-agent-trust/commit/7e8327f1b7f300526dfcd32aadf02be879f3459d)).

## URL rot, and the silent-skip lesson

The most instructive bug in the whole project was about URL rot of a
second kind. The validator extracts every repository URL from the
README and checks it against the GitHub API. That worked beautifully
— and it silently ignored everything that was not a GitHub link.

Entries pointing at websites or other code hosts skipped every
validation gate without anyone noticing. No warning, no advisory, no
trace. The validator only knew how to doubt GitHub, so everywhere
else entered the list on faith. The fix ([#31](https://github.com/CodeSigils/awesome-agent-trust/commit/7e8327f1b7f300526dfcd32aadf02be879f3459d))
added a whitelist of recognised hosts and turned everything else into
an explicit `UNVALIDATED_HOST` or `UNVALIDATED_LINK` advisory, so a
silent pass became a visible question.

There is a general lesson here for anyone building checks for agent
workflows: a checker that quietly skips what it does not understand is
worse than no checker, because it manufactures confidence. The fix is
to make the skip itself visible.

For non-GitHub links generally — documentation sites, specification
pages, project homes — a separate reporter checks every external link
and labels it ok, redirect, broken, or unknown, degrading from HEAD to
GET requests before giving up ([report-external-links.py](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/scripts/report-external-links.py)).
Because the network itself lies, a link the reporter cannot reach is
labelled unknown, never broken — an API or network error is not
evidence of deletion. The same principle sits in the gate: when the
validator's API call fails, that is a hard error, and the merge is
blocked rather than the entry being dropped on the word of a
transient timeout. It is far better to ask a human than to delete an
entry.

## Submitting a pull request to a governed list

So what does a valid pull request actually look like? The gate
itself is the first contract, and branch protection enforces it on
every merge — including on my own admin commits, because the
repository does not use approving reviews and I am the only
maintainer. The validation workflow runs against every pull request
to main, on every push to main, weekly, and whenever I trigger it by
hand. The checks are not a suggestion; the branch settings make them
a condition of merging.

Before a proposal ever reaches that pipeline, the entry must satisfy
the criteria file — and it doubles as a checklist an agent can run
through before opening anything. The repository exists and is not
archived. A software entry carries an open-source license and lives
on a recognised code host. The description says more than the title;
the entry follows the list's format and sits in the right
alphabetical place inside its category. The pipeline refuses what it
cannot verify; the softer items on that checklist are tracked, not
ignored — they are the difference between a proposal that is clearly
valid and one that starts its life trailing advisories.

Stars are advisory and never gate anything. But a proposal for a
low-star project still brings its evidence: the contribution guide
asks for independent verification, documented adoption, or foundation
governance, alongside a request for a `repo-exceptions.json` entry
naming the project, the exact checks waived, a reason, and a future
review date ([contributing.md](https://github.com/CodeSigils/awesome-agent-trust/blob/main/contributing.md)).
The waiver is not granted silently; it is requested inside the pull
request and recorded by the maintainer, so the decision is documented
at the same moment as the addition.

The human rituals sit on top of the same machine. The contribution
guide and the pull request template set the shape every submission is
expected to follow ([pull request
template](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/pull_request_template.md)),
and the pre-submission ritual — `npm ci`, `npm run lint`, `npm test`,
then the two local validator scripts — is the same work the pipeline
does, run by hand first. An agent that wants to contribute starts
there: prove the entry against the criteria locally, submit the
evidence with the proposal, and let branch protection do the arguing.

## Two state files that never mix

The advisory machinery lives in two files, and keeping them separate
is the whole point.

[`advisory-baseline.json`](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/advisory-baseline.json)
is a dated snapshot of known soft flags: as of late September it
carried two inactive projects, forty low-star entries, and nineteen
with no detected license. It is monitoring state. It records what the
list already knows, it does not approve anything.

[`repo-exceptions.json`](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/repo-exceptions.json)
is the only place a soft advisory can be waived — and even then under
conditions: the entry names the exact checks being waived, a reason,
and a future review date. Exceptions expire. An expired exception is a
configuration error, not a nag; the pipeline refuses to treat a stale
waiver as a current decision, and a human must re-decide.

Mixing the two would be drift dressed up as automation. One file says
"we know", the other says "we decided". The list is honest only while
those two sentences stay in separate drawers.

## Freshness as reporting, not gating

The other half of the machinery is a weekly freshness ritual
([dependency-freshness.yml](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/workflows/dependency-freshness.yml)).
Every Monday it produces four reports appended to the workflow
summary:

- whether pinned GitHub Actions still match their latest tags
  ([report-action-freshness.py](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/scripts/report-action-freshness.py));
- how the advisory baseline has drifted — what is new, known,
  resolved, or accepted ([validate-repos.py](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/scripts/validate-repos.py));
- the health of every non-GitHub link in the README;
- a triage report of exceptions and their review dates, flagging any
  that are overdue ([report-advisory-triage.py](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/scripts/report-advisory-triage.py)).

The word that matters here is *report*. The freshness workflow never
blocks anything. It always exits successfully and writes its findings
where a human reads them. Gating freshness would punish the list for
the upstream world's carelessness; reporting it lets the maintainer
decide what is urgent. It also deliberately does not replace
Dependabot — tooling freshness and repository freshness are different
problems, and the report keeps them apart.

On top of the weekly pulse sits a cadence: monthly triage of new and
overdue advisories, and a quarterly audit of the low-star baseline
that classifies every entry as resolved, still below, or unavailable
before anything is cleared. A star count is not evidence of a
resolution by itself — a temporary bump above the threshold changes
nothing until the entry has genuinely earned its way out.

## A small CI on purpose

The gate itself is deliberately small: three jobs, each with a single
clear job. One lints the list and checks every repository-relative
link in the markdown offline. One runs the validator against the live
API with eight concurrent workers and fails on hard errors only. One
scans the full git history for leaked secrets with a SHA-pinned
gitleaks action behind an allow-list.

The restraint is as deliberate as the checks. There is no Python
formatter or type checker in CI, even though the scripts are Python —
not because they are optional, but because their cost and maintenance
were weighed consciously and deferred. A check that exists because it
was cheap to add is how pipelines learn to cry wolf. The scripts are
stdlib-only, typed, and covered by regression tests, and the lint
pass runs periodically as a maintainer ritual instead of a gate
([#20](https://github.com/CodeSigils/awesome-agent-trust/commit/919631a)).

Even the workflow's permissions are lean: read-only contents access,
a token scoped to exactly the API calls the validator makes. The
secret scan is the one place that insists on full history, because a
leaked token hidden three commits ago is still a leaked token.

## The paperwork is part of the machine

Underneath all of it sits the part most awesome lists never write: a
maintenance guide and a roadmap that are read like contracts
([MAINTENANCE.md](https://github.com/CodeSigils/awesome-agent-trust/blob/main/docs/MAINTENANCE.md),
[ROADMAP.md](https://github.com/CodeSigils/awesome-agent-trust/blob/main/docs/ROADMAP.md)).
The guide must be revisited before *and* after every relevant action —
a merge, an exception, a criteria change. If the guide and the roadmap
disagree, that contradiction is drift to resolve before anything else
happens, not a detail to fix later.

The repo even carries an explicit directive telling agents which
document is authoritative before they touch anything ([#35](https://github.com/CodeSigils/awesome-agent-trust/commit/bb404bb982415f45dcd2c46d301334798f8e5e0f)).
Agents read the maintenance guide first, so a future automated
contributor starts from the same contract as the human one. Auto-merge
is on for our own PRs, but external pull requests are never merged
automatically ([#38](https://github.com/CodeSigils/awesome-agent-trust/commit/d1a6186f875ea09cb47b150bdce739f7ecba99ee)) —
the machine handles the checks, and the human keeps the judgement call.

## What I look for now

When I look at any project that wants to call itself maintained, I
check for three things: whether its checks fail closed or pass
silently; whether its state files separate what we know from what we
decided; and whether its freshness ritual reports before it gates.
An awesome list kept this way is not guaranteed to stay true. But when
something rots, the list will notice out loud, and a human will be
standing there to decide what it means.

If this resonated, the longer family of notes lives in the two
articles about guidance and memory: [when agent instructions start to
drift](agent-instruction-drift.md) and [where an agent's memory
actually lives](agent-memory-surfaces.md). The machinery of this list
is the same problem wearing a different coat.

## Related reading

- [awesome-agent-trust](https://github.com/CodeSigils/awesome-agent-trust) — the repository itself; every check and file mentioned above is real and visible there.
- [CRITERIA.md](https://github.com/CodeSigils/awesome-agent-trust/blob/main/CRITERIA.md) — the gate contract: hard failures, soft advisories, and the licence rule.
- [MAINTENANCE.md](https://github.com/CodeSigils/awesome-agent-trust/blob/main/docs/MAINTENANCE.md) — the ritual: three automation layers, review cadence, and handover procedure.
- [validate-repos.py](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/scripts/validate-repos.py) — the validator: eight-worker API checking, hard/soft signals, and the quarterly baseline audit.
- [dependency-freshness.yml](https://github.com/CodeSigils/awesome-agent-trust/blob/main/.github/workflows/dependency-freshness.yml) — the weekly freshness ritual in one file.
- [commit #31](https://github.com/CodeSigils/awesome-agent-trust/commit/7e8327f1b7f300526dfcd32aadf02be879f3459d) — the silent-skip fix, the most instructive bug in the project.