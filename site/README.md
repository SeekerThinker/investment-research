# Research Reading Layer

This is the source for the filtered web reading layer. The private repository remains canonical.

`monitor/build_public_site.py` builds a disposable `_site/` artifact using an allowlist.

Public artifact includes only:
- latest daily / weekly / monthly summaries;
- historical report catalog metadata (type + period only);
- curated market/news health fields;
- methodology and disclosure UI.

It deliberately excludes full historical report bodies, `tracking/**`, `index/**`, raw NEWS candidate/state data, private notes, credentials, and portfolio/position data.

The Member page is a real publication boundary, not fake client-side gating: member-only bodies are absent from the public artifact until an authenticated backend is connected.
