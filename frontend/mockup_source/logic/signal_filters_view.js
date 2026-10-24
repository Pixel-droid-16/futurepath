    // Signals page: stored trend signals from /api/signals (curated reports + refreshed feeds), newest first.
    const TAG = { curated: ["Curated & verified", "var(--upbg)", "var(--up)"], claude: ["Tagged by Claude", "var(--soft)", "var(--pr)"], keyword: ["Keyword fallback", "var(--sf2)", "var(--mu)"] };
    const fmtDate = d => { try { return new Date(d + (d.length === 10 ? "T00:00:00" : "")).toLocaleDateString(fpIntlLocale(st.lang), { day: "numeric", month: "short", year: "numeric" }); } catch (e) { return d; } };
    const signals = st.liveSignals.filter(x => st.sig === "all" || (st.sig === "up") === (x.direction === "emerging")).map(x => { const tag = TAG[x.tagged_by] || TAG.keyword;
      return { t: x.title, summary: x.summary === x.title ? "" : x.summary, url: x.url, type: x.source_type[0].toUpperCase() + x.source_type.slice(1),
        dir: x.direction === "emerging" ? "↑ Emerging" : "↓ Declining", dc: x.direction === "emerging" ? "var(--sky)" : "var(--dn)", db: x.direction === "emerging" ? "var(--skybg)" : "var(--dnbg)",
        tag: tag[0], tb: tag[1], tc: tag[2], dots: "●".repeat(x.strength) + "○".repeat(5 - x.strength),
        roles: x.role_titles.length ? x.role_titles.join(", ") : (x.skill_ids.length ? "Linked through skills only" : "General context"),
        src: x.source_name + " · " + new Date(x.published_date + "T00:00:00").toLocaleDateString(fpIntlLocale(st.lang), { month: "short", year: "numeric" }) }; });
    const f = k => st.sig === k ? { b: "var(--pr)", c: "var(--pri)" } : { b: "var(--sf)", c: "var(--ink)" };
    const lastRun = st.signalRuns[0];
    const sigUpdated = st.liveSignals.length ? fmtDate(st.liveSignals.map(x => x.fetched_at).sort().slice(-1)[0]) : "—";
    const sigLastRun = lastRun ? (lastRun.status === "ok" ? "● OK" : lastRun.status === "running" ? "● Running" : "● " + lastRun.status[0].toUpperCase() + lastRun.status.slice(1)) + " · " + lastRun.accepted + " accepted · " + fmtDate(lastRun.finished_at || lastRun.started_at) : "Not refreshed yet";
    const sigLastRunC = !lastRun ? "var(--mu)" : lastRun.status === "ok" ? "var(--up)" : lastRun.status === "failed" ? "var(--dn)" : "var(--am)";
    const sigFeeds = lastRun ? lastRun.feeds.map(x => ({ name: x.name, state: x.ok ? x.items + " items" : "failed: " + (x.error || "error"), c: x.ok ? "var(--mu)" : "var(--dn)" })) : [];
    // What changed (Results): the latest refresh's effect on the current profile's ranking.
    const statusDate = value => {
      if (!value) return "—";
      const date = new Date(value);
      return Number.isNaN(date.getTime()) ? "—" : date.toLocaleString(fpIntlLocale(st.lang), { day: "numeric", month: "short", year: "numeric", hour: "numeric", minute: "2-digit" });
    };
    const feedStatus = st.signalStatus;
    const reviewRows = (st.reviewItems || []).map(item => {
      const signal = item.signal || {};
      const rawUrl = String(signal.url || "");
      let url = "";
      try { const parsed = new URL(rawUrl, location.origin); if (["http:", "https:"].includes(parsed.protocol)) url = parsed.href; } catch (e) {}
      return {
        id: item.id, status: item.status || "pending", statusLabel: (item.status || "pending").replace(/^\w/, c => c.toUpperCase()),
        title: signal.title || "Untitled evidence", summary: signal.summary || "No summary supplied.",
        source: signal.source_name || "Unknown source", sourceType: signal.source_type || "—",
        published: signal.published_date ? fmtDate(String(signal.published_date)) : "Date not supplied",
        created: statusDate(item.created_at), reviewed: statusDate(item.reviewed_at),
        url, direction: signal.direction || "Unclassified", strength: signal.strength ?? "—",
        notes: item.validation_notes || "", reason: item.decision_reason || "",
        canDecide: item.status === "pending",
        approve: () => this.decideSignal(item.id, "approve"),
        reject: () => this.decideSignal(item.id, "reject")
      };
    });
    const wc = st.whatChanged;
    const wcMoves = (wc?.moves || []).slice(0, 3).map(m => ({ text: m.after_rank < m.before_rank ? `${m.title} moved up from #${m.before_rank} to #${m.after_rank}` : m.after_rank > m.before_rank ? `${m.title} moved down from #${m.before_rank} to #${m.after_rank}` : `${m.title} stayed at #${m.after_rank}`,
      why: `Trends ${m.before_trend} → ${m.after_trend} from ${m.new_signals} new signal${m.new_signals === 1 ? "" : "s"}` }));
    const wcSummary = wc?.has_change ? `${wc.new_signal_count} new signals from the refresh on ${fmtDate(wc.run.finished_at || wc.run.started_at)}.` : "No earlier ranking to compare yet. When new signals arrive, changes to your ranking will show here.";
