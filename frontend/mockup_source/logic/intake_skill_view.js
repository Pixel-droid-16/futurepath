const lvl = (a, b) => a === b ? { b: "var(--pr)", c: "var(--pri)" } : { b: "transparent", c: "var(--mu)" };
    const skills = SK.filter(s => !st.removed.includes(s[0])).map(([name, ev, lv]) => {
      const a = lvl(lv, 1), b = lvl(lv, 2), c = lvl(lv, 3);
      return { name, ev, b1: a.b, c1: a.c, b2: b.b, c2: b.c, b3: c.b, c3: c.c, remove: () => this.setState(s => ({ removed: [...s.removed, name] })) };
    });
