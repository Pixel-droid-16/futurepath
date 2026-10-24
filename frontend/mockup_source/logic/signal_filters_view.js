    // Signals page: stored trend signals from /api/signals (curated reports + refreshed feeds), newest first.
    const TAG = { curated: ["Curated report", "var(--upbg)", "var(--up)"], claude: ["AI-tagged feed", "var(--soft)", "var(--pr)"], keyword: ["Reviewed feed", "var(--sf2)", "var(--mu)"] };
    const fmtDate = d => { try { return new Date(d + (d.length === 10 ? "T00:00:00" : "")).toLocaleDateString(fpIntlLocale(st.lang), { day: "numeric", month: "short", year: "numeric" }); } catch (e) { return d; } };
    // Keep verified imported live evidence first, then archived curated reports, all sorted by publication date.
    const visibleEvidence = st.liveSignals.filter(x => st.sig === "all" || (st.sig === "up") === (x.direction === "emerging"))
      .sort((a,b) => Number(a.tagged_by === 'curated') - Number(b.tagged_by === 'curated')
        || String(b.published_date).localeCompare(String(a.published_date))
        || (Number(b.id) || 0) - (Number(a.id) || 0));
    const signalsTotal = visibleEvidence.length, signalPagesTotal = Math.max(1, Math.ceil(signalsTotal / 8));
    const signalsCurrent = Math.min(signalPagesTotal, Math.max(1, Number(st.signalsPage) || 1));
    const goSignalsPage = page => this.setState({ signalsPage: Math.min(signalPagesTotal, Math.max(1, page)) });
    // Keep page-number buttons bounded as the live evidence collection grows.
    const signalPageFirst = Math.max(1, Math.min(signalsCurrent - 2, signalPagesTotal - 4));
    const signalPageLast = Math.min(signalPagesTotal, signalPageFirst + 4);
    const signalsPages = Array.from({ length:signalPageLast-signalPageFirst+1 }, (_, i) => {
      const n = signalPageFirst+i;
      return { n, current:String(signalsCurrent === n),
        bg:signalsCurrent === n ? 'var(--pr)' : 'var(--sf)',
        c:signalsCurrent === n ? 'var(--pri)' : 'var(--ink)', go:()=>goSignalsPage(n) };
    });
    const signals = visibleEvidence.slice((signalsCurrent-1)*8,signalsCurrent*8).map(x => { const tag = TAG[x.tagged_by] || TAG.keyword;
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
    const lang = st.lang === 'ms' ? 'ms' : st.lang === 'zh' ? 'zh' : 'en';
    // Never claim daily updates if the scheduler is disabled or the host is asleep.
    const uiText = {
      en: { auto:'Automatic evidence checks', off:'Checks paused in this environment',
        schedule:'Best-effort checks every {n} hours while the server runs',
        last:'Last successful source check', next:'Next expected check', none:'Not available',
        status:'Status', ready:'Latest check completed', partial:'Some sources failed; saved evidence remains available',
        failed:'Latest check failed; saved evidence remains available', running:'Checking sources…',
        waiting:'Awaiting first check', paused:'Checks paused',
        held:'AI verification is off; new feed items remain staged, not published',
        active:'AI validation enabled; passing sources can publish automatically',
        inactive:'Stored evidence only until automatic checks are enabled',
        empty:'No signals match this filter yet.',
        page:'Page', of:'of', previous:'Previous', nextButton:'Next' },
      ms: { auto:'Semakan bukti automatik', off:'Semakan dijeda dalam pemasangan ini',
        schedule:'Semakan usaha terbaik setiap {n} jam ketika pelayan beroperasi',
        last:'Semakan sumber berjaya terakhir',next:'Semakan seterusnya dijangka',none:'Tidak tersedia',
        status:'Status',ready:'Semakan terkini selesai',partial:'Sebahagian sumber gagal; bukti tersimpan masih tersedia',
        failed:'Semakan terakhir gagal; bukti tersimpan masih tersedia',running:'Menyemak sumber…',
        waiting:'Menunggu semakan pertama',paused:'Semakan dijeda',
        held:'Pengesahan AI dimatikan; sumber baharu disimpan untuk semakan, bukan diterbitkan',
        active:'Pengesahan AI aktif; sumber yang lulus boleh diterbitkan secara automatik',
        inactive:'Bukti tersimpan sahaja sehingga semakan automatik diaktifkan',
        empty:'Tiada isyarat yang sepadan dengan penapis ini.',
        page:'Halaman',of:'daripada',previous:'Sebelumnya',nextButton:'Seterusnya' },
      zh: { auto:'自动证据检查',off:'此部署暂停了自动检查',
        schedule:'服务器运行时，每 {n} 小时尽力检查一次',
        last:'最近成功来源检查',next:'预计下次检查',none:'不可用',
        status:'状态',ready:'最近检查已完成',partial:'部分来源检查失败；历史证据仍可查看',
        failed:'最近检查失败；历史证据仍可查看',running:'正在检查来源…',
        waiting:'等待首次检查',paused:'检查已暂停',
        held:'AI验证未启用；新来源仅暂存，不会自动发布',
        active:'AI验证已启用；通过审核的来源可自动发布',
        inactive:'启用自动检查前仅显示已保存证据',
        empty:'此筛选条件下暂无信号。',
        page:'第',of:'页，共',previous:'上一页',nextButton:'下一页' }
    }[lang];
    const hours = Number(feedStatus?.interval_hours);
    const sigAutoFrequency = feedStatus?.enabled && Number.isFinite(hours) && hours > 0
      ? uiText.schedule.replace('{n}', String(hours)) : uiText.off;
    const successDate = statusDate(feedStatus?.last_successful_at);
    const sigLastSuccessful = successDate === '—' ? uiText.none : successDate;
    const sigNextExpected = feedStatus?.enabled && feedStatus?.next_due
      ? statusDate(feedStatus.next_due) : uiText.none;
    const sigHealth = !feedStatus?.enabled ? uiText.paused : ({
      ok:uiText.ready, partial:uiText.partial, failed:uiText.failed,
      running:uiText.running
    }[feedStatus.status] || uiText.waiting);
    const sigAIGuard = !feedStatus?.enabled ? uiText.inactive
      : feedStatus?.automatic_ai_enabled ? uiText.active : uiText.held;
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
