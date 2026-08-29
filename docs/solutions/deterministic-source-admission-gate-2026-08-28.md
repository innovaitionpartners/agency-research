---
title: Deterministic source admission needs a ledger boundary
date: 2026-08-28
skill: research-with-receipts
type: solution
---

# Deterministic source admission needs a ledger boundary

## Problem

Citation-format validation happens too late to stop a weak candidate from influencing synthesis. Prompt instructions can tell a researcher to reject an unopened, mismatched, superseded, inaccessible, or excluded source, but the output script cannot tell whether the final citation ever passed that decision boundary.

## Maintainer rule

Separate source admission from answer formatting:

1. Record the confirmed scope, material claims or explicit gaps, candidate metadata, page evidence, scope fit, limitations, and verdict in a strict machine-readable ledger.
2. Run a deterministic admission gate before drafting. Hard-fail mechanical violations and claims attached to anything except a `use` source.
3. Pass the same ledger to the final validator. Every final citation must match an approved source URL and exact ledger metadata; every approved source must be cited.
4. Keep the epistemic boundary explicit: a script can validate recorded facts and relationships, but it cannot prove that the researcher recorded them honestly or that the evidence semantically supports the wording.

Allow explicit, auditable exceptions only where a mechanical rule would otherwise reject valid evidence. The initial gate permits an older source outside the discovery window only when `date_exception` explains why it remains controlling and the researcher checked for supersession. It does not permit bypasses for unopened, inaccessible, excluded, superseded, or scope-mismatched evidence.

## Preserve publication-date precision

A displayed month or year is dated evidence, not an undated source. Preserve the precision the publisher actually provides rather than inventing a day. The gate should accept exact dates, month-year dates, year-only dates, and `date not shown`. Convert a partial date to its implied interval for scope checking: admit it without exception only when that whole interval is inside the confirmed range; require a documented `date_exception` when it straddles a boundary or falls outside.

## Close exact mixed-rule surfaces without claiming semantic truth

The source ledger makes several mixed rules mechanically observable after the researcher has made the semantic classification. Each claim recorded as a gap requires its own visible `No adequate source found` disclosure. For supported inference, estimate, anecdote, or uncertain material, code can require the corresponding label to be present, while allowing one heading to scope several claims. It cannot prove that a visible label semantically corresponds to the right prose, so that remains part of final review. The same boundary applies to URL syntax, reserved hosts, required-section substance, and absolute artifact paths: enforce the exact surface, then retain the researcher-owned semantic review.
