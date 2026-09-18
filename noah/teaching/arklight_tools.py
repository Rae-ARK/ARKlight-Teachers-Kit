"""Tool-call wrappers around the ARKlight CLI, for grounding the model
that drives Noah's teaching actions.

Why this exists: `Foundational/OVERVIEW.md` is explicit that ARKlight
is still evolving and its own docs/CLI are the source of truth for its
current API -- "check the actual ARKlight repository/docs rather than
relying on memory of an earlier version." A 1B model has exactly zero
memory of anything past its training data and, per
`docs/Implementation/MINICPM5-1B-INTEGRATION.md`, weaker
instruction-following than larger models -- so letting it *guess* at
ARKlight's component API or CLI flags is a bad combination. These
wrappers give it a way to look the real thing up live instead,
via `arklight search` and `arklight <subcommand> --help`, matching
`DATA-MODEL.md`'s "AI model role" principle (structured, validated
grounding around the model, not trust-the-model-output-as-is).

**Scope note, worth reading before wiring this into a harness:**
Noah's actual teaching subject (`Foundational/SCOPE.md`'s first
concept, `variables`) is general programming fundamentals, not
ARKlight itself. These tools are grounding for anything
ARKlight-shaped that comes up -- e.g. if a later concept touches UI
components, or if this is used for Noah's own development rather than
its student-facing teaching loop -- not something the `variables`
lesson's `evaluate`/`hint` harness needs. Don't wire these into that
harness's tool list by default; add them only for a teaching action
that actually needs ARKlight-specific grounding.

Verified against ARKlight alpha (arklight 0.641) in
`docs/Implementation/MINICPM5-1B-INTEGRATION.md`'s environment. Two
integration gotchas found there and handled here:

1. Every functional `arklight` subcommand (not `--help`) requires
   license acceptance -- either accepted once interactively, or
   `ARKLIGHT_ACCEPT_LICENSE=1` in the environment. `--help` itself
   does not need this. Read `ARKlight/LICENSE` before setting this in
   a real deployment; it's baked in here as a constant specifically so
   it's one visible place to revisit, not scattered through call
   sites.
2. `arklight search` exits 0 whether it's a hit or a miss -- a miss is
   still `returncode == 0` with "No component named ... Did you mean"
   on stdout. Do not use the exit code to detect success; these
   wrappers check stdout content instead.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass

# See docstring point 1. Sourced from ARKlight/LICENSE (GPLv3 +
# additional terms) -- revisit this constant, not call sites, if that
# ever needs to change.
_ARKLIGHT_ENV = {"ARKLIGHT_ACCEPT_LICENSE": "1"}

# Doc-tree retrieval can return tens of KB of prose (measured: ~18KB
# for the bare index, ~22KB for a single Foundational file with
# --file). That's fine for MiniCPM5-1B's 131K context in principle,
# but dumping that much text at once into a 1B model's context is a
# real risk on its own -- weaker instruction-following means more
# context isn't free, it's more chances to get pulled off task. Cap
# what a single tool call can return and let the model ask again with
# a narrower query rather than handing it everything at once.
_MAX_DOC_CHARS = 4000


@dataclass
class ToolResult:
    ok: bool
    text: str


def _run(args: list[str], *, needs_license: bool = True) -> subprocess.CompletedProcess:
    # subprocess.run's env= REPLACES the whole environment, not merges
    # it -- passing just _ARKLIGHT_ENV loses PATH and 'arklight' stops
    # resolving at all. Found by actually running this, not by
    # inspection; worth leaving this comment so it doesn't regress.
    env = {**os.environ, **_ARKLIGHT_ENV} if needs_license else os.environ
    return subprocess.run(
        ["arklight", *args],
        capture_output=True,
        text=True,
        env=env,
        timeout=15,
    )


def arklight_search_component(name: str, near: str | None = None) -> ToolResult:
    """Look up a built-in ARKlight component's schema by name.

    Returns required props / children rules on a hit, or a "did you
    mean" suggestion on a miss -- both come back as ok=True with the
    real CLI text, since a miss is still useful grounding (it tells
    the model the name it guessed doesn't exist, which is exactly the
    thing worth surfacing rather than silently correcting).
    """
    args = ["search", name]
    if near:
        args += ["--near", near]
    proc = _run(args)
    if proc.returncode != 0:
        return ToolResult(ok=False, text=proc.stderr.strip() or "arklight search failed")
    return ToolResult(ok=True, text=proc.stdout.strip())


_DOC_SECTION_FLAGS = {
    "foundational": "--foundational",
    "backends": "--backends",
    "proposals": "--proposals",
    "implementation": "--implementation",
    "js-backend": "--js-backend",
    "far-future": "--far-future",
    "version-history": "--version-history",
}


def arklight_search_docs(section: str | None = None, file: str | None = None) -> ToolResult:
    """Retrieve ARKlight's own doc-tree instead of a component schema.

    `section` must be one of `_DOC_SECTION_FLAGS`'s keys (omit for the
    root docs/README.md index). `file` narrows to one file within that
    section, matched case-insensitively by stem. Output is truncated
    to `_MAX_DOC_CHARS` -- if the model needs more than that, it
    should be asking a narrower question (a specific --file), not
    reading an entire folder index in one call.
    """
    args = ["search", "--retrieve-doc"]
    if section:
        flag = _DOC_SECTION_FLAGS.get(section)
        if flag is None:
            return ToolResult(
                ok=False,
                text=f"Unknown section '{section}'. Valid: {', '.join(_DOC_SECTION_FLAGS)}",
            )
        args.append(flag)
    if file:
        args += ["--file", file]
    proc = _run(args)
    if proc.returncode != 0:
        return ToolResult(ok=False, text=proc.stderr.strip() or "arklight search --retrieve-doc failed")
    text = proc.stdout.strip()
    if len(text) > _MAX_DOC_CHARS:
        text = text[:_MAX_DOC_CHARS] + f"\n\n[...truncated, {len(proc.stdout)} chars total. Ask for a narrower --file if you need more.]"
    return ToolResult(ok=True, text=text)


def arklight_help(subcommand: str | None = None) -> ToolResult:
    """Get real `arklight --help` / `arklight <subcommand> --help` text.

    Does not need the license env var (verified -- --help is exempt).
    Useful for grounding exact flag names/syntax rather than letting
    the model guess CLI shape from training data, which per
    `Foundational/OVERVIEW.md` may already be stale for an actively
    developed alpha project.
    """
    args = [subcommand, "--help"] if subcommand else ["--help"]
    proc = _run(args, needs_license=False)
    if proc.returncode != 0:
        return ToolResult(ok=False, text=proc.stderr.strip() or "arklight --help failed")
    return ToolResult(ok=True, text=proc.stdout.strip())


# JSON-schema tool definitions for the model's native tool calling
# (llama-cpp-python's create_chat_completion(tools=...), OpenAI-style
# schema -- MiniCPM5-1B's chat template renders these into its own
# native XML-style tool-call format under the hood).
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "arklight_search_component",
            "description": (
                "Look up a built-in ARKlight component's real schema (required "
                "props, whether it allows children) by exact or near name. "
                "Use before asserting anything about an ARKlight component's "
                "API -- do not guess from training data, ARKlight is an "
                "actively developed alpha project."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Component name, e.g. 'Button'."},
                    "near": {
                        "type": "string",
                        "description": "Optional: bias suggestions toward a component structurally close to this one.",
                    },
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "arklight_search_docs",
            "description": (
                "Retrieve a section of ARKlight's own documentation tree. "
                "Prefer arklight_help for CLI flag questions and "
                "arklight_search_component for component schema questions -- "
                "use this only for architecture/design-rationale questions "
                "those two don't cover. Result is truncated; ask again with a "
                "narrower `file` if truncated."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "section": {
                        "type": "string",
                        "enum": list(_DOC_SECTION_FLAGS),
                        "description": "Doc folder to read the index of. Omit for the root docs index.",
                    },
                    "file": {
                        "type": "string",
                        "description": "Optional: one file's full contents within that section, matched by stem.",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "arklight_help",
            "description": (
                "Get real `arklight --help` output for the top-level CLI or "
                "one subcommand (build, pack, unpack, pwa, android, desktop, "
                "new, search, live-streaming). Use before stating exact flag "
                "names/syntax."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "subcommand": {
                        "type": "string",
                        "description": "Optional: one subcommand name. Omit for the top-level --help.",
                    },
                },
                "required": [],
            },
        },
    },
]

TOOL_DISPATCH = {
    "arklight_search_component": arklight_search_component,
    "arklight_search_docs": arklight_search_docs,
    "arklight_help": arklight_help,
}
