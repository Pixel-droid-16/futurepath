    // Home "What's rising, what's fading": net skill outlook from stored signals (/api/skill-outlook).
    const radarUp = st.skillOutlook.rising.map(k => ({ t: k.name, w: k.width + "%" }));
    const radarDn = st.skillOutlook.declining.map(k => ({ t: k.name, w: k.width + "%" }));
    // When the live feeds were last pulled, and the automatic schedule (SIGNALS_REFRESH_HOURS on the server).
    const fpWhen = iso => new Date(iso).toLocaleString(fpIntlLocale(st.lang), { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });
    const fpEvery = st.skillOutlook.auto_refresh_hours ? (st.skillOutlook.auto_refresh_hours === 24 ? "daily" : `every ${st.skillOutlook.auto_refresh_hours} h`) : "";
    const radarUpdated = (st.skillOutlook.updated_at ? `Live feeds last checked ${fpWhen(st.skillOutlook.updated_at)}` : "Live feeds not checked yet; showing dated reports only")
      + (fpEvery ? ` · refreshes automatically ${fpEvery}` : " · refreshed manually");
