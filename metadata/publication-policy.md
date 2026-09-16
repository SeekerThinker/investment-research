# Publication Policy

This file defines how the private investment-research system may feed a public blog, website, dashboard, or member product without turning the canonical research database itself into a public repository.

## 1. Canonical state remains private

`SeekerThinker/investment-research` remains the canonical private research engine.

Do not change this repository to public as part of normal publishing. Public/member content must be produced as a derived, filtered output into a separate publication layer or separate repository/site.

The publication layer must never become a second canonical research state. Corrections and state migrations happen in the private research engine first, then flow outward.

## 2. Three-layer model

Preferred architecture:

`Private Research Engine → Publication Filter → Public / Member Reading Layer`

### Private Research Engine

Contains the complete internal state, including machine discovery queues, raw candidate history, research-stage transitions, Model Audit gaps, falsification history, source-health diagnostics, and other working material.

### Public Reading Layer

Suitable for a personal research blog/dashboard. Prefer:

- verified facts and clearly separated inference/scenario;
- methodology and Research OS explanations;
- selected themes and event chains;
- selected historical research with immutable timestamps;
- price/fundamental divergence discussion;
- falsification points and what changed after publication;
- data freshness and source-health disclosures;
- selected daily/weekly/monthly research summaries.

### Member Reading Layer

If a member product is later created, the preferred added value is deeper research infrastructure rather than hidden mechanical recommendations. Examples include:

- richer historical databases and research chains;
- complete theme dossiers;
- deeper Model Audit and scenario tables;
- leading-indicator archives and research tools;
- research-process reviews and educational material;
- structured archives, filters, and comparative views.

Any paid product that moves toward specific securities recommendations, forecasts, personalized advice, position sizing, entry/exit instructions, or other regulated investment-advisory activity requires jurisdiction-specific legal/compliance review before launch. A disclaimer alone must not be treated as a substitute for that review.

## 3. Publication eligibility

Before material is exported to a public/member layer, check:

1. **Evidence state** — F/I/S must remain visibly separated. R/unverified material should normally stay private until independently verified; exceptional discussion of rumors must be clearly identified as unverified and should not support an investment conclusion.
2. **Freshness** — show the relevant data/report cutoff. Stale machine data cannot be presented as current.
3. **Source role** — NEWS/discovery is not a truth layer. Material investment facts should preferentially link back to primary/official/company sources or reliable independent verification.
4. **Transmission chain** — avoid publishing an industry story as a company-profit conclusion without Company Exposure → Revenue → Margin/Expenses → Profit → CFO/FCF reasoning.
5. **Price In / falsification** — important research pieces should state what the market appears to price in, what would confirm the thesis, and what would falsify it.
6. **Model Audit** — material company conclusions should disclose unresolved audit gaps where relevant.
7. **Corrections** — later corrections, falsifications, or contradictory evidence must be preserved rather than silently rewriting the historical publication.

## 4. Content that should remain private by default

Do not automatically export:

- raw `data/news/state.json` or internal dedup state;
- unreviewed raw discovery queues and low-confidence candidate dumps;
- credentials, tokens, private connector/config secrets, internal account information, or private contact details;
- unpublished personal notes or private portfolio/position information unless explicitly approved for publication;
- internal process/debug information that adds no reader value;
- material whose third-party licence or redistribution terms do not permit republication.

Raw machine data may be published only when its source/redistribution terms and presentation context are appropriate. Derived metrics should identify the data cutoff and the fact that machine hints are diagnostic rather than formal research conclusions.

## 5. Public-facing research discipline

Public/member content must not mechanically map M stage, PF Gap, crowding, Distribution Risk, NEWS score, or machine hints to BUY/SELL/position-sizing instructions.

The preferred public identity is an independent, auditable research process: explain how hypotheses form, how they are verified, what evidence is missing, and when they fail.

For every substantial public research piece, prefer the same quality gate used internally:

- What changed?
- Why does it matter?
- What is the transmission mechanism?
- What does the market appear to price in?
- What evidence would confirm it?
- What evidence would falsify it?

## 6. Disclosure and correction policy

Before a real public/member launch, add a publication-level disclosure template covering at minimum:

- publication timestamp and data cutoff;
- source attribution and evidence type;
- conflicts/positions disclosure policy appropriate to the publisher;
- correction/version-history policy;
- statement that research is informational/educational and not personalized advice, while recognizing that legal obligations depend on the actual product, audience, jurisdiction, and charging model.

Do not rely on boilerplate wording to justify a product design that is substantively regulated.

## 7. Technical publication boundary

When a public site is implemented, prefer a separate repository or deployment target containing only explicitly exported files. Use an allowlist, not a blocklist.

A future exporter should read from the private repository and write only approved publication artifacts. It should never mirror the private repository wholesale.

Until that filtered exporter/site exists, keep this repository private and treat `dashboard/README.md` as an internal workbench rather than a public website.
