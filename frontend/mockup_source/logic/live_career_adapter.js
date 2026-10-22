/* FuturePath backend adapter. This file changes DATA only, never the v2 layout.
   All APIs use the user's active local FastAPI server and synthetic demo evidence. */
const FP_API = {
  async json(path) {
    const response = await fetch(path, { headers: { Accept: 'application/json' }, credentials: 'same-origin' });
    if (!response.ok) throw new Error(`FuturePath API ${response.status}: ${path}`);
    return await response.json();
  },
  async send(path, options) {
    const response = await fetch(path, { credentials: 'same-origin', ...options, headers: { Accept: 'application/json', ...(options.headers || {}) } });
    const body = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(typeof body.detail === 'string' ? body.detail : `FuturePath API ${response.status}: ${path}`);
    return body;
  },
  num(value) { return Number.isFinite(Number(value)) ? Math.max(0, Math.min(100, Number(value))) : 0; },
  card(rec, ws, wd) {
    // Same formula as backend/engine.py; the sliders only redistribute the skills/demand share (interest stays 20%).
    // This is a live PREVIEW of the published formula, recomputed in the browser.
    const m = rec.match || {};
    const skill = this.num(m.skill), demand = this.num(m.demand), hasInterest = m.interest !== null && m.interest !== undefined;
    const interest = hasInterest ? this.num(m.interest) : 0, wi = hasInterest ? 0.2 : 0, share = (ws + wd) || 1;
    const wS = (1 - wi) * ws / share, wD = (1 - wi) * wd / share;
    const exact = wS * skill + wD * demand + wi * interest, score = Math.round(exact), spread = wD * (m.demand_band || 18);
    const gaps = Array.isArray(rec.gaps) ? rec.gaps : [];
    const f = x => x.toFixed(2).replace(/0$/, '');
    return {
      id: rec.role_id, title: rec.title, sector: rec.sector, score, exact,
      lo: Math.max(0, Math.round(exact - spread)), hi: Math.min(100, Math.round(exact + spread)),
      skill: Math.round(skill), demand: Math.round(demand), band: m.demand_band || 18,
      skillW: `${Math.round(skill)}%`, demW: `${Math.round(demand)}%`,
      demC: demand >= 50 ? 'var(--up)' : 'var(--dn)',
      ring: `conic-gradient(var(--pr) ${score*3.6}deg, var(--sf2) 0)`,
      sdgs: (rec.sdgs || []).map(n => ({n,c:(typeof SDG !== 'undefined' && SDG[n]) || 'var(--pr)'})),
      have: gaps.filter(g => g.status === 'satisfied').map(g => g.name),
      gap: gaps.filter(g => g.status !== 'satisfied').map(g => g.name),
      formula: `${f(wS)} × ${Math.round(skill)} + ${f(wD)} × ${Math.round(demand)}` + (hasInterest ? ` + 0.2 × ${Math.round(interest)}` : '') + ` = ${score}`,
      why: (rec.signals?.cited || []).map(c => ({ t: c.title, src: `${c.source} · ${c.date} · ${c.direction} · ${c.via}`, url: c.url })),
      signalLine: rec.signals ? `${rec.signals.signal_count} dated signal${rec.signals.signal_count === 1 ? '' : 's'} behind demand (${rec.signals.confidence} confidence).` : 'Demand uses the synthetic snapshot value.',
      interestWhy: m.interest_why || '', topSource: rec.signals?.cited?.[0] ? `${rec.signals.cited[0].source} · ${rec.signals.cited[0].date}` : '',
      goPathway: null, source: rec,
    };
  },
  summary(result) {
    if (!result) return { tasks: [], priorities: [], title: 'Select a career', score: '—', completeness: '—' };
    return {
      title: result.title,
      score: result.suitability,
      completeness: result.completeness,
      readiness: result.readiness === null ? 'Unknown' : result.readiness,
      priorities: (result.pathway || []).slice(0, 4).map(item => ({
        title: item.skill, category: item.category, reason: item.why,
        label: item.status === 'unknown' ? 'Assess first' : 'Learning priority',
      })),
      tasks: result.scenario_details?.tasks || [],
      assumption: result.scenario_details?.assumption || '',
      recommended_action: result.scenario_details?.recommended_action || '',
      uncertainty: result.scenario_details?.uncertainty || '',
    };
  },
};
