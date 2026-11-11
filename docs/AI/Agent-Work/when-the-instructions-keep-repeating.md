---
title: When the Instructions Keep Repeating
description: A field note on treating repeated agent instructions as a requirements backlog, what a six-defect fleet CI investigation taught about rot versus behavior, and how incident reports grew their own machine checks.
keywords:
  - AI agents
  - agent instructions
  - documentation drift
  - evidence
  - CI gates
  - incident reports
  - skill-repo-standards
---

I kept asking agents to check the working tree before committing, to compare a
README with the code and CI, and to report before making a change. The wording
varied. The request did not. I eventually treated that repetition as evidence
of a missing requirement.

This field note follows what happened when I gave those repeated instructions a
home in the repository: a directive when an agent needed to see the rule, a
machine check when a failure was deterministic, and a clearer route to an
existing rule when I had merely lost it in the documentation.

## The instructions I kept repeating

Some were small practical reminders:

- "Is the information in `README.md` still accurate? Review it carefully and
  report any staleness or drift."
- "Check git status for pending changes before committing."
- "Review the code first for bugs, duplication, drift, and conventions. Why
  did you commit before doing that?"
- "Check the working tree, index, upstream relation, remotes, and latest
  commit. I want the full status, not just 'clean' or 'dirty'."

Others governed evidence and scope: read the existing research before making a
recommendation, keep `ROADMAP.md` and `AGENTS.md` aware of a material change,
and honour “report only.” I had said each of these often enough that the
repetition stopped looking like an attention problem.

## A repeated instruction is a signal

One repeated instruction may be a lapse in attention. A pattern across
sessions, repositories, and kinds of work means the rule needs a home outside
the conversation.

"Check git status before committing" should not depend on whether I remember
to say it. "Use evidence rather than speculation" should not depend on the
agent happening to recall a previous chat. "Make sure the README reflects
current reality" should not require me to notice, yet again, that the
documentation has quietly drifted away from the code. These are workflow
requirements. They belong in a specification, a checklist, a template, a
validation step, or some other inspectable part of the repository.

There is a working model behind this, and I wish I had adopted it earlier.
Context behaves like working memory. Durable rules need storage outside the
conversation. The agent failures I saw in long sessions were usually failures
of accumulation: stale exploration, dead ends, and verbose outputs crowding
out the thing we had agreed on twenty minutes earlier. An instruction typed
into that crowded space decays. The same instruction filed in `AGENTS.md`, a
hook, or a machine check persists. My instinct to externalize was directionally
correct long before I had the vocabulary for it.

I want to avoid creating a file swamp full of prose for its own sake. The goal
is narrower. Good behavior should be easier to repeat than the failure it is
meant to prevent.

Over time each recurring instruction sorted itself into one of three
destinations. It can become a machine check that fails loudly when the rule
is broken. It can become a durable directive written into the repository's
own agent instructions, so any agent that reads them starts from the right
place. Occasionally, the rule is already covered somewhere I forgot. That
repetition calls for a better route to the existing rule.

## The fleet is messy on purpose

The CodeSigils repositories are deliberately uneven. Some are skills, some
are research records, and some are small spikes that test an idea before it
becomes a maintained project. The difference is useful evidence. It shows
which practices survive more than one context.

It also makes drift visible. One repository may carry a dated evidence
registry while another has only a research note. The work is to identify the
repeatable parts, adopt them deliberately, and retire the rest with an
explicit decision. I need to know which information supports a decision now.

## Research you can still trust

I keep a broader set of notes in the agent-concepts-study private repo. Its
research directory holds a lot of material I consider valuable and
challenging to keep. The wider observations need
more caution. A substantial share is outdated, incomplete, or simply wrong
now, which is why that repository stays private for now. They were useful
when written. They should not automatically be treated as current guidance.

The conclusion I drew from that is probably the most important line in this
piece: the failure mode is no longer missing evidence. It is unindexed
evidence that cannot be trusted without re-verification. I am not
overwhelmed by a lack of research. I am overwhelmed by my own corpus of it.
The fix is triage. Dated rows with statuses and recheck conditions mark each
item current, outdated, or wrong without re-verifying everything in place.

