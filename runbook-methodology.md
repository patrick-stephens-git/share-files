---
name: runbook-methodology
description: Apply this skill when the user is creating a runbook or any multi-step procedure where the LLM needs input from the user or produces output the user must review before moving on. The two core use cases are: (1) collecting input from the user one question at a time, and (2) presenting LLM-generated output for user review and approval before advancing to the next step.
version: 1.0.0
---

# Runbook Methodology

Two rules govern every runbook you build with this skill. They apply whenever you need input from the user and whenever you produce output the user should review.

---

## Rule 1 — One Input at a Time

**Ask one question per message. Never ask multiple questions at once.**

One input means one decision for the user to make. Presenting three options for the user to choose *one* from is a single input — that's fine. Asking three separate questions and expecting three separate answers in one message is not.

**Wrong — three separate questions bundled together:**
> "What is the name of the runbook? Who is the audience? What systems are involved?"

**Right — one question, then wait:**
> "What is the name of this runbook?"

Wait for the answer. Then ask the next question.

**Also fine — one question with multiple options:**
> "Who is the primary audience for this runbook?
> - `engineering` — on-call engineers responding to incidents
> - `ops` — operations team running deployments
> - `both` — applies to both audiences"

This is still one input: the user makes one choice.

If the user volunteers information that answers upcoming questions, acknowledge it and skip those questions — don't ask something you already know.

---

## Rule 2 — Review Gate After Every Output

**After producing any output the user needs to evaluate — a draft, a section, a plan, a list — always pause and present a review gate before advancing.**

Never proceed to the next step without explicit user confirmation.

### The Review Gate

Present the following block **verbatim** after each output. Substitute `[output description]` with a one-phrase label for what was just produced (e.g. "the scope outline", "Step 3", "the full draft"):

---

> "Here is [output description]. What would you like to do?
>
> - `confirm` — looks good, proceed to the next step
> - `refine` — I'll give you feedback to apply before moving on
> - `regenerate` — discard this and produce a new version from scratch
>
> Enter your selection:"

---

### Handling Responses

- **`confirm`** — proceed to the next task or step.

- **`refine`** — apply every change the user requests. Re-display the full updated output. Re-present the review gate. Repeat until the user confirms.

- **`regenerate`** — discard the current output and re-produce it from scratch. Re-display and re-present the review gate.

- **Freeform instructions** — treat as `refine`. Interpret the user's intent, apply the changes, re-display, and repeat the review gate.

### Warning Before Applying a Destructive Refinement

If a requested refinement would remove or break something that another part of the runbook depends on, **warn the user before applying**:

> "Heads up: removing [X] would affect [Y downstream dependency]. Want to proceed anyway, or adjust the request?"

Wait for confirmation before applying.

---

## Applying Both Rules Together

When building a runbook step by step, the flow looks like this:

1. Ask one question to collect the input needed. Wait for the answer.
2. Ask the next question if more input is needed. Wait for the answer.
3. Produce output for the current step.
4. Present the review gate.
5. Handle the response (confirm → advance; refine/regenerate → loop).
6. Repeat from step 1 for the next step.

The user always moves the process forward. Never advance on your own.
