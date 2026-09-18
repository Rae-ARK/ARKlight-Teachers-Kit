# Overview

## What Noah is

Noah is a teaching assistant designed to help a student understand a
concept — not just answer their question. It's the companion project
to [ARKlight](https://github.com/Rae-ARK/ARKlight), built as a real
application on top of it: Noah owns the teaching logic and the
student model, and ARKlight generates its UI, the same relationship
any other ARKlight site has to the compiler.

Noah is **not** a new compiler project. It is not intended to grow
into a large AI platform, agent framework, orchestration system, or
general-purpose educational SaaS unless that's explicitly decided
later. If a Noah problem starts to look like it needs a compiler
change, the default answer is "work around it in the application,"
not "extend ARKlight."

## Why this project exists

Noah exists partly as a break from compiler work — something smaller
and more contained to work on occasionally, for stress relief, rather
than a full-time commitment. That's a real constraint on scope, not
just flavor text: see `SCOPE.md` for what that means concretely, and
resist expanding infrastructure before the current interaction is
genuinely useful.

## Relationship to ARKlight

Conceptually:

```
Noah
  |-- Lesson UI
  |-- Explanation UI
  |-- Example UI
  |-- Exercise UI
  |-- Feedback UI
  `-- Progress UI
         |
         v
      ARKlight
         |
         v
      Generated UI
```

Noah is a real application built with ARKlight — it uses ARKlight's
component/state/behavior model the way any other project would, and
its domain components (`Lesson`, `Question`, `CodeExercise`, `Hint`,
`ConceptMap`, `Progress`, ...) are things to build *with* ARKlight,
not additions *to* it.

**Important:** ARKlight is still an evolving project, and its own
docs are the source of truth for its current API and architecture —
not this repo's notes, which can drift. When implementing something
that needs current ARKlight knowledge, check the actual ARKlight
repository/docs rather than relying on memory of an earlier version.
ARKlight's `alpha` branch specifically matters whenever "alpha
branch" is mentioned explicitly — don't silently substitute `main`
for it.

## Development priorities

In order:

1. Correct educational behavior
2. Simple architecture
3. Maintainability
4. Performance
5. Cleverness

Implementation decisions should still be technically sound even at
small scale — "the framework will handle it" isn't an architectural
explanation. When performance matters, reason from concrete things
(data structures, memory layout, allocations, control flow, locality,
concurrency, generated code, I/O), not vibes.
