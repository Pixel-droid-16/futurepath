class Component extends DCLogic {
  state = { theme: this.props.defaultTheme ?? "light", lang: "en", page: pageFromPath() ?? this.props.startPage ?? "home", fast: false, ws: 55, wd: 45, liveStatus: "loading", liveError: "", liveModerate: [], liveRapid: [], selectedRole: "data-analyst", scenarioComparison: null, profileDemo: null, sig: "all",
    // Start flow (/start): choose -> cv | form -> check -> quiz -> results. Nothing is saved until the quiz step ends.
    startStep: "choose", cvName: "", extracting: false, startError: "", catalog: [],
    form: { role: "", years: 0, qualification: "", languages: "", goals: "" }, formPicked: [], formQuery: "",
    draft: null, draftSource: "", scannedCv: false, addOpen: false, formOpen: false, meta: { name: "My profile", headline: "", years: 0, hours: 6 }, approved: false, addQuery: "",
    quizQuestions: [], quizLikert: [], quizAnswers: {}, saving: false, confirmError: "",
    // Saved people: each finished Start run is a person; activeProfileId is whose results are shown (remembered in this browser).
    people: [], activeProfileId: savedActiveProfile(), editingId: null, confirmDeleteId: null,
    // Trend signals (/api/signals): curated reports plus refreshed feeds; whatChanged explains the latest refresh.
    liveSignals: [], signalRuns: [], whatChanged: null, refreshing: false, refreshMsg: "", skillOutlook: { rising: [], declining: [], updated_at: null, auto_refresh_hours: 0 } };
  componentDidUpdate(p) {
    const q = this.props, u = {};
    if (q.defaultTheme !== p.defaultTheme && q.defaultTheme) u.theme = q.defaultTheme;
    if (q.startPage !== p.startPage && q.startPage && !pageFromPath()) u.page = q.startPage;
    if (Object.keys(u).length) this.setState(u);
  }
  componentDidMount() {
    this._alive = true;
    this._t = setInterval(() => this.setState(s => ({ tick: (s.tick || 0) + 1 })), 1000);
    this._onPop = () => { const p = pageFromPath(); if (p) this.setState({ page: p }); };
    try { window.addEventListener("popstate", this._onPop); } catch (e) {}
    this.refreshLiveCareers();
    this.loadCatalog();
    this.loadSignals();
    this.loadQuiz();
    this.loadPeople();
  }
  async loadSignals() {
    try {
      const [liveSignals, signalRuns, whatChanged, meta, skillOutlook] = await Promise.all([FP_API.json('/api/signals'), FP_API.json('/api/signals/runs'), FP_API.json('/api/what-changed' + this.profileQuery('?')), FP_API.json('/api/meta'), FP_API.json('/api/skill-outlook')]);
      if (this._alive) this.setState({ liveSignals, signalRuns, whatChanged, courseTotal: meta.courses_count, skillOutlook });
    } catch (e) { console.warn('FuturePath: could not load trend signals', e); }
  }
  async refreshSignals() {
    if (this.state.refreshing) return;
    this.setState({ refreshing: true, refreshMsg: 'Fetching feeds and tagging new items… this can take a minute.' });
    try {
      const r = await FP_API.send('/api/signals/refresh', { method: 'POST' });
      if (!this._alive) return;
      this.setState({ refreshing: false, refreshMsg: `Refresh ${r.status}: checked ${r.checked} items, ${r.accepted} new signals, ${r.rejected} rejected, ${r.failed} failed (tagged by ${r.tagger}).` });
      await Promise.all([this.loadSignals(), this.refreshLiveCareers()]);
    } catch (err) {
      if (this._alive) this.setState({ refreshing: false, refreshMsg: 'Refresh failed: ' + String(err.message || err) });
    }
  }
  async refreshLiveCareers() {
    this.setState({liveStatus: 'loading', liveError: ''});
    try {
      const [moderate, rapid, profile] = await Promise.all([
        FP_API.json('/api/matches?scenario=moderate' + this.profileQuery('&')),
        FP_API.json('/api/matches?scenario=rapid' + this.profileQuery('&')),
        FP_API.json(profileUrl(this.state.activeProfileId)),
      ]);
      if (!Array.isArray(moderate) || !Array.isArray(rapid) || !moderate.length || moderate.length !== rapid.length) throw new Error('Invalid career data');
      if (!this._alive) return;
      this.setState({liveModerate: moderate, liveRapid: rapid, profileDemo: profile, liveStatus: 'connected', liveError: ''});
      this.loadScenarioPair(this.state.selectedRole);
    } catch (err) {
      // A remembered person that no longer exists (e.g. a reset database): fall back to the shared profile once.
      if (this.state.activeProfileId && String(err.message).includes(' 404')) { this.setActivePerson(null); return this.refreshLiveCareers(); }
      if (this._alive) this.setState({liveStatus: 'error', liveError: String(err.message || err)});
    }
  }
  profileQuery(sep) { return this.state.activeProfileId ? sep + 'profile=' + encodeURIComponent(this.state.activeProfileId) : ''; }
  setActivePerson(id) { try { id ? localStorage.setItem('fp.activeProfile', id) : localStorage.removeItem('fp.activeProfile'); } catch (e) {} this.setState({ activeProfileId: id }); }
  async loadPeople() {
    try { const people = await FP_API.json('/api/profiles'); if (this._alive) this.setState({ people }); } catch (e) {}
  }
  // Show another saved person's results.
  async switchPerson(id) {
    if (!id || id === this.state.activeProfileId) return;
    this.setActivePerson(id);
    await Promise.all([this.refreshLiveCareers(), this.loadSignals()]);
    if (this.state.page !== 'results') { this.go('start'); this.setStep('results'); }
  }
  async loadScenarioPair(roleId) {
    const token = (this._scenarioRequest || 0) + 1;
    this._scenarioRequest = token;
    this.setState({selectedRole: roleId, scenarioComparison: null});
    try {
      const comparison = await FP_API.json('/api/scenarios/' + encodeURIComponent(roleId) + this.profileQuery('?'));
      if (this._alive && token === this._scenarioRequest) this.setState({scenarioComparison: comparison});
    } catch (err) {
      if (this._alive && token === this._scenarioRequest) this.setState({liveError: String(err.message || err)});
    }
  }
  selectCareer(roleId, openPathway=false) {
    if (!roleId) return;
    this.loadScenarioPair(roleId);
    if (openPathway) this.go('pathway');
  }
  componentWillUnmount() { this._alive = false; clearInterval(this._t); try { window.removeEventListener("popstate", this._onPop); } catch (e) {} }
  go(p) {
    this.setState({ page: p });
    try { if (location.pathname !== PAGE_PATH[p]) history.pushState({ page: p }, "", PAGE_PATH[p]); window.scrollTo(0, 0); } catch (e) {}
  }
  setStep(step) { this.setState({ startStep: step, startError: '', confirmError: '' }); try { window.scrollTo(0, 0); } catch (e) {} }
  // A new person: nothing is overwritten; finishing Start saves them alongside the others.
  startOver() { this._cvFile = null; this.setState(s => ({ draft: null, cvName: '', formPicked: [], quizAnswers: {}, approved: false, editingId: null,
    form: { role: '', years: 0, qualification: '', languages: '', goals: '' }, meta: { name: '', headline: '', years: 0, hours: 6 } })); this.go('start'); this.setStep('choose'); }
  async loadCatalog() {
    try {
      const skills = await FP_API.json('/api/skills');
      if (this._alive) this.setState({ catalog: Array.isArray(skills) ? skills : [] });
    } catch (e) {}
  }
  async loadQuiz() {
    try {
      const quiz = await FP_API.json('/api/interest-quiz');
      if (this._alive) this.setState({ quizQuestions: quiz.questions, quizLikert: quiz.likert });
    } catch (e) {}
  }
  skillName(id) { return (this.state.catalog.find(s => s.id === id) || {}).name || id; }
  // Lowest unused "Person N": people saved under their own names (e.g. a real nickname) don't use up a number.
  newPersonName() {
    if (this.state.editingId) return this.state.meta.name;
    const taken = new Set(this.state.people.map(x => x.name));
    let n = 1; while (taken.has('Person ' + n)) n++;
    return 'Person ' + n;
  }
  // Called from the in-page "Yes, delete" confirmation (native confirm() dialogs are blocked in some browsers, e.g. the app's browser pane).
  async deletePerson(id) {
    this.setState({ confirmDeleteId: null });
    try {
      await FP_API.send('/api/profiles/' + encodeURIComponent(id), { method: 'DELETE' });
      if (!this._alive) return;
      if ((this.state.activeProfileId || 'demo') === id) this.setActivePerson(null);
      await Promise.all([this.loadPeople(), this.refreshLiveCareers(), this.loadSignals()]);
    } catch (err) { if (this._alive) this.setState({ startError: 'Could not delete: ' + String(err.message || err) }); }
  }
  toCheck(draft, draftSource, meta = {}) {
    this.setState(s => ({ draft, draftSource, approved: false, meta: { ...s.meta, ...meta } }));
    this.setStep('check');
  }
  onCvFile(e) {
    const file = e.target.files && e.target.files[0];
    this._cvFile = file || null;
    this.setState({ cvName: file ? file.name : '', startError: '' });
  }
  async readCv() {
    if (!this._cvFile) return this.setState({ startError: 'Choose a PDF first.' });
    this.setState({ extracting: true, startError: '' });
    try {
      const body = new FormData(); body.append('file', this._cvFile); body.append('provider', 'auto');
      const result = await FP_API.send('/api/extract', { method: 'POST', body });
      if (!this._alive) return;
      // A scanned PDF is flagged so the person checks the quotes carefully.
      this.setState({ extracting: false, scannedCv: !!result.scanned });
      this.toCheck((result.candidates || []).map(c => ({ id: c.skill_id, name: c.name, ev: 'Your CV mentions “' + c.excerpt + '”', level: 2 })),
        result.provider === 'dictionary' ? 'keywords' : 'ai', { name: this.newPersonName() });
    } catch (err) {
      if (this._alive) this.setState({ extracting: false, startError: String(err.message || err) });
    }
  }
  useForm() {
    const st = this.state;
    this.setState({ scannedCv: false });
    if (!st.formPicked.length) return this.setState({ startError: 'Add at least one skill.' });
    this.toCheck(st.formPicked.map(id => ({ id, name: this.skillName(id), ev: 'Added in the form', level: 2 })), 'form',
      { name: this.newPersonName(), headline: st.form.role, years: Number(st.form.years) || 0 });
  }
  // Re-open the saved profile at a step (e.g. "Take the quiz" from the results page).
  editProfile(step) {
    const p = this.state.profileDemo || {};
    this.setState(s => ({ draft: Object.entries(p.skills || {}).map(([id, level]) => ({ id, name: this.skillName(id), ev: 'Saved in your profile', level })),
      draftSource: 'saved', approved: true, quizAnswers: p.quiz_answers || {}, editingId: this.state.activeProfileId || 'demo',
      meta: { name: p.name || 'My profile', headline: p.headline || '', years: p.years_experience || 0, hours: p.study_hours || 6 },
      form: { ...s.form, role: p.current_role || '', qualification: p.qualification || '', languages: (p.languages || []).join(', '), goals: p.goals || '' } }));
    this.go('start');
    this.setStep(step);
  }
  toQuiz() {
    const st = this.state;
    if (!(st.draft || []).length) return this.setState({ confirmError: 'Add at least one skill.' });
    if (!st.approved) return this.setState({ confirmError: 'Tick the box to confirm these skills describe you.' });
    this.setStep('quiz');
  }
  async saveProfile(withQuiz) {
    const st = this.state, base = st.profileDemo || {}, langs = st.form.languages.split(',').map(x => x.trim()).filter(Boolean).slice(0, 10);
    const payload = { user_type: base.user_type || 'student', country: base.country || 'Malaysia', interests: base.interests || [], mode: base.mode || 'discover',
      skills: Object.fromEntries(st.draft.map(d => [d.id, d.level])), name: st.meta.name.slice(0, 80), headline: st.meta.headline.slice(0, 160),
      years_experience: Math.max(0, Math.min(60, Number(st.meta.years) || 0)), study_hours: Math.max(1, Math.min(60, Number(st.meta.hours) || 6)),
      current_role: st.form.role.slice(0, 160), qualification: st.form.qualification.slice(0, 160), languages: langs, goals: st.form.goals.slice(0, 1000),
      quiz_answers: withQuiz ? st.quizAnswers : null };
    this.setState({ saving: true, confirmError: '' });
    try {
      // Editing a saved person updates them; otherwise this is a new person, saved alongside the others.
      const editing = st.editingId, json = { headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) };
      const saved = editing ? await FP_API.send(profileUrl(editing), { method: 'PUT', ...json }) : await FP_API.send('/api/profiles', { method: 'POST', ...json });
      if (!this._alive) return;
      this.setActivePerson(saved.id);
      this.setState({ saving: false, editingId: null });
      await Promise.all([this.refreshLiveCareers(), this.loadPeople(), this.loadSignals()]);
      this.setStep('results');
    } catch (err) {
      if (this._alive) this.setState({ saving: false, confirmError: String(err.message || err) });
    }
  }
