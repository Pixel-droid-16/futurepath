    const GOALS = [["No Poverty","#E5243B"],["Zero Hunger","#DDA63A"],["Good Health","#4C9F38"],["Quality Education","#C5192D"],["Gender Equality","#FF3A21"],["Clean Water","#26BDE2"],["Clean Energy","#FCC30B"],["Decent Work","#A21942"],["Industry & Innovation","#FD6925"],["Reduced Inequalities","#DD1367"],["Sustainable Cities","#FD9D24"],["Responsible Consumption","#BF8B2E"],["Climate Action","#3F7E44"],["Life Below Water","#0A97D9"],["Life on Land","#56C02B"],["Peace & Justice","#00689D"],["Partnerships","#19486A"]];
    // Goals linked to at least one career in the catalogue (role sdgs from the matching API).
    const LIT = [...new Set(st.liveModerate.flatMap(r => r.sdgs || []))];
    const sdgLinkedCount = LIT.length || "—";
    const sdgTiles = GOALS.map(([name, c], i) => { const n = i + 1, on = LIT.includes(n);
      return { n, name, bgImg: "url(assets/sdg/E-WEB-Goal-" + String(n).padStart(2, "0") + ".png) center/cover no-repeat", filter: on ? "none" : "grayscale(1)", op: on ? 1 : 0.35, note: on ? " · linked" : " · not linked yet" }; });
