    // Pathway (/pathway) for the selected career, from Python/FastAPI results for the active scenario.
    const fpMod = st.scenarioComparison?.moderate || st.liveModerate.find(r => r.role_id === st.selectedRole) || null;
    const fpRapid = st.scenarioComparison?.rapid || st.liveRapid.find(r => r.role_id === st.selectedRole) || null;
    const fpActive = st.fast ? fpRapid : fpMod;
    // The date each course's provider page was checked (catalogue field verification_status: 'checked YYYY-MM-DD').
    const fpCheckedIso = r => ((r && r.verification_status) || '').replace('checked ', '');
    const fpDay = iso => iso ? new Date(iso + 'T00:00:00').toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) : '';
    // Checked courses only (they have a URL), cheapest and shortest first; the rest are listed as alternatives.
    const fpSteps = (fpActive?.pathway || []).slice(0,6).map((item,i) => { const checked = (item.resources || []).filter(r => r.url), course = checked[0];
      return {
      n:i+1, w:`Priority ${i+1}`, cost: course ? course.cost : 'No checked course yet', cb: course && course.cost === 'Free' ? 'var(--upbg)' : 'var(--sf2)', cc: course && course.cost === 'Free' ? 'var(--up)' : 'var(--mu)',
      h: course ? course.duration : 'Duration unknown', hours: course ? course.hours : 0, t:(item.status === 'unknown' ? 'Assess: ' : 'Build: ')+item.skill,
      p:item.status === 'unknown' ? 'Confirm proficiency before treating this as a gap' : 'Learning priority from the current scenario',
      covers:item.why || 'Review skill requirements', lang: course ? course.provider : '—',
      alternatives: checked.slice(1).map(r => ({ title: r.title + ' · ' + r.provider, url: r.url, info: r.cost + ' · ' + r.duration + (fpCheckedIso(r) ? ' · checked ' + fpDay(fpCheckedIso(r)) : '') })), hasAlternatives: checked.length > 1,
      hasCourse: !!course, noCourse: !course, course: course ? course.title : '', checked: course && fpCheckedIso(course) ? 'checked ' + fpDay(fpCheckedIso(course)) : '', checkedIsos: checked.map(fpCheckedIso).filter(Boolean), courseUrl: course ? course.url : '', skill: item.skill,
    }; });
    const studyHours = Math.max(1, Number(st.profileDemo?.study_hours) || 6);
    const pathHoursNum = Math.round(fpSteps.reduce((s, x) => s + x.hours, 0));
    const pathCostSet = new Set(fpSteps.filter(x => x.hasCourse).map(x => x.cost));
    const pathMissing = fpSteps.filter(x => !x.hasCourse).map(x => x.skill);
    const pathChecked = [...new Set(fpSteps.flatMap(x => x.checkedIsos))].sort();
