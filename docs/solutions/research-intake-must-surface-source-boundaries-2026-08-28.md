---
title: Research intake must surface source boundaries
date: 2026-08-28
skill: research-with-receipts
type: solution
---

# Research intake must surface source boundaries

## Correction

The skill originally told the researcher to identify timeframe, geography, and exclusions but only ask when an unstated boundary seemed materially consequential. That made important user preferences too easy to infer silently, especially preferences about press releases, vendor-authored sources, paywalled material, or other source classes.

## Maintainer rule

Research With Receipts must make three scope controls visible before Standard or Deep retrieval:

1. date range or recency window;
2. geography or jurisdiction; and
3. source-type inclusion or exclusion policy.

The first attempted fix was also wrong: it told Standard mode to propose defaults and bundle all three controls. In immediate use, the skill invented `January 2024–August 2026`, inferred a U.S./U.K. emphasis without evidence, and asked about date, geography, and source policy in one dense prompt.

The corrected interaction is sequential, non-inferential, and host-adaptive:

1. Ask recency first, as one screen or response, with `Past 30 days`, `Past 6 months`, `Past year`, and a custom range. Claude's `AskUserQuestion` authors the first three options and uses its automatic `Other` for the custom range; plain chat labels the fourth choice `Another range`.
2. Always ask geography as the next separate question. Never infer it from the user's identity, locale, profile, organization, or topic. If the prompt already names a geography, ask the user to confirm it.
3. Always ask source exclusions as the third separate question; if the prompt already states them, ask for confirmation.
4. Deep mode completes this intake before producing the approval frame. Quick mode still asks geography; it asks recency or source exclusions only when material.

Tool-specific interaction is an enhancement, not a runtime dependency. A distributed skill must preserve the same semantic questions and ordering when `AskUserQuestion` is unavailable. Chat/plugin packaging can add an optional choice UI, but the skill remains useful through its plain-text fallback.

When the user explicitly delegates the choices, the neutral default is 30 days for fast-moving news and six months for broader current trends; global coverage has no regional emphasis. Durable or historical questions do not receive an arbitrary recency window.

Do not default to excluding press releases or first-party material. They may be the primary source for what an organization announced or claims. Treat them as first-party evidence whose incentives are visible, and require independent corroboration when the claim extends beyond the issuer's own actions or position.
