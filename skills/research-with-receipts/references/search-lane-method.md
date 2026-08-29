# Search-lane method

Use this method for Standard and Deep research. A lane is a distinct evidence route, not another wording of the same search.

## 1. Build a coverage plan for the requested deliverable

Map the material areas the final deliverable must cover. Choose the organizing logic that fits the user's request: themes, chronology, comparisons, cases, practices, findings, recommendations, or specific questions. For each area, specify the evidence that could support it and the scope that evidence must match: date, jurisdiction, population, definition, entity, or product version.

Apply the user's confirmed source exclusions before searching. Source type is not a quality verdict by itself: a press release or vendor page may be authoritative for the issuer's announcement or stated position but cannot independently verify its effectiveness, prevalence, or impact. When first-party incentives matter, pair the Authority lane with an applicable Application or Challenge lane.

## 2. Assign evidence lanes

Choose only the lanes that can change the answer:

| Lane | Purpose | Typical source targets |
|---|---|---|
| Authority | Establish the controlling or original fact | Statute, regulator, official dataset, filing, standard, original study, first-party documentation |
| Application | Show how the fact operates in the relevant setting | Implementation guidance, methods appendix, enforcement record, case study, transparent independent analysis |
| Challenge | Seek a credible contradiction or alternative explanation | Contrary studies, critical reviews, appeals, corrections, counterexamples, competing measurements |
| Scope | Test whether evidence matches the user's situation | Jurisdiction-, population-, entity-, or version-specific sources |
| Freshness | Find amendments, replacements, corrections, or current status | Updated guidance, changelogs, repeal/supersession notices, recent datasets |

Do not run every lane mechanically. Quick work may need only Authority plus one cross-check. Standard work normally needs more than one source class and a Challenge lane for decision-driving conclusions. Deep work should cover every material area in the plan and explicitly include Challenge and Freshness where applicable.

## 3. Build source-targeted queries

Combine the exact entity or claim with terms that identify the desired evidence, not with generic quality words.

Useful query components:

- exact program, law, product, dataset, or study name;
- issuing body, likely publisher, or `site:` restriction;
- jurisdiction, population, version, or date range;
- document type such as `rule`, `technical documentation`, `dataset`, `methods`, `filing`, `correction`, or `appeal`;
- disconfirming terms such as `limitations`, `critique`, `failed`, `reversed`, `not associated`, or a plausible competing explanation.

Use discovered terminology to improve the next query. Do not repeat near-identical queries after the result set converges.

## 4. Adapt after weak results

| Weak result | Next move |
|---|---|
| Many pages repeat one claim | Trace the claim to its original source; stop counting repetitions as corroboration. |
| Results discuss the topic but miss the user's scope | Add the jurisdiction, population, entity, version, or controlling definition. |
| Only snippets or summaries expose the claim | Search the exact title, quoted phrase, report identifier, or issuing body to reach the underlying page. |
| An identified primary page times out or fails to fetch | Retry the direct page at most once, then switch to an available interactive or automated browser and search for an official alternate endpoint before declaring it inaccessible. |
| Evidence is old | Search for `updated`, `amended`, `repealed`, `superseded`, `correction`, or the current year. |
| Sources conflict | Compare definitions and methods, then search the precise point of disagreement. |
| No adequate evidence appears | Record the attempted lane and gap; do not broaden into adjacent evidence and pretend it covered the area. |

Repeated coverage of one original source is one evidence lineage. Do not count those repetitions as independent corroboration, especially when the underlying source was never inspected.

## Worked planning example

**Question:** Should a fictional 75-person U.S. employer adopt automated interview scoring next year?

**Coverage plan:** what the product does; applicable legal constraints by hiring location; evidence of predictive validity and bias; operational benefits and failure modes; safer alternatives.

**Lane plan:**

- Authority: applicable federal and state agency pages, enacted text, and the vendor's current technical documentation.
- Application: enforcement guidance and transparent implementation studies matching employment selection.
- Challenge: independent validation studies, critiques of measurement validity, and documented counterexamples.
- Scope: sources matching the employer's hiring jurisdictions and applicant population.
- Freshness: amendments, effective dates, current product version, and superseding guidance.

**Candidate rejection:** A consultancy article summarizing a proposed law is `context only` if enacted text or an official legislative record is available. A vendor claim about accuracy is not independent corroboration. A study of a different population cannot support an unqualified claim about this employer.

**Final epistemic treatment:** Applicable enacted requirements may be stated as sourced facts. A prediction about reduced hiring time is an **Estimate** unless measured in a comparable setting. The adoption recommendation is an **Inference** based on the cited legal, validity, and operational evidence.
