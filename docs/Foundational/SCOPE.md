# Scope

## v0.1: keep it extremely small

Initial capabilities:

- explain a concept
- provide an example
- ask a question
- generate a small exercise
- evaluate an attempt
- provide a hint
- summarize what was learned
- maintain minimal student state

## Explicitly out of scope (for now)

Do not build any of the following until there's a specific,
demonstrated reason to:

- multi-agent systems
- vector databases
- complex RAG pipelines
- autonomous agents
- plugin ecosystems
- elaborate analytics
- social features
- accounts/authentication, unless actually required
- distributed backend infrastructure
- elaborate persistence
- dozens of abstractions

No fixed directory structure is required yet, either — don't create
abstractions merely to make the tree look architectural. A rough
starting shape might be:

```
/noah
    concepts/
    lessons/
    teaching/
    student/
    ui/
    main.py
```

with each part doing roughly what its name suggests (concept
definitions, lesson sequencing, explain/hint/evaluate logic, student
state, ARKlight UI definitions) — but this is a starting point, not a
contract.

## First subject

Prefer starting with **one subject** rather than trying to teach
everything at once. Programming fundamentals are a natural first
choice: well-defined, easy to exercise interactively, and suitable
for structured concept dependencies. Candidate first concepts:

```
values, variables, types, expressions, conditionals, loops,
functions, data structures, recursion
```

Don't implement all of these immediately — start with a tiny concept
set (e.g. just `variables`) and expand once that one works well.

## First milestone

Something like: **"Noah can teach one programming concept from start
to finish."**

```
Concept: variables

Noah explains variables
    -> shows a tiny example
    -> asks a conceptual question
    -> gives an exercise
    -> student submits an attempt
    -> Noah evaluates it
    -> Noah gives a hint or correction
    -> Noah summarizes the concept
```

If that works well, expand to another concept. Don't expand
infrastructure before this interaction is genuinely useful.

## Success criteria

Noah succeeds if:

1. A student can learn something through it.
2. The interaction is better than simply reading an answer.
3. Noah can recognize common mistakes.
4. Noah can adapt its explanation.
5. The implementation remains small enough to understand.
6. ARKlight is actually useful for building the UI.

## Current mindset

This project exists partly as a break from compiler work — don't
turn every Noah problem into an opportunity to redesign ARKlight. If
a simple solution works, use it. The purpose is to explore
educational interaction, stateful assistance, structured knowledge,
adaptive explanation, and practical ARKlight usage, without creating
another large systems project.
