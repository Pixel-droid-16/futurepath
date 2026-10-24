    const liveRecords = st.fast ? st.liveRapid : st.liveModerate;
    // Recompute with the sliders, then keep near-identical skill sets apart. The backend applies the
    // same idea (engine._diversity_order); this preview version defers only exact near-duplicates.
    const skillIds = r => new Set(((r.source && r.source.gaps) || []).map(g => g.skill_id));
    const jaccard = (a, b) => { let both = 0; a.forEach(x => { if (b.has(x)) both++; }); const union = a.size + b.size - both; return union ? both / union : 0; };
    const diverse = cards => {
      const sorted = [...cards].sort((a, b) => b.exact - a.exact), keep = [], later = [];
      for (const card of sorted) {
        const set = skillIds(card), duplicate = keep.some(x => jaccard(set, skillIds(x)) >= 0.85);
        (duplicate ? later : keep).push(card);
      }
      return keep.concat(later);
    };
    const ranked = diverse((st.liveStatus === 'connected' ? liveRecords : []).map(r => FP_API.card(r, st.ws, st.wd)))
      .map((r,i)=>({...r,rank:i+1,
        goPathway:()=>this.selectCareer(r.id,true)}));
    const on = { bg: "var(--pr)", fg: "var(--pri)" }, off = { bg: "transparent", fg: "var(--ink)" };
    const m = st.fast ? off : on, f2 = st.fast ? on : off;
