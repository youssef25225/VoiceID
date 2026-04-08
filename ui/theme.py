# -*- coding: utf-8 -*-
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap');

/* ═══════════════════════════════════════════════════════════
   DESIGN TOKENS
═══════════════════════════════════════════════════════════ */
:root {
  --ff-display: 'Syne', system-ui, sans-serif;
  --ff-body:    'Syne', system-ui, sans-serif;
  --ff-arabic:  'IBM Plex Sans Arabic', system-ui, sans-serif;
  --ff-mono:    'IBM Plex Mono', monospace;

  --sz-2xs: 10px; --sz-xs: 12px; --sz-sm: 13px; --sz-md: 15px;
  --sz-lg: 18px;  --sz-xl: 24px; --sz-2xl: 36px; --sz-3xl: 56px;

  --r-xs: 4px;  --r-sm: 8px;  --r-md: 12px;
  --r-lg: 18px; --r-xl: 24px; --r-full: 9999px;

  /* Spacing */
  --sp-1: 4px; --sp-2: 8px; --sp-3: 12px;
  --sp-4: 16px; --sp-5: 24px; --sp-6: 32px; --sp-7: 48px;
}

/* ── Colour palette (dark-first, light override) ── */
:root {
  --bg:       #0a0a0b;
  --bg2:      #111114;
  --surface:  #16161a;
  --surface2: #1e1e24;
  --surface3: #26262e;
  --surface4: #2e2e38;

  --border:        rgba(255,255,255,.06);
  --border-md:     rgba(255,255,255,.10);
  --border-strong: rgba(255,255,255,.18);

  --ink:  #f0eff6;
  --ink2: #9b99aa;
  --ink3: #5e5d6e;
  --ink4: #3a3948;

  /* Accent — electric violet */
  --accent:       #7c6fff;
  --accent-dim:   rgba(124, 111, 255, .15);
  --accent-border:rgba(124, 111, 255, .35);

  /* Semantic */
  --green:        #34d399;
  --green-bg:     rgba(52, 211, 153, .10);
  --green-border: rgba(52, 211, 153, .28);

  --red:        #f87171;
  --red-bg:     rgba(248, 113, 113, .10);
  --red-border: rgba(248, 113, 113, .28);

  --amber:        #fbbf24;
  --amber-bg:     rgba(251, 191, 36, .10);
  --amber-border: rgba(251, 191, 36, .28);

  --blue:        #60a5fa;
  --blue-bg:     rgba(96, 165, 250, .10);
  --blue-border: rgba(96, 165, 250, .28);
}

/* Light mode override */
@media (prefers-color-scheme: light) {
  :root {
    --bg:       #f5f4f8;
    --bg2:      #ededf2;
    --surface:  #ffffff;
    --surface2: #f0eff6;
    --surface3: #e6e5ef;
    --surface4: #dddce8;

    --border:        rgba(0,0,0,.07);
    --border-md:     rgba(0,0,0,.11);
    --border-strong: rgba(0,0,0,.20);

    --ink:  #0f0e17;
    --ink2: #4a4860;
    --ink3: #8b89a0;
    --ink4: #c0bfd0;

    --accent:        #6c5ce7;
    --accent-dim:    rgba(108, 92, 231, .12);
    --accent-border: rgba(108, 92, 231, .30);
  }
}

/* ═══════════════════════════════════════════════════════════
   BASE RESET
═══════════════════════════════════════════════════════════ */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
  background: var(--bg) !important;
  color: var(--ink) !important;
  font-family: var(--ff-body) !important;
}

[data-testid="stToolbar"],
[data-testid="stDecoration"],
footer, header { display: none !important; }

[data-testid="stAppViewContainer"] > .main > .block-container {
  padding: 0 2rem 5rem !important;
  max-width: 1060px !important;
}

/* ═══════════════════════════════════════════════════════════
   APP HEADER
═══════════════════════════════════════════════════════════ */
.app-header {
  padding: 2.4rem 0 1.8rem;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.2rem;
  border-bottom: 1px solid var(--border-md);
  position: relative;
}

.app-header::before {
  content: '';
  position: absolute;
  bottom: -1px; left: 0;
  width: 64px; height: 2px;
  background: var(--accent);
  border-radius: 2px;
}

.app-wordmark {
  display: flex; align-items: center; gap: 12px;
}

.app-icon {
  width: 40px; height: 40px;
  background: var(--accent-dim);
  border: 1px solid var(--accent-border);
  border-radius: var(--r-md);
  display: flex; align-items: center; justify-content: center;
  font-size: 20px;
}

.app-title {
  font-size: var(--sz-xl);
  font-weight: 700;
  color: var(--ink);
  letter-spacing: -.03em;
  font-family: var(--ff-display);
}

