# Research With Receipts Eval Results

## 2026-08-28 — Agency Research standalone plugin migration

Research With Receipts moved from the shared always-on InnovAItion Partners skill registry into the standalone public `agency-research` repository. The skill description was preserved exactly, while internal `answer slots` terminology became a flexible `coverage plan` that follows the requested deliverable rather than forcing reports into question-and-answer form. Claude and Codex plugin manifests validate, Skill Creator validation passes, and the complete deterministic fixture suite passes from repository-local paths. The active copies were removed from Sally's Claude, Codex, and Agent skill registries; maintainers test through an explicit path or isolated plugin session.

## 2026-08-28 — Reader-first substance correction

An immediate Claude Standard run exposed a thin, repetitive report: two core evidence lineages were recycled across the answer, statistics crowded out qualitative insight and practices, citations interrupted the prose, and the skill silently selected the depth. Runtime commits `8728629` and `ec0e944` now ask for depth when effort is materially ambiguous, require a broad Standard landscape to map at least five material answer slots and use at least five distinct usable sources across at least three source types unless it reports a real evidence shortfall, and require a question-appropriate mix of quantitative and qualitative evidence. A bundled reader-first output contract uses familiar language, descriptive sections, substantive bullets, and parenthetical receipts after the supported sentence or bullet. The output validator mechanically rejects non-parenthetical receipt syntax and broad-landscape ledgers with fewer than five admitted sources, five evidence lineages, or three source types unless a written breadth exception is paired with an explicit gap. Semantic receipt placement, honest lineage labeling, and evidence usefulness remain final-review judgments. Skill Creator validation, JSON validation, diff checks, and the full deterministic fixture suite pass, including positive and negative breadth-gate regressions.

## 2026-08-28 — Primary-source access fallback

Added a controlled Standard-depth regression for the agency-adoption failure: the original report times out through the initial fetch route while a distinct browser route remains available. The runtime now requires at most one direct retry before switching routes, records `Access escalation`, treats repeated articles as one evidence lineage, and preserves claims dependent on an unseen original as gaps. The deterministic suite passes, including rejection of a record missing the new field. A fresh-context test returned `PASS`: it tried distinct access routes and official alternate endpoints, rejected three repeating secondary articles, used accessible first-party material only for what it established, and retained the unavailable methodology as an explicit gap.

## 2026-08-28 — Ultra 9/10 remediation

The Ultra audit scored the source-gated runtime 9/10. Approved remediation added exact enforcement for angle-wrapped parenthesized URLs, one visible insufficiency disclosure per ledger gap, a visible epistemic label for every supported non-fact kind used by the ledger, substantive required sections that ignore comments and empty fence markers, absolute artifact paths, reserved non-public hosts, and clean UTF-8 read failures. A single epistemic heading may scope several claims; semantic correspondence remains a final-review judgment. The behavioral manifest now conforms to the canonical Skill Creator schema, and protocol limits use named documented constants. Positive and adversarial engine fixtures pass. A fresh independent settled audit returned `PASS` with no remaining concrete finding.

## 2026-08-28 — Deterministic source-admission gate

Added a strict candidate-source ledger and a pre-synthesis validator. The gate now hard-fails mechanical contract violations before drafting, while the final validator rejects citations not approved as `use` and metadata that differs from the ledger. Valid Quick, Standard, Deep, honest-insufficiency, month-precision date, parenthesized-URL, escaped-bracket-title, and public-IP fixtures pass. Dedicated negative fixtures prove rejection of search pages, queried homepages, excluded types, unopened or inaccessible evidence, date and scope mismatch, boundary-ambiguous partial dates, supersession, malformed or non-public direct URLs, unrepresentable metadata, missing evidence or scope records, canonical duplicate URLs, unsupported claim links, unapproved final citations in alternate syntaxes, and altered citation metadata. Semantic support remains a researcher-owned judgment.

**Runtime commit:** `27c16a31f8fd5cd7df10ba9932b739cd666a5ac4`

**Independent adversarial review:** PASS after four hardening rounds. The reviewer verified partial-date intervals, public/private host handling, canonical duplicate detection, malformed-schema failures, final citation binding, and the explicit semantic-validation boundary.

**Run date:** 2026-08-28

**Initial runtime commit:** `38437a965d848d2d774f10dd119c78371ee86eb7`

**Post-fix runtime commit:** `c52d00e80d141d99684a629edcb553becd7506aa`

**Scope-intake follow-up commit:** `d4050c2a5543155f6386fb97ca323c577d251188`

