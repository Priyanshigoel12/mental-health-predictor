# MindScan — Premium Health & Wellness Redesign.
import streamlit as st
import pandas as pd
import numpy as np
import pickle, os

st.set_page_config(
    page_title="MindScan · Mental Health Assessment",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Google Fonts + Premium Health CSS Overhaul ───────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
/* Calming, airy off-white background */
.stApp { background: #F8FAFC; }
.block-container {
    padding: 0 !important;
    max-width: 680px !important;
    margin: 0 auto !important;
}
/* Hide all streamlit chrome */
#MainMenu, footer, header,
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"] { display: none !important; }

/* ── HERO: Premium Glassmorphism & Serene Gradients ── */
.ms-hero {
    background: linear-gradient(135deg, #0F766E 0%, #0284C7 100%);
    padding: 60px 32px 50px;
    text-align: center;
    position: relative;
    overflow: hidden;
    border-bottom-left-radius: 32px;
    border-bottom-right-radius: 32px;
    box-shadow: 0 10px 30px rgba(15, 118, 110, 0.15);
}
/* Soft glowing orbs for that "wow" modern tech feel */
.ms-hero::before {
    content: "";
    position: absolute; top: -100px; right: -50px;
    width: 300px; height: 300px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    filter: blur(40px);
}
.ms-hero::after {
    content: "";
    position: absolute; bottom: -80px; left: -80px;
    width: 250px; height: 250px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 50%;
    filter: blur(40px);
}
.ms-logo {
    font-size: 3.5rem;
    margin-bottom: 16px;
    display: block;
    position: relative; z-index: 1;
    text-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.ms-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -1.2px;
    margin-bottom: 8px;
    position: relative; z-index: 1;
}
.ms-subtitle {
    font-size: 1.1rem;
    color: rgba(255,255,255,0.9);
    font-weight: 400;
    margin-bottom: 24px;
    position: relative; z-index: 1;
}
.ms-tags {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    position: relative; z-index: 1;
}
.ms-tag {
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(10px);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 6px 16px;
    border-radius: 30px;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

/* ── STATS BAR ── */
.ms-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    background: white;
    margin: -20px 24px 20px;
    border-radius: 20px;
    position: relative;
    z-index: 10;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
    border: 1px solid rgba(226, 232, 240, 0.8);
}
.ms-stat {
    padding: 20px 12px;
    text-align: center;
    border-right: 1px solid #F1F5F9;
}
.ms-stat:last-child { border-right: none; }
.ms-stat-num {
    font-size: 1.5rem;
    font-weight: 800;
    color: #0F766E;
    line-height: 1;
}
.ms-stat-lbl {
    font-size: 0.7rem;
    color: #64748B;
    font-weight: 600;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* ── PRIVACY NOTICE ── */
.ms-privacy {
    background: #F0FDF4;
    margin: 0 24px 24px;
    border-radius: 12px;
    padding: 12px 24px;
    text-align: center;
    font-size: 0.85rem;
    color: #166534;
    font-weight: 600;
    border: 1px solid #DCFCE7;
}

/* ── SECTION CARD ── */
.ms-section {
    background: white;
    margin: 16px 24px;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.03);
    border: 1px solid #F1F5F9;
    transition: transform 0.2s ease;
}
.ms-section:hover {
    box-shadow: 0 14px 40px rgba(15, 23, 42, 0.06);
}
.ms-section-head {
    padding: 20px 24px 16px;
    border-bottom: 1px solid #F8FAFC;
    display: flex;
    align-items: center;
    gap: 12px;
}
.ms-section-icon {
    width: 40px; height: 40px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
}
.ms-section-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0F172A;
}
.ms-section-sub {
    font-size: 0.8rem;
    color: #64748B;
    font-weight: 400;
    margin-top: 2px;
}
.ms-section-body { padding: 20px 24px 24px; }

/* ── QUESTION LABEL ── */
.ms-qlabel {
    font-size: 0.9rem;
    font-weight: 600;
    color: #334155;
    margin-bottom: 12px;
    margin-top: 20px;
    line-height: 1.5;
}
.ms-qlabel:first-child { margin-top: 0; }

/* ── PILL RADIO — Soft, modern bubbles ── */
div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 10px !important;
    margin-top: 4px !important;
}
div[data-testid="stRadio"] > div > label {
    background: #F8FAFC !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 999px !important;
    padding: 10px 18px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    color: #475569 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    white-space: nowrap !important;
}
div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: #0F766E !important;
    border-color: #0F766E !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 6px 16px rgba(15, 118, 110, 0.25) !important;
}
div[data-testid="stRadio"] > div > label:hover:not(:has(input:checked)) {
    background: #F1F5F9 !important;
    border-color: #CBD5E1 !important;
}
div[data-testid="stRadio"] > div > label > div { display: none !important; }

