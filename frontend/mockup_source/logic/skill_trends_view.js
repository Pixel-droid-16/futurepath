    // Signals page cards (/api/skill-trends): rising skills, and declining skills and jobs, each from stored dated signals.
    const tr = st.skillTrends, trDark = st.theme === "dark";
    const trUp = trDark ? "#4a8de0" : "#1d5fa8", trDn = trDark ? "#e0567a" : "#b4234a";  // = --chup / --chdn
    const TR_CAT = { ai: "AI", technical: "Technical", analytical: "Analytical", engineering: "Engineering", domain: "Domain knowledge", transferable: "Transferable", job: "Declining job" };
    // Sparkline as a CSS background SVG (the template runtime can't bind SVG attributes, and an <img> would request "{{ }}" first): cumulative signed signal strength per month.
    const trSpark = (vals, color) => {
      const w = 76, h = 24, lo = Math.min(...vals), hi = Math.max(...vals), span = hi - lo || 1;
      const pts = vals.map((v, i) => [i / Math.max(1, vals.length - 1) * (w - 4) + 2, h - 3 - (v - lo) / span * (h - 6)]);
      const last = pts[pts.length - 1];
      return 'url("data:image/svg+xml,' + encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><polyline points="${pts.map(p => p.map(n => n.toFixed(1)).join(",")).join(" ")}" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="${last[0].toFixed(1)}" cy="${last[1].toFixed(1)}" r="2.5" fill="${color}"/></svg>`) + '")';
    };
    const trCard = (c, up) => ({
      cat: TR_CAT[c.category] || c.category, t: c.title, spark: trSpark(c.line, up ? trUp : trDn),
      badge: `${up ? "↑" : "↓"} ${c.signal_count} ${c.kind === "job" ? "report" : "signal"}${c.signal_count === 1 ? "" : "s"}`,
      bb: up ? "var(--skybg)" : "var(--dnbg)", bc: up ? "var(--chup)" : "var(--chdn)",
      latest: (c.kind === "job" ? "Source: " : "Latest: ") + c.latest.title, src: `${c.latest.source} · ${fmtDate(c.latest.date)}`, url: c.latest.url,
      sdgs: c.sdgs.map(n => ({ n, c: SDG[n] || "var(--pr)" })), hasSdgs: c.sdgs.length > 0,
      sparkAlt: `${c.title}: ${up ? "rising" : "declining"} signals over the last 3 years`,
    });
    const trRising = tr?.rising || [], trDecl = tr?.declining || [], trLimit = st.trendsAll ? Infinity : 6;
    const sv = st.sigView || 'trends', svOn = k => sv === k ? { b: 'var(--pr)', c: 'var(--pri)' } : { b: 'transparent', c: 'var(--ink)' };
    Object.assign(out, {
      // Signals page switch: Skill trends cards or the list of signals.
      showTrends: sv === 'trends', showSigs: sv === 'signals', vTrends: () => this.setState({ sigView: 'trends' }), vSigs: () => this.setState({ sigView: 'signals' }),
      vTrB: svOn('trends').b, vTrC: svOn('trends').c, vTrBOn: String(sv === 'trends'), vSgB: svOn('signals').b, vSgC: svOn('signals').c, vSgBOn: String(sv === 'signals'),
      trReady: !!tr, trLoading: !tr,
      trRisingLbl: `Rising skills (${trRising.length})`, trDeclLbl: `Declining skills & jobs (${trDecl.length})`,  // one text node each, so they translate
      trRising: trRising.slice(0, trLimit).map(c => trCard(c, true)),
      trDecl: trDecl.slice(0, trLimit).map(c => trCard(c, false)),
      trHasMore: trRising.length > 6 || trDecl.length > 6, trMoreLbl: st.trendsAll ? "Show fewer" : "Show all",
      toggleTrends: () => this.setState(s => ({ trendsAll: !s.trendsAll })),
    });
