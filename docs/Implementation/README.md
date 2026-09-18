# Implementation

## Overview

Records for work that's moved past "should we?" and into "here's
what happened when we tried." Borrowed directly from
[ARKlight's own `docs/Implementation/`](https://github.com/Rae-ARK/ARKlight/blob/alpha/docs/Implementation/README.md),
scaled down the same way the rest of this doc tree is.

## Why this is separate from `docs/Proposals/` and `docs/Foundational/`

Three different states, three different folders:

- **`docs/Proposals/`** — *unsettled*. An idea, not yet tried.
- **`docs/Implementation/`** (here) — *accepted, in progress*. Someone
  decided to actually try it. A file here is a log of what was set
  up, what worked, what broke, and what's still open — not a polished
  writeup, a working record.
- **`docs/Foundational/`** — *settled and permanent*. Once something
  here is actually working end-to-end and the decisions in it are
  final, fold what's still true into the relevant `Foundational/` doc
  and trim or remove the file here.

Noah is small and worked on occasionally — this folder exists so an
in-progress experiment survives between sessions instead of living
only in someone's memory or a chat transcript.

## What belongs here

- A log of an accepted idea actually being built/tried: what was
  installed, what config was needed, what failed and why, what's
  confirmed working, what's still blocked.
- Concrete findings — exact error messages, exact versions, exact
  commands — not vibes. Future-session-you (or a contributor) should
  be able to pick this up without re-discovering the same dead ends.

## What doesn't

- An idea nobody has started on — that's `docs/Proposals/`.
- A finished, settled design decision — that's `docs/Foundational/`.

## Index

| File | Covers |
| --- | --- |
| [`MINICPM5-1B-INTEGRATION.md`](MINICPM5-1B-INTEGRATION.md) | Using MiniCPM5-1B (via `llama.cpp`/GGUF) as the model backing Noah's `evaluate`/`hint` teaching actions. Environment setup log, what broke, what's confirmed working, what's still blocked, and early findings on 1B-scale limitations specific to Noah's teaching-loop requirements. |

## Contributing

Update the file in place as the experiment progresses — this is a
living log, not a one-shot report. Once something here actually works
end-to-end, fold the lasting decisions into `Foundational/` (likely
`DATA-MODEL.md`'s "AI model role" section) and trim this down to
history, or remove it, the same "graduate or remove" rule
`docs/Proposals/` uses.
