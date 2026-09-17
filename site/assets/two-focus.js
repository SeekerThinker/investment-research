/* Presentation-only enhancement for the TWO explicit latest-daily editorial groups.
   app.js owns fetching, archives, report rendering and escaping. Curator owns
   group assignment; this file never classifies news or manufactures claims. */
(() => {
  'use strict';
  const labels = ['事实', '传导', '潜在预期差', '成立条件', '风险触发', '强度/期限', '验证',
                  '影响', '机会', '风险', '已定价/验证', '来源'];
  // Replace the generic single-paragraph parser for all three report types.
  // Old weekly/monthly prose remains readable as a clearly marked summary.
  analysisParts = function (summary) {
    const parts = String(summary || '').split('｜').map(x => x.trim()).filter(Boolean);
    return parts.map(part => {
      const label = labels.find(x => part.startsWith(x + '：') || part.startsWith(x + ':'));
      return label ? [label, part.slice(label.length + 1).trim()] : ['摘要', part];
    });
  };
  function sectionOrEmpty(id, title, description, items) {
    if (items.length) return briefSection(id, title, description, items);
    return `<section class="brief-section" id="${id}"><div class="shell"><div class="brief-heading"><div><div class="eyebrow">${description}</div><h2>${title}</h2></div></div><p class="muted">本期没有满足证据要求的相关重点，不为填满栏目而编造。</p></div></section>`;
  }
  // app.js resolves its first fetch asynchronously; this script executes
  // synchronously afterwards and replaces only the homepage presentation.
  home = function (target) {
    const feed = data.feed || {};
    const latest = data.latest.find(x => x.type === 'daily');
    const daily = feed.daily || [];
    const opportunities = daily.filter(x => x.focus === 'opportunity');
    const risks = daily.filter(x => x.focus === 'risk');
    const weekly = feed.weekly || [];
    const monthly = feed.monthly || [];
    const total = daily.length + weekly.length + monthly.length;
    const links = [
      ['opportunity', '投资机遇', opportunities.length],
      ['risk-focus', '风险规避', risks.length],
      ['weekly', '周报观察', weekly.length],
      ['monthly', '月度视角', monthly.length],
    ];
    app.innerHTML = `<section class="news-hero"><div class="shell"><div class="eyebrow">SeekerThinker · Independent Research</div><h1>投资机遇与风险规避</h1><p class="lede">全市场广泛扫描后，分别聚焦潜在收益错位与可能造成较大损失的事项；标题不是已验证的收益率或亏损预测。</p><div class="issue-meta"><span>最新日报：<strong>${esc(latest?.period || '暂无')}</strong></span><span>预期差与个股价值须有市场预期、同日价格和现金流证据；不足时明确标记待验证</span><span>各条均为其报告期内的历史研究，非实时行情</span></div><div class="channel-links" aria-label="研究栏目">${links.map(([id, name, count]) => `<a href="#home/${id}">${name} <span>${count}</span></a>`).join('')}</div></div></section>${sectionOrEmpty('opportunity', '投资机遇 · 值得进一步验证的错位', 'Opportunity · 成立条件优先', opportunities)}${sectionOrEmpty('risk-focus', '风险规避 · 可能被低估的损失', 'Risk · 风险触发条件优先', risks)}${briefSection('weekly', '本周研究观察', 'Weekly · 独立保留，不受日报精选上限影响', weekly)}${briefSection('monthly', '月度研究视角', 'Monthly · 独立保留，不受日报精选上限影响', monthly)}<section class="brief-section"><div class="shell"><div class="end-links"><div><strong>首页共 ${total} 条当期与跨期研究要点；日报 ${daily.length} 条分属机遇与风险两类。</strong><p class="muted">日报的其他事实、对立情景、市场行为及风险细项可在免费完整报告阅读；周报、月报和历史报告未删减。</p><small class="muted">站点构建：${esc(data.generated_at)}</small></div><a class="button" href="#reports">浏览全部历史报告 →</a></div><h2 class="health-title">数据源状态</h2><div class="health-grid">${health('Market Data', data.health.market)}${health('News Discovery', data.health.news)}</div></div></section>`;
    if (target) document.getElementById(target)?.scrollIntoView();
    else window.scrollTo(0, 0);
  };
})();
