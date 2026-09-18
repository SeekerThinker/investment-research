#!/usr/bin/env bash
# Cloudflare Pages Git build entrypoint. Build only a public, curated reading site.
# Cloudflare dashboard: build command `bash monitor/build_cloudflare_pages.sh`;
# output directory `_site`; production branch `main`; repository root `/`.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 monitor/validate_philosophy.py
python3 monitor/test_public_site_feed.py
python3 monitor/test_two_focus.py
python3 monitor/build_public_site.py --output _site
python3 monitor/include_intraday_site.py
python3 monitor/curate_homepage.py

python3 - <<'PY'
import json
from pathlib import Path

root = Path('_site')
index = root / 'content/index.json'
assert (root / 'index.html').is_file(), 'site landing page missing'
assert (root / 'assets/two-focus.js').is_file(), 'two-focus layout missing'
assert index.is_file(), 'public content index missing'
data = json.loads(index.read_text(encoding='utf-8'))
assert data['sponsorship']['no_access_benefit'] is True
assert 1 <= len(data['feed']['daily']) <= 12, 'daily selection missing or exceeds editorial cap'
assert all(item.get('focus') in ('opportunity', 'risk') for item in data['feed']['daily'])
assert sum(data['editorial']['focus_counts'].values()) == len(data['feed']['daily'])
assert data['editorial']['weekly_monthly_independent'] is True
for kind in ('weekly', 'monthly'):
    if any(report['type'] == kind for report in data['latest']):
        assert data['feed'][kind], f'{kind} homepage section missing'
for report in data['latest'] + data['archive']:
    assert report['access'] == 'public' and (root / report['path']).is_file(), f'broken report: {report}'
for private_path in ('tracking', 'index', 'data/news/state.json', 'data/news/candidates'):
    assert not (root / private_path).exists(), f'nonpublic working data copied to site: {private_path}'
print('PASS Cloudflare Pages build: curated two-focus daily, independent weekly/monthly, free archives, no private working data')
PY
