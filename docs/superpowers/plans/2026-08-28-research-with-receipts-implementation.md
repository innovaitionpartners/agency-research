# Research With Receipts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and behaviorally validate a portable adaptive-research skill with an invariant claim-adjacent receipts contract.

**Architecture:** Keep the receipts contract, routing, depth selection, stopping rules, and output contracts in `SKILL.md`. Progressively disclose Standard/Deep search-lane craft and the optional researcher handoff in one focused file each. Ship a narrow standard-library validator for deterministic output surfaces; keep behavioral evals and validator fixtures in this maintenance sidecar.

**Tech Stack:** Markdown Agent Skill instructions, YAML UI metadata, live-web behavioral evaluation.

**Spec:** `research-with-receipts/docs/superpowers/specs/2026-08-28-research-with-receipts-design.md`

## Global Constraints

- Runtime source is the isolated `innovaition-partners-skills` worktree on branch `codex/research-with-receipts`.
- Do not edit the shared `~/.agents/skills` main checkout.
- Do not merge, push, or deploy without Sally's separate approval.
- Include no private InnovAItion Partners dependency or client-specific example.
- Depth and evidence rigor are independent; do not impose a single-question or fixed-source ceiling.
- Citation metadata and source-admission rules remain in `SKILL.md`, not an optional reference.

---

### Task 1: Scaffold the runtime skill

**Files:**
- Create: `/Users/sally/.codex/worktrees/research-with-receipts/research-with-receipts/SKILL.md`
- Create: `/Users/sally/.codex/worktrees/research-with-receipts/research-with-receipts/agents/openai.yaml`

**Interfaces:**
- Consumes: Approved design specification.
- Produces: Discoverable skill folder accepted by `quick_validate.py`.

- [ ] **Step 1:** Run the bundled `init_skill.py` initializer with the `research-with-receipts` name and no optional resource directories.
- [ ] **Step 2:** Replace scaffold text with the complete frontmatter, depth router, receipts contract, workflow, output shapes, boundaries, and final check from the design.
- [ ] **Step 3:** Set UI metadata to display name `Research With Receipts`, a 25–64 character description, and a default prompt explicitly invoking `$research-with-receipts`.
- [ ] **Step 4:** Run `quick_validate.py` against the runtime folder and fix every failure.

### Task 2: Add the behavioral evaluation contract

**Files:**
- Create: `research-with-receipts/tests/eval-cases.md`

**Interfaces:**
- Consumes: Runtime contract from Task 1.
- Produces: Five live-web cases with observable pass/fail criteria.

- [ ] **Step 1:** Define quick, standard, deep, insufficiency/conflict, and neighboring-skill routing cases.
- [ ] **Step 2:** Require live retrieval for research cases and prohibit fabricated frozen sources.
- [ ] **Step 3:** Map each design success criterion to at least one observable evaluation check.

### Task 3: Run quality gates and iterate

**Files:**
- Modify if failures justify it: `/Users/sally/.codex/worktrees/research-with-receipts/research-with-receipts/SKILL.md`
- Record: `research-with-receipts/tests/eval-results.md`

**Interfaces:**
- Consumes: Runtime skill and eval cases.
- Produces: Structural, security, and behavioral evidence supporting approval.

- [ ] **Step 1:** Run `quick_validate.py`, scan for private paths/client terms, and check all referenced files exist.
- [ ] **Step 2:** Run repository security scanning for the new skill or the narrowest supported equivalent.
- [ ] **Step 3:** Execute representative live-web behavior when an isolated evaluator is available; otherwise run a rigorous contract-based review and disclose the limitation.
- [ ] **Step 4:** Correct only observed failures, rerun affected checks, and record results with dates and limitations.

### Task 4: Commit and prepare maintainer handoff

**Files:**
- Modify: `CATALOG.md`
- Modify: `_skills-index.md`
- Modify: `research-with-receipts/AGENTS.md`

**Interfaces:**
- Consumes: Passing runtime and evaluation evidence.
- Produces: Two local commits and a no-deploy approval brief.

- [ ] **Step 1:** Add a private standalone-product entry to `CATALOG.md` and maintenance-sidecar entry to `_skills-index.md`.
- [ ] **Step 2:** Record the runtime commit SHA and evaluation status in `research-with-receipts/AGENTS.md`.
- [ ] **Step 3:** Commit runtime changes on `codex/research-with-receipts` and sidecar/catalog changes on the current isolated `12_Skills` worktree.
- [ ] **Step 4:** Verify both worktrees are clean and report exact paths, branches, commits, tests, and the maintainer action required. Do not push or merge.

### Post-deploy Ultra hardening

Previously contemplated after an initial public deployment; superseded by the decision to keep the product private:

- Replace sibling-skill naming with capability-only routing.
- Add a staged Deep Research Frame and approval gate, with an explicit advance-authorization bypass.
- Add search-lane construction/adaptation guidance and a worked planning example.
- Add a structured execution record and deterministic output validator without assigning semantic source verdicts to code.
- Add a portable optional research-lane brief.
- Convert the five behavioral cases to canonical `evals/evals.json` and retain validator fixtures under `tests/`.
