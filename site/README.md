# Open Research Reading Site

The project owner has intentionally made `SeekerThinker/investment-research` public. This repository remains canonical; the GitHub Pages website is a disposable presentation layer.

`python monitor/build_public_site.py --output _site` builds the site from an explicit manifest (`metadata/publication-manifest.json`). It includes the latest daily/weekly/monthly summaries, full immutable historical report markdown, the searchable report catalog, curated health timestamps and a method/disclosure page. Existing reports are free for every visitor; there is no login, member tier or paywall.

The **支持研究** page explains voluntary sponsorship. It intentionally displays no payment address until the owner explicitly supplies and approves a real HTTPS destination in the manifest (`sponsorship.enabled` and `sponsorship.url`). Sponsorship has no reading, timing, coverage or opinion benefits.

The generated `_site/` does not copy tracking, indexes, raw news candidates/state or credentials. This is a site output allowlist, **not a privacy control**: because the GitHub repository is public, repository files and history are publicly accessible. Never put passwords or otherwise private information into the repository. Do not fabricate past reports or overwrite immutable research records.
