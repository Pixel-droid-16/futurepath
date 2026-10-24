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
      // Signals page.
       signals, sigCount: signalsTotal, sigUpdated, sigLastRun, sigLastRunC, sigFeeds,
        signalsPages, signalsCurrent, signalsTotal: signalPagesTotal,
        sigNoMatches: signalsTotal === 0, sigNoMatchesLbl: uiText.empty,
        signalsPrev:()=>goSignalsPage(signalsCurrent-1),signalsNext:()=>goSignalsPage(signalsCurrent+1),
        signalsFirst:signalsCurrent===1,signalsLast:signalsCurrent===signalPagesTotal,
        pagerPrevLbl:uiText.previous,pagerNextLbl:uiText.nextButton,pagerPageLbl:uiText.page,pagerOfLbl:uiText.of,
        sigAutoTitle:uiText.auto,sigAutoFrequency,
        sigLastSuccessTitle:uiText.last,sigLastSuccessful,sigNextTitle:uiText.next,sigNextExpected,
        sigHealthTitle:uiText.status,sigHealth,sigAIGuard:uiText.held,
       sigChecked: statusDate(feedStatus?.last_checked), sigDue: statusDate(feedStatus?.next_due),
       sigPending: feedStatus ? Number(feedStatus.pending_count) || 0 : "—",
       sigAutoStatus: feedStatus?.status || (feedStatus ? "unknown" : "Unavailable"),
       sigInterval: feedStatus?.interval_hours ?? "—", sigTagger: feedStatus?.automatic_tagger || "keywords",
        reviewEnabled: st.refreshAccess?.mode === "admin" && !!feedStatus && !feedStatus.public_demo,
       reviewOpen: !!st.reviewOpen, reviewLoading: !!st.reviewLoading, reviewItems: reviewRows,
       reviewTotal: Number(st.reviewTotal) || 0, reviewFilter: st.reviewFilter || "pending", reviewMsg: st.reviewMsg || "",
       loadReviewQueue: () => this.loadReviewQueue(),
        showPendingReview: () => { this.setState({ reviewFilter: "pending" }); this.loadReviewQueueFor("pending"); },
        showApprovedReview: () => { this.setState({ reviewFilter: "approved" }); this.loadReviewQueueFor("approved"); },
        showRejectedReview: () => { this.setState({ reviewFilter: "rejected" }); this.loadReviewQueueFor("rejected"); },
        showAllReview: () => { this.setState({ reviewFilter: "all" }); this.loadReviewQueueFor("all"); },
        closeReview: () => this.setState({ reviewOpen: false, reviewItems: [], reviewTotal: 0 }),
      refreshSignals: () => this.refreshSignals(), reloadSignals: () => this.reloadStoredSignals(),
       adminRefreshAvailable: !!st.refreshAccess?.can_refresh && !!st.signalStatus && !st.signalStatus.public_demo,
      refreshAccessMsg: st.refreshAccess?.message || "Checking refresh permissions…",
      refreshLbl: st.refreshing ? "Working…" : "Admin: refresh live feeds",
      reloadLbl: st.refreshing ? "Loading…" : "Reload saved signals",
      refreshMsg: st.refreshMsg, hasRefreshMsg: !!st.refreshMsg,
      fAll: () => this.setState({ sig: "all", signalsPage: 1 }), fUp: () => this.setState({ sig: "up", signalsPage: 1 }), fDn: () => this.setState({ sig: "dn", signalsPage: 1 }),
      fAllB: f("all").b, fAllC: f("all").c, fUpB: f("up").b, fUpC: f("up").c, fDnB: f("dn").b, fDnC: f("dn").c
    };
  }
}
