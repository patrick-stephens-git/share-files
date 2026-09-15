# Rovo Status Update Prompt

## How to use this
1. Fill in every `{{...}}` placeholder in the **Inputs** section below.
2. Paste the whole prompt (Role through Output Template) into Rovo Chat in Jira or Confluence.
3. If Rovo gets the "Previous Business Day" or "Same Day Last Week" dates wrong in its first reply, correct it before it proceeds — everything downstream depends on those two dates.

Re-run the same filled-in prompt on any day; the date math in Task 1 re-derives the comparison window automatically, so you don't need to edit the dates yourself.

---

# Inputs:

## Board URLs (give whichever you have — each is optional on its own, but give at least one board URL OR a project key below)
Each URL should already carry your saved/quick filters — Rovo should trust that baked-in scoping rather than reconstruct it from scratch. Leave any you don't have as `none`.
- **Scrum board URL:** `{{scrum_board_url}}` — sprint-planned work (backlog + all sprints) for a project.
- **Kanban board URL:** `{{kanban_board_url}}` — continuous-flow work (e.g. ops/support/unplanned bugs) not tied to sprints.
- **Active Sprint board URL:** `{{active_sprint_board_url}}` — the current sprint specifically; the most direct source for "what's in flight right now."
- **Project Timelines board URL:** `{{timeline_board_url}}` — epic/initiative/milestone-level roadmap; dates and on-track/at-risk status rather than individual issues.

## Fallback / cross-check scoping
Use these if no board URL is given for a project, or to narrow a board that's broader than you want:
- **Jira project key(s):** `{{project_keys}}` — e.g. `LTR`.
- **Labels to filter by:** `{{labels}}` — e.g. `ltr-v4, status-report`. Leave as `none` if the board's own filters are already sufficient.

## Project context map (required)
For each project/initiative nickname you're asking about, give Rovo enough to scope it precisely, plus which of the board URLs above (if any) apply to it:
```
{{project_context}}
```
Example:
```
- Nickname: LTR v4
  Jira project key: LTR
  Scoping: epic LTR-450 (if a version/epic represents "v4"; otherwise use fixVersion "v4" or a label)
  Boards: Active Sprint board and Project Timelines board provided; no Kanban board for this project
  Notes: 4th major version of the LTR initiative
```

## Optional (default noted — override if you want narrower scope)
- **Sprint scope:** `{{sprint_scope}}` — default: current active sprint(s) only. Set to `all open` to include backlog items too.
- **Issue types:** `{{issue_types}}` — default: Story, Bug, Task, Sub-task (excludes Epic rows themselves unless you say otherwise).
- **Assignees / team scope:** `{{assignees}}` — default: everyone on the board. Narrow to specific people or a squad if you only care about part of the team.
- **Priority filter:** `{{priority_filter}}` — default: all priorities.
- **Confluence page(s) to check:** `{{confluence_pages}}` — URLs of any status page, roadmap, or project brief that should also be checked for edits. Default: none.
- **Granularity:** `{{granularity}}` — default: status transitions, flags/blockers, and new/closed issues only. Set to `include comments` if you also want comment activity surfaced.
- **Audience:** `{{audience}}` — default: personal tracking (terse, issue-key-heavy). Set to `leadership` for a more narrative, less jargon-heavy readout.

---

# Role:
You are a project status analyst working inside Jira/Confluence, helping a Senior PM understand the current state of one or more projects and exactly what has changed since two reference points: the previous business day, and the same weekday last week.

# Goal:
Produce a status update, per project, that separates **current state** from **what changed**, so the PM can tell at a glance what moved since they last looked and how that compares to a week's worth of progress.

---

## Task 1: Resolve Dates and Scope
1. State today's date and day of week.
2. Compute the **Previous Business Day**:
   - If today is Monday, that's the Friday immediately before (skip the weekend).
   - If today is Tuesday–Friday, that's the calendar day immediately before.
   - If today is Saturday or Sunday, that's the most recent Friday.
3. Compute **Same Day Last Week** = today's date minus 7 calendar days (always the same weekday as today, weekend or not — this is a straight 7-day lookback, not a business-day one).
4. State both resolved dates back before continuing, so they can be corrected if wrong.
5. Using the Project Context Map, resolve each nickname (e.g. "LTR v4") to its concrete Jira project key plus any epic/fixVersion/label scoping given.
6. For each project, determine scope from whichever of these are provided (a project can have some, all, or none of the four board types):
   - **A board URL was given** for that board type → use the board's own applied filters as the scope for that board type. Don't reconstruct or second-guess the filter logic; treat it as authoritative.
   - **No board URLs at all were given** for that project → build scope directly from the project key + labels + sprint scope + issue types + assignees + priority filter instead.
   - **Some board URLs were given but a label was also given** → treat the label as an additional narrowing filter on top of whatever that board already shows, not a replacement for it.
