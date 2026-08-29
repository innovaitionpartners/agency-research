# Agency Research

Agency Research is an InnovAItion Partners plugin for readable, source-verified public-web research. Its first bundled skill, **Research With Receipts**, supports quick checks, standard briefs, and deep reports while keeping citations beside the claims they support.

## What it does

- Opens and checks every cited page.
- Prefers applicable primary or authoritative sources.
- Distinguishes sourced facts from inference, estimates, anecdotes, and uncertainty.
- Escalates to another available browser route before treating an identified original source as inaccessible.
- Prevents repeated coverage of one underlying study from masquerading as independent corroboration.
- Produces reports shaped around the user's purpose: themes, chronology, comparisons, cases, practices, findings, recommendations, or direct questions.
- States `No adequate source found` when public evidence cannot support a requested claim.

## Included skills

- `research-with-receipts` — adaptive public-web research with claim-adjacent, parenthetical receipts.

The skill's trigger description is intentionally broad for isolated product testing. Maintainers should test from this repository or an isolated plugin session rather than installing it in a personal always-on skill registry.

## Local testing

Validate the skill and plugin:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/research-with-receipts
python3 /path/to/plugin-creator/scripts/validate_plugin.py .
bash tests/run-fixtures.sh
```

Test in Claude Code for one session without installing it globally:

```bash
claude --plugin-dir /absolute/path/to/agency-research
```

For agent-based testing, give the evaluator the absolute path to `skills/research-with-receipts/SKILL.md`. Do not symlink this repository into a maintainer's active skill directory.

## Repository layout

```text
agency-research/
  .claude-plugin/plugin.json
  .codex-plugin/plugin.json
  skills/research-with-receipts/
  evals/
  tests/
  docs/
```

## Controlled packaging

Use `python3 scripts/package_plugin.py` to create `dist/agency-research.zip` for private testing or a specifically approved controlled deployment. The package contains the dual-platform manifests, README, and runtime skill only; maintenance docs, tests, and build tooling stay in the repository. This repository and its packages are not approved for public release or external distribution.
