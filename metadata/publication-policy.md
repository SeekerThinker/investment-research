# Publication Policy — Open Reading and Voluntary Support

## 1. Repository and site status

The project owner has explicitly chosen to make `SeekerThinker/investment-research` a **public GitHub repository**. It remains the one canonical research state. The GitHub Pages site is a generated, disposable reading view of this public project; it is not a separate source of truth. Do not imply that files excluded from the Pages artifact are secret: they remain accessible in the public repository and its Git history. A future change in repository visibility requires the owner's direction and a fresh privacy review.

## 2. Free reading, no membership

All reports that are included in the website are equally readable by everyone, free of charge. Publish the latest daily/weekly/monthly summaries and the existing immutable historical report markdown under `reports/{daily,weekly,monthly}/`. There is no member tier, paywall, early-access tier, privileged research feed, or donation-dependent access. New reports join the website when the normal report-writing workflow commits them; do not backfill missing historical reports or rewrite immutable originals.

## 3. Voluntary sponsorship

A support page may explain how readers can voluntarily fund independent research. Supporting must not change content access, ranking, timing, coverage, or the substance of research conclusions; it must not buy personalized advice or securities recommendations. Do not manufacture a payment account, QR code, URL, payment amount, sponsor identity, or claim of a completed transaction. The external payment link must remain disabled until the owner explicitly approves a real HTTPS destination in `metadata/publication-manifest.json`. Record and disclose material sponsorship-related conflicts as appropriate; investigate applicable local fundraising/payment, tax, consumer and financial-regulatory requirements before accepting real funds. A disclaimer is not a substitute for applicable compliance.

## 4. Site export boundary versus repository publicity

`monitor/build_public_site.py` uses an allowlist to produce only the website UI, latest report summaries, historical report markdown, report catalog, and a small health summary. The site deliberately does not copy raw NEWS queues/state, `tracking/**`, `index/**`, debug data, passwords or tokens. This is a *website presentation boundary*, NOT an access restriction on the public repository. Never commit credentials, personal contact details, private positions, or other sensitive content to a public repository, even if omitted from `_site/`. Review source licenses and personal information before committing or republishing data. If confidential material was previously committed, removing it from current files is not enough to revoke past Git history or copies.

## 5. Research quality and disclosure

- Separate confirmed facts (F), inference (I), scenario (S) and unverified information (R); R cannot alone underpin high-confidence earnings claims.
- NEWS discovery is not a verification layer; major claims need primary sources and appropriate independent corroboration.
- State report publication date and market-data cutoff; historical reports are dated records, not real-time investment views.
- Distinguish industry exposure from company revenue, margin, profit and CFO/FCF transmission; document Model Audit gaps, Price In and falsification conditions where relevant.
- Never automatically turn machine hints or formal M/PF/crowding/distribution-risk categories into mechanical BUY/SELL or position-sizing instructions.
- Preserve corrections and falsification history in subsequent reports or a transparent correction record rather than silently rewriting immutable historical reports.
- Disclose relevant sponsorship, issuer/holding conflicts, source attribution and limitations as appropriate. Research is for information and education, not personalized advice; actual legal duties depend on the audience, jurisdiction, fees and real activity.

## 6. Publication operations

`metadata/publication-manifest.json` is the explicit website output configuration. Before any website release, validate the manifest, build the site, check that historical reports are readable and raw state/credentials are absent from the generated artifact, and only then deploy GitHub Pages. Repository integrity, report immutability, source freshness and editorial evidence rules remain in force independently of whether the repository is public.