Two smaller admissions belong here too. I implemented before I researched
established methodologies. The spec I built became a consumer of existing
standards and recorded which source informed each decision. The vocabulary
already existed. Conformance profiles and assessment schemes gave me better
names for work I had been describing with near-synonyms. Similarly, I found
[agentskills.io](https://agentskills.io/home) months after I needed it, deep
into bad prompt-engineering habits that its guidance would have prevented.

This is why I started the
[`skill-repo-standards`](https://github.com/CodeSigils/skill-repo-standards)
spec. It began as a consumer of industry standards: a place to investigate
emerging patterns around compliance, discovery, and good practice for agent
skills. The README describes it modestly and it is still under development
and evaluation, so I do not want to oversell it. The intention is practical:
reduce the decision uncertainty that comes up every time I start a new piece
of work. What should a skill repository document? What evidence should
support a recommendation? When should research be captured, reviewed,
refreshed, or retired? How can an agent distinguish a completed task from an
open gap or an unverified assumption?

Inside that repository now lives a small research register. Each entry has a
question, a finding, explicit limitations, a recheck condition, and a list of
source URLs. A companion registry file records each source with the date it
was last verified and, for important pages, a phrase that must appear in the
fetched body before the entry counts as current. There are decisions with
IDs, and research entries point at the decisions they inform. The whole
shape exists so that the question "why do we believe this?" has an address.

## The week the fleet showed what was actually wrong

The following case study is from October 2026. The dated [fleet CI rot incident
report](https://github.com/CodeSigils/skill-repo-standards/blob/main/docs/research/incident-reports/2026-10-17-fleet-ci-rot-and-agent-drift.md)
holds its detailed evidence and remediation. The point here is the repeated
instruction it exposed.

A fleet-wide cleanup, meant to reduce advisory noise in the READMEs of eleven
repositories, was issued before any repository was inspected for its current
state. Correcting the resulting wreckage surfaced six distinct defects. Five
were silent configuration rot that pre-existed the cleanup. The sixth was a
behavioral failure by the operating agent, which was me in effect, through the
agent I was driving.

For a skim, three of the six were the kind that stop work: a red
documentation gate on `skill-discovery`'s default branch that scheduled runs
reported as green, a deleted upstream project whose 404 kept an unrelated
pull request blocked in `awesome-agent-trust`, and a required check in
`zero-md-formatter` naming a job no workflow produced anymore, which meant
no pull request there could ever pass. The other two rot defects were
quieter: expired evidence that automation could not see, and a duplicated
history whose matching trees hid the provenance question. The sixth defect was
mine, and it is further down.

The rot, concretely:

- In `skill-discovery`, two research-evidence documents had passed their
  expiry dates, so the documentation gate was failing on the default branch.
  The scheduled run stayed green anyway, because the gating jobs are filtered
  out of schedule events. Worse, intervening merges had been performed by
  automation using the repository's own `GITHUB_TOKEN`, and events triggered
  by that token do not create new workflow runs at all. The branch advanced
  for days without any CI running. GitHub documents both behaviors in its
  [automatic token authentication](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication)
  and [events that trigger workflows](https://docs.github.com/en/actions/reference/events-that-trigger-workflows)
  pages, which is exactly where the investigation ended up.
- In `awesome-agent-trust`, a third-party project listed in the README had
  been deleted upstream, so its URL returned 404. The validator classifies
  that as a hard error with no waiver, so a required check was failing on
  the default branch, which blocked an entirely unrelated documentation PR.
  The rot in one file held up work in another. The fix was the
  [dead-entry removal](https://github.com/CodeSigils/awesome-agent-trust/pull/54)
  and merging the [stranded docs PR](https://github.com/CodeSigils/awesome-agent-trust/pull/55).
- `zero-md-formatter` carried three of them. Its evidence had passed a
  30-day freshness window while the checking cadence was weekly, a defect I
  will come back to under corrections. Its required status checks named a
  job, `test (25.x)`, that no longer existed in the workflow matrix, which
  means no pull request in that repository could ever satisfy its required
  checks regardless of CI results. And its default branch turned out to
  carry a duplicate history with no common ancestor: ahead 95 and behind 95
  against its own remote, with identical commit subjects but different
  SHAs. Comparing tree object hashes showed identical snapshots, which
  proves the trees match and proves nothing about provenance. The refresh
  landed in [one careful PR](https://github.com/CodeSigils/zero-md-formatter/pull/7)
  after real re-verification of every evidence URL through live fetches. No
  blind date bump was used.

Then the behavioral failure, which was mine. I had first left a clean change
uncommitted because a gate was red, then committed and pushed it anyway on a
later “handle git hygiene” instruction. I measured success as “the fix is in a
branch” when the relevant state was a green default branch. Configuration rot
calls for an automated guard. A behavior failure calls for a directive. Each
needs its own repair.

The general findings that came out of it are now recorded in my lab notes
with their sources, and three of them read like laws at this point. A
scheduled run is not a gate run. Judge health by the event class that actually
gates merges. A known-red gate calls for a stop-and-report decision. Measure
“done” by the default branch. The investigation also left one open question I
had not expected. A repository
that publishes a package has a second front, the release surface, where
version, tag, and registry are three separate facts that must agree. Ours
did not. The published artifact and the default branch both claimed the same
version while differing in content, and a later release attempt created a
tag and a GitHub Release before the registry publish failed, leaving a
version spent and half-landed. Merged is not released.

## A real incident, and the check it exposed

One of the fleet repositories had no branch protection configured on its
default branch. I found out through the GitHub API, which returned a plain
"Branch not protected" for `main`. That meant pushes to the default branch
were observed only after they landed. There was no required status check, so
nothing mechanically stood between a broken tree and the main branch. The
[official documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
had been telling me what protection could enforce all along. I had simply
never read it for this repository.

The fix was available the same day. I enabled protection on `main` with
required status checks, and here the fleet had already taught me a specific
trap: the required check names must match the rendered job names exactly. A
few days earlier I had watched a repository whose protection required a
check that no workflow produced anymore, which blocks every pull request,
silently and permanently, until someone notices. So the contexts were set
from the actual rendered names, "Validate standard (3.10)" and "Validate
standard (3.14)", and I read the configuration back through the API to
confirm what was live: both contexts required, no admin enforcement, strict
status checks off so the maintainer can still push directly when needed.

Then I wrote an incident report, and I kept it short. The file carries a
dated header with a status line, an owner-of-record pointing at the research
register, and a scope note. The body holds a summary, two findings with the
evidence behind each, a remediation section I appended the same day to
record what was changed and how it was verified, and a sources section
listing the official GitHub documentation pages the claims rested on. The
report also recorded one thing I could not repair in the repository itself:
a private sibling where the same API call returns a 403 explaining that
branch protection needs a paid plan or a public repository. That limitation
stands, it is documented, and the decision about it lives with the owner,
outside the public tree.

Writing that report surfaced the hole. Nothing in the repository validated
reports like it. A report file could be added, orphaned from the register,
cite a URL that was never verified anywhere, and every check would still
pass. The reports I most wanted to trust were the least checked artifacts in
the tree.

So that got fixed too, in the same careful, small way the rest of the spec
grows. The standards checker now walks the incident-report directory. A
report must be referenced from the body of a research register entry, or the
check fails. The URLs a report cites must appear in the source registry, in
their registered spelling, or the check fails. The header shape is checked:
date, status, owner of record, scope, a summary section, a sources section.
No opinion about prose. No freshness score. Just the three structural
guarantees that make a report findable and its evidence addressable.

The first run of that check found two real mistakes in the report I had just
written by hand. I had cited the GitHub REST endpoint without the `/en/`
path segment, and I had used a path variant of a documentation page that
differed from the registered one. Both pages exist. Both resolve. But the
registry spells them one way, and a citation that only almost matches a
registered source is exactly the kind of quiet drift the whole system is
meant to catch. The check caught an error in the record it was designed to
protect.

The new checks come with fixtures, in the spirit of the conformance corpus
the repository already keeps: small synthetic trees, one per behavior, with
expected findings recorded and compared in both directions, so a check that
no fixture exercises is a gap the harness reports. The corpus grew from
thirteen trees to seventeen, and the honest count is part of the point.

## Corrections are part of the record

A smaller lesson from the same week deserves its own paragraph, because it
was embarrassing in the best way.

An earlier research entry of mine argued that a piece of evidence had gone
stale faster than the cadence that was supposed to check it. The reasoning
was tidy and wrong. On rechecking, the evidence window was thirty days, and
the checking cadence was weekly. The window was longer than the cadence, so
the evidence expired inside its own window while the weekly check kept
reporting green. Checking is not refreshing. That is the whole correction.
The register carries it as a dated amendment to the original entry. The
original finding stays, marked as corrected, with the new analysis beside it.

This pattern has good company.
[Google's SRE postmortem template](https://sre.google/sre-book/example-postmortem/)
gives every report a status field that is a lifecycle, reading something
like "Complete, action items in progress", instead of a one-shot label, and
its action items carry owners and tracked statuses.
[PagerDuty's practice](https://docs.pagerduty.com/ops-guides/postmortem-best-practices/accountability)
gives action items explicit expiry windows, fifteen days for the most
severe incidents and thirty for the next tier, because an action item that
is never closed becomes decoration.
[incident.io's follow-up states](https://docs.incident.io/post-incident/follow-ups)
include "not doing" as a recorded decision, so items leave the open list
without vanishing from the record. And the
[USENIX ;login: article on postmortem follow-through](https://www.usenix.org/system/files/login/articles/login_spring17_09_lunney.pdf)
makes the same case from practice: close obsolete action items rather than
keeping them around forever, and report burndown so the outliers are
visible. What none of the primary sources I found prescribes is an expiry
for the report itself. Reports are treated as dated records that get amended
and re-reviewed. Action items expire. The record does not. I have adapted
that distinction deliberately, and the register says so.

There are also precedents for the completeness instinct, from places that
are not about incidents at all.
[MkDocs can be configured](https://www.mkdocs.org/user-guide/configuration/)
to warn about pages that exist in the docs directory but are missing from
the navigation, and its strict mode turns that warning into a build
failure.
[GitLab's documentation testing](https://docs.gitlab.com/development/documentation/testing/)
fails a pipeline when a deleted or renamed document leaves no redirect
behind. Different tools, same sentence: every artifact that exists has to be
registered somewhere, or the system does not consider it done. My
incident-report check is a small, local version of that idea.

## After delegating, check the repository

One more pattern from the same week, because it changed how I measure work
I hand off.

I delegated three long tasks to background agents on the same governance
repository. All three ended with the same platform message: timed out after
thirty minutes of inactivity. Their outcomes had nothing in common. One left
no repository footprint at all: no branch, no commit, no pull request,
nothing. One left two coherent documentation edits and none of the code I
had asked for. One had completed most of a release before dying: the version
bump, the tag, and the GitHub Release existed, but the registry publish had
failed on a configuration error that needs a human, and the agent timed out
before reporting. That is the half-landed version I mentioned in the fleet
section, and it cannot simply be re-created.

A background agent's running status is not evidence of progress. Two of the
three spent the full window producing no repository change. After any
delegation I inspect the live state of the target, branches, commits, tags,
and workflow runs before I call anything done. The tasks that failed shared a
shape. Each opened with a long read of governance documentation, hundreds of
lines before the first write. Smaller deliverables, incremental commits, and
the irreversible step sequenced last are practical adjustments. Verification
at the boundary remains necessary.

## The small gates that actually stick

Not every repeated instruction grew into a research register. Some got the
humbler treatment, and those are often the ones that hold best.

The commit hook in the standards repository rejects a commit message unless
it has a summary line and separate `what:` and `why:` lines. My first
attempt at the incident-report commit failed the hook, because I had put both
lines in one paragraph. The hook did not care about my intentions. It showed
me the expected shape, and the next commit passed. That is a machine check
doing the job I had been doing by memory, badly, at the end of long sessions.

My notes repository taught the same lesson from the other direction, about
what happens when a gate itself is sloppy. Its validation script checks that
open questions written inside notes also appear in the aggregate index. The
note-side scanner looked for a literal substring, while the index-side
extractor used a tolerant pattern. When I bolded a question marker, the two
parsers disagreed about the same text, and the tool reported the symptom,
"a marker is missing", instead of the real cause, "a marker form I cannot
parse". The fix was one line of tolerance, and the deeper finding went into
the notes: one marker, one parser, and a validator that cannot recognize a
variant should say what it cannot parse. When several invariants refer to the
same token, they must share a single extraction function.

"Check the working tree, index, upstream relation, remotes, and latest
commit" became a small script and a standing habit in the agent instructions,
so the full status arrives before any commit conversation starts. "Report
only, do not implement" is now a phrase I say once at the start of a task,
and the better repositories carry it as a directive in their own agent
instructions. The directive makes the boundary findable.

None of this is novel. A linter makes a rule available at the point of use.
My chat history had become a style guide that I reread constantly and still
failed to apply.

## Where human review belongs

I still do not want an agent to make every decision autonomously. The
moments where I want my own judgment are specific: destructive git
operations, architectural changes, releases, governance rules, publication,
and the decision about whether a piece of research is current enough to act
on.

The week I have just described gave each of those categories a concrete
case. The failed registry publish failed on trusted-publisher configuration,
which lives on the maintainer's side of the fence and cannot be completed by
an agent alone. The release needed a human before it needed a retry. The
fleet's stale required-check entry was a governance configuration nobody
should change without understanding which pull requests it will block. The
freshness correction was a judgment call about what my own earlier evidence
actually showed, and the register records my reasoning so someone, including
future me, can disagree with it on the record.

Good human-in-the-loop practice, to me, puts review where accountability and
risk actually live. Small reversible actions can remain delegated. A human may
approve a destructive git operation while the agent
warns and proposes the safer path. A human may review an architectural
change after the agent has clarified the options and reported the gaps. A
human may decide whether a research finding is current enough to act on,
after the agent has shown the finding, its sources, and its check dates. A
human may approve publication or a change to the governance rules. And a
human should decide when it is time to stop researching and start
implementing, with the agent's findings in view before the first edit.

The agent gathers status, compares documentation with implementation,
identifies gaps, warns on destructive actions, summarizes research, and
proposes a next step aligned with the backlog. Only then can I decide whether
the proposal makes sense and whether the evidence is sufficient. That division of labor
feels healthier than either extreme, and it only works if the gathering half
is trustworthy, which is what all the checks are for.

## What I am hoping to stop typing

I would like a workflow where the current state is easy to establish, the
relevant rules are discoverable, and research is connected to the decisions
it supports. Documentation with a clearer relationship to reality. Explicit
Git hygiene that remains available under pressure.
Recommendations that show their evidence and name what remains uncertain.
Quality review before the commit, not after the regret.

Most of all, I would like to stop typing the same instructions. If a rule
keeps recurring, it is probably trying to become part of the system: a
specification, a checklist, a template, a validation script, a workflow
gate. The next time I notice one, I will add it to the backlog with an owner,
an evidence boundary, and the smallest check that can prove it is working.
That gives the next agent a rule it can find and gives me a record I can
challenge when the rule no longer fits.

## Related reading

- [When an AI Agent Signs Your Commits](when-an-ai-signs-your-commits.md)
- [When Agent Instructions Start to Drift](agent-instruction-drift.md)
- [Where Agent Memory Actually Lives](agent-memory-surfaces.md)
