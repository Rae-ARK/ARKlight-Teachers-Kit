# Data Model

Keep these as simple, deterministic shapes until there's a
demonstrated reason to introduce more complexity — no sophisticated
ML model needed for v0.1.

## Concept

```
Concept
    id
    name
    description
    prerequisites
    explanations
    examples
    common_misconceptions
    exercises
    hints
```

Example:

```
Concept:
    id: variables
    prerequisites: []
    explanation:
        "A variable gives a name to a stored value."
    examples:
        ...
    misconceptions:
        ...
    exercises:
        ...
```

## Student state

```
StudentState
    known_concepts
    uncertain_concepts
    failed_attempts
    misconception_hypotheses
    current_lesson
```

A useful way to represent per-concept confidence is a simple mapping:

```
concept -> confidence
```

e.g.

```
variables       -> high
functions       -> medium
recursion       -> low
```

This does not need to become a sophisticated model initially —
simple, deterministic state is preferable until there's a
demonstrated reason for more.

## AI model role

If an LLM is used anywhere in Noah, treat it as one component of the
teaching system, not the entire architecture. Prefer explicit
application state around the model rather than letting important
state live only inside a conversation:

```
Student Input
    |
    v
Teaching State
    |
    v
Teaching Decision
    |
    v
Model Prompt / Call
    |
    v
Structured Result
    |
    v
Teaching State Update
    |
    v
UI
```

Where practical, model outputs should be structured and validated
rather than trusted as-is.
