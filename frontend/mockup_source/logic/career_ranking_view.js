    const liveRecords = st.fast ? st.liveRapid : st.liveModerate;
    const ranked = (st.liveStatus === 'connected' ? liveRecords : []).map(r => FP_API.card(r, st.ws, st.wd))
      .sort((a,b)=>b.exact-a.exact).map((r,i)=>({...r,rank:i+1,
        goPathway:()=>this.selectCareer(r.id,true)}));
    const on = { bg: "var(--pr)", fg: "var(--pri)" }, off = { bg: "transparent", fg: "var(--ink)" };
    const m = st.fast ? off : on, f2 = st.fast ? on : off;
