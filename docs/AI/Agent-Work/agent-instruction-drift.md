---
title: When Agent Instructions Start to Drift
description: A field note on duplicated agent guidance, canonical sources, and checks that stay worth their cost in an AI-assisted project.
keywords:
  - AI agents
  - agent instructions
  - documentation drift
  - AGENTS.md
  - skills
  - maintenance
---

<div class="image-wrapper">
  <img src="/assets/images/agent-instruction-drift-wires-1440.webp"
       srcset="/assets/images/agent-instruction-drift-wires-768.webp 768w,
               /assets/images/agent-instruction-drift-wires-1440.webp 1440w"
       sizes="(max-width: 768px) calc(100vw - 2rem), 960px"
       alt="Close-up of tangled coloured network cables and connectors"
       width="1440"
       height="958" />
</div>

<p class="image-attribution"><em>Photo: <a href="https://freebie.photography/technology/wires.jpg">Tangle of coloured cables and connectors</a> from <a href="https://freebie.photography/about.htm">freebie.photography</a>, used under its attribution licence.</em></p>

The drift showed up while I was tightening the agent guidance in one of my own
projects. The first problems were ordinary: stale paths, old counts, references
to files that had moved. Once that clutter was gone, the problem that mattered
was still there. The same search order appeared in more than one mode, and a
compact list of authority files overlapped a larger list somewhere else.

That is the drift I look for first. An agent can follow an instruction
perfectly and still land on the wrong version of a rule, because the project
offered two versions of it.

## Drift is usually a maintenance problem first

It is tempting to call this an agent failure: the wrong file was read, an
instruction was missed, an old context survived. In this project the useful
diagnosis was simpler. I had created more than one place that could sound
authoritative.

Once guidance is duplicated, every future edit becomes a synchronization task.
One copy gets updated, another keeps the old wording, and an agent has no
reliable way to infer which version is intended. A human reviewer can skim past
the difference because the text reads as familiar either way.

One enormous `AGENTS.md` file fails in its own way, because the important rules
become hard to find. The question that helped was narrower:

> Which place owns this rule, and what does every other mention of it point to?

## One owner, useful pointers

For the repeated guidance I found, the repair was unglamorous. Keep the full
rule in one canonical location. Elsewhere, explain the local exception or the
stopping condition and point back to that owner. A file that says plainly what
it owns is easier to maintain than a short file that quietly owns everything.

That also changed how I think about separate instruction files. Splitting a
document is justified when a rule applies only to a directory, a tool, or a
workflow. Splitting it because a heading feels important usually creates one
more surface to keep current.

The tooling vendors describe the same shape. Codex reads `AGENTS.md` before it
starts, layering concise project guidance over smaller override files for
specific directories
([Codex and AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)).
Copilot keeps one repository-wide `copilot-instructions.md` and adds
path-scoped instruction files only where a folder needs its own
([repository instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)).
Both keep the owner and treat the local file as a pointer with a narrow
subject.

!!! tip "Review overlap before adding another rule"

    Before adding a new instruction, search for an existing explanation of the
    same decision. If one exists, extend the owner or add a pointer to it.

## A justified split can still drift

My `py-review` skill is built around a routing table. It tells a reviewing
agent which focused checklist to load for a given kind of code change. Each
checklist owns its own territory, and the table points back to it, so the
design follows the rule above. Then the table stopped reaching rules it was
meant to point at.

The checklists carried signals for duplicated logic, string construction, and
constants that the routing row for style work never named. A reviewer working
from the table skipped checks the checklists documented. A reviewer opening a
checklist directly applied them. Two catalogs described the same work from
different angles, and the pointer between them had gone quiet
([the repair](https://github.com/CodeSigils/py-review-skill/commit/a32600df068aac5e0eff25e14f049b1d7ae2104e)).

The same pass tightened the version guidance. The router used to let a
project's Python version decide that every relevant core skill should load. It
now routes by what the changed code touches and applies a rule when that rule's
own compatibility caveat matches.

## Checks should earn their place

Some drift needs a check, especially after it has caused a real mistake. The
first cleanup passes in this project exposed stale paths and references that
had lost their context. A small check against the current project state is
useful when it tests a specific claim that has already failed.

A check is a different kind of surface from an instruction. An instruction file
says how the project works. A check compares one specific claim with the
current state, which makes it useful for a known failure and decorative for an
imagined one. Its assumptions need an owner and a reason to exist, the same as
any other rule in the project.

I keep the budget small. Verification supports the source of truth, and a
checker that quietly becomes a second source of truth with unexplained rules
costs more than it saves. A check can protect the wrong path, run at the wrong
time, or stop representing the risk it was meant to catch. When the protected
claim disappears, when the check costs more than the harm it prevents, or when
a better control replaces it, repair or retire it. Process that has lost its
reason is another form of drift.

My working rule is now modest: add a control after an observed failure or a
clear project contract, keep its purpose easy to explain, and revisit it when
the protected part of the project changes.

## What I look for now

When an agent-assisted project starts feeling harder to steer, I look for
repeated guidance, unclear ownership, and claims that no longer match the
repository. The first repair is often a pointer, a deletion, or one small
verification step. More process earns its place when it protects a specific,
observed problem.

The routing table in `py-review-skill` is the part I reread after every
checklist change, because a pointer is the cheapest rule to let rot. That is
where the next gap of this shape will appear first, and the repository is open
if you want to watch it happen:
[CodeSigils/py-review-skill](https://github.com/CodeSigils/py-review-skill).
