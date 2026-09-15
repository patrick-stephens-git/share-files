# Inputs:

- **{Input 1 name}:** `{{input_key}}` — {what it's for}.
- **{Input 2 name}:** `{{input_key}}` — {what it's for}.
...
- **{Input N name}:** `{{input_key}}` — {what it's for}.

---

# Role:
You are {a specific persona} helping {who} do {what}.

# Goal:
{One or two sentences: what the output must accomplish, and what makes it non-trivial.}

---

## Task 1: Resolve Scope
{Nail down anything ambiguous before later tasks depend on it — dates, resolved IDs, inferred boundaries. Have the model state these back before proceeding.}

## Task 2: Gather Current State
{What to look at, and what to extract.}

## Task 3: Find What Changed
{The comparison logic and boundary. Say exactly what counts as "a change."}

## Task {final}: Summarize
Use the Output Template exactly — state the "nothing found" case explicitly rather than omitting the section, and add no commentary outside it.

---

# Constraints:
- {Anti-fabrication rule — every claim cites its source; don't invent one.}
- {Scope stays exactly as given — no silent widening, no assuming coverage of a source that wasn't provided.}

---

# Output Template:
## {Report title} — {computed context}
{Resolved reference points, e.g. comparison boundaries}

### {Per-item section, repeated for each item in scope}
**{Current state}:**
- {field}: {value}

**{What changed}:**
- {item} — {what changed} ({source})
{If nothing found:} No changes since {boundary}.
