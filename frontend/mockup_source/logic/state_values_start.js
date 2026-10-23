  renderVals() {
    const st = this.state, out = {};
    PAGES.forEach(p => { const a = st.page === p; out["is_" + p] = a; out["go_" + p] = () => this.go(p); out["nb_" + p] = a ? "var(--sf)" : "transparent"; out["nc_" + p] = a ? "var(--ink)" : "var(--mu)"; out["t_" + p] = T[st.lang][p]; });
    out.t_cta = T[st.lang].cta;
    const sum = (st.ws + st.wd) || 1, ws = st.ws / sum, wd = st.wd / sum;