.app-subtitle {
  font-size: var(--sz-xs);
  color: var(--ink3);
  font-family: var(--ff-mono);
  margin-top: 2px;
}

.header-pills {
  display: flex; gap: 8px; align-items: center; flex-wrap: wrap;
}

.pill {
  padding: 5px 12px;
  border-radius: var(--r-full);
  font-size: var(--sz-xs);
  font-family: var(--ff-mono);
  font-weight: 500;
  border: 1px solid var(--border-md);
  background: var(--surface2);
  color: var(--ink2);
  display: flex; align-items: center; gap: 5px;
  transition: all .2s;
}
.pill::before {
  content: '';
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--ink4);
}
.pill.active::before { background: var(--green); box-shadow: 0 0 6px var(--green); }
.pill.active {
  background: var(--green-bg);
  border-color: var(--green-border);
  color: var(--green);
}

/* ═══════════════════════════════════════════════════════════
   STEPPER
═══════════════════════════════════════════════════════════ */
.stepper {
  display: flex; gap: 6px; margin-bottom: 2rem;
  background: var(--surface);
  border: 1px solid var(--border-md);
  border-radius: var(--r-lg);
  padding: 6px;
}

.step-btn {
  flex: 1;
  display: flex; align-items: center; gap: 10px;
  padding: 12px 16px;
  border-radius: var(--r-md);
  transition: background .2s;
}

.step-btn.active {
  background: var(--surface3);
  box-shadow: 0 1px 3px rgba(0,0,0,.15), 0 0 0 1px var(--border-md);
}

.step-btn.done {
  background: var(--green-bg);
}

.step-badge {
  width: 26px; height: 26px;
  border-radius: var(--r-sm);
  display: flex; align-items: center; justify-content: center;
  font-size: var(--sz-xs);
  font-weight: 700;
  font-family: var(--ff-mono);
  flex-shrink: 0;
}

.step-btn.done   .step-badge { background: var(--green);   color: #000; }
.step-btn.active .step-badge { background: var(--accent);  color: #fff; }
.step-btn.idle   .step-badge { background: var(--surface3); color: var(--ink3); }

.step-name {
  font-size: var(--sz-sm);
  font-weight: 600;
  color: var(--ink);
}
.step-btn.idle .step-name { color: var(--ink3); }

.step-hint {
  font-size: var(--sz-2xs);
  color: var(--ink3);
  margin-top: 2px;
  font-family: var(--ff-mono);
}

/* ═══════════════════════════════════════════════════════════
   RESULT CARD
═══════════════════════════════════════════════════════════ */
.result-card {
  border-radius: var(--r-xl);
  padding: 2.4rem 2rem 2rem;
  text-align: center;
  border: 1px solid;
  position: relative;
  overflow: hidden;
  margin: var(--sp-4) 0;
}

/* Glow blob */
.result-card::before {
  content: '';
  position: absolute;
  top: -60px; left: 50%;
  transform: translateX(-50%);
  width: 200px; height: 120px;
  border-radius: 50%;
  filter: blur(40px);
  opacity: .35;
  pointer-events: none;
}

.result-card.match {
  background: var(--green-bg);
  border-color: var(--green-border);
}
.result-card.match::before { background: var(--green); }

.result-card.unknown {
  background: var(--red-bg);
  border-color: var(--red-border);
}
.result-card.unknown::before { background: var(--red); }

.result-eyebrow {
  font-size: var(--sz-2xs);
  font-family: var(--ff-mono);
  letter-spacing: .18em;
  text-transform: uppercase;
  margin-bottom: var(--sp-2);
}
.result-card.match   .result-eyebrow { color: var(--green); }
.result-card.unknown .result-eyebrow { color: var(--red); }

.result-name {
  font-size: var(--sz-3xl);
  font-weight: 800;
  letter-spacing: -.04em;
  margin-bottom: var(--sp-3);
  font-family: var(--ff-display);
  line-height: 1.0;
}
.result-card.match   .result-name { color: var(--green); }
.result-card.unknown .result-name { color: var(--red); }

.result-meta {
  font-size: var(--sz-xs);
  font-family: var(--ff-mono);
  color: var(--ink3);
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}
.result-meta b { color: var(--ink2); }

.conf-track {
  width: 50%;
  height: 3px;
  background: var(--border-md);
  border-radius: 2px;
  margin: var(--sp-4) auto 0;
  overflow: hidden;
}
.conf-fill {
  height: 100%;
  border-radius: 2px;
  transition: width .6s cubic-bezier(.34,1.56,.64,1);
}
.conf-fill.match   { background: var(--green); }
.conf-fill.unknown { background: var(--red); }

/* ═══════════════════════════════════════════════════════════
   VOTE BARS
═══════════════════════════════════════════════════════════ */
.vote-row {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
}
.vote-row:last-child { border-bottom: none; }

.vote-name {
  font-size: var(--sz-sm);
  font-family: var(--ff-mono);
  color: var(--ink2);
  min-width: 110px;
}
.vote-track {
  flex: 1;
  background: var(--surface3);
  border-radius: 3px;
  height: 6px;
  overflow: hidden;
}
.vote-fill {
  height: 100%;
  border-radius: 3px;
  background: var(--accent-dim);
  border: 1px solid var(--accent-border);
  transition: width .5s ease;
}
.vote-fill.winner {
  background: var(--green);
  border-color: transparent;
}
.vote-pct {
  font-size: var(--sz-xs);
  font-family: var(--ff-mono);
  color: var(--ink3);
  min-width: 34px;
  text-align: right;
}

/* ═══════════════════════════════════════════════════════════
   LOG ITEMS
═══════════════════════════════════════════════════════════ */
.log-item {
  display: grid;
  grid-template-columns: 1fr auto auto;
  align-items: center;
  gap: var(--sp-3);
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
}
.log-item:last-child { border-bottom: none; }
.log-name { font-size: var(--sz-sm); font-family: var(--ff-mono); }
.log-k    { font-size: var(--sz-2xs); font-family: var(--ff-mono); color: var(--ink4); }
.log-conf { font-size: var(--sz-2xs); font-family: var(--ff-mono); text-align: right; color: var(--ink3); }

/* ═══════════════════════════════════════════════════════════
   SECTION HEADERS
═══════════════════════════════════════════════════════════ */
.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 1rem;
  font-size: var(--sz-sm);
  font-weight: 600;
  font-family: var(--ff-display);
  color: var(--ink);
  text-transform: uppercase;
  letter-spacing: .08em;
}
.section-header::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border-md);
}

