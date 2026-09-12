---
title: When Agent Instructions Start to Drift
description: A field note on duplicated agent guidance, canonical sources, and proportionate checks in an AI-assisted project.
keywords:
  - AI agents
  - agent instructions
  - documentation drift
  - AGENTS.md
  - skills
  - maintenance
---

<div class="image-wrapper">
  <img src="/assets/images/agent-instruction-drift-wires.jpg"
       alt="An overloaded telecom junction box filled with tangled cables" />
</div>

*Photo: [Tangled telecom wires](https://commons.wikimedia.org/wiki/File:Tangled_telecom_wires.jpg) by [Tulumnes](https://commons.wikimedia.org/wiki/User:Tulumnes), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).*

An agent can follow an instruction perfectly and still do the wrong thing when
the project gives it two slightly different versions of the same rule. I ran
into that while tightening one of my own agent-assisted projects. The surface
problems were ordinary: stale paths, old counts, and references that had moved.
The more interesting problem appeared later, when the obvious clutter was out
of the way: the guidance itself had begun to repeat.

The same search order appeared in more than one mode. A list of authority
files existed in more than one place. A small catalog overlapped with a larger
one. None of those copies was wildly wrong. That was the problem. Each looked
reasonable on its own, so the maintenance dependency between them stayed
invisible.

## Drift is usually a maintenance problem first

It is tempting to describe this as an agent failure: the agent read the wrong
file, missed an instruction, or followed stale context. Sometimes that is true.
But in this project the more useful diagnosis was simpler: I had created more
than one place that could sound authoritative.

Once guidance is duplicated, every future edit becomes a synchronization task.
One copy can be updated, another can keep the old wording, and an agent has no
reliable way to infer which version is the intended one. Even a human reviewer
can skim past the difference because the text is familiar.

The lesson was not to force every project into one enormous `AGENTS.md` file.
Large instruction files have their own failure mode: important rules become
hard to find. The useful question is narrower:

> Where is the one place that owns this rule, and what should every other place
> do instead of repeating it?

## One owner, useful pointers

For the repeated guidance I found, the repair was usually unglamorous. Keep the
full rule in one canonical location. Elsewhere, explain the local exception or
stopping condition and point back to that owner. A shorter file is not always a
better file, but a file that clearly says what it owns is easier to maintain.

That also changed how I think about separate instruction files. Splitting a
document is justified when a rule genuinely applies only to a directory, tool,
or workflow. Splitting it merely because a heading feels important often creates
another surface to keep current.

!!! tip "Review overlap before adding another rule"

    Before adding a new instruction, search for an existing explanation of the
    same decision. If one exists, extend the owner or add a pointer instead of
    creating a parallel version.

## Checks should earn their place

Some drift needs a check, especially after it has caused a real mistake. In
this project, the first cleanup passes exposed stale paths and references that
had lost their context. A small check against the current project state is
useful when it tests a specific claim that has already failed.

That is different from adding a checker for every imaginable inconsistency.
Verification should support the source of truth, not become a second source of
truth with its own unexplained rules. A check can drift too: it may protect the
wrong path, run at the wrong time, or quietly stop representing the risk it was
meant to catch.

My working rule is now modest: add a control after an observed failure or a
clear project contract, keep its purpose easy to explain, and revisit it when
the protected part of the project changes.

## What I look for now

When an agent-assisted project starts feeling harder to steer, I do not begin
by adding more instructions. I look for repeated guidance, unclear ownership,
and claims that no longer match the repository. The first useful repair is
often a pointer, a deletion, or one small verification step—not another layer
of process.

That does not make an agent infallible. It makes the project easier for both
the agent and its maintainer to understand next time.
