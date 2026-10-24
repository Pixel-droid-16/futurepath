    // Results (step 4 of /start; /results opens the same view directly).
    const hasQuiz = !!st.profileDemo?.riasec;
    // Fast AI scenario summary, measured from the two live rankings at the current weights (not a fixed claim).
    const scOrder = list => list.map(r => FP_API.card(r, st.ws, st.wd)).sort((a, b) => b.exact - a.exact).map(r => r.id);
    const scMod = scOrder(st.liveModerate), scFast = scOrder(st.liveRapid);
    const scShifts = st.liveRapid.map(r => Math.round(r.assumption_shift || 0)), scChanged = scShifts.filter(x => x !== 0).length;
    const scSigned = n => n > 0 ? `+${n}` : n < 0 ? `−${-n}` : '0';
    const scNoAiCount = st.liveRapid.filter(r => r.signals && !r.signals.ai_signal_count).length;
    const scenarioImpact = scShifts.length ? `Right now this changes demand for ${scChanged} of ${scShifts.length} careers (${scSigned(Math.min(...scShifts))} to ${scSigned(Math.max(...scShifts))} points) and ${scFast.filter((id, i) => scMod[i] !== id).length} careers change rank.` : '';
    const scenarioNoAi = scNoAiCount ? `${scNoAiCount} career${scNoAiCount === 1 ? ' has' : 's have'} no AI-related signals yet, so ${scNoAiCount === 1 ? 'its' : 'their'} demand stays the same.` : '';
    return { ...out, ...startBindings, theme: st.theme, sdgReady: true, sdgTiles, sdgLinkedCount, live: FEED[li], liveNext: [1, 2, 3].map(k => FEED[(li + k) % FEED.length]), liveProg: (((tk % CYC) + 1) / CYC * 100) + "%", clock, accent: this.props.accent ?? "violet", lbl: st.theme === "dark" ? "Light" : "Dark",
      toggle: () => this.setState(s => ({ theme: s.theme === "dark" ? "light" : "dark" })),
      langEn: st.lang === "en", langMs: st.lang === "ms", langZh: st.lang === "zh",
      onLangChange: e => this.setLanguage(e.target.value),
      goHome: () => this.go("home"), goStart: () => this.startOver(), goSignals: () => this.go("signals"), goAbout: () => this.go("about"),
      go_start: () => this.startOver(),
      feedLabel: st.liveSignals.length ? "LIVE " + "SIGNAL FEED" : "SAMPLE SIGNAL FEED",  // "live" only once real stored signals have loaded
      sigTotal: st.liveSignals.length || "—", courseTotal: st.courseTotal || "—", roleCount: st.liveModerate?.length || "—", sigNewWeek, sinceFetch,
      showResults: st.page === "results" || (st.page === "start" && st.startStep === "results"),
      resultsProfileName: st.profileDemo?.name || "My profile",
      resultsStepper: ["Choose start", "Check profile", "Interest quiz", "Results"].map((label, i) => ({ label, mark: i < 3 ? "✓" : "4", line: i < 3,
        c: i < 3 ? "var(--up)" : "var(--pr)", bg: i < 3 ? "var(--upbg)" : "var(--pr)", fg: i < 3 ? "var(--up)" : "var(--pri)" })),
      startOver: () => this.startOver(),
      hasOtherPeople: st.people.length > 1, personChips: st.people.map(x => { const on = x.id === (st.activeProfileId || "demo");
        return { name: x.name, b: on ? "var(--pr)" : "var(--sf)", c: on ? "var(--pri)" : "var(--ink)", bd: on ? "var(--pr)" : "var(--ln)", open: () => this.switchPerson(x.id) }; }),
      top4: ranked.slice(0, 4), rest: st.rolesAll ? ranked.slice(4) : ranked.slice(4, 10), hasMoreRoles: ranked.length > 10,
      moreRolesLbl: st.rolesAll ? "See less" : `See more (${ranked.length - 10})`, toggleRoles: () => this.setState(s => ({ rolesAll: !s.rolesAll })),
      count: ranked.length,
      ws: st.ws, wd: st.wd, wsPct: Math.round(ws * 100), wdPct: Math.round(wd * 100),
      onWs: e => this.setState({ ws: +e.target.value, wd: 100 - (+e.target.value) }), onWd: e => this.setState({ wd: +e.target.value, ws: 100 - (+e.target.value) }),
      reset: () => this.setState({ ws: 55, wd: 45 }),
      noQuiz: !hasQuiz, takeQuiz: () => this.editProfile("quiz"),
      interestNote: hasQuiz ? `Interest fit counts for 20%. Your strongest interests: ${st.profileDemo.riasec_code}.` : "Interest fit: Take the optional RIASEC interest quiz to add it.",
      setMod: () => this.setState({ fast: false }), setFast: () => this.setState({ fast: true }),
      modBg: m.bg, modFg: m.fg, fastBg: f2.bg, fastFg: f2.fg,
      isFast: st.fast, scenarioImpact, scenarioNoAi,
      scenarioText: st.fast ? "AI adoption speeds up. Every AI-related trend signal (its headline or summary mentions AI, automation, machine learning or robots) counts double; other signals count as usual."
        : "AI adoption continues at roughly the pace employers reported in the WEF Future of Jobs Report 2025. Signals are used as they are.",
      scenarioNote: st.fast ? "A modelling assumption chosen by the FuturePath team, not a forecast. Your skill match is unchanged." : "Baseline estimate, not a prediction.",
      wcMoves, wcSummary, hasWcMoves: wcMoves.length > 0,
      // Pathway (/pathway) for the selected career.
      backToResults: () => { if (st.startStep === "results") { this.go("start"); } else { this.go("results"); } },
      pathTitle: fpActive?.title || 'Choose a career on the results page',
      pathIntroduction: `${st.fast ? 'Fast' : 'Moderate'} AI disruption · ${studyHours} h a week · free, low-cost and HRD Corp claimable courses`,
      pathSdgs: (fpActive?.sdgs || []).map(n => ({ n, label:`SDG ${n} · ${SDG_GOALS[n] || 'Sustainable Development Goal'}`, c: SDG[n] || 'var(--pr)' })),
      pathSdgJustification: fpActive?.sdg_justification || 'Select a career to see its SDG connection.',
      // Hours and weeks still to go: completed steps no longer count.
      ...(left => ({ pathHours: pathHoursNum ? left : '—', pathWeeks: pathHoursNum ? Math.ceil(left / studyHours) : '—',
        pathHoursLbl: fpSteps.some(x => x.done) ? 'hours left' : 'hours', pathWeeksLbl: fpSteps.some(x => x.done) ? 'weeks left' : 'weeks' }))
        (Math.max(0, pathHoursNum - Math.round(fpSteps.filter(x => x.done).reduce((a, x) => a + x.hours, 0)))),
      pathCost: !pathCostSet.size ? '—' : pathCostSet.has('Free') && pathCostSet.size === 1 ? 'Free' : [...pathCostSet].some(c => c.startsWith('HRD')) ? 'HRD Corp' : 'Low cost',
      pathCostNote: !pathChecked.length ? 'No course verification dates recorded' : [...new Set(pathChecked)].join(' · '),
      pathNote: 'Provider-page dates are shown for individually checked courses; imported entries show their catalogue snapshot date. Confirm current costs, hours and HRD Corp eligibility with the provider. Weeks assume your study hours per week.',
      pathProgress: `${fpSteps.filter(x => x.done).length}/${fpSteps.length}`,
      pathProgressW: fpSteps.length ? `${Math.round(100 * fpSteps.filter(x => x.done).length / fpSteps.length)}%` : '0%',
      pathProgressNote: `steps completed · ${Math.round(fpSteps.filter(x => x.done).reduce((a, x) => a + x.hours, 0))} of ${pathHoursNum} hours done`,
      steps: fpSteps,
      weeks: [1, 2, 3, 4, 5, 6].map(w => ({ w, bg: w <= 4 ? (w <= 2 ? "var(--pr)" : "color-mix(in oklch, var(--pr) 60%, var(--sf))") : (w <= 7 ? "var(--sky)" : "var(--up)") })),
       // Signals page. Each list has independent page state; the trend arrays are fully prepared by skill_trends_view.
        ...(() => {
          const words = ({
            en: { automatic: "Automatic updates", frequency: "Frequency", every: "Every 24 hours", last: "Last successful check", next: "Next expected run", unavailable: "Unavailable — best-effort schedule", unavailableStatus: "Unavailable", status: "Status", health: "Health", off: "Off", ai: "AI verification", quarantined: "Held unverified", noPublish: "AI verification is off. No new unverified evidence is published.", published: "Published", evidenceUpdated: "LATEST EVIDENCE", intro: "Curated reports form the baseline. New evidence appears only after validation; unverified evidence stays out of rankings.", previous: "Previous page", nextPage: "Next page", page: "Page", of: "of", noStatus: "Update status is temporarily unavailable.", risingNav: "Rising skills pages", decliningNav: "Declining skills and jobs pages", signalNav: "Signal evidence pages", emptyTrends: "No trend evidence is available yet.", emptySignals: "No signals match this filter." },
            ms: { automatic: "Kemas kini automatik", frequency: "Kekerapan", every: "Setiap 24 jam", last: "Semakan terakhir yang berjaya", next: "Jangkaan semakan seterusnya", unavailable: "Tidak tersedia — jadual usaha terbaik", unavailableStatus: "Tidak tersedia", status: "Status", health: "Kesihatan", off: "Dimatikan", ai: "Pengesahan AI", quarantined: "Ditahan tanpa pengesahan", noPublish: "Pengesahan AI dimatikan. Bukti baharu yang belum disahkan tidak diterbitkan.", published: "Diterbitkan", evidenceUpdated: "BUKTI TERKINI", intro: "Laporan pilihan menjadi asas. Bukti baharu hanya dipaparkan selepas pengesahan; bukti belum disahkan tidak dimasukkan dalam kedudukan.", previous: "Halaman sebelumnya", nextPage: "Halaman seterusnya", page: "Halaman", of: "daripada", noStatus: "Status kemas kini tidak tersedia buat sementara waktu.", risingNav: "Halaman kemahiran meningkat", decliningNav: "Halaman kemahiran dan pekerjaan menurun", signalNav: "Halaman bukti isyarat", emptyTrends: "Bukti trend belum tersedia.", emptySignals: "Tiada isyarat yang sepadan dengan penapis ini." },
            zh: { automatic: "自动更新", frequency: "频率", every: "每 24 小时", last: "最近一次成功检查", next: "预计下次运行", unavailable: "暂不可用 — 尽力安排，非保证时间", unavailableStatus: "不可用", status: "状态", health: "运行状况", off: "已关闭", ai: "AI 验证", quarantined: "未验证内容已暂存", noPublish: "AI 验证已关闭。新的未验证证据不会发布。", published: "发布日期", evidenceUpdated: "最新证据", intro: "精选报告构成基线。新证据只有通过验证后才会显示；未经验证的证据不会影响排名。", previous: "上一页", nextPage: "下一页", page: "第", of: "页，共", noStatus: "更新状态暂时不可用。", risingNav: "上升技能分页", decliningNav: "下降技能和职业分页", signalNav: "信号证据分页", emptyTrends: "暂无趋势证据。", emptySignals: "没有符合此筛选条件的信号。" }
          })[st.lang] || { automatic: "Automatic updates", frequency: "Frequency", every: "Every 24 hours", last: "Last successful check", next: "Next expected run", unavailable: "Unavailable — best-effort schedule", unavailableStatus: "Unavailable", status: "Status", health: "Health", off: "Off", ai: "AI verification", quarantined: "Held unverified", noPublish: "AI verification is off. No new unverified evidence is published.", published: "Published", evidenceUpdated: "LATEST EVIDENCE", intro: "Curated reports form the baseline. New evidence appears only after validation; unverified evidence stays out of rankings.", previous: "Previous page", nextPage: "Next page", page: "Page", of: "of", noStatus: "Update status is temporarily unavailable.", risingNav: "Rising skills pages", decliningNav: "Declining skills and jobs pages", signalNav: "Signal evidence pages", emptyTrends: "No trend evidence is available yet.", emptySignals: "No signals match this filter." };
          const pageMeta = (total, current, prefix) => Array.from({ length: total }, (_, i) => {
            const page = i + 1;
            const isCurrent = page === current;
            return { label: String(page), current: isCurrent ? "page" : "false", isCurrent,
              border: isCurrent ? "var(--pr)" : "var(--ln)", background: isCurrent ? "var(--soft)" : "var(--sf)", color: isCurrent ? "var(--pr)" : "var(--ink)",
              ariaLabel: `${words.page} ${page} ${words.of} ${total}`, change: () => this.setState({ [prefix]: page }) };
          });
          const rising = Array.isArray(out.trRising) ? out.trRising : [], declining = Array.isArray(out.trDecl) ? out.trDecl : [];
          const risingCount = Math.max(1, Math.ceil(rising.length / 5)), decliningCount = Math.max(1, Math.ceil(declining.length / 5));
          const risingPage = Math.min(st.risingPage || 1, risingCount), decliningPage = Math.min(st.decliningPage || 1, decliningCount);
          const signalCount = signals.length, signalPageCount = Math.max(1, Math.ceil(signalCount / 8));
          const signalPage = Math.min(st.signalPage || 1, signalPageCount);
           const knownStatus = st.lang === "ms"
             ? { ok: "Baik", healthy: "Sihat", running: "Sedang berjalan", failed: "Gagal", degraded: "Terjejas", unavailable: "Tidak tersedia", unknown: "Tidak diketahui", best_effort: "Usaha terbaik" }
             : st.lang === "zh"
               ? { ok: "正常", healthy: "健康", running: "运行中", failed: "失败", degraded: "受影响", unavailable: "不可用", unknown: "未知", best_effort: "尽力运行" }
               : { ok: "OK", healthy: "Healthy", running: "Running", failed: "Failed", degraded: "Degraded", unavailable: "Unavailable", unknown: "Unknown", best_effort: "Best effort" };
           const statusLabel = value => {
             if (!value) return words.unavailableStatus;
             const key = String(value).toLowerCase().replace(/[\s-]+/g, "_");
             return knownStatus[key] || String(value).replace(/[_-]+/g, " ").replace(/^\w/, c => c.toUpperCase());
           };
          return {
            signals: signals.slice((signalPage - 1) * 8, signalPage * 8), sigCount: signalCount, sigUpdated, sigLastRun, sigLastRunC, sigFeeds,
            sigStatusTitle: words.automatic, sigFrequencyLabel: words.frequency, sigFrequency: words.every,
            sigLastSuccessLabel: words.last, sigLastSuccess: statusDate(feedStatus?.last_successful_check),
            sigNextLabel: words.next, sigNextExpected: feedStatus?.schedule_guaranteed === false ? words.unavailable : statusDate(feedStatus?.next_expected_run),
            sigStatusLabel: words.status, sigHealthLabel: words.health,
            sigAutoStatus: statusLabel(feedStatus?.status), sigHealth: statusLabel(feedStatus?.health),
            sigAIlabel: words.ai, sigAIStatus: feedStatus?.paid_verification_enabled === true ? (st.lang === "ms" ? "Dihidupkan" : st.lang === "zh" ? "已启用" : "On") : words.off,
            sigQuarantinedLabel: words.quarantined, sigQuarantined: Number.isFinite(Number(feedStatus?.quarantined_count)) ? Number(feedStatus.quarantined_count) : 0,
             sigStatusMessage: feedStatus?.message || words.noStatus, sigNoPublish: words.noPublish,
             sigIntro: words.intro, sigUpdatedLabel: words.evidenceUpdated,
            trRising: rising.slice((risingPage - 1) * 5, risingPage * 5),
            trDecl: declining.slice((decliningPage - 1) * 5, decliningPage * 5),
            risingPages: pageMeta(rising.length ? risingCount : 0, risingPage, "risingPage"),
            decliningPages: pageMeta(declining.length ? decliningCount : 0, decliningPage, "decliningPage"),
            sigPages: pageMeta(signalCount ? signalPageCount : 0, signalPage, "signalPage"),
            hasRisingPages: rising.length > 0, hasDecliningPages: declining.length > 0, hasSigPages: signalCount > 0,
            showRisingEmpty: rising.length === 0, showDecliningEmpty: declining.length === 0, showSignalsEmpty: signalCount === 0,
            risingEmpty: words.emptyTrends, decliningEmpty: words.emptyTrends, signalsEmpty: words.emptySignals,
            sigPublishedLabel: words.published,
            risingPrev: () => this.setState({ risingPage: Math.max(1, risingPage - 1) }),
            risingNext: () => this.setState({ risingPage: Math.min(risingCount, risingPage + 1) }),
            decliningPrev: () => this.setState({ decliningPage: Math.max(1, decliningPage - 1) }),
            decliningNext: () => this.setState({ decliningPage: Math.min(decliningCount, decliningPage + 1) }),
            sigPrev: () => this.setState({ signalPage: Math.max(1, signalPage - 1) }),
            sigNext: () => this.setState({ signalPage: Math.min(signalPageCount, signalPage + 1) }),
            risingPrevDisabled: risingPage <= 1, risingNextDisabled: risingPage >= risingCount,
            decliningPrevDisabled: decliningPage <= 1, decliningNextDisabled: decliningPage >= decliningCount,
            sigPrevDisabled: signalPage <= 1, sigNextDisabled: signalPage >= signalPageCount,
            risingPrevEnabled: risingPage > 1, risingNextEnabled: risingPage < risingCount,
            decliningPrevEnabled: decliningPage > 1, decliningNextEnabled: decliningPage < decliningCount,
            sigPrevEnabled: signalPage > 1, sigNextEnabled: signalPage < signalPageCount,
            paginationPrevious: words.previous, paginationNext: words.nextPage,
            paginationPage: words.page, paginationOf: words.of,
            risingNavLabel: words.risingNav, decliningNavLabel: words.decliningNav, signalNavLabel: words.signalNav,
            fAll: () => this.setState({ sig: "all", signalPage: 1 }), fUp: () => this.setState({ sig: "up", signalPage: 1 }), fDn: () => this.setState({ sig: "dn", signalPage: 1 }),
          };
        })(),
      fAllB: f("all").b, fAllC: f("all").c, fUpB: f("up").b, fUpC: f("up").c, fDnB: f("dn").b, fDnC: f("dn").c
    };
  }
}