/* ═══════════════════════════════════════════════════════════
   SPEAKER GRID
═══════════════════════════════════════════════════════════ */
.speaker-card {
  background: var(--surface);
  border: 1px solid var(--border-md);
  border-radius: var(--r-lg);
  padding: 14px 16px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 14px;
  transition: border-color .2s;
}
.speaker-card:hover { border-color: var(--border-strong); }

.speaker-avatar {
  width: 40px; height: 40px;
  border-radius: var(--r-md);
  background: var(--accent-dim);
  border: 1px solid var(--accent-border);
  display: flex; align-items: center; justify-content: center;
  font-size: var(--sz-sm);
  font-weight: 700;
  font-family: var(--ff-mono);
  color: var(--accent);
  flex-shrink: 0;
}
.speaker-card.ready .speaker-avatar {
  background: var(--green-bg);
  border-color: var(--green-border);
  color: var(--green);
}

.speaker-info { flex: 1; min-width: 0; }
.speaker-name {
  font-size: var(--sz-sm);
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.progress-bar {
  height: 4px;
  background: var(--surface3);
  border-radius: 2px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  border-radius: 2px;
  transition: width .5s ease;
}
.progress-fill.ready   { background: var(--green); }
.progress-fill.partial { background: var(--amber); }

.speaker-meta {
  font-size: var(--sz-2xs);
  font-family: var(--ff-mono);
  color: var(--ink3);
  margin-top: 5px;
  display: flex;
  gap: 10px;
}

.status-dot {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--sz-2xs);
  font-family: var(--ff-mono);
  padding: 3px 8px;
  border-radius: var(--r-full);
}
.status-dot.ready   { background: var(--green-bg); color: var(--green); border: 1px solid var(--green-border); }
.status-dot.partial { background: var(--amber-bg); color: var(--amber); border: 1px solid var(--amber-border); }
.status-dot::before {
  content: '';
  width: 5px; height: 5px;
  border-radius: 50%;
  background: currentColor;
}

/* ═══════════════════════════════════════════════════════════
   BADGE
═══════════════════════════════════════════════════════════ */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--sz-2xs);
  font-family: var(--ff-mono);
  font-weight: 500;
  padding: 3px 8px;
  border-radius: var(--r-full);
}
.badge.green { background: var(--green-bg); color: var(--green); border: 1px solid var(--green-border); }
.badge.amber { background: var(--amber-bg); color: var(--amber); border: 1px solid var(--amber-border); }
.badge.blue  { background: var(--blue-bg);  color: var(--blue);  border: 1px solid var(--blue-border); }
.badge.violet{ background: var(--accent-dim); color: var(--accent); border: 1px solid var(--accent-border); }

/* ═══════════════════════════════════════════════════════════
   TEXT BLOCKS (transcript, corrected)
═══════════════════════════════════════════════════════════ */
.text-block-label {
  font-size: var(--sz-2xs);
  font-family: var(--ff-mono);
  color: var(--ink3);
  text-transform: uppercase;
  letter-spacing: .12em;
  margin-bottom: 8px;
}

