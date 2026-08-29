---
title: Primary-source fetch failure needs an access escalation ladder
date: 2026-08-28
skill: research-with-receipts
type: solution
---

# Primary-source fetch failure needs an access escalation ladder

## Correction

When an original Forrester page timed out through the default web fetcher, the researcher treated articles repeating Forrester's figures as an acceptable substitute and moved toward drafting. That undermined the receipts contract: repeated secondary coverage does not prove that the researcher inspected the original evidence, and it is not independent corroboration of the original claim.

## Maintainer rule

A failed default fetch is an access-route failure, not yet an inaccessible-source verdict. Before substituting secondary coverage for an identified primary or authoritative source, try the available alternate retrieval routes appropriate to the host, such as an interactive browser, browser automation, Claude in Chrome, or a Playwright-capable CLI. Also look for an official PDF, canonical mirror, print view, filing, dataset, or other first-party endpoint.

Only call the primary evidence inaccessible after reasonable alternate routes fail. At that point:

1. record the failed access attempts;
2. classify articles that merely repeat the original as secondary or context-only, not independent corroboration;
3. cite a secondary source only for what that secondary source itself reports and label the limitation; and
4. write `No adequate source found` when the answer slot depends on evidence that was never inspected.

The public skill should describe this as a capability-based fallback ladder, not depend on one named host or browser product. Host-specific packaging may map the ladder to Claude in Chrome, an in-app browser, Playwright, or another available tool.
