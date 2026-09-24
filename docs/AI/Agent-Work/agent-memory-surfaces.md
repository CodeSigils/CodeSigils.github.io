---
title: Where an Agent's Memory Actually Lives
description: A field note on the places "memory" shows up when working with AI agents — and how each one forgets differently.
keywords: AI agents, agent memory, context window, CLAUDE.md, AGENTS.md, context engineering
---

"Memory" may be the most overloaded word in agent work. It appears
in the model's context window, in a project's CLAUDE.md, in a skill
definition, in a user profile field, in a session summary. Every one
of those places holds onto something and quietly drops something
else. The question I kept coming back to was simple: where does an
agent's memory actually live?

I started from my own work across a few tools — Hermes, Claude Code,
Codex, Cursor, Copilot — and from the documentation they publish
today. This is a map, not a benchmark: I checked the platform
details against current docs rather than re-testing each behavior
myself.

## The room that resets

The context window is an agent's working memory: everything
currently in the prompt, from system instructions to the latest tool
output. It is also the most temporary surface there is. Content
beyond the window falls away, and in long contexts the material in
the middle is the least reliably attended to. A large window is not
the same thing as full resolution — the classic "lost in the middle"
finding showed performance dropping as relevant information moves
toward the center of long contexts
([Liu et al., 2023](https://arxiv.org/abs/2307.03172)).

The conversation trace is the visible record of that room — what the
human and agent said to each other. It preserves the dialogue until
it is pruned, but it records what was said, not what was understood.
A decision that looks agreed-upon in the log may never have been
shared understanding.

Tool outputs are memory at its freshest: exact, byte-level, and
valid only at the moment of the call. They snapshot an external
system; they are not the system. And each new session starts from a
clean room — the whole room is re-earned, or carried over only
through a summary someone bothered to write.

## The filing cabinet

Repository files are the memory the project checks in: structure,
behavior, documented conventions, decision records. They are
immutable per commit, and they forget by omission — the reasoning
behind a decision, the alternatives that were rejected, anything
nobody wrote down. They are also read only when the agent decides to
go looking. A comprehensive README does not mean a well-understood
project.

One of my own projects ran into the omission form of this. The
README's repository layout tree was hand-maintained, and new files
kept landing in the repo without it
([the tree that drifted](https://github.com/CodeSigils/python-project-workflow-skill)).
I added a check that compares the tree against `git ls-files` and
wired it into CI
([check-readme-tree.py](https://github.com/CodeSigils/python-project-workflow-skill/blob/main/scripts/check-readme-tree.py)).
About a month later the tree had drifted again anyway and needed a
manual correction
([docs: keep repository tree current](https://github.com/CodeSigils/python-project-workflow-skill/commit/6c1a5c2b67e934b35cc2633626875248ff346b12)).
The file remembered its content; nothing remembered its promise to
stay current.

Instruction files are the exception to that. AGENTS.md, CLAUDE.md,
`.cursorrules`, and repository Copilot instructions are loaded at
session start, before any work begins, as the behavioral contract
for the project. The current OpenAI guidance describes this
explicitly: Codex reads `AGENTS.md` files before doing any work
([Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)),
and Claude Code opens each session expecting its `CLAUDE.md` and
auto-memory notes
([How Claude remembers your project](https://code.claude.com/docs/en/memory)).

That make-believe power comes with a trap. Instruction files forget
the rationale behind their own rules, the exceptions, the "this
applied during phase one" qualifiers. They drift when conventions
change and the old rule stays. Two instruction files in one
project, or a long one with rules appended and never pruned, quietly
become two different memories competing for the same session.

## Beyond the repo

A user profile is durable memory with a human's name on it:
preferences, recurring corrections, identity. Its blind spot is the
difference between a one-time instruction and a durable preference —
and profile entries that generalized further than their owner
intended.

External docs and knowledge bases are memory held at a distance.
They preserve reference facts and platform specifications, and they
drift independently of your project: versions move, links rot,
deprecated APIs stay documented until somebody notices. An agent can
answer from stale training data instead of fetching the current page,
and the reader may never know.

## The muscle memory

Skills and personalities are memory in the form of procedure: a
reusable definition of how to do a recurring kind of work. They load
at session start like instruction files do. Unlike them, a skill
does not learn from repeated use — the same mistake recurs identically
next month. And loaded skills interact in ways nobody fully
controls: order matters, conflicting guidance composes silently, and
a skill written for one domain can be pulled into another where it
does not fit.

## The compression layer

Summaries and compaction sit on top of everything else. They exist
to fit more history into less space, and they forget by design:
nuance, tone, the chain of reasoning that led to a conclusion.
Errors compound across chained summaries, and the summarizer's idea
of what mattered quietly becomes the session's idea of what
happened. A "lossless" compaction is rarely lossless.

## Every surface forgets differently

Put the surfaces side by side and a pattern appears: each one has
its own failure mode. The context window forgets by position. Traces
forget by pruning. Repo files forget by omission. Summaries forget
by compression. Skills forget by not learning. If you plan for one
kind of forgetting, you will be surprised by the others.

Two observations have been the most useful to me since.

Nothing preserves *why*. Repo files record what was decided; traces
record what was said; neither reliably keeps the reasoning, the
rejected alternatives, or the constraints at the time. This is the
most common source of drift I see: a rule survives in an instruction
file long after the context that justified it has gone. I wrote
about that in
[When Agent Instructions Start to Drift](agent-instruction-drift.md),
and this is the same story from the other side — memory scattered
across surfaces, rather than guidance repeated across files.

And false confidence compounds. A project with AGENTS.md, CLAUDE.md,
a user profile, and a few loaded skills can *feel* well-memoried.
Each layer adds its own confidence zone: "it's documented," "it was
in the session," "it's in my preferences." When the layers disagree,
the agent resolves the conflict silently — by recency, by position,
or by whichever file loaded last.

!!! tip "When a rule keeps getting forgotten"
    Ask which surface was supposed to hold it, and how that surface
    forgets. A rule buried in a deep doc is memory only if the agent
    decides to go looking; a rule in an instruction file is memory
    whether or not it is still true.

## What I look for now

Three questions, when something goes missing:

Where was this supposed to live? If the answer is "nowhere
specific," that is the diagnosis — memory that has no surface is
memory that was never really kept.

Which forgetting does this surface have? A stale rule in an
instruction file needs different care than a lossy summary. Name the
failure mode before reaching for a fix.

Is the *why* stored next to the rule? When I write a rule, I try to
leave its justification one line beneath it, or point to where it
lives. The note is worth more than the instruction the day the
instruction stops being true.

## Related reading

- [When Agent Instructions Start to Drift](agent-instruction-drift.md)
  — the companion field note on guidance that repeats and drifts.
- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)
  — the evidence that position, not just size, shapes what a context
  window remembers.
- [How Claude remembers your project](https://code.claude.com/docs/en/memory)
  — a current example of instruction files plus auto-memory as the
  two session-to-session surfaces.
- [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
  — how Codex discovers and layers project guidance before working.
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  — a wider view of context as a finite resource to be curated.
- [Cool URIs don't change](https://www.w3.org/Provider/Style/URI.html)
  — why stable identifiers matter for any memory that lives in files
  and links.

The platform pages above change; the links were reachable when this
article was written in September 2026. None of this makes an agent
remember everything. It makes the places where it remembers easier
to see — and the next forgotten thing a little less mysterious.