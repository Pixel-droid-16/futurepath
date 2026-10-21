/* FuturePath backend adapter. This file changes DATA only, never the v2 layout.
   All APIs use the user's active local FastAPI server and synthetic demo evidence. */
const FP_API = {
  async json(path) {
    const response = await fetch(path, { headers: { Accept: 'application/json' }, credentials: 'same-origin' });
    if (!response.ok) throw new Error(`FuturePath API ${response.status}: ${path}`);
    return await response.json();
  },
  num(value) { return Number.isFinite(Number(value)) ? Math.max(0, Math.min(100, Number(value))) : 0; },
  card(rec, ws, wd) {
    const components = rec.components || {};
    const skill = this.num(components.skills), demand = this.num(components.trends);
    const interest = this.num(components.interests), feasibility = this.num(components.feasibility);
    const weightSum = (ws + wd) || 1;
    // User slider: redistribute only the official 65% skills-and-trends share.
    // 20% interests + 15% feasibility stay fixed. This is a PREVIEW, not a saved score.
    const score = Math.round(0.65 * (ws / weightSum * skill + wd / weightSum * demand) + 0.2 * interest + 0.15 * feasibility);
    const gaps = Array.isArray(rec.gaps) ? rec.gaps : [];
    return {
      id: rec.role_id, title: rec.title, sector: rec.sector, score,
      skill: Math.round(skill), demand: Math.round(demand), pm: 0,
      completeness: Math.round(this.num(rec.completeness)), provisional: !!rec.provisional,
      skillW: `${Math.round(skill)}%`, demW: `${Math.round(demand)}%`,
      demC: demand >= 50 ? 'var(--up)' : 'var(--dn)',
      ring: `conic-gradient(var(--pr) ${score*3.6}deg, var(--sf2) 0)`,
      sdgs: (rec.sdgs || []).map(n => ({n,c:(typeof SDG !== 'undefined' && SDG[n]) || 'var(--pr)'})),
      have: gaps.filter(g => g.status === 'satisfied').slice(0, 3).map(g => g.name),
      gap: gaps.filter(g => g.status !== 'satisfied').slice(0, 3).map(g => g.name),
      formula: `Skills ${skill} · Trends ${demand} · Interests ${interest} · Feasibility ${feasibility}`,
      goPathway: null, source: rec, lo: score, hi: score,
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
