# Research With Receipts Design

## Product decision

Research With Receipts is an open-source adaptive-research skill within the Agency Research plugin. It is not limited to one question, a short answer, or a fixed source count. It asks the user to choose `quick`, `standard`, or `deep` when those choices would materially change the work, while enforcing the same source and citation contract at every depth.

**Skill name:** Research With Receipts

**Tagline:** Research at the depth the task deserves. Receipts for every claim that matters.

## Job to be done

When a non-expert needs reliable research, produce an answer or report whose consequential claims can be checked without requiring the user to design the research method, vet the sources, or repair the citations.

## Depth model

- `quick`: A narrow factual or explanatory task with a small number of decisive sources and little material conflict.
- `standard`: Several related answer components, corroboration, at least one disconfirming search where conclusions matter, and explicit reconciliation of material conflicts.
- `deep`: Multiple material question families or evidence lanes requiring a staged research frame, gap tracking, more than one search wave, disconfirming evidence, reconciliation, and a substantial synthesis. By default, the user approves the frame before substantial retrieval; an initial request may explicitly authorize uninterrupted execution.

When depth is not explicit and the task could reasonably fit more than one level, the skill asks the user first. It chooses the lightest responsible depth only when the user delegates that choice or the task is unambiguously a narrow Quick lookup, and states the reason briefly. Depth controls research effort, evidence coverage, and output shape, not citation quality.

## Scope intake

Depth, date range, geography or jurisdiction, and source-type inclusion/exclusion policy are user controls, not silent researcher assumptions. When depth is materially ambiguous, intake asks it first. Standard and Deep then resolve boundaries sequentially, one question per response or structured-question call: recency, geography, and source exclusions. Geography is always asked at every depth and never inferred; a geography already named in the request is confirmed. Deep produces its staged Research Frame only after intake. Quick asks recency or source exclusions only when the missing boundary could materially change the answer.

The interaction contract is platform-adaptive. When Claude's `AskUserQuestion` is available, depth uses a single-select choice, and recency offers `Past 30 days`, `Past 6 months`, and `Past year`, with the automatic `Other` accepting a custom range. Geography is a separate single-select question whose `Other` field accepts the exact scope. Source exclusions are a separate multi-select question. In chat environments without structured questions, plain text presents equivalent choices and asks each control in a separate turn. A future ChatGPT/Codex plugin may add optional choice chips, but the skill cannot depend on that UI to function.

Source types are not inherently credible or noncredible. Press releases and vendor-authored pages may establish what an issuer announced, did, or claims, but they do not independently verify effectiveness, prevalence, or impact. The skill makes incentives visible and corroborates material claims beyond the issuer's own action or position.

## Receipts contract

1. Use live retrieved sources as evidence; memory may guide discovery but cannot support the final answer.
2. Open and inspect every page that appears in the answer.
3. Prefer original, primary, or authoritative sources when they are applicable; applicability outranks prestige.
4. Put each citation after the sentence or bullet it supports, inside parentheses, so the receipt does not interrupt the reader.
5. Retain source title, publisher or author, publication/update date at the precision displayed, and a direct URL. Never invent a day for a month- or year-dated source; say `date not shown` only when no date is displayed.
6. Distinguish sourced fact from inference, estimate, anecdote, and uncertainty.
7. Search for disconfirming evidence when a conclusion is consequential, disputed, or surprising.
8. Investigate material conflicts and preserve unresolved disagreement.
9. State `No adequate source found` when the available evidence cannot support the claim.
10. Never cite search results, snippets, indirect links, or a decorative bibliography.

## Research architecture

1. Frame the task: intended decision or answer, scope, timeframe, geography, source policy, depth, exclusions, and deliverable. Surface depth when materially ambiguous, then the three boundary controls according to the depth-specific intake rule rather than inferring them silently.
2. Build a flexible coverage plan and map its evidence needs. The plan follows the requested deliverable and may use themes, chronology, comparisons, cases, practices, findings, recommendations, or questions. Every mode maintains a compact execution record; standard and deep modes use an explicit Authority/Application/Challenge/Scope/Freshness lane method.
3. Deep mode presents a standalone Research Frame and waits for approval unless uninterrupted execution was explicitly authorized. Run discovery only after that gate, then open and evaluate candidate sources. Search again only for identified gaps, conflicts, supersession, or disconfirmation.
4. Before synthesis, record claims, gaps, and candidate-source verdicts in a strict JSON ledger. A standard-library admission gate rejects mechanical contract violations: search URLs, excluded source types, unopened or inaccessible evidence, duplicate URLs, scope mismatch, supersession, out-of-range evidence without an explicit controlling-authority exception, and supported claims attached to non-`use` sources.
5. Stop when each material coverage area has sufficient applicable evidence or an explicit gap, uncertainty is bounded, and another targeted search is unlikely to change the conclusion. Repeated weaker evidence is a stopping signal.
6. Synthesize around the answer, not the search history. Use familiar language, descriptive sections, and substantive bullets. For a broad Standard landscape, use at least five genuinely distinct usable sources across at least three evidence classes unless public evidence cannot support that breadth; repeated reporting from one evidence lineage counts once. Match the evidence mix to the job, including qualitative patterns, examples, practices, barriers, and practical guidance when relevant rather than defaulting to survey statistics. The final validator permits only approved `use` sources in explicit HTTP(S) inline citations, requires parenthetical receipts and ledger-matching citation metadata, blocks alternate URL syntax from bypassing admission, and blocks approved sources that were never cited.

## Boundaries and routing

- A draft checked against supplied sources routes by capability to a supplied-source audit; the skill does not name or depend on a sibling skill.
- Transcript/background inventory and audience-specific content-gap filling routes by capability; the skill does not name or depend on an internal implementation.
- Primary interviews, inaccessible proprietary data, or definitive professional advice remain out of scope.
- High-stakes legal, medical, financial, regulatory, or safety work requires current authoritative sources, stronger corroboration, explicit limitations, and professional review where appropriate.

## Output contract

All depths lead with the answer. Quick mode returns a compact cited answer plus material limits. Standard mode adds a plain-language bottom line, descriptive themes with several evidence-bearing bullets under each material theme, and explicit limits and gaps. Deep mode adds scope, method summary, synthesis by question family, conflicts, gaps, and conclusions or recommendations when requested. Bullets make a substantial report easier to scan; they are not a reason to compress away useful detail.

There is no detached bibliography by default. A source index is permitted only for long deep deliverables where it improves navigation, and it never replaces claim-adjacent citations.

## Packaging

The MIT-licensed public package is standalone and portable. `SKILL.md` retains the load-bearing receipts contract and routing. Focused references supply Standard/Deep search-lane craft and the strict source-ledger schema; an optional agent brief defines bounded parallel-lane evidence handoffs. One standard-library script validates source admission before synthesis, and the output validator binds final citations to that approved ledger. Neither script claims semantic source truth. Evals and fixtures remain outside the packaged runtime.

## Success criteria

- Asks the user to choose depth when effort is materially ambiguous, and self-selects only under the narrow-task or delegated-choice exceptions.
- Every consequential sourced claim has a parenthetical direct citation after the supported sentence or bullet, with required metadata.
- Broad Standard landscapes use at least five genuinely distinct usable sources across at least three evidence classes unless the evidence shortfall is explicit, and include the quantitative and qualitative evidence dimensions the question requires.
- Standard and Deep outputs use familiar language, descriptive headings, and substantive bullets without thinning the research.
- Deep mode demonstrates coverage planning, gap-driven follow-up, disconfirmation, reconciliation, and a justified stopping condition.
- Deep mode honors the staged Research Frame approval gate unless the user explicitly authorizes uninterrupted execution.
- Insufficient and conflicting evidence survive synthesis visibly.
- Neighboring fact-checking and content-research inputs route cleanly.
- Source-admission and final-output validators pass; semantic verification remains model-owned, and the skill contains no private dependency.