.text-block {
  background: var(--surface);
  border: 1px solid var(--border-md);
  border-radius: var(--r-md);
  padding: 16px 18px;
  font-size: var(--sz-md);
  color: var(--ink2);
  line-height: 1.9;
}
.text-block.corrected {
  border-color: var(--green-border);
  background: var(--green-bg);
}
.text-block[dir="rtl"] { text-align: right; font-family: var(--ff-arabic); }

.diff-legend {
  display: flex;
  gap: 14px;
  margin-bottom: 8px;
  font-size: var(--sz-2xs);
  font-family: var(--ff-mono);
  color: var(--ink3);
}
.diff-legend span { display: flex; align-items: center; gap: 4px; }
.diff-legend span::before {
  content: '■';
  font-size: 8px;
}
.diff-legend .changed::before { color: var(--amber); }
.diff-legend .same::before    { color: var(--green); }

/* ═══════════════════════════════════════════════════════════
   STREAMLIT COMPONENT OVERRIDES
═══════════════════════════════════════════════════════════ */
/* Buttons */
.stButton > button {
  background: var(--surface) !important;
  border: 1px solid var(--border-md) !important;
  color: var(--ink) !important;
  font-family: var(--ff-body) !important;
  font-size: var(--sz-sm) !important;
  font-weight: 600 !important;
  border-radius: var(--r-md) !important;
  padding: 9px 20px !important;
  transition: all .15s !important;
  box-shadow: 0 1px 2px rgba(0,0,0,.06) !important;
  letter-spacing: .01em !important;
}
.stButton > button:hover {
  border-color: var(--border-strong) !important;
  background: var(--surface2) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 3px 8px rgba(0,0,0,.12) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Primary button (first button in some contexts) */
.stButton > button[kind="primary"],
.stButton:first-child > button {
  background: var(--accent) !important;
  border-color: transparent !important;
  color: #fff !important;
}
.stButton > button[kind="primary"]:hover {
  background: #6a5ff0 !important;
}

/* Inputs */
.stTextInput input {
  background: var(--surface) !important;
  border: 1px solid var(--border-md) !important;
  border-radius: var(--r-md) !important;
  color: var(--ink) !important;
  font-family: var(--ff-body) !important;
  font-size: var(--sz-md) !important;
  padding: 10px 14px !important;
  transition: border-color .15s !important;
}
.stTextInput input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px var(--accent-dim) !important;
}
.stTextInput label,
div[data-testid="stWidgetLabel"] p {
  color: var(--ink2) !important;
  font-size: var(--sz-sm) !important;
  font-weight: 600 !important;
  font-family: var(--ff-body) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border: 1px solid var(--border-md) !important;
  border-radius: var(--r-lg) !important;
  padding: 5px !important;
  gap: 4px !important;
  margin-bottom: 1.8rem !important;
}
.stTabs [data-baseweb="tab"] {
  font-family: var(--ff-body) !important;
  font-size: var(--sz-sm) !important;
  font-weight: 600 !important;
  color: var(--ink3) !important;
  border-radius: var(--r-md) !important;
  padding: 9px 20px !important;
  transition: all .15s !important;
}
.stTabs [aria-selected="true"] {
  background: var(--surface3) !important;
  color: var(--ink) !important;
  box-shadow: 0 1px 4px rgba(0,0,0,.12), 0 0 0 1px var(--border-md) !important;
}

/* Alerts */
[data-testid="stAlert"] {
  border-radius: var(--r-md) !important;
  font-family: var(--ff-body) !important;
  font-size: var(--sz-sm) !important;
  border: 1px solid var(--border-md) !important;
}

/* Slider */
[data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stThumbValue"] {
  font-family: var(--ff-mono) !important;
  font-size: var(--sz-xs) !important;
}

/* Spinner */
.stSpinner { color: var(--accent) !important; }

/* Divider */
hr { border-color: var(--border-md) !important; margin: 1.5rem 0 !important; }

/* Expander */
[data-testid="stExpander"] {
  border: 1px solid var(--border-md) !important;
  border-radius: var(--r-md) !important;
  background: var(--surface) !important;
}

/* Text area */
.stTextArea textarea {
  background: var(--surface) !important;
  border: 1px solid var(--border-md) !important;
  border-radius: var(--r-md) !important;
  color: var(--ink) !important;
  font-family: var(--ff-mono) !important;
  font-size: var(--sz-sm) !important;
}

/* Info / warning / error colour overrides */
[data-testid="stAlert"][data-baseweb="notification"] {
  background: var(--surface2) !important;
}
</style>
"""