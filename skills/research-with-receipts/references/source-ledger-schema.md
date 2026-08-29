# Candidate-source ledger

Use this JSON ledger to gate sources before synthesis. The script validates the record; the researcher remains responsible for whether the recorded evidence actually supports the claim.

## Shape

```json
{
  "version": 1,
  "scope": {
    "date_start": "2026-02-28",
    "date_end": "2026-08-28",
    "geography": "United States",
    "excluded_source_types": ["press_release"],
    "research_shape": "broad_landscape",
    "breadth_exception": ""
  },
  "claims": [
    {
      "id": "C1",
      "text": "The exact material claim to support.",
      "kind": "fact",
      "status": "supported",
      "source_ids": ["S1"],
      "qualification": ""
    }
  ],
  "sources": [
    {
      "id": "S1",
      "title": "Exact page title",
      "publisher": "Publisher or author",
      "publication_date": "2026-08-01",
      "url": "https://example.com/direct-page",
      "source_type": "company_documentation",
      "evidence_lineage": "Acme 2026 controls study",
      "opened": true,
      "access": "full",
      "evidence": "Specific evidence found on the opened page.",
      "scope_match": "match",
      "scope_note": "Why the date, geography, population, definition, entity, or version fits.",
      "limitations": "Material incentives, method limits, or none material.",
      "superseded": false,
      "date_exception": "",
      "verdict": "use",
      "verdict_reason": "Why this source is admitted for C1."
    }
  ]
}
```

Use `null` for an inapplicable scope boundary. Record publication dates as `YYYY-MM-DD`, `Month YYYY` (full or common abbreviated month), `YYYY-MM`, `YYYY`, or `date not shown`. Preserve the precision the page displays; never invent a day. The gate treats a partial date as its full implied month or year. Inside a bounded date range, an undated source or a partial date that crosses a boundary requires a written, evidence-based `date_exception` explaining how applicability or currency was established. Valid `kind` values are `fact`, `inference`, `estimate`, `anecdote`, and `uncertain`. A claim with `status: gap` has no `source_ids` and uses `qualification` to explain why no adequate source was found.

For Standard and Deep work, set `research_shape` to `narrow_question`, `comparison`, `broad_landscape`, `how_to`, `multi_question`, or `other`. For every source used in a broad landscape, set `evidence_lineage` to the original study, dataset, reporting effort, case, or authority from which its evidence descends. Pages repeating the same underlying report share one lineage. Leave `breadth_exception` empty when the normal breadth floor is met. If public evidence cannot support the breadth floor, explain the shortfall there and add at least one explicit gap claim; this does not authorize invented or weak sources.

Valid source types are `government`, `regulator`, `academic`, `standards_body`, `company_documentation`, `company_statement`, `press_release`, `vendor_material`, `trade_publication`, `news`, `nonprofit`, `social_post`, and `other`. Use the narrowest accurate type.

`access` is `full`, `partial`, or `inaccessible`. `scope_match` is `match`, `partial`, `mismatch`, or `not_applicable`. A supported claim using a partial-scope source must state the qualification that prevents overgeneralization.

When a primary or authoritative candidate fails through the initial fetch route, keep it in the ledger while trying reasonable alternate access routes. Record the final access state and use `limitations` or `verdict_reason` to note why an inaccessible candidate was rejected. Articles that merely repeat that candidate are a shared evidence lineage, not corroboration or a substitute for the unseen original; admit only distinct facts or analysis established by the opened secondary page itself.

## Admission behavior

The gate blocks a `use` source when it:

- is a search-result page, homepage, duplicate candidate URL, malformed direct URL, or local/non-public host;
- belongs to a source type the user excluded;
- was not opened or its substantive evidence is inaccessible;
- has no specific evidence recorded from the page;
- materially mismatches the confirmed scope;
- has been superseded;
- falls outside the confirmed date range, has no shown date within a bounded range, or has partial date precision that crosses the range boundary, without a written, evidence-based `date_exception`; or
- is not attached to a supported claim.

The final output validator permits only `use` sources, requires parenthetical citation syntax, requires the citation label to match the ledger's title, publisher, and date exactly, rejects approved sources that never appear in the answer, and rejects HTTP(S) URLs outside inline Markdown citation links. Standard and Deep ledgers must declare `research_shape`. A `broad_landscape` must have at least five distinct `use` sources, five evidence lineages, and three source types; a shortfall passes only with a written `breadth_exception` and an explicit gap claim. Final semantic review verifies that lineage labels are honest, evidence types fit the question, and each receipt appears after the exact supported sentence or bullet. Every ledger `gap` requires its own visible `No adequate source found` disclosure. For every supported non-fact kind present in the ledger, the answer must include the corresponding visible epistemic label; one heading may legitimately scope several claims. The validator checks label presence, not semantic correspondence, which remains part of final review. Reclassify discovery-only material as `context_only` and unusable material as `reject`; neither may appear as a final citation.
