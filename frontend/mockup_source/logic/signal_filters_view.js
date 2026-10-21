    const SIG = [
      { up: true, t: "Solar installation roles and vocational teachers expected to grow", src: "WEF Future of Jobs Report 2025 · Jan 2025", type: "Report", tag: "Curated & verified", s: 4, roles: "Solar PV Installation & Systems Technician, Vocational & Digital Skills Trainer" },
      { up: false, t: "Data entry, secretarial and bookkeeping roles declining in every edition since 2016", src: "WEF Future of Jobs Report 2025 · Jan 2025", type: "Report", tag: "Curated & verified", s: 5, roles: "Data Entry Clerk, Administrative Assistant / Executive Secretary" },
      { up: true, t: "Malaysia launches National AI Office to coordinate AI adoption, governance and talent", src: "Google News · Dec 2024", type: "News", tag: "Tagged by Claude", s: 3, roles: "Responsible AI & Governance Specialist" },
      { up: true, t: "Anthropic Economic Index: learning-focused AI conversations rising", src: "Anthropic Economic Index · Sep 2025", type: "Dataset", tag: "Keyword fallback", s: 2, roles: "Vocational & Digital Skills Trainer" }
    ];
    const tagC = { "Curated & verified": ["var(--upbg)", "var(--up)"], "Tagged by Claude": ["var(--soft)", "var(--pr)"], "Keyword fallback": ["var(--sf2)", "var(--mu)"] };
    const signals = SIG.filter(x => st.sig === "all" || (st.sig === "up") === x.up).map(x => ({ ...x,
      dir: x.up ? "↑ Emerging" : "↓ Declining", dc: x.up ? "var(--sky)" : "var(--dn)", db: x.up ? "var(--skybg)" : "var(--dnbg)",
      tb: tagC[x.tag][0], tc: tagC[x.tag][1], dots: "●".repeat(x.s) + "○".repeat(5 - x.s) }));
    const f = k => st.sig === k ? { b: "var(--pr)", c: "var(--pri)" } : { b: "var(--sf)", c: "var(--ink)" };
    
