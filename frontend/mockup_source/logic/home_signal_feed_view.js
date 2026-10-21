    const FEED = [
      { dir: "↑", kind: "Emerging", t: "Solar installation roles and vocational teachers expected to grow", src: "Demo · synthetic", roles: "Solar PV Technician, Skills Trainer", c: "var(--up)", bg: "var(--upbg)" },
      { dir: "↓", kind: "Declining", t: "Data entry, secretarial and bookkeeping roles declining in every edition since 2016", src: "Demo · synthetic", roles: "Data Entry Clerk, Admin Assistant", c: "var(--dn)", bg: "var(--dnbg)" },
      { dir: "↑", kind: "Emerging", t: "Malaysia launches National AI Office to coordinate AI adoption, governance and talent", src: "Demo · synthetic", roles: "Responsible AI Specialist", c: "var(--up)", bg: "var(--upbg)" },
      { dir: "↑", kind: "Emerging", t: "Malaysia's green jobs expected to grow about tenfold by 2050, mostly in solar", src: "Demo · synthetic", roles: "Renewable Energy Engineer", c: "var(--up)", bg: "var(--upbg)" },
      { dir: "↑", kind: "Emerging", t: "Care economy jobs expected to grow significantly as populations age", src: "Demo · synthetic", roles: "Elderly & Personal Care Aide", c: "var(--up)", bg: "var(--upbg)" },
      { dir: "↓", kind: "Declining", t: "Client information and customer service workers among largest-declining jobs", src: "Demo · synthetic", roles: "Customer Service Worker", c: "var(--dn)", bg: "var(--dnbg)" }
    ];
    const tk = st.tick || 0, CYC = 5, li = Math.floor(tk / CYC) % FEED.length;
    const now = new Date();
    let clock = ""; try { clock = now.toLocaleTimeString("en-GB", { timeZone: "Asia/Kuala_Lumpur", hour: "2-digit", minute: "2-digit", second: "2-digit" }); } catch (e) { clock = now.toTimeString().slice(0, 8); }
    const mins = 12 + Math.floor(tk / 60);