/* ── SLIDERS (Teal theme) ── */
.stSlider > div > div > div > div { background: #0D9488 !important; }
.stSlider > div > div > div > div > div { background: #0D9488 !important; box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.2) !important;}
div[data-testid="stSlider"] p {
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: #334155 !important;
}

/* ── SELECT SLIDER ── */
div[data-baseweb="slider"] [role="slider"] { background: #0D9488 !important; border-color: #0D9488 !important; }
div[data-baseweb="slider"] div[data-testid^="stThumb"] { background: #0D9488 !important; box-shadow: 0 2px 6px rgba(0,0,0,0.1) !important;}

/* ── PHQ LIVE BAR ── */
.ms-phq-bar {
    margin-top: 24px;
    padding: 16px 20px;
    background: #F8FAFC;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
}
.ms-phq-bar-header {
    display: flex; justify-content: space-between; align-items: center;
    font-size: 0.85rem; color: #64748B; margin-bottom: 10px; font-weight: 600;
}
.ms-phq-score { font-weight: 800; font-size: 1.1rem; }
.ms-phq-track { background: #E2E8F0; border-radius: 8px; height: 10px; overflow: hidden; }
.ms-phq-fill { height: 100%; border-radius: 8px; transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1); }

/* ── CTA BUTTON: Premium Pill ── */
div[data-testid="stButton"] > button {
    width: calc(100% - 48px) !important;
    background: linear-gradient(135deg, #0F766E, #0284C7) !important;
    color: white !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    padding: 18px 24px !important;
    border-radius: 999px !important; /* Full pill shape */
    border: none !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 10px 25px rgba(15, 118, 110, 0.3) !important;
    margin: 16px 24px 32px !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 14px 35px rgba(15, 118, 110, 0.4) !important;
}

/* ── RESULT CARD ── */
.ms-result {
    margin: 16px 24px;
    border-radius: 32px;
    padding: 40px 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.ms-result.low      { background: linear-gradient(145deg, #ECFDF5, #D1FAE5); border: 1px solid #A7F3D0; box-shadow: 0 10px 30px rgba(16, 185, 129, 0.1); }
.ms-result.moderate { background: linear-gradient(145deg, #FFFBEB, #FEF3C7); border: 1px solid #FDE68A; box-shadow: 0 10px 30px rgba(245, 158, 11, 0.1); }
.ms-result.high     { background: linear-gradient(145deg, #FEF2F2, #FEE2E2); border: 1px solid #FECACA; box-shadow: 0 10px 30px rgba(239, 68, 68, 0.1); }
.ms-result-emoji    { font-size: 4rem; margin-bottom: 16px; display: block; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1)); }
.ms-result-label    {
    font-size: 2.2rem; font-weight: 800; margin-bottom: 12px; letter-spacing: -0.5px;
}
.ms-result.low      .ms-result-label { color: #065F46; }
.ms-result.moderate .ms-result-label { color: #92400E; }
.ms-result.high     .ms-result-label { color: #991B1B; }
.ms-result-desc { font-size: 1rem; color: #475569; line-height: 1.7; max-width: 440px; margin: 0 auto; font-weight: 500; }
.ms-result-score {
    display: inline-block;
    margin-top: 24px;
    padding: 8px 20px;
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(5px);
    border-radius: 30px;
    font-size: 0.85rem;
    font-weight: 700;
    color: #1E293B;
    border: 1px solid rgba(0,0,0,0.05);
}

/* ── CONFIDENCE BARS ── */
.ms-conf-section {
    background: white;
    margin: 16px 24px;
    border-radius: 24px;
    padding: 24px 28px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.03);
    border: 1px solid #F1F5F9;
}
.ms-conf-title {
    font-size: 0.75rem;
    font-weight: 800;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 20px;
}
.ms-conf-row { margin-bottom: 16px; }
.ms-conf-row:last-child { margin-bottom: 0; }
.ms-conf-header {
    display: flex; justify-content: space-between;
    font-size: 0.88rem; font-weight: 600; color: #334155;
    margin-bottom: 8px;
}
.ms-conf-pct { font-weight: 800; }
.ms-conf-track { background: #F1F5F9; border-radius: 8px; height: 12px; overflow: hidden; }
.ms-conf-fill  { height: 100%; border-radius: 8px; }

/* ── TIPS ── */
.ms-tips-section {
    background: white;
    margin: 16px 24px;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.03);
    border: 1px solid #F1F5F9;
}
.ms-tips-head {
    padding: 20px 24px;
    background: #F8FAFC;
    border-bottom: 1px solid #E2E8F0;
    font-size: 0.75rem;
    font-weight: 800;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}
.ms-tip {
    padding: 16px 24px;
    border-bottom: 1px solid #F8FAFC;
    display: flex;
    align-items: flex-start;
    gap: 16px;
}
.ms-tip:last-child { border-bottom: none; }
.ms-tip-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #0D9488;
    flex-shrink: 0;
    margin-top: 6px;
    box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.1);
}
.ms-tip-text { font-size: 0.95rem; color: #334155; line-height: 1.6; font-weight: 500; }

/* ── CRISIS BOX ── */
.ms-crisis {
    background: #FEF2F2;
    margin: 16px 24px;
    border-radius: 24px;
    padding: 28px;
    border: 1px solid #FECACA;
    box-shadow: 0 10px 30px rgba(239, 68, 68, 0.1);
}
.ms-crisis-title { font-size: 1.1rem; font-weight: 800; color: #991B1B; margin-bottom: 16px; }
.ms-crisis-line {
    display: flex; align-items: center; gap: 12px;
    font-size: 0.95rem; color: #7F1D1D; margin-bottom: 12px; font-weight: 600;
}
.ms-crisis-line:last-child { margin-bottom: 0; }
.ms-crisis-icon { font-size: 1.2rem; flex-shrink: 0; }

/* ── SHAP SECTION ── */
.ms-shap-section {
    background: white;
    margin: 16px 24px;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.03);
    border: 1px solid #F1F5F9;
}
.ms-shap-head {
    padding: 24px;
    background: linear-gradient(135deg, #0F172A, #1E293B);
    color: white;
}
.ms-shap-head-title { font-size: 1.05rem; font-weight: 700; margin-bottom: 4px; }
.ms-shap-head-sub   { font-size: 0.85rem; color: #94A3B8; font-weight: 400; }
.ms-shap-body { padding: 24px; }
.ms-shap-desc {
    font-size: 0.9rem; color: #64748B; line-height: 1.6; margin-bottom: 20px;
}

/* ── DISCLAIMER ── */
.ms-disclaimer {
    background: #F8FAFC;
    margin: 16px 24px;
    border-radius: 16px;
    padding: 20px 24px;
    border: 1px solid #E2E8F0;
    font-size: 0.85rem;
    color: #64748B;
    line-height: 1.6;
}

/* ── FOOTER ── */
.ms-footer {
    text-align: center;
    padding: 32px 24px 48px;
    font-size: 0.85rem;
    color: #94A3B8;
    line-height: 1.8;
}
.ms-footer a { color: #0D9488; text-decoration: none; font-weight: 600; transition: color 0.2s; }
.ms-footer a:hover { color: #0F766E; }

@media (max-width: 480px) {
    .ms-title { font-size: 2.2rem; }
    .ms-hero  { padding: 50px 20px 40px; border-bottom-left-radius: 24px; border-bottom-right-radius: 24px; }
    .ms-section, .ms-result, .ms-stats, .ms-privacy, .ms-tips-section, .ms-conf-section, .ms-shap-section, .ms-crisis, .ms-disclaimer { 
        margin-left: 16px; margin-right: 16px; 
    }
    div[data-testid="stButton"] > button { width: calc(100% - 32px) !important; margin: 16px 16px 32px !important; }
    div[data-testid="stRadio"] > div > label { font-size: 0.85rem !important; padding: 8px 14px !important; }
}
</style>
""", unsafe_allow_html=True)


# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open('best_model.pkl',    'rb') as f: model    = pickle.load(f)
    with open('scaler.pkl',        'rb') as f: scaler   = pickle.load(f)
    with open('feature_names.pkl', 'rb') as f: features = pickle.load(f)
    return model, scaler, features

try:
    model, scaler, FEATURES = load_model()
    model_ok = True
except Exception as e:
    model_ok = False
    err = str(e)

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="ms-hero">
    <span class="ms-logo">🌿</span>
    <div class="ms-title">MindScan</div>
    <div class="ms-subtitle">AI-Powered Mental Health Risk Assessment</div>
    <div class="ms-tags">
        <span class="ms-tag">PHQ-9 Validated</span>
        <span class="ms-tag">100% Anonymous</span>
        <span class="ms-tag">Instant Results</span>
        <span class="ms-tag">SHAP Explained</span>
    </div>
</div>
<div class="ms-stats">
    <div class="ms-stat">
        <div class="ms-stat-num">95.6%</div>
        <div class="ms-stat-lbl">Accuracy</div>
    </div>
    <div class="ms-stat">
        <div class="ms-stat-num">1,151</div>
        <div class="ms-stat-lbl">Students</div>
    </div>
    <div class="ms-stat">
        <div class="ms-stat-num">~3 min</div>
        <div class="ms-stat-lbl">To Complete</div>
    </div>
</div>
<div class="ms-privacy">
    🔒 Your responses are completely private and never stored.
</div>
""", unsafe_allow_html=True)

if not model_ok:
    st.error(f"Model files not found: {err}")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# PROGRESS (calculated at top, rendered inline)
# ══════════════════════════════════════════════════════════════════════════════

# ── SECTION 1: ABOUT YOU ─────────────────────────────────────────────────────
st.markdown("""
<div class="ms-section">
<div class="ms-section-head">
    <div class="ms-section-icon" style="background:#E0F2FE; color:#0284C7;">👤</div>
    <div>
        <div class="ms-section-title">About You</div>
        <div class="ms-section-sub">Basic demographic information</div>
    </div>
</div>
<div class="ms-section-body">
""", unsafe_allow_html=True)

st.markdown('<div class="ms-qlabel">How old are you?</div>', unsafe_allow_html=True)
age_r = st.radio("age_q", ["18","19","20","21","22","23","24","25","26","27+"],
                 horizontal=True, label_visibility="collapsed")
age = int(age_r.replace("+","")) if "+" not in age_r else 27

st.markdown('<div class="ms-qlabel">Gender</div>', unsafe_allow_html=True)
gender_r = st.radio("gender_q", ["Male","Female","Non-binary","Prefer not to say"],
                    horizontal=True, label_visibility="collapsed")
gender_val = {"Male":0,"Female":1,"Non-binary":2,"Prefer not to say":2}[gender_r]

st.markdown('<div class="ms-qlabel">Year of study</div>', unsafe_allow_html=True)
year_r = st.radio("year_q", ["1st year","2nd year","3rd year","4th year","5th year","Masters / PhD"],
                  horizontal=True, label_visibility="collapsed")
year_val = {"1st year":1,"2nd year":2,"3rd year":3,"4th year":4,"5th year":5,"Masters / PhD":6}[year_r]

st.markdown('</div></div>', unsafe_allow_html=True)

# ── SECTION 2: LIFESTYLE ─────────────────────────────────────────────────────
st.markdown("""
<div class="ms-section">
<div class="ms-section-head">
    <div class="ms-section-icon" style="background:#FEF3C7; color:#D97706;">🌙</div>
    <div>
        <div class="ms-section-title">Lifestyle & Habits</div>
        <div class="ms-section-sub">Sleep, exercise and daily routine</div>
    </div>
</div>
<div class="ms-section-body">
""", unsafe_allow_html=True)

st.markdown('<div class="ms-qlabel">How much do you sleep on average per night?</div>', unsafe_allow_html=True)
sleep_r = st.radio("sleep_q", ["Less than 5 hrs","5–6 hrs","6–7 hrs","7–8 hrs","More than 8 hrs"],
                   horizontal=True, label_visibility="collapsed")
sleep_val = {"Less than 5 hrs":0,"5–6 hrs":1,"6–7 hrs":2,"7–8 hrs":3,"More than 8 hrs":4}[sleep_r]

st.markdown('<div class="ms-qlabel">How often do you exercise?</div>', unsafe_allow_html=True)
ex_r = st.radio("ex_q", ["Never","1–2 times/week","3–4 times/week","Daily"],
                horizontal=True, label_visibility="collapsed")
ex_val = {"Never":0,"1–2 times/week":1,"3–4 times/week":2,"Daily":3}[ex_r]

st.markdown('<div class="ms-qlabel">How much screen time per day (outside studying)?</div>', unsafe_allow_html=True)
screen_r = st.radio("screen_q", ["Less than 2 hrs","2–4 hrs","More than 4 hrs"],
                    horizontal=True, label_visibility="collapsed")
screen_val = {"Less than 2 hrs":0,"2–4 hrs":1,"More than 4 hrs":2}[screen_r]

st.markdown('<div class="ms-qlabel">How many hours do you study outside class daily?</div>', unsafe_allow_html=True)
study_r = st.radio("study_q", ["0–1 hour","1–2 hours","2–3 hours","More than 3 hours"],
                   horizontal=True, label_visibility="collapsed")
study_val = {"0–1 hour":0,"1–2 hours":1,"2–3 hours":2,"More than 3 hours":3}[study_r]

st.markdown('</div></div>', unsafe_allow_html=True)

# ── SECTION 3: ACADEMIC & SOCIAL ─────────────────────────────────────────────
st.markdown("""
<div class="ms-section">
<div class="ms-section-head">
    <div class="ms-section-icon" style="background:#F3E8FF; color:#9333EA;">📚</div>
    <div>
        <div class="ms-section-title">Academic & Social</div>
        <div class="ms-section-sub">Support systems and academic load</div>
    </div>
</div>
<div class="ms-section-body">
""", unsafe_allow_html=True)

st.markdown('<div class="ms-qlabel">How often do you feel supported by friends or family?</div>', unsafe_allow_html=True)
sup_r = st.radio("sup_q", ["Never","Rarely","Sometimes","Often","Always"],
                 horizontal=True, label_visibility="collapsed")
sup_val = {"Never":0,"Rarely":1,"Sometimes":2,"Often":3,"Always":4}[sup_r]

st.markdown('<div class="ms-qlabel">Do you feel academically overloaded?</div>', unsafe_allow_html=True)
over_r = st.radio("over_q", ["No, I manage well","Yes, it feels too much"],
                  horizontal=True, label_visibility="collapsed")
over_val = 0 if "No" in over_r else 1

st.markdown('</div></div>', unsafe_allow_html=True)

# ── SECTION 4: STRESS ────────────────────────────────────────────────────────
st.markdown("""
<div class="ms-section">
<div class="ms-section-head">
    <div class="ms-section-icon" style="background:#FFE4E6; color:#E11D48;">😰</div>
    <div>
        <div class="ms-section-title">Stress Indicators</div>
        <div class="ms-section-sub">Rate each from 1 (Never) to 5 (Always)</div>
    </div>
</div>
<div class="ms-section-body">
""", unsafe_allow_html=True)

sw = st.slider("I feel stressed due to academic workload", 1, 5, 3)
dr = st.slider("I find it difficult to relax",             1, 5, 3)
ow = st.slider("I feel overwhelmed by responsibilities",   1, 5, 3)
ea = st.slider("I feel anxious about exams or deadlines",  1, 5, 3)

st.markdown('</div></div>', unsafe_allow_html=True)

# ── SECTION 5: PHQ-9 ─────────────────────────────────────────────────────────
st.markdown("""
<div class="ms-section">
<div class="ms-section-head">
    <div class="ms-section-icon" style="background:#D1FAE5; color:#059669;">🔬</div>
    <div>
        <div class="ms-section-title">PHQ-9 Depression Screening</div>
        <div class="ms-section-sub">Clinically validated — last 2 weeks</div>
    </div>
</div>
<div class="ms-section-body">
""", unsafe_allow_html=True)

st.markdown("**Over the last 2 weeks, how often were you bothered by:**")
st.markdown("")

PHQ_Q = [
    ("PHQ-1","Little interest or pleasure in doing things"),
    ("PHQ-2","Feeling down, depressed, or hopeless"),
    ("PHQ-3","Trouble falling or staying asleep, or sleeping too much"),
    ("PHQ-4","Feeling tired or having little energy"),
    ("PHQ-5","Poor appetite or overeating"),
    ("PHQ-6","Feeling bad about yourself — or that you are a failure"),
    ("PHQ-7","Trouble concentrating on things"),
    ("PHQ-8","Moving or speaking slowly, OR being restless/fidgety"),
    ("PHQ-9","Thoughts that you would be better off dead or hurting yourself"),
]
PHQ_OPTS   = [0,1,2,3]
PHQ_FORMAT = ["Not at all","Several days","More than half the days","Nearly every day"]

phq = []
for tag, q in PHQ_Q:
    st.markdown(f'<div class="ms-qlabel">{tag}: {q}</div>', unsafe_allow_html=True)
    v = st.select_slider(f"_{tag}", options=PHQ_OPTS, value=0,
                         format_func=lambda x: PHQ_FORMAT[x],
                         label_visibility="collapsed")
    phq.append(v)

phq_total = sum(phq)
bar_c = "#10B981" if phq_total<=9 else "#F59E0B" if phq_total<=19 else "#EF4444"
bar_w = f"{phq_total/27*100:.0f}"
st.markdown(f"""
<div class="ms-phq-bar">
    <div class="ms-phq-bar-header">
        <span>PHQ-9 Running Score</span>
        <span class="ms-phq-score" style="color:{bar_c}">{phq_total} / 27</span>
    </div>
    <div class="ms-phq-track">
        <div class="ms-phq-fill" style="width:{bar_w}%;background:{bar_c};"></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CTA BUTTON
# ══════════════════════════════════════════════════════════════════════════════
go = st.button("✨ Analyse My Mental Health Risk")
if go:
    st.session_state["analysis_submitted"] = True

# ══════════════════════════════════════════════════════════════════════════════
# RESULTS
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.get("analysis_submitted", False):
    inp = {
        'Age': age, 'Gender': gender_val, 'Year of Study': year_val,
        'Average sleep hours': sleep_val,
        'How often do you feel supported by friends or family?': sup_val,
        'Physical exercise frequency': ex_val,
        'Daily screen time': screen_val,
        'Do you feel academically overloaded?': over_val,
        'I feel stressed because of academic workload': sw,
        'I find it difficult to relax': dr,
        'I feel overwhelmed by responsibilities': ow,
        'I feel anxious about exams or deadlines': ea,
        'How many hours per day do you spend studying outside class?': study_val,
        '[Little interest or pleasure in doing things]': phq[0],
        '[Feeling down, depressed, or hopeless]': phq[1],
        '[Trouble falling or staying asleep, or sleeping too much]': phq[2],
        '[Feeling tired or having little energy]': phq[3],
        '[Poor appetite or overeating]': phq[4],
        '[Feeling bad about yourself — or that you are a failure]': phq[5],
        '[Trouble concentrating on things]': phq[6],
        '[Moving or speaking slowly OR being restless/fidgety]': phq[7],
        '[Thoughts that you would be better off dead or hurting yourself]': phq[8],
    }
    try:
        df_in  = pd.DataFrame([inp])[FEATURES]
        sc_in  = scaler.transform(df_in)
        pred   = model.predict(sc_in)[0]
        prob   = model.predict_proba(sc_in)[0]
    except Exception as e:
        st.error(f"Prediction error: {e}"); st.stop()

    RISK = {
        0: {
            "css":"low","emoji":"🌿","label":"Low Risk",
            "desc":"Your responses suggest low depression risk. Your current habits and lifestyle are supporting your mental wellbeing — keep it up.",
            "tips":[
                "Your sleep is your superpower — keep that schedule consistent.",
                "Social connection is protective. Stay close to the people who lift you.",
                "Continue your physical activity — even short walks make a real difference.",
                "Try a 5-minute breathing exercise on stressful days.",
                "Check in with yourself every week — emotional awareness is mental health.",
            ],"crisis":False,
        },
        1: {
            "css":"moderate","emoji":"⚖️","label":"Moderate Risk",
            "desc":"Your responses suggest moderate depression risk. A few targeted changes to your daily habits can significantly improve how you feel.",
            "tips":[
                "Prioritise 7–8 hours of sleep — it is the single most impactful change you can make.",
                "Break large tasks into tiny 15-minute steps to reduce overwhelm.",
                "Talk to someone today — a friend, mentor, or counsellor. You don't need to carry this alone.",
                "Step outside for 20 minutes a day. Sunlight and movement reset your nervous system.",
                "Cut screen time 1 hour before bed. Your brain needs a wind-down window.",
                "iCall: 9152987821 — free, confidential, judgment-free support.",
            ],"crisis":False,
        },
        2: {
            "css":"high","emoji":"🤍","label":"High Risk",
            "desc":"Your responses suggest high depression risk. Please reach out to a professional today — support is available and you deserve it.",
            "tips":[
                "Contact your university counselling centre — this is the most important step.",
                "Tell one trusted person how you're really feeling, right now.",
                "Remember: asking for help is an act of strength, not weakness.",
                "You do not have to feel this way forever. The right support changes everything.",
            ],"crisis":True,
        },
    }
    cfg = RISK[pred]

    # Result card
    st.markdown(f"""
    <div class="ms-result {cfg['css']}">
        <span class="ms-result-emoji">{cfg['emoji']}</span>
        <div class="ms-result-label">{cfg['label']}</div>
        <div class="ms-result-desc">{cfg['desc']}</div>
        <div class="ms-result-score">PHQ-9 Score: {phq_total} / 27</div>
    </div>
    """, unsafe_allow_html=True)

    # Confidence
    conf_meta = [
        ("Low Risk",      prob[0], "#10B981"),
        ("Moderate Risk", prob[1], "#F59E0B"),
        ("High Risk",     prob[2], "#EF4444"),
    ]
    bars_html = ""
    for lbl, p, col in conf_meta:
        bars_html += f"""
        <div class="ms-conf-row">
            <div class="ms-conf-header">
                <span>{lbl}</span>
                <span class="ms-conf-pct" style="color:{col}">{p*100:.1f}%</span>
            </div>
            <div class="ms-conf-track">
                <div class="ms-conf-fill"
                     style="width:{p*100:.1f}%;background:{col};"></div>
            </div>
        </div>"""
    st.markdown(f"""
    <div class="ms-conf-section">
        <div class="ms-conf-title">Prediction Confidence</div>
        {bars_html}
    </div>
    """, unsafe_allow_html=True)

    # Crisis helplines
    if cfg["crisis"]:
        st.markdown("""
        <div class="ms-crisis">
            <div class="ms-crisis-title">🆘 Reach out right now</div>
            <div class="ms-crisis-line">
                <span class="ms-crisis-icon">📞</span>
                <span><strong>iCall:</strong> 9152987821 — Free, confidential, Mon–Sat 8am–10pm</span>
            </div>
            <div class="ms-crisis-line">
                <span class="ms-crisis-icon">📞</span>
                <span><strong>Vandrevala Foundation:</strong> 1860-2662-345 — Available 24/7</span>
            </div>
            <div class="ms-crisis-line">
                <span class="ms-crisis-icon">📞</span>
                <span><strong>NIMHANS:</strong> 080-46110007</span>
            </div>
            <div class="ms-crisis-line" style="margin-top:16px;font-style:italic;color:#9CA3AF;font-size:0.9rem;">
                You reaching out is the bravest thing you can do. 💜
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Tips
    tips_html = "".join(
        f'<div class="ms-tip"><div class="ms-tip-dot"></div>'
        f'<div class="ms-tip-text">{t}</div></div>'
        for t in cfg["tips"]
    )
    st.markdown(f"""
    <div class="ms-tips-section">
        <div class="ms-tips-head">Personalised Recommendations</div>
        {tips_html}
    </div>
    """, unsafe_allow_html=True)

    # SHAP
    st.markdown("""
    <div class="ms-shap-section">
        <div class="ms-shap-head">
            <div class="ms-shap-head-title">🧬 Model Transparency</div>
            <div class="ms-shap-head-sub">SHAP values explaining the AI's reasoning</div>
        </div>
        <div class="ms-shap-body">
            <div class="ms-shap-desc">
                The charts below show which of your responses had the biggest impact on the result.
                Features with longer bars contributed more to the AI's decision.
            </div>
    """, unsafe_allow_html=True)

    for f, cap in [
        ("shap_1_global_importance.png","Global feature importance — average across all 1,151 students"),
        ("shap_3_per_class_bar.png",    "Top features driving each risk class specifically"),
    ]:
        if os.path.exists(f):
            st.image(f, caption=cap, use_column_width=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

    # Disclaimer
    st.markdown("""
    <div class="ms-disclaimer">
        ⚕️ <strong>Medical Disclaimer:</strong> MindScan is an AI research tool created for
        educational purposes. It does not constitute medical advice, psychiatric diagnosis,
        or clinical assessment. If you are experiencing distress, please speak with a
        qualified mental health professional or contact one of the helplines listed above.
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ms-footer">
    <strong style="color:#0F172A;">MindScan</strong> by Priyanshi Goel<br>
    Major Project DS4270 · Manipal University Jaipur · Dr. Aparna Tripathi<br>
    Built with Python · scikit-learn · SHAP · Streamlit<br><br>
    <a href="https://github.com/Priyanshigoel12/mental-health-predictor">View Source on GitHub ↗</a>
</div>
""", unsafe_allow_html=True)
