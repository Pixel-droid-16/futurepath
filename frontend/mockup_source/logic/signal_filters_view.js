    // Preserve the API's publication-chronological order; never sort evidence by ingestion time.
    const TAG = { curated: ["Curated & verified", "var(--upbg)", "var(--up)"], claude: ["Tagged by Claude", "var(--soft)", "var(--pr)"], keyword: ["Keyword fallback", "var(--sf2)", "var(--mu)"] };
    const localeText = {
      en: { curated: "Curated evidence", validated: "AI-validated live evidence", stored: "Stored evidence", unknown: "Provenance unavailable", published: "Published", pending: "Not published: unverified evidence is held back", verified: "Verified", unverified: "Unverified", pendingStatus: "Pending verification", rejected: "Rejected" },
      ms: { curated: "Bukti pilihan", validated: "Bukti langsung disahkan AI", stored: "Bukti tersimpan", unknown: "Asal-usul tidak tersedia", published: "Diterbitkan", pending: "Tidak diterbitkan: bukti belum disahkan ditahan", verified: "Disahkan", unverified: "Belum disahkan", pendingStatus: "Menunggu pengesahan", rejected: "Ditolak" },
      zh: { curated: "精选证据", validated: "经 AI 验证的实时证据", stored: "已存储证据", unknown: "来源信息不可用", published: "发布日期", pending: "未发布：未经验证的证据不会公开", verified: "已验证", unverified: "未验证", pendingStatus: "等待验证", rejected: "已拒绝" }
    }[st.lang] || { curated: "Curated evidence", validated: "AI-validated live evidence", stored: "Stored evidence", unknown: "Provenance unavailable", published: "Published", pending: "Not published: unverified evidence is held back", verified: "Verified", unverified: "Unverified", pendingStatus: "Pending verification", rejected: "Rejected" };
    const fmtDate = value => {
      if (!value) return "—";
      try {
        const raw = String(value), date = new Date(/^\d{4}-\d{2}-\d{2}$/.test(raw) ? raw + "T00:00:00" : raw);
        return Number.isNaN(date.getTime()) ? raw : date.toLocaleDateString(fpIntlLocale(st.lang), { day: "numeric", month: "short", year: "numeric" });
      } catch (e) { return String(value); }
    };
    const provenanceLabel = row => {
      const translated = { curated: localeText.curated, live_ai_validated: localeText.validated, stored: localeText.stored }[row.provenance];
      return (st.lang === "en" && row.provenance_label) || translated || row.provenance_label || localeText.unknown;
    };
    const verificationLabel = value => {
      const normalized = String(value || "").toLowerCase().replace(/[\s-]+/g, "_");
      return ({ verified: localeText.verified, validated: localeText.verified, live_ai_validated: localeText.verified,
        unverified: localeText.unverified, pending: localeText.pendingStatus, pending_verification: localeText.pendingStatus,
        rejected: localeText.rejected }[normalized] || String(value || ""));
    };
    const signals = (st.liveSignals || []).filter(x => st.sig === "all" || (st.sig === "up") === (x.direction === "emerging")).map(x => { const tag = TAG[x.tagged_by] || TAG.keyword;
      const published = x.published_at || x.published_date;
      const sourceType = String(x.source_type || "evidence");
      return { t: x.title, summary: x.summary === x.title ? "" : x.summary, url: x.url, type: sourceType ? sourceType[0].toUpperCase() + sourceType.slice(1) : "Evidence",
        provenance: provenanceLabel(x), verification: verificationLabel(x.verification_status), published: fmtDate(published), provenanceCode: x.provenance || "",
        dir: x.direction === "emerging" ? "↑ Emerging" : "↓ Declining", dc: x.direction === "emerging" ? "var(--sky)" : "var(--dn)", db: x.direction === "emerging" ? "var(--skybg)" : "var(--dnbg)",
        tag: tag[0], tb: tag[1], tc: tag[2], dots: "●".repeat(Math.max(0, Math.min(5, Number(x.strength) || 0)) ) + "○".repeat(5 - Math.max(0, Math.min(5, Number(x.strength) || 0))),
        roles: (x.role_titles || []).length ? x.role_titles.join(", ") : ((x.skill_ids || []).length ? "Linked through skills only" : "General context"),
        src: x.source_name || "Unknown source" }; });
    const f = k => st.sig === k ? { b: "var(--pr)", c: "var(--pri)" } : { b: "var(--sf)", c: "var(--ink)" };
    const lastRun = st.signalRuns[0];
    const sigUpdated = st.liveSignals.length ? fmtDate(st.liveSignals[0].published_at || st.liveSignals[0].published_date || st.liveSignals[0].fetched_at) : "—";
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
    const wc = st.whatChanged;
    const wcMoves = (wc?.moves || []).slice(0, 3).map(m => ({ text: m.after_rank < m.before_rank ? `${m.title} moved up from #${m.before_rank} to #${m.after_rank}` : m.after_rank > m.before_rank ? `${m.title} moved down from #${m.before_rank} to #${m.after_rank}` : `${m.title} stayed at #${m.after_rank}`,
      why: `Trends ${m.before_trend} → ${m.after_trend} from ${m.new_signals} new signal${m.new_signals === 1 ? "" : "s"}` }));
    const wcSummary = wc?.has_change ? `${wc.new_signal_count} new signals from the refresh on ${fmtDate(wc.run.finished_at || wc.run.started_at)}.` : "No earlier ranking to compare yet. When new signals arrive, changes to your ranking will show here.";
