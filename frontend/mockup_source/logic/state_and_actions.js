class Component extends DCLogic {
  state = { theme: this.props.defaultTheme ?? "light", lang: "en", page: this.props.startPage ?? "home", fast: false, ws: 69, wd: 31, liveStatus: "loading", liveError: "", liveModerate: [], liveRapid: [], selectedRole: "data-analyst", scenarioComparison: null, profileDemo: null, incDecl: false, removed: [], sig: "all", auth: "login", showPw: false };
  componentDidUpdate(p) {
    const q = this.props, u = {};
    if (q.defaultTheme !== p.defaultTheme && q.defaultTheme) u.theme = q.defaultTheme;
    if (q.startPage !== p.startPage && q.startPage) u.page = q.startPage;
    if (Object.keys(u).length) this.setState(u);
  }
  componentDidMount() {
    this._alive = true;
    this._t = setInterval(() => this.setState(s => ({ tick: (s.tick || 0) + 1 })), 1000);
    this.refreshLiveCareers();
  }
  async refreshLiveCareers() {
    this.setState({liveStatus: 'loading', liveError: ''});
    try {
      const [moderate, rapid, profile] = await Promise.all([
        FP_API.json('/api/matches?scenario=moderate'),
        FP_API.json('/api/matches?scenario=rapid'),
        FP_API.json('/api/profile'),
      ]);
      if (!Array.isArray(moderate) || !Array.isArray(rapid) || !moderate.length || moderate.length !== rapid.length) throw new Error('Invalid career data');
      if (!this._alive) return;
      this.setState({liveModerate: moderate, liveRapid: rapid, profileDemo: profile, liveStatus: 'connected', liveError: ''});
      this.loadScenarioPair(this.state.selectedRole);
    } catch (err) {
      if (this._alive) this.setState({liveStatus: 'error', liveError: String(err.message || err)});
    }
  }
  async loadScenarioPair(roleId) {
    const token = (this._scenarioRequest || 0) + 1;
    this._scenarioRequest = token;
    this.setState({selectedRole: roleId, scenarioComparison: null});
    try {
      const comparison = await FP_API.json('/api/scenarios/' + encodeURIComponent(roleId));
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
  componentWillUnmount() { this._alive = false; clearInterval(this._t); }
  go(p) { this.setState({ page: p }); try { window.scrollTo(0, 0); } catch (e) {} }
