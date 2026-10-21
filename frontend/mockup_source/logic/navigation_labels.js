const PAGES = ["home","start","results","pathway","signals","about"];
const PAGE_PATH = { home: "/", start: "/start", results: "/results", pathway: "/pathway", signals: "/signals", about: "/about" };
const pageFromPath = () => { try { const p = location.pathname.replace(/\/+$/, "") || "/"; return PAGES.find(k => PAGE_PATH[k] === p); } catch (e) { return undefined; } };
const T = { en: { home: "Home", start: "Start", results: "Results", pathway: "Pathway", signals: "Signals", about: "About", cta: "Start free →" }, ms: { home: "Utama", start: "Mula", results: "Keputusan", pathway: "Laluan", signals: "Isyarat", about: "Perihal", cta: "Mula percuma →" } };
// Saved people: 'demo' is the original shared profile; other ids come from POST /api/profiles.
const profileUrl = id => !id || id === 'demo' ? '/api/profile' : '/api/profiles/' + encodeURIComponent(id);
const savedActiveProfile = () => { try { return localStorage.getItem('fp.activeProfile') || null; } catch (e) { return null; } };
