    const SAMPLE_FEED = [
      { dir: "↑", kind: "Emerging", t: "Solar installation roles and vocational teachers expected to grow", src: "Demo · synthetic", roles: "Solar PV Technician, Skills Trainer", c: "var(--up)", bg: "var(--upbg)" },
      { dir: "↓", kind: "Declining", t: "Data entry, secretarial and bookkeeping roles declining in every edition since 2016", src: "Demo · synthetic", roles: "Data Entry Clerk, Admin Assistant", c: "var(--dn)", bg: "var(--dnbg)" },
      { dir: "↑", kind: "Emerging", t: "Malaysia launches National AI Office to coordinate AI adoption, governance and talent", src: "Demo · synthetic", roles: "Responsible AI Specialist", c: "var(--up)", bg: "var(--upbg)" },
      { dir: "↑", kind: "Emerging", t: "Malaysia's green jobs expected to grow about tenfold by 2050, mostly in solar", src: "Demo · synthetic", roles: "Renewable Energy Engineer", c: "var(--up)", bg: "var(--upbg)" },
      { dir: "↑", kind: "Emerging", t: "Care economy jobs expected to grow significantly as populations age", src: "Demo · synthetic", roles: "Elderly & Personal Care Aide", c: "var(--up)", bg: "var(--upbg)" },
      { dir: "↓", kind: "Declining", t: "Client information and customer service workers among largest-declining jobs", src: "Demo · synthetic", roles: "Customer Service Worker", c: "var(--dn)", bg: "var(--dnbg)" }
    ];
    // Latest stored trend signals (newest first); the sample list only shows until /api/signals has loaded.
    const FEED = st.liveSignals.length ? st.liveSignals.slice(0, 6).map(x => ({ dir: x.direction === "emerging" ? "↑" : "↓", kind: x.direction === "emerging" ? "Emerging" : "Declining", t: x.title,
      src: x.source_name + " · " + new Date(x.published_date + "T00:00:00").toLocaleDateString(fpIntlLocale(st.lang), { month: "short", year: "numeric" }), roles: x.role_titles.join(", ") || "General context", c: x.direction === "emerging" ? "var(--up)" : "var(--dn)", bg: x.direction === "emerging" ? "var(--upbg)" : "var(--dnbg)" })) : SAMPLE_FEED;
    const tk = st.tick || 0, CYC = 5, li = Math.floor(tk / CYC) % FEED.length;
    const now = new Date();
    let clock = ""; try { clock = now.toLocaleTimeString(fpIntlLocale(st.lang), { timeZone: "Asia/Kuala_Lumpur", hour: "2-digit", minute: "2-digit", second: "2-digit" }); } catch (e) { clock = now.toTimeString().slice(0, 8); }
    // Feed stats: signals fetched in the last 7 days, and hours since the last refresh run finished.
    const weekAgo = new Date(Date.now() - 7 * 86400000).toISOString().slice(0, 10);
    const sigNewWeek = st.liveSignals.filter(x => x.tagged_by !== "curated" && x.fetched_at >= weekAgo).length;  // added by feed refreshes, not the curated baseline
    const lastFetch = st.signalRuns.find(r => r.finished_at);
    const sinceFetch = lastFetch ? Math.max(0, Math.round((Date.now() - new Date(lastFetch.finished_at).getTime()) / 3600000)) + "h" : "—";
