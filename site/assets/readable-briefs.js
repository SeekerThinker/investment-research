/* Presentation only: split already-published analysis fields without inventing claims.
   Works for homepage briefs and full-report numbered/bulleted news. */
(() => {
  'use strict';
  const app = document.getElementById('app');
  if (!app) return;
  const field = /^\s*(事实|影响|机会|风险|强度\s*\/\s*期限|已定价\s*\/\s*验证|已定价及验证|验证|来源)\s*[：:]\s*/;
  const normalized = s => s.replace(/\s*\/\s*/g, '/');
  function reshape(node) {
    if (node.dataset.impactStructured === '1') return;
    // Use the already-sanitized HTML rendered by app.js so existing Markdown
    // links and bold text in complete reports survive the layout change.
    const parts = node.innerHTML.split(/\s*｜\s*/);
    if (parts.length < 3 || !parts.slice(1).some(part => field.test(part))) return;
    const lines = document.createElement('div');
    lines.className = 'analysis-lines';
    for (const [i, original] of parts.entries()) {
      if (!original.trim()) continue;
      const matched = original.match(field);
      const label = matched ? normalized(matched[1]) : (i === 0 ? '事实' : '补充');
      const copy = matched ? original.slice(matched[0].length) : original;
      const row = document.createElement('div');
      row.className = 'analysis-line';
      const term = document.createElement('span');
      term.className = 'analysis-label';
      term.textContent = label;
      const value = document.createElement('span');
      value.className = 'analysis-copy';
      value.innerHTML = copy;
      row.append(term, value);
      lines.append(row);
    }
    node.dataset.impactStructured = '1';
    if (node.matches('.brief-card > p')) node.replaceWith(lines);
    else {
      node.classList.add('impact-report-item');
      node.replaceChildren(lines);
    }
  }
  function render() {
    app.querySelectorAll('.brief-card > p, .reader article li').forEach(reshape);
  }
  // Report and hash routing are asynchronous; observe only DOM changes.
  const observer = new MutationObserver(render);
  observer.observe(app, { childList: true, subtree: true });
  render();
})();
