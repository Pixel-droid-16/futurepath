    const liveRecords = st.fast ? st.liveRapid : st.liveModerate;
    const ranked = (st.liveStatus === 'connected' ? liveRecords : []).map(r => FP_API.card(r, st.ws, st.wd))
      .sort((a,b)=>b.score-a.score).map((r,i)=>({...r,rank:i+1,
        goPathway:()=>this.selectCareer(r.id,true)}));
    const on = { bg: "var(--sf)", fg: "var(--ink)" }, off = { bg: "transparent", fg: "var(--mu)" };
    const m = st.fast ? off : on, f2 = st.fast ? on : off;