The follow-up makes date range, geography/jurisdiction, and source-type policy explicit before Standard or Deep retrieval and adds those fields to the validated execution record. Quick retains a materiality gate to avoid needless intake friction. Validator fixtures and structural gates passed; the canonical behavioral cases were updated to cover this contract.

**Post-fix runtime branch:** `codex/research-with-receipts-ultra-fixes`

## Post-fix Ultra regression

Five fresh-context evaluators received the revised runtime path and one canonical case each. Four cases used live public-web retrieval; the supplied-source routing case did not browse. No evaluator modified either repository.

| Case | Result | Evidence |
|---|---|---|
| Quick current policy | PASS | Opened two official Slack Help Center pages, distinguished the 90-day visibility rule from configurable deletion, completed the execution record, and passed the validator. |
| Standard product comparison | PASS | Used current first-party Otter and Zoom evidence, preserved plan limitations and gaps, ran a disconfirming route, labeled the recommendation as inference, and passed with one reviewed insufficiency warning. |
| Deep staged investigation | PASS | First response contained only the Research Frame; the approved run used official sources, documented conflicts and gaps, completed the critical recheck, and passed the validator. |
| Insufficient public evidence | PASS | Distinguished net-fee figures and payroll-defined headcount from audited revenue, stated the remaining insufficiency, documented disconfirming routes, and passed with the expected insufficiency warning. |
| Supplied-source routing | PASS | Routed by capability, requested the draft and PDFs, preserved the no-web boundary, and did not name a sibling skill. |

Both independent post-fix reviewers completed successfully. The craft review found decision-enabling support for all 14 workflow steps. The enforcement review found no semantic verdict incorrectly assigned to code; its remaining exact-template observation was closed by enforcing one depth line, the Deep report title, allowed level-two headings, required heading order, and regression fixtures.

## Initial deployment summary

Five independent evaluators received only the runtime skill path and a realistic request. Research cases used the live public web. The evaluators did not receive the design specification, eval rubric, intended answer, or parent conclusions.

| Case | Final result | Evidence |
|---|---|---|
| Quick authoritative answer | PASS | Distinguished Slack's 90-day access limit from retention; used opened official pages, exact source metadata, direct adjacent links, and the required Quick/Answer/Limits shape. |
| Standard comparison | PASS after two revisions | Reconciled Otter and Zoom policy conflicts, preserved unavailable plan/backup answers, labeled inference and judgment, and placed supporting links beside every recommendation. |
| Deep multi-lane investigation | PASS after one revision | Used primary laws and official guidance across jurisdictions, separated current from 2027 duties, preserved rulemaking and access gaps, traced each recommendation to evidence, and justified the stop. |
| Inadequate evidence | PASS after one formatting revision | Said `No adequate source found` for the exact small-U.S.-agency statistic; treated 30% only as an explicitly limited proxy and explained the gated primary report. |
| Supplied-source routing | PASS after one revision | Explicitly identified the request as supplied-source fact-checking, routed to `fact-checker`, and requested the missing files without browsing as a substitute. |

## Observed failures and fixes

1. **Silent neighboring-skill imitation:** The first routing run requested attachments without explaining that the work belonged to supplied-source fact-checking. The routing rule now requires the distinction before input collection.
2. **Template drift:** Early standard and insufficiency runs renamed or omitted required sections and added trailing tool notes. The skill now requires the depth template exactly and places access limitations inside the appropriate limits/gaps section.
3. **Uncited recommendations:** Early standard and deep outputs labeled recommendations as inference but did not consistently put source links beside each recommendation. The templates and final check now require adjacent evidence for every recommendation.

## Static and security gates

- Skill Creator `quick_validate.py`: PASS.
- Ultra structural rules, reference-depth, and script-wiring diagnostics: PASS.
- Output validator fixtures: PASS for Quick, Standard, Deep, and honest insufficiency; expected failures for search-result links, invalid dates, and unapproved level-two sections.
- Canonical `evals/evals.json`: valid JSON with five behavioral cases.
- `git diff --check`: PASS.
- Private-path/client/example scan: PASS; zero hits.
- Cisco AI Skill Scanner: `SAFE`, zero critical/high findings.
  - Medium: `agents/openai.yaml` detected as textproto rather than YAML. This is a scanner false positive on the standard generated OpenAI metadata shape.
  - Info: no public license declared. Licensing is intentionally held for Sally's pre-release decision rather than inferred during the build.

## Limitations

- Live facts and source availability will change; these evals test behavior and evidence fit as of the run date, not permanent conclusions.
- The public distribution ZIP and landing-page copy do not exist yet.
- No Suits variant or Suits-runtime test was attempted for V1.
- The initial runtime is deployed. The Ultra remediation remains on isolated local branches until Sally separately authorizes push/merge.
