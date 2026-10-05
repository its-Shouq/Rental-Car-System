# -*- coding: utf-8 -*-
"""Look and feel: colors, CSS, car card, brand panel, top bar, navigation helpers."""
import streamlit as st

COLOR_HEX = {
    "White": "#F6F7F8", "Black": "#22282D", "Silver": "#B9C1C7",
    "Red": "#C7362F", "Blue": "#2C5E9E", "Grey": "#7C868D",
}

BASE_CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap');

:root{
  --asphalt:#1E2428; --signal:#F2C230; --mist:#EDF0F2; --paper:#FFFFFF;
  --ink:#151A1D; --muted:#5E6A72; --line:#D5DBDF;
}
html, body, [class*="css"], .stApp { font-family:'IBM Plex Sans Arabic', sans-serif; color:var(--ink); }
.stApp { background:var(--mist); }
#MainMenu, footer { visibility:hidden; }
header[data-testid="stHeader"] { background:transparent; }
.block-container { padding-top:1.2rem; max-width:1150px; }

/* sidebar */
[data-testid="stSidebar"] { background:var(--paper); border-right:1px solid var(--line); }
[data-testid="stSidebar"] .block-container { padding-top:2rem; }

/* hero */
.hero { background:var(--asphalt); color:#fff; border-radius:14px; padding:2.2rem 2.4rem 0 2.4rem; margin-bottom:1.6rem; overflow:hidden; }
.hero h1 { font-family:'Big Shoulders Display',sans-serif; font-weight:800; font-size:clamp(2.6rem,6vw,4.6rem);
  line-height:.95; letter-spacing:.01em; margin:0 0 .7rem 0; color:#fff; padding:0; }
.hero p { color:#B8C2C9; font-size:1.02rem; margin:0 0 1.8rem 0; max-width:34rem; }
.hero .road { height:14px; margin:0 -2.4rem; background:
  repeating-linear-gradient(90deg, var(--signal) 0 46px, transparent 46px 86px) center/100% 4px no-repeat; }

/* car card */
.car-card { background:var(--paper); border:1px solid var(--line); border-radius:12px; overflow:hidden; }
.car-art { background:linear-gradient(180deg,#F7F9FA,#E3E8EB); padding:1.1rem 1rem .4rem; border-bottom:1px solid var(--line); }
.car-art svg { width:100%; height:auto; display:block; }
.car-body { padding:1rem 1.2rem 1.1rem; display:flex; justify-content:space-between; align-items:flex-end; gap:1rem; }
.car-brand { color:var(--muted); font-size:.9rem; font-weight:500; }
.car-model { font-family:'Big Shoulders Display',sans-serif; font-weight:700; font-size:2rem; line-height:1; margin:.1rem 0 .55rem; }
.chip { display:inline-flex; align-items:center; gap:.4rem; font-size:.85rem; margin-right:.9rem; color:var(--ink); }
.chip i { width:.8rem; height:.8rem; border-radius:50%; border:1px solid var(--ink); display:inline-block; }
.stock { font-size:.85rem; color:var(--muted); }

/* price shown like a number plate */
.plate { display:inline-flex; align-items:stretch; background:#fff; border:2px solid var(--ink); border-radius:6px; overflow:hidden; white-space:nowrap; }
.plate b { background:var(--signal); padding:.25rem .5rem; font-size:.75rem; display:flex; align-items:center; border-right:2px solid var(--ink); }
.plate span { font-family:'Big Shoulders Display',sans-serif; font-weight:800; font-size:1.7rem; padding:0 .55rem; line-height:1.5; }
.plate em { font-style:normal; font-size:.78rem; color:var(--muted); padding:0 .55rem 0 0; display:flex; align-items:center; }

/* buttons */
.stButton > button, .stFormSubmitButton > button { border-radius:8px; font-weight:600; border:1.5px solid var(--ink);
  background:var(--paper); color:var(--ink); transition:transform .08s ease, background .15s ease; }
.stButton > button:hover, .stFormSubmitButton > button:hover { background:var(--mist); border-color:var(--ink); color:var(--ink); }
.stButton > button:active, .stFormSubmitButton > button:active { transform:translateY(1px); }
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] { background:var(--signal); color:var(--ink); border-color:var(--ink); }
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover { background:#FFD34D; color:var(--ink); }
button:focus-visible { outline:3px solid var(--signal) !important; outline-offset:2px; }

/* tabs */
button[data-baseweb="tab"] { font-weight:600; font-size:1rem; }
div[data-baseweb="tab-highlight"] { background:var(--ink) !important; height:3px; }

/* summary + receipt */
.panel { background:var(--paper); border:1px solid var(--line); border-radius:12px; padding:1.3rem 1.4rem; }
.row { display:flex; justify-content:space-between; padding:.55rem 0; border-bottom:1px dashed var(--line); font-size:.98rem; }
.row:last-child { border-bottom:none; }
.row span:first-child { color:var(--muted); }
.total { display:flex; justify-content:space-between; align-items:center; margin-top:.8rem; padding-top:.9rem; border-top:2px solid var(--ink); }
.total strong { font-family:'Big Shoulders Display',sans-serif; font-size:2.3rem; font-weight:800; }
.ticket { background:var(--paper); border:2px solid var(--ink); border-radius:12px; padding:1.5rem 1.6rem; position:relative; margin-bottom:1rem; }
.ticket h3 { font-family:'Big Shoulders Display',sans-serif; font-size:2rem; margin:0 0 .2rem; padding:0; }
.ticket .ref { color:var(--muted); font-size:.9rem; margin-bottom:.8rem; }
.empty { background:var(--paper); border:1.5px dashed var(--line); border-radius:12px; padding:2.2rem; text-align:center; color:var(--muted); }
.empty strong { display:block; color:var(--ink); font-size:1.15rem; margin-bottom:.3rem; }
.who { font-weight:600; font-size:1.05rem; }
.who small { display:block; color:var(--muted); font-weight:400; }
@media (prefers-reduced-motion: reduce){ *{ transition:none !important; } }
"""

EXTRA_CSS = """
/* ---- layout pieces added for the multi-page version ---- */
.block-container { max-width:1500px; padding-left:7rem; padding-right:7rem; }
.brand-panel { background:var(--asphalt); border-radius:14px; min-height:640px; display:flex; flex-direction:column;
  justify-content:space-between; overflow:hidden; }
.brand-panel .inner { padding:2.2rem 2.4rem 0 2.4rem; }
.brand-panel .logo { font-family:'Big Shoulders Display',sans-serif; font-weight:800; font-size:1.9rem; color:var(--signal); margin-bottom:2rem; }
.brand-panel h1 { font-family:'Big Shoulders Display',sans-serif; font-weight:800; font-size:clamp(2.6rem,5vw,4.4rem);
  line-height:.98; color:#fff; margin:0 0 1.2rem 0; padding:0; }
.brand-panel p { color:#B8C2C9; font-size:1.05rem; max-width:26rem; margin:0; }
.brand-panel .road { height:14px; background:repeating-linear-gradient(90deg, var(--signal) 0 46px, transparent 46px 86px) center/100% 4px no-repeat; margin-bottom:.9rem; }
.side-title { font-family:'Big Shoulders Display',sans-serif; font-weight:800; font-size:3rem; line-height:1; margin:.3rem 0 .2rem; }
.side-sub { color:var(--muted); margin-bottom:1rem; }
.pill { display:inline-block; border-radius:20px; padding:.25rem .8rem; font-size:.82rem; font-weight:500; margin-bottom:.4rem; }
.pill-signal { background:var(--signal); color:var(--ink); }
.pill-ink { background:var(--ink); color:#fff; }

/* top bar */
.st-key-topbar { background:var(--asphalt); border-radius:12px; padding:.8rem 1.3rem; margin-bottom:1.2rem; }
.st-key-topbar .logo { font-family:'Big Shoulders Display',sans-serif; font-weight:800; font-size:1.9rem; color:var(--signal); }
.st-key-topbar .topname { color:#fff; text-align:right; font-weight:500; }
.st-key-topbar .pill { margin:0 .7rem 0 0; font-size:.75rem; }

/* search bar + tables */
.st-key-searchbar { background:var(--paper); border:1px solid var(--line); border-radius:12px; padding:.4rem .6rem; }.st-key-searchbar { background:var(--paper); border:1px solid var(--line); border-radius:12px; padding:.4rem 1.6rem 1rem 1.6rem; }
.daytag { background:var(--signal); border:1.5px solid var(--ink); border-radius:8px; height:2.6rem; display:flex; align-items:center; justify-content:center; font-weight:600; white-space:nowrap; margin-bottom:1rem; }
.count { color:var(--muted); text-align:right; padding-top:1.6rem; }
.st-key-fleet_table { background:var(--paper); border:1px solid var(--line); border-radius:12px; overflow:hidden; gap:0; }
[class*="st-key-row_"] { border-bottom:1px solid var(--line); padding:.35rem 1.2rem; }
.st-key-row_head { background:#F5F7F8; padding:.7rem 1.2rem; }
.th { font-size:.8rem; font-weight:600; color:var(--muted); }
.td { font-size:.95rem; }
.cardtotal strong { font-family:'Big Shoulders Display',sans-serif; font-size:2rem; font-weight:800; display:block; line-height:1; }
.cardtotal span { color:var(--muted); font-size:.82rem; }
.rtable { width:100%; border-collapse:collapse; background:var(--paper); border:1px solid var(--line); border-radius:12px; overflow:hidden; }
.rtable th { background:#F5F7F8; color:var(--muted); font-size:.8rem; font-weight:600; text-align:left; padding:.7rem 1.2rem; }
.rtable td { padding:.8rem 1.2rem; border-top:1px solid var(--line); font-size:.95rem; }
.rtable td.num, .rtable th.num { text-align:right; }
.section-title { font-family:'Big Shoulders Display',sans-serif; font-weight:800; font-size:2.2rem; margin:1.6rem 0 .6rem; }
.page-title { font-family:'Big Shoulders Display',sans-serif; font-weight:800; font-size:3.2rem; line-height:1; margin:.2rem 0 .8rem; }

/* car card, new layout: year, model on its own line, color/stock left and price plate right */
.car-body { display:block; }
.car-year { color:var(--muted); font-size:.9rem; font-weight:500; }
.car-model { font-size:1.8rem; line-height:1.05; margin:.15rem 0 .8rem; }
.car-foot { display:flex; justify-content:space-between; align-items:center; gap:1rem; }
.car-meta { display:flex; flex-direction:column; gap:.3rem; }
.car-meta .chip { margin-right:0; }

/* labels inside the search bar (Pick-up dates, Search) */
.st-key-searchbar [data-testid="stWidgetLabel"] p {
    color: #5E6A72 !important;
    font-size: 0.85rem;
    font-weight: 500;
    padding-left: 0.3rem;
}

/* borders on the input boxes (date, search, dropdowns) */
[data-baseweb="input"],
[data-baseweb="select"] > div {
    border: 1.5px solid #5E6A72 !important;
    border-radius: 8px !important;
}
/* darker border when the box is clicked */
[data-baseweb="input"]:focus-within,
[data-baseweb="select"] > div:focus-within {
    border-color: #151A1D !important;
}
.vline { width:1px; height:2.5rem; background:#D5DBDF; margin:0 auto 15px auto; }
"""


def inject_css():
    st.markdown(f"<style>{BASE_CSS}{EXTRA_CSS}</style>", unsafe_allow_html=True)


# ----------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------
def money(x):
    return f"{x:,.2f}"


def fmt_date(d):
    return f"{d.day} {d:%b %Y}"


def fmt_day_long(d):
    return f"{d:%a}, {d.day} {d:%b %Y}"


def flash(msg):
    st.session_state.toast = msg


def goto(page, **state):
    """Callback for buttons: switch page and optionally set session values."""
    st.session_state.page = page
    for key, value in state.items():
        st.session_state[key] = value


def sign_out():
    st.session_state.username = None
    st.session_state.receipt = None
    st.session_state.page = "welcome"


# ----------------------------------------------------------------------
# HTML pieces
# ----------------------------------------------------------------------
def car_svg(color):
    fill = COLOR_HEX.get(color, "#8A949B")
    return f"""
    <svg viewBox="0 0 250 100" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{color} car">
      <ellipse cx="125" cy="88" rx="105" ry="6" fill="#000" opacity=".12"/>
      <path d="M12 68 Q12 54 34 50 L66 47 Q84 24 118 22 L156 22 Q186 26 204 47 L230 53
               Q242 57 242 68 L242 74 L12 74 Z" fill="{fill}" stroke="#151A1D" stroke-width="2.5" stroke-linejoin="round"/>
      <path d="M80 47 Q92 31 120 30 L152 30 Q172 33 188 47 Z" fill="#A9C4D4" stroke="#151A1D" stroke-width="2"/>
      <line x1="134" y1="30" x2="134" y2="47" stroke="#151A1D" stroke-width="2"/>
      <rect x="226" y="56" width="12" height="6" rx="2" fill="#F2C230" stroke="#151A1D" stroke-width="1.5"/>
      <circle cx="68" cy="74" r="15" fill="#151A1D"/><circle cx="68" cy="74" r="6" fill="#B9C1C7"/>
      <circle cx="186" cy="74" r="15" fill="#151A1D"/><circle cx="186" cy="74" r="6" fill="#B9C1C7"/>
    </svg>"""


def car_card_html(car):
    dot = COLOR_HEX.get(car["color"], "#8A949B")
    return f"""
    <div class="car-card">
      <div class="car-art">{car_svg(car['color'])}</div>
      <div class="car-body">
        <div class="car-year">{car['year']}</div>
        <div class="car-model">{car['model']}</div>
        <div class="car-foot">
          <div class="car-meta">
            <span class="chip"><i style="background:{dot}"></i>{car['color']}</span>
            <span class="stock">{car['quantity']} available</span>
          </div>
          <div class="plate"><b>SAR</b><span>{money(car['price'])}</span><em>per day</em></div>
        </div>
      </div>
    </div>"""


def brand_panel(headline, sub):
    return f"""
    <div class="brand-panel">
      <div class="inner">
        <div class="logo">RENTAL</div>
        <h1>{headline}</h1>
        <p>{sub}</p>
      </div>
      <div class="road"></div>
    </div>"""


def topbar(name=None, role=None):
    """Dark bar at the top of the pages. Without a name it shows a Back button."""
    with st.container(key="topbar"):
        a, b, c = st.columns([5, 3, 1.3], vertical_alignment="center")
        a.markdown('<span class="logo">RENTAL</span>', unsafe_allow_html=True)
        if name:
            pill = '<span class="pill pill-signal">Admin account</span>' if role == "admin" else ""
            b.markdown(f'<div class="topname">{pill}{name}</div>', unsafe_allow_html=True)
            c.button("Sign out", key="signout", on_click=sign_out, use_container_width=True)
        else:
            c.button("Back", key="back", on_click=goto, args=("welcome",), use_container_width=True)