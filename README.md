# Research With Receipts

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

## Download and install

- **[Download the skill ZIP](https://github.com/innovaitionpartners/agency-research/releases/latest/download/research-with-receipts.zip)** for skill upload or manual installation.
- **[Download the Claude plugin ZIP](https://github.com/innovaitionpartners/agency-research/releases/latest/download/agency-research-plugin.zip)** for plugin installation.
- [All releases and SHA-256 checksums](https://github.com/innovaitionpartners/agency-research/releases/latest).

For Claude Cowork, upload `research-with-receipts.zip` through its skill settings. For Claude Code or Codex, extract the skill ZIP and copy the enclosed `research-with-receipts` folder into your skill directory (`~/.claude/skills/` or `~/.agents/skills/`). Restart or refresh the host to discover the skill.

To try the plugin in Claude Code, extract the plugin ZIP and run `claude --plugin-dir /absolute/path/to/extracted-plugin`. The repository also includes Codex plugin metadata; the skill ZIP provides a direct manual-install option for Codex.

Requires an agent host with live web search, page retrieval, filesystem access, and Python 3. Bundled validators use only the Python standard library. The skill needs no API keys of its own; host subscriptions and web-tool access are separate. Browser automation and parallel agents are optional capabilities.

Try: “Use Research With Receipts to compare these three options using current public evidence.” Choose a Quick scan, Standard brief, or Deep report when prompted.

The validators check source records, citation formatting, and report structure. They cannot prove that a source is truthful or that it supports a claim; the researching agent must inspect the evidence.

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

## Build release packages

Run `python3 scripts/package_plugin.py` to create deterministic, versioned ZIPs and stable download aliases in `dist/`, plus `SHA256SUMS.txt`. Packages include the runtime and MIT license. Maintenance docs, tests, and build tooling stay in the repository.

## License

[MIT](LICENSE). Copyright 2026 InnovAItion Partners.
