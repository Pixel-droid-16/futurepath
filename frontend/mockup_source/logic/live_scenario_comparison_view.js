    // These results come from Python/FastAPI, not from the original static mockup arrays.
    const fpMod = st.scenarioComparison?.moderate || st.liveModerate.find(r => r.role_id === st.selectedRole) || null;
    const fpRapid = st.scenarioComparison?.rapid || st.liveRapid.find(r => r.role_id === st.selectedRole) || null;
    const fpModView = FP_API.summary(fpMod), fpRapidView = FP_API.summary(fpRapid);
    const fpActive = st.fast ? fpRapid : fpMod;
    const fpActiveView = st.fast ? fpRapidView : fpModView;
    const fpTasks = fpModView.tasks.map((task,i) => ({
      name: task.task,
      moderate: task.adoption_impact,
      rapid: fpRapidView.tasks[i]?.adoption_impact || 'Not available',
      oversight: `${task.human_oversight}/100 (assumption)`,
    }));
    const fpSteps = (fpActive?.pathway || []).slice(0,6).map((item,i) => ({
      n:i+1, w:`Priority ${i+1}`, cost:'Resource unverified', cb:'var(--sf2)', cc:'var(--mu)',
      h:'Duration unknown', t:(item.status === 'unknown' ? 'Assess: ' : 'Build: ')+item.skill,
      p:item.status === 'unknown' ? 'Confirm proficiency before treating this as a gap' : 'Learning priority from the current scenario',
      covers:item.why || 'Review skill requirements', lang:'—',
    }));
    const fpOptions = st.liveModerate.map(r => ({id:r.role_id,title:r.title,selected:r.role_id === st.selectedRole}));