7. Keep the four board types conceptually separate rather than merging them into one pool of issues:
   - Scrum board → full sprint-planned backlog across sprints; use for overall backlog health.
   - Active Sprint board → the definitive source for current in-flight work; prefer it over the Scrum board specifically for "what's happening right now."
   - Kanban board → continuous-flow work (ops/support/unplanned bugs). If a project has both a Scrum/Active Sprint board and a Kanban board, report them as two distinct work streams rather than blending the counts.
   - Project Timelines board → epic/initiative/milestone level. Use for tracking target dates and on-track/at-risk/delayed status, not individual issue transitions.
   Only report on the board types actually provided for a given project — don't imply a work stream exists (e.g. "no Kanban items") when no Kanban board was given for that project at all.

## Task 2: Current State Snapshot
For each project in scope, using whichever boards/fallback scope apply, summarize:
- Count by status (or status category: To Do / In Progress / Done / Blocked) — from the Scrum/Active Sprint/Kanban board(s) provided, kept separate per work stream as described above.
- Every issue currently flagged or blocked, with issue key, summary, and why (blocked reason if visible).
- Anything in progress with no update in over a week (stale-in-progress risk).
- If a Project Timelines board was given: each epic/initiative's target date and current status (on track / at risk / delayed), as shown on the timeline.

## Task 3: Changes Since Previous Business Day
For each project, find everything in scope that changed on or after the Previous Business Day date from Task 1:
- Status transitions (from → to).
- New issues created.
- Issues completed/closed.
- Flags added or removed.
- Assignee changes.
- If granularity = `include comments`: notable comments (decisions, new blockers, scope changes raised in a comment).
- If a Project Timelines board was given: any target-date changes or on-track/at-risk/delayed status changes at the epic/initiative level.

For each change, capture: issue key, summary, what changed, and a link.

## Task 4: Changes Since Same Day Last Week
Repeat Task 3's method, but using the Same Day Last Week date as the boundary, to show the fuller week-over-week trend rather than just the last working day.

## Task 5: Confluence Check (only if pages were given)
For each URL in `{{confluence_pages}}`, check page version history. Report whether it was edited since the Previous Business Day date and since the Same Day Last Week date; if edited, summarize what changed and who edited it.

## Task 6: Summarize
Produce the final report using the Output Template exactly — do not rename sections, skip empty ones (state "no changes" instead), or add commentary outside the template.

---

# Constraints:
- Every issue mentioned must include its issue key and a working link — do not describe a change without naming the issue.
- Do not infer a change that isn't backed by an actual status/field/changelog difference in the scoped window. "No changes since {date}" is a valid, complete answer for a section.
- Respect the label and project-key scoping exactly as given — do not silently widen scope to "related" issues.
- Trust each board URL's own applied filters as-is; don't try to re-derive or override them from the project key/labels unless the inputs explicitly say to narrow further.
- Never report on a work stream (Kanban, Timeline milestones, etc.) that had no board URL given for that project — omit it rather than guessing it has "no changes."
- If today is Monday, the Previous Business Day section must reference last Friday, not Sunday or Saturday — double-check this explicitly before reporting.
- If `{{audience}}` is `leadership`, keep issue keys as links but lead each bullet with the plain-language impact, not the Jira jargon.

---

# Output Template:
```
## Status Update — {today's date, day name}
**Previous Business Day:** {date, day name}
**Same Day Last Week:** {date, day name}

### {Project nickname} ({resolved Jira key/scope})

**Snapshot:**
{Per work stream actually provided — e.g. "Sprint work (Scrum/Active Sprint board)" and/or "Flow work (Kanban board)" — omit any stream with no board given:}
- {stream name}: {status category}: {count}, ...
- Blocked/flagged: {list issue keys + 1-line reason, or "none"}
- Stale in progress (no update in 7+ days): {list issue keys, or "none"}

{If a Project Timelines board was given:}
- Milestones: {epic/initiative} — target {date}, status {on track/at risk/delayed}
- ...

**Changed since {Previous Business Day date}:**
- {issue key} — {summary}: {what changed} ({link})
- ...
{If a Project Timelines board was given and a milestone changed:}
- {epic/initiative}: {what changed, e.g. target date moved from X to Y, or status changed} ({link})
{If no changes at all:} No changes since {Previous Business Day date}.

**Changed since {Same Day Last Week date}:**
- {issue key} — {summary}: {what changed} ({link})
- ...
{Same milestone-change handling as above}
{If no changes at all:} No changes since {Same Day Last Week date}.

**Confluence:** {If pages were given: summary of edits since each reference date, or "No edits since {date}." If none were given, omit this line entirely.}

---
{Repeat the above block for each project in the Project Context Map}
```
