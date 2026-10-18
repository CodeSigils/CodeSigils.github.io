---
title: When the Instructions Keep Repeating
description: A field note on treating repeated agent instructions as a requirements backlog, and what a real branch-protection incident taught about checks, corrections, and research you can still trust.
keywords:
  - AI agents
  - agent instructions
  - documentation drift
  - evidence
  - branch protection
  - research register
  - skill-repo-standards
---

I have been working on a growing collection of repositories under
[CodeSigils](https://github.com/CodeSigils). Most of them are still works in
progress and personal exploration: skills, research notes, review tools,
documentation experiments, and the occasional small spike used to test an idea
before committing to something larger. They are all trying to answer a similar
question: how do I work with AI agents in a way that is useful, repeatable, and
grounded in evidence?

Along the way I noticed something mildly embarrassing. I kept typing the same
instructions. Again. And again. And that is a no-no for me, in code and in
life.

## The instructions I kept repeating

Some were small practical reminders. They hide a lot of laugh and tears
behind them:

- "Is the information in `README.md` still accurate? Review it carefully and
  report any staleness or drift."
- "Are the docs updated?"
- "Is `ROADMAP.md` aware of this? Do we have a gap?"
- "Is `AGENTS.md` aware of this?"
- "Check git status for pending changes before committing."
- "Review the code first for bugs, duplication, drift, and conventions. Why
  did you commit before doing that?"
- "Check the working tree, index, upstream relation, remotes, and latest
  commit. I want the full status, not just 'clean' or 'dirty'."
- "Tighten the README so it matches what CI actually does."
- "Audit the README against the repository structure, executable checks,
  current-state record, and recent history. Report only. Do NOT implement."

Others were more about how decisions get made:

- "Are we following good human-in-the-loop practice here? Research it and
  report what you find. Official docs from industry leaders take priority."
- "What do the official Git or GitHub docs say about this?"
- "Those recommendations should be evidence based, not speculative. Read the
  research already captured in the docs."
- "Do we have a directive somewhere? This was supposed to be evidence based
  first."
- "Why is this the best next step? Did we skip a previous one because of my
  new query? What is the best next step now, and why?"
- "Check the stated backlog against the current implementation and release
  state before making a recommendation."

And some were just me, my attention span, and my limits:

- "I said report only, do not implement. Haven't we enforced this? Sorry that
  was in another repo. My bad."
- "SO many dependabot PRs for review and merging! Review and handle git as
  needed. I'm tired."

At first these felt like separate annoyances that added to my fatigue. Then
my pre-AI-generation brain eventually caught up with the pattern.

## A repeated instruction is a signal

When I have to repeat an instruction once, it may be a lapse in attention.
When I have to repeat it across sessions, repositories, and different kinds
of work, it usually means something else: the rule needs a home outside the
conversation.

"Check git status before committing" should not depend on whether I remember
to say it. "Use evidence rather than speculation" should not depend on the
agent happening to recall a previous chat. "Make sure the README reflects
current reality" should not require me to notice, yet again, that the
documentation has quietly drifted away from the code. These are workflow
requirements. They belong in a specification, a checklist, a template, a
validation step, or some other inspectable part of the repository.

I try to remind myself not to create bureaucracy in a file swamp full of
prose for its own sake. The goal is narrower: make good behavior easier to
repeat than the alternative. That is harder than it sounds, and I am still
not good at it.

Over time each recurring instruction sorted itself into one of three
destinations. It can become a machine check that fails loudly when the rule
is broken. It can become a durable directive written into the repository's
own agent instructions, so any agent that reads them starts from the right
place. Or, occasionally, I notice the rule is already covered somewhere I
forgot, and the repetition was really a signal that I could not find the
existing one. Dropping it then means making the existing rule easier to
find, not just typing it one more time and moving on.

## The fleet is messy on purpose

The CodeSigils repositories cover a range of concerns:

- [`ai-repo-sanitize`](https://github.com/CodeSigils/ai-repo-sanitize)
- [`awesome-agent-trust`](https://github.com/CodeSigils/awesome-agent-trust)
- [`py-review-skill`](https://github.com/CodeSigils/py-review-skill)
- [`python-project-workflow`](https://github.com/CodeSigils/python-project-workflow)
- [`repo-architecture-skill`](https://github.com/CodeSigils/repo-architecture-skill)
- [`repo-health-scan`](https://github.com/CodeSigils/repo-health-scan)
- [`skill-discovery`](https://github.com/CodeSigils/skill-discovery)
- [`tina-cms-skill`](https://github.com/CodeSigils/tina-cms-skill)
- [`zensical-skill`](https://github.com/CodeSigils/zensical-skill)
- [`zola-skill`](https://github.com/CodeSigils/zola-skill)
- [`zero-md-formatter`](https://github.com/CodeSigils/zero-md-formatter)
- [`neovim-latest-ubuntu`](https://github.com/CodeSigils/neovim-latest-ubuntu)

Some are skills. Some are research repositories. Some contain companion
spikes, such as [`repo-architecture-inspect-spike`](https://github.com/CodeSigils/repo-architecture-inspect-spike)
and [`markdown-oxc-spike`](https://github.com/CodeSigils/markdown-oxc-spike).
Others are mainly places to collect notes and references for later
evaluation. The neovim one was exploring DevOps and the Linux packaging
world, mostly for the fun of collaborating with an agent through some
particular problems. All of them required some kind of research capturing.

This unevenness is partly on purpose. I was exploring different strategies to
tackle similar problems, and the differences between repositories are data.
Comparing how two approaches aged is how I learn which patterns are worth
converging on. The mess is exploratory work, not neglect. What it costs me is
exactly the problem this article is about: some documentation is current,
some is incomplete, and some captures research that was valuable when written
but may no longer reflect the state of a tool, a standard, or a repository. I
do not need uniformity for its own sake. I need to know which information I
can rely on when making a decision.

## Research that can still answer questions

I keep a broader set of notes in
[`agent-concepts-study`](https://github.com/CodeSigils/agent-concepts-study).
Its research directory holds a lot of material I consider valuable. The
wider observations in that repository need more caution. Many are outdated,
incomplete, or simply wrong now, which is why I keep it private for now. They
were useful when written. They should not automatically be treated as
current guidance.

Capturing research is only part of the job. The harder part is making it
possible to answer questions like: where did this claim come from? When was
it checked? What source supports it? Is it still relevant? Does it apply to
this repository? What remains uncertain? What decision does it inform?
Without those connections, research becomes another pile of potentially
stale documents. And we all know how URL reference links that maybe contain
useful info now tend to
[rot irreversibly in the future](https://www.w3.org/Provider/Style/URI "cool urls").

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

## A real incident, and the check it exposed

The part I want to tell in full is the branch protection incident, because
it is the clearest example I have of the loop working, including the part
where the loop had a hole in it.

One of the fleet repositories had no branch protection configured on its
default branch. I found out through the GitHub API, which returned a plain
"Branch not protected" for `main`. That meant pushes to the default branch
were observed only after they landed. There was no required status check, so
nothing mechanically stood between a broken tree and the main branch.

The fix was available the same day. I enabled protection on `main` with
required status checks, and here the fleet had already taught me a specific
trap: the required check names must match the rendered job names exactly. The
workflow runs a matrix, so the check names are the rendered forms, something
like "Validate standard (3.10)" and "Validate standard (3.14)". A required
check that matches no job in the workflow blocks every pull request, silently
and permanently, until someone notices. I had watched that failure mode
before, so the contexts were set from the actual rendered names, and I read
the configuration back through the API to confirm what was live: both
contexts required, no admin enforcement, strict status checks off so the
maintainer can still push directly when needed.

Then I wrote an incident report. Not a sprawling one. A dated file with a
short header: the date, a status line, an owner-of-record pointing at the
research register, and a scope note. A summary. Two findings, each with its
evidence. A remediation section appended the same day, recording what was
changed and how it was verified. A sources section listing the official
GitHub documentation pages the claims rested on. The report recorded one
thing I could not repair in the repository itself: the private sibling where
the same API call returns a 403 explaining that branch protection needs a
paid plan or a public repository. That limitation stands, it is documented,
and the decision about it lives with the owner, outside the public tree.

Writing that report surfaced the hole. Nothing in the repository validated
reports like it. A report file could be added, orphaned from the register,
cite a URL that was never verified anywhere, and every check would still
pass. The reports I most wanted to trust were the least checked artifacts in
the tree.

So that got fixed too, in the same careful, small way the rest of the spec
grows. The standards checker now walks the incident-report directory. A
report must be referenced from a body of a research register entry, or the
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
meant to catch. That felt good, in the way a test that fails on your own bug
always does.

The new checks come with fixtures, in the spirit of the conformance corpus
the repository already keeps: small synthetic trees, one per behavior, with
expected findings recorded and compared in both directions, so a check that
no fixture exercises is a gap the harness reports. The corpus grew from
thirteen trees to seventeen, and the honest count is part of the point.

## Corrections are part of the record

A smaller lesson from the same work deserves its own paragraph, because it
was embarrassing in the best way.

An earlier research entry of mine argued that a piece of evidence had gone
stale faster than the cadence that was supposed to check it. The reasoning
was tidy and wrong. On rechecking, the evidence window was thirty days, and
the checking cadence was weekly. The window was longer than the cadence, so
the evidence expired inside its own window while the weekly check kept
reporting green. Checking is not refreshing. That is the whole correction,
and the register now carries it as a dated amendment to the original entry
rather than a silent rewrite. The original finding stays, marked as
corrected, with the new analysis beside it.

This pattern has good company. Google's SRE postmortem template gives every
report a status field that is a lifecycle, reading something like "Complete,
action items in progress", instead of a one-shot label. PagerDuty's own
practice gives action items explicit expiry windows, fifteen days for the
most severe incidents, thirty for the next tier, because an action item that
is never closed becomes decoration. incident.io's follow-up states include
"not doing" as a recorded decision, so items leave the open list without
vanishing from the record. What none of the primary sources I found
prescribes is an expiry for the report itself. Reports are treated as dated
records that get amended and re-reviewed. Action items expire. The record
does not. I have adapted that distinction deliberately, and the register
says so.

There are also precedents for the completeness instinct, from places that
are not about incidents at all. MkDocs can be configured to warn about pages
that exist in the docs directory but are missing from the navigation, and
its strict mode turns that warning into a build failure. GitLab's
documentation testing fails a pipeline when a deleted or renamed document
leaves no redirect behind. Different tools, same sentence: every artifact
that exists has to be registered somewhere, or the system does not consider
it done. My incident-report check is a small, local version of that idea.

## The small gates that actually stick

Not every repeated instruction grew into a research register. Some got the
humbler treatment, and those are often the ones that hold best.

The commit hook in the standards repository rejects a commit message unless
it has a summary line and separate `what:` and `why:` lines. My first
attempt at the incident-report commit failed the hook, because I had put both
lines in one paragraph. The hook did not care about my intentions. It showed
me the expected shape, and the next commit passed. That is a machine check
doing the job I had been doing by memory, badly, at the end of long sessions.

"Check the working tree, index, upstream relation, remotes, and latest
commit" became a small script and a standing habit in the agent instructions,
so the full status arrives before any commit conversation starts. "Report
only, do not implement" is now a phrase I say once at the start of a task,
and the better repositories carry it as a directive in their own agent
instructions, which makes it findable instead of remembered.

None of this is novel. It is the same instinct that makes a linter better
than a style guide you reread when you remember to. The novel part, for me,
was noticing that my chat history had become a style guide I reread
constantly and still failed.

## Where human review belongs

I still do not want an agent to make every decision autonomously. The
moments where I want my own judgment are specific: destructive git
operations, architectural changes, releases, governance rules, publication,
and the decision about whether a piece of research is current enough to act
on.

Good human-in-the-loop practice, to me, means placing review where
accountability and risk actually live, rather than approving every small
action. A human may approve a destructive git operation while the agent
warns and proposes the safer path. A human may review an architectural
change after the agent has clarified the options and reported the gaps. A
human may decide whether a research finding is current enough to act on,
after the agent has shown the finding, its sources, and its check dates. A
human may approve publication or a change to the governance rules. And a
human should decide when it is time to stop researching and start
implementing, with the agent's findings in view before the first edit.

The agent gathers status, compares documentation with implementation,
identifies gaps, warns on destructive actions, summarizes research, and
proposes a next step that respects the backlog rather than the most
immediately interesting thread. Only then can I decide whether the proposal
makes sense and whether the evidence is sufficient. That division of labor
feels healthier than either extreme, and it only works if the gathering half
is trustworthy, which is what all the checks are for.

## What I am hoping to stop typing

I would like a workflow where the current state is easy to establish, the
relevant rules are discoverable, and research is connected to the decisions
it supports. Documentation with a clearer relationship to reality. Git
hygiene that is explicit instead of remembered under pressure.
Recommendations that show their evidence and name what remains uncertain.
Quality review before the commit, not after the regret.

Most of all, I would like to stop typing the same instructions. If a rule
keeps recurring, it is probably trying to become part of the system: a
specification, a checklist, a template, a validation script, a workflow
gate. The repetitions were never really annoyances. They were the backlog
talking, patiently, in my own words, waiting for me to file them somewhere
an agent can find them too.

And when I do, the interesting part begins. Because a rule that survives
contact with real repositories, real fixtures, and real incidents stops
being something I believe and becomes something the repository knows. The
agent drifts less. I type less. And the final laugh, when it comes, belongs
to the checks.

## Related reading

- [When an AI Agent Signs Your Commits](when-an-ai-signs-your-commits.md)
- [When Agent Instructions Start to Drift](agent-instruction-drift.md)
- [Where Agent Memory Actually Lives](agent-memory-surfaces.md)
