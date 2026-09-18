# Noah Documentation

This folder is the documentation index for **Noah** (`ARKlight-Teachers-Kit`)
— a small teaching assistant, built as a real application on top of
[ARKlight](https://github.com/Rae-ARK/ARKlight), maintained as an
occasional side project rather than a full-time one.

Start here, then follow the links below into the subfolder for what
you need.

## Philosophy

- **Noah is small on purpose.** This is a side project worked on
  occasionally, for stress relief — not a platform. Scope stays
  deliberately tiny (`Foundational/SCOPE.md`); resist the urge to
  add infrastructure before the current interaction is genuinely
  useful.
- **Teach, don't just answer.** Noah's whole point is the loop of
  explain → example → guided attempt → feedback, not a Q&A box
  (`Foundational/TEACHING-MODEL.md`).
- **Noah is an application, not a compiler extension.** It *uses*
  ARKlight to build its UI the same way any other ARKlight site
  would; it doesn't fork or extend the compiler
  (`Foundational/OVERVIEW.md`).
- **This documentation exists for onboarding.** The audience is
  beginners and first-time contributors — someone opening this repo
  for the first time should be able to find "what is this" and
  "where do I start" without digging through source or old chat
  context.

## Folder Guide

Borrowed from ARKlight's own `docs/` lifecycle model
([`ARKlight/docs/README.md`](https://github.com/Rae-ARK/ARKlight/blob/alpha/docs/README.md)),
scaled down to what Noah actually needs today. Three folders now —
`Implementation/` was added once the first real feature attempt
(MiniCPM5-1B integration) needed a home that was neither an untried
idea nor a finished design record; see "Adding a new doc" below for
when a new folder is actually earned.

### [`docs/Foundational/`](Foundational/README.md) — permanent

The core reading for understanding what Noah is, how it teaches, and
how it relates to ARKlight. Not deletable — this is the permanent
design record, updated in place rather than removed. Everything here
was migrated and organized from the project's original scratch notes
(`context.txt`, kept in the repo root for history).

### [`docs/Proposals/`](Proposals/README.md) — unsettled

Ideas for where Noah could go next — new concepts to teach, new
domain components, changes to the teaching loop — that haven't been
tried yet. Empty until there's an actual idea worth writing down;
see that folder's own README for the rationale and format.

### [`docs/Implementation/`](Implementation/README.md) — accepted, in progress

Working logs for accepted ideas actually being built/tried — what was
installed, what broke, what's confirmed, what's still open. Between
`Proposals/` (not yet tried) and `Foundational/` (settled); see that
folder's own README for the rationale and format.

## Adding a new doc

Same two checks ARKlight's own doc tree uses:

1. **Does this fact already have a home?** Search first
   (`grep -r` the term, or skim the tables in the folder READMEs). If
   it does, link to that file instead of restating it — copies drift
   the moment one gets updated and the other doesn't.
2. **Which folder matches this content's *state*?** Settled and
   permanent → `Foundational/`. An idea, not yet tried → `Proposals/`.
   If neither fits (e.g. Noah ships its first real feature and needs
   a staged rollout plan, or its first version-history entry), that's
   a sign a new folder is earned — add it then, following the same
   pattern, not preemptively.

When in doubt, keep it short and keep it friendly. The reader is
probably new here.
