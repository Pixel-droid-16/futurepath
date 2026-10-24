    // Start (/start): choose -> cv | form -> check -> quiz -> results (results.html renders step 4).
    const LEVELS = [[2, "Basic"], [3, "Working"], [4, "Strong"]];
    const pick = on => on ? { b: "var(--pr)", c: "var(--pri)" } : { b: "transparent", c: "var(--mu)" };
    const match = (s, q) => !q || s.name.toLowerCase().includes(q) || (s.aliases || []).some(a => a.toLowerCase().includes(q));
    const step = st.startStep, stepNo = { choose: 1, cv: 1, form: 1, check: 2, quiz: 3, results: 4 }[step];
    const STEP_LABELS = ["Choose start", "Check profile", "Interest quiz", "Results"];
    const stepper = STEP_LABELS.map((label, i) => { const n = i + 1, done = n < stepNo, active = n === stepNo;
      return { label, mark: done ? "✓" : String(n), c: done ? "var(--up)" : active ? "var(--pr)" : "var(--mu)",
        bg: done ? "var(--upbg)" : active ? "var(--pr)" : "transparent", fg: active ? "var(--pri)" : "inherit", bd: done || active ? "0" : "1.5px solid var(--ln)",
        line: n < 4, lineC: n < stepNo ? "var(--up)" : "var(--ln)" }; });
    const startTiles = [
      { icon: "PDF", t: "Upload a CV", d: "PDF, up to 2 MB. Skills are matched to our catalog for you to check.", choose: () => this.setStep("cv") },
      { icon: "✎", t: "Fill a short form", d: "Pick your skills from a list. Takes about 3 minutes.", choose: () => this.setStep("form") }];
    const prof = st.profileDemo || {};
    // Saved people (/api/profiles), newest first; "See results" switches the active person.
    const fmtDay = d => { try { return new Date(d).toLocaleDateString(fpIntlLocale(st.lang), { day: "numeric", month: "short" }); } catch (e) { return ""; } };
    const peopleRows = st.people.map(x => ({ name: x.name, sub: [x.headline, x.skills + " skills", x.has_quiz ? "quiz done" : "no quiz", x.updated_at ? "saved " + fmtDay(x.updated_at) : ""].filter(Boolean).join(" · "),
      open: () => { this.switchPerson(x.id); this.go("start"); this.setStep("results"); }, asking: st.confirmDeleteId === x.id, notAsking: st.confirmDeleteId !== x.id,
      ask: () => this.setState({ confirmDeleteId: x.id }), cancel: () => this.setState({ confirmDeleteId: null }), confirm: () => this.deletePerson(x.id) }));
    const setForm = k => e => { const v = e.target.value; this.setState(x => ({ form: { ...x.form, [k]: v, ...(k === "qualification" ? { qualificationLegacy: "" } : {}) }, startError: "" })); };
    const setMeta = k => e => { const v = e.target.value; this.setState(x => ({ meta: { ...x.meta, [k]: v } })); };
    const commonStudyHours = [3, 6, 10, 15], selectedHours = Number(st.meta.hours) || 6;
    const studyHourOptions = [...new Set([...commonStudyHours, selectedHours])].sort((a, b) => a - b)
      .map(value => { const selected = selectedHours === value; return { value, label: `${value} hours/week${commonStudyHours.includes(value) ? "" : " (current)"}`, pressed: selected ? "true" : "false",
        b: selected ? "var(--pr)" : "var(--sf)", c: selected ? "var(--pri)" : "var(--ink)", bd: selected ? "var(--pr)" : "var(--ln)",
        select: () => this.setState(x => ({ meta: { ...x.meta, hours: value } })) }; });
    const fq = st.formQuery.trim().toLowerCase();
    const formChosen = st.formPicked.map(id => ({ name: this.skillName(id), remove: () => this.setState(x => ({ formPicked: x.formPicked.filter(i => i !== id) })) }));
    // Clicking a "+ Search skills…" box opens the whole catalogue (A-Z); typing filters it. It stays open to add several.
    const byName = (a, b) => a.name.localeCompare(b.name);
    const formResults = st.formOpen || fq ? st.catalog.filter(s => match(s, fq) && !st.formPicked.includes(s.id)).sort(byName).map(s => ({ name: s.name,
      add: () => this.setState(x => ({ formPicked: [...x.formPicked, s.id], formQuery: "", startError: "" })) })) : [];
    const draft = st.draft || [];
    const setLevel = (id, level) => this.setState(x => ({ draft: x.draft.map(d => d.id === id ? { ...d, level } : d), approved: false }));
    const draftRows = draft.map(d => ({ name: d.name, ev: d.ev,
      levels: LEVELS.map(([v, label]) => { const c = pick(d.level === v); return { label, b: c.b, c: c.c, set: () => setLevel(d.id, v) }; }),
      remove: () => this.setState(x => ({ draft: x.draft.filter(k => k.id !== d.id), approved: false })) }));
    const aq = st.addQuery.trim().toLowerCase();
    const addOptions = st.addOpen || aq ? st.catalog.filter(s => match(s, aq) && !draft.some(d => d.id === s.id)).sort(byName).map(s => ({ name: s.name,
      add: () => this.setState(x => ({ draft: [...(x.draft || []), { id: s.id, name: s.name, ev: "Added by you", level: 2 }], addQuery: "", approved: false })) })) : [];
    const hints = st.draftSource === 'ai' ? (st.profileHints || {}) : {};
    const profileHintRows = [
      ['Current role', hints.current_role],
      ['Education (may be in progress)', hints.education],
      ['Highest completed qualification (confirm)', hints.completed_qualification],
      ['Industry', hints.industry],
    ].filter(x => x[1]?.value).map(([title, item]) => ({
      title, value: item.value, evidence: item.excerpt,
    }));
    const projectHints = (hints.projects || []).slice(0, 6).map(item => ({
      value: item.value, evidence: item.excerpt,
    }));
    const achievementHints = (hints.achievements || []).slice(0, 4).map(item => ({
      value: item.value, evidence: item.excerpt,
    }));
    const certificationHints = (hints.certifications || []).slice(0, 4).map(item => ({
      value: item.value, evidence: item.excerpt,
    }));
    const hasProfileHints = profileHintRows.length > 0 || projectHints.length > 0
      || achievementHints.length > 0 || certificationHints.length > 0;
    const aiCount = st.sourceCounts?.ai || 0;
    const dictionaryCount = st.sourceCounts?.dictionary || 0;
    const draftNote = { ai: st.scannedCv
      ? "Claude reviewed a PDF with little or no extractable text, and the local dictionary checked its transcription. Verify the suggested details, skills and evidence."
      : st.extractionProvider === "runpod"
        ? aiCount
          ? `Qwen on RunPod suggested ${aiCount} skills; the local dictionary added ${dictionaryCount} more. Review all evidence and proficiency levels.`
          : `Qwen completed analysis but returned no validated skill suggestions. The local dictionary found ${dictionaryCount} possible skills; review them carefully.`
        : "Claude and the local dictionary suggested skills from your CV. Review their evidence and choose each proficiency level.",
      keywords: "Skills matched by the local dictionary, not GPU AI. Review every suggestion carefully.",
      form: "Skills you added in the form. Set how strong each one is.", saved: "These are the skills saved in your profile." }[st.draftSource] || "Add the skills you have.";
    const quizDone = st.quizQuestions.filter(q => st.quizAnswers[q.id]).length, quizTotal = st.quizQuestions.length || 18;
    const quizRows = st.quizQuestions.map((q, i) => ({ n: i + 1, text: q.text, options: st.quizLikert.map(l => { const on = st.quizAnswers[q.id] === l.value;
      return { label: l.label, b: on ? "var(--pr)" : "var(--sf)", c: on ? "var(--pri)" : "var(--ink)", bd: on ? "var(--pr)" : "var(--ln)",
        pick: () => this.setState(x => ({ quizAnswers: { ...x.quizAnswers, [q.id]: l.value }, confirmError: "" })) }; }) }));
    const quizComplete = st.quizQuestions.length > 0 && quizDone === st.quizQuestions.length;
    const startBindings = { showStartFlow: st.page === "start" && step !== "results", stepNo, stepper, startTiles,
      isChoose: step === "choose", isCvStep: step === "cv", isFormStep: step === "form", isCheckStep: step === "check", isQuizStep: step === "quiz",
      hasPeople: peopleRows.length > 0, peopleCount: peopleRows.length, peopleRows, backToChoose: () => this.setStep("choose"),
      cvPickLbl: st.cvName || "Choose a PDF", onCvFile: e => this.onCvFile(e), readCv: () => { if (!st.extracting && st.cvName) this.readCv(); },
      readLbl: st.extracting ? "Extracting skills (GPU may be starting)…" : "Read my CV", readOp: st.cvName && !st.extracting ? "1" : ".45",
      fRole: st.form.role, fYears: st.form.years, fQual: st.form.qualification, fIndustry: st.form.industry, fInterests: st.form.interests,
      fAiComfort: st.form.aiComfort, fArrangement: st.form.workArrangement, fMotivation: st.form.motivation,
      fLangs: st.form.languages, fGoals: st.form.goals, studyHourOptions,
      onFRole: setForm("role"), onFYears: setForm("years"), onFQual: setForm("qualification"), onFIndustry: setForm("industry"),
      onFInterests: setForm("interests"), onFAiComfort: setForm("aiComfort"), onFArrangement: setForm("workArrangement"),
      onFMotivation: setForm("motivation"), onFLangs: setForm("languages"), onFGoals: setForm("goals"),
      formEmpty: !st.formPicked.length, formChosen, formResults, hasFormResults: formResults.length > 0, formListOpen: st.formOpen, openFormList: () => this.setState({ formOpen: true }), closeFormList: () => this.setState({ formOpen: false, formQuery: "" }),
      formNoMatch: (st.formOpen || !!fq) && !formResults.length, formQuery: st.formQuery, onFormQuery: e => this.setState({ formQuery: e.target.value }),
      useForm: () => this.useForm(), formOp: st.formPicked.length ? "1" : ".45",
      draftNote, hasProfileHints, profileHintRows, projectHints, achievementHints, certificationHints, draftRows, hasAddOptions: addOptions.length > 0, addListOpen: st.addOpen, openAddList: () => this.setState({ addOpen: true }), closeAddList: () => this.setState({ addOpen: false, addQuery: "" }),
      addNoMatch: (st.addOpen || !!aq) && !addOptions.length, draftCount: draft.length, addQuery: st.addQuery, onAddQuery: e => this.setState({ addQuery: e.target.value }), addOptions,
      mName: st.meta.name, mYears: st.meta.years,
      isCvDraft: st.draftSource !== "form",
      onMName: setMeta("name"), onMYears: setMeta("years"),
      approved: st.approved, toggleApproved: () => this.setState(x => ({ approved: !x.approved, confirmError: "" })),
      backFromCheck: () => this.setStep(st.draftSource === "form" ? "form" : st.draftSource === "saved" ? "choose" : "cv"),
      toQuiz: () => this.toQuiz(), quizOp: st.approved && draft.length && (st.draftSource !== 'ai' || draft.every(d => [2, 3, 4].includes(d.level))) ? "1" : ".45",
      quizRows, quizDone, quizTotal, quizPct: Math.round(100 * quizDone / quizTotal) + "%", backToCheck: () => this.setStep("check"),
      skipQuiz: () => { if (!st.saving) this.saveProfile(false); }, finishQuiz: () => { if (!st.saving && quizComplete) this.saveProfile(true); },
      finishLbl: st.saving ? "Saving…" : "See my results →", finishOp: quizComplete && !st.saving ? "1" : ".45",
      confirmError: st.confirmError, hasConfirmError: !!st.confirmError, startError: st.startError, hasStartError: !!st.startError };
