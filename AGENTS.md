# Agency Research

This public repository is the source of truth for the open-source **Agency Research** plugin from InnovAItion Partners, including **Research With Receipts**. It is distributed under the MIT license.

## Product boundary

- Plugin and repository name: `agency-research`.
- Product name: **Agency Research**.
- First bundled skill: `research-with-receipts`.
- Preserve the skill's frontmatter description unless a deliberate trigger redesign is approved.
- This is a standalone open-source product, not Sally's personal research skill. Do not install or symlink it into `~/.agents/skills/` or `~/.codex/skills/` for routine development.
- Test through an explicit repository path, `claude --plugin-dir`, a temporary plugin profile, or a fresh-context evaluator.

## Runtime and maintenance separation

- Runtime skill files live under `skills/<skill-name>/`.
- Behavioral evals and deterministic fixtures live at repository root under `evals/` and `tests/`.
- Maintainer lessons and product specifications live under `docs/`.
- Generated caches, temporary ledgers, reports, and packaged ZIPs do not belong in source control.

## Research output rule

`Coverage plan` is internal planning language. It may use themes, chronology, comparisons, cases, practices, findings, recommendations, or questions. Never force a research report into question-and-answer form or expose internal planner terminology as the user's deliverable structure.

## Quality gate

Every material change must pass:

1. Skill Creator validation for each bundled skill.
2. Plugin manifest validation.
3. The complete deterministic fixture suite.
4. Behavioral eval review or a fresh-context test proportional to the change.
5. Ultra Skill Optimizer for material architecture changes.
