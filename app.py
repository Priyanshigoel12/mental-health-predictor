# =============================================================================
# MindScan — AI Mental Health Risk Assessment (FIXED VERSION)
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

st.set_page_config(
    page_title="MindScan — Mental Health Risk Assessment",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── MINIMAL, CLEAN CSS (ALL TEXT EXPLICITLY BLACK) ─────────────────────────────
st.markdown("""
<style>
body { background-color: #F5F7FA !important; color: #000000 !important; }
.stApp { background-color: #F5F7FA !important; color: #000000 !important; }
.block-container { max-width: 800px; padding: 2rem 1.5rem; }

/* Hero */
.hero-box { 
    background: linear-gradient(135deg, #0F766E, #064E3B);
    padding: 3rem 2rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 2rem;
    color: white !important;
}
.hero-icon { font-size: 3rem; margin-bottom: 1rem; display: block; }
.hero-title { font-size: 2.5rem; font-weight: 900; color: white !important; margin: 0.5rem 0; }
.hero-subtitle { font-size: 1.1rem; color: #A7F3D0; font-weight: 500; margin: 0.5rem 0; }
.hero-tag { font-size: 0.8rem; color: #64B5F6; letter-spacing: 1px; }

/* Stats */
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 2rem 0; }
.stat-card { background: white; padding: 1.5rem; border-radius: 12px; text-align: center; }
.stat-num { font-size: 1.8rem; font-weight: 900; color: #0F766E; margin: 0; }
.stat-label { font-size: 0.75rem; color: #64748B; font-weight: 700; margin-top: 0.5rem; }

/* Privacy */
.privacy { background: #D1FAE5; color: #065F46; padding: 1rem; border-radius: 12px; text-align: center; font-weight: 600; margin-bottom: 2rem; }

/* Section */
.section { background: white; padding: 2rem; border-radius: 16px; margin-bottom: 1.5rem; border: 1px solid #E5E7EB; }
.section-title { font-size: 1.2rem; font-weight: 800; color: #000000 !important; margin-bottom: 1rem; border-bottom: 2px solid #0F766E; padding-bottom: 0.5rem; }

/* Button */
.stButton > button { background: linear-gradient(135deg, #0F766E, #064E3B) !important; color: white !important; padding: 1rem !important; font-weight: 700 !important; border-radius: 12px !important; font-size: 1.1rem !important; }

/* Results */
.result-low { background: #E8F5E9; border-left: 5px solid #2E7D32; padding: 2rem; border-radius: 12px; color: #000000 !important; }
.result-mid { background: #FFFDE7; border-left: 5px solid #F59E0B; padding: 2rem; border-radius: 12px; color: #000000 !important; }
.result-high { background: #FFEBEE; border-left: 5px solid #EF4444; padding: 2rem; border-radius: 12px; color: #000000 !important; }
.result-label { font-size: 2rem; font-weight: 900; color: #000000 !important; }
.result-msg { font-size: 1rem; color: #000000 !important; margin-top: 1rem; }

/* Force All Text Black */
h1, h2, h3, h4, h5, h6 { color: #000000 !important; }
p, div, span, label, li { color: #000000 !important; }
.stMetricLabel { color: #000000 !important; }
.stSelectbox, .stNumberInput, .stSlider { color: #000000 !important; }

</style>
""", unsafe_allow_html=True)

# ── Load Model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        with open('best_model.pkl', 'rb') as f:
            model = pickle.load(f)
    except:
        with open('best_model_smote.pkl', 'rb') as f:
            model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('feature_names.pkl', 'rb') as f:
        features = pickle.load(f)
    return model, scaler, features

try:
    model, scaler, FEATURES = load_model()
except Exception as e:
    st.error(f"❌ Error loading model: {e}")
    st.stop()

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
    <div class="hero-icon">🧠</div>
    <div class="hero-title">MindScan</div>
    <div class="hero-subtitle">AI Mental Health Risk Assessment</div>
    <div class="hero-tag">CONFIDENTIAL • ANONYMOUS • EVIDENCE-BASED</div>
</div>
""", unsafe_allow_html=True)

# Stats
st.markdown("""
<div class="stats">
    <div class="stat-card"><div class="stat-num">95.6%</div><div class="stat-label">Accuracy</div></div>
    <div class="stat-card"><div class="stat-num">1,151</div><div class="stat-label">Students</div></div>
    <div class="stat-card"><div class="stat-num">~3 min</div><div class="stat-label">To Complete</div></div>
</div>
<div class="privacy">🔒 100% Anonymous. Your data is never stored.</div>
""", unsafe_allow_html=True)

# ── FORM ──────────────────────────────────────────────────────────────────────

# About You
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">👤 About You</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: 
    age = st.number_input("Age", 17, 30, 20)
with c2: 
    gender_r = st.selectbox("Gender", ["Male", "Female", "Other"])
    gender = {"Male": 0, "Female": 1, "Other": 2}[gender_r]
with c3: 
    year = st.selectbox("Year", [1, 2, 3, 4, 5, 6], index=2)
st.markdown('</div>', unsafe_allow_html=True)

# Lifestyle
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🌙 Lifestyle & Habits</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    sleep_r = st.selectbox("Sleep", ["<5 hrs", "5-6 hrs", "6-7 hrs", "7-8 hrs", ">8 hrs"], index=2)
    sleep = {"<5 hrs": 0, "5-6 hrs": 1, "6-7 hrs": 2, "7-8 hrs": 3, ">8 hrs": 4}[sleep_r]
    screen_r = st.selectbox("Screen Time", ["<2 hrs", "2-4 hrs", ">4 hrs"], index=1)
    screen = {"<2 hrs": 0, "2-4 hrs": 1, ">4 hrs": 2}[screen_r]
with c2:
    ex_r = st.selectbox("Exercise", ["Never", "1-2x/wk", "3-4x/wk", "Daily"], index=1)
    exercise = {"Never": 0, "1-2x/wk": 1, "3-4x/wk": 2, "Daily": 3}[ex_r]
    study_r = st.selectbox("Study Hours", ["0-1", "1-2", "2-3", ">3"], index=1)
    study = {"0-1": 0, "1-2": 1, "2-3": 2, ">3": 3}[study_r]
st.markdown('</div>', unsafe_allow_html=True)

# Academic
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📚 Academic & Social</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    support_r = st.selectbox("Supported?", ["Never", "Rarely", "Sometimes", "Often", "Always"], index=2)
    support = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3, "Always": 4}[support_r]
with c2:
    overload_r = st.selectbox("Overloaded?", ["No", "Yes"], index=0)
    overload = 1 if overload_r == "Yes" else 0
st.markdown('</div>', unsafe_allow_html=True)

# Stress
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">😰 Stress (1=Never, 5=Always)</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    workload = st.slider("Workload Stress", 1, 5, 3)
    relax = st.slider("Difficulty Relaxing", 1, 5, 3)
with c2:
    overwhelm = st.slider("Feeling Overwhelmed", 1, 5, 3)
    exam = st.slider("Exam Anxiety", 1, 5, 3)
st.markdown('</div>', unsafe_allow_html=True)

# PHQ-9
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🔬 PHQ-9 Screening</div>', unsafe_allow_html=True)
st.markdown('<p style="color: #000000; font-weight: 600;">Last 2 weeks: How often bothered by...</p>', unsafe_allow_html=True)

phq_items = [
    "No interest/pleasure",
    "Down/depressed/hopeless",
    "Sleep trouble",
    "Tired/low energy",
    "Appetite changes",
    "Feeling bad about self",
    "Trouble concentrating",
    "Slow/restless movements",
    "Thoughts of self-harm"
]

phq = []
for i, item in enumerate(phq_items):
    v = st.select_slider(f"{i+1}. {item}", options=[0, 1, 2, 3], value=0,
                         format_func=lambda x: ["Not at all", "Several days", "Half+ days", "Nearly daily"][x])
    phq.append(v)

phq_total = sum(phq)
st.markdown(f'<p style="font-weight: 900; font-size: 1.1rem; color: #000000; text-align: center;">PHQ-9 Score: {phq_total}/27</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── BUTTON & RESULTS ──────────────────────────────────────────────────────────

if st.button("✨ ANALYZE MY MENTAL HEALTH RISK", use_container_width=True):
    input_data = {
        'Age': age, 'Gender': gender, 'Year of Study': year,
        'Average sleep hours': sleep,
        'How often do you feel supported by friends or family?': support,
        'Physical exercise frequency': exercise,
        'Daily screen time': screen,
        'Do you feel academically overloaded?': overload,
        'I feel stressed because of academic workload': workload,
        'I find it difficult to relax': relax,
        'I feel overwhelmed by responsibilities': overwhelm,
        'I feel anxious about exams or deadlines': exam,
        'How many hours per day do you spend studying outside class?': study,
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
        df = pd.DataFrame([input_data])[FEATURES]
        scaled = scaler.transform(df)
        pred = model.predict(scaled)[0]
        probs = model.predict_proba(scaled)[0]
        
        risk_info = {
            0: {"class": "low", "emoji": "🌿", "label": "LOW RISK", "msg": "Your mental health is good. Keep up positive habits!"},
            1: {"class": "mid", "emoji": "⚠️", "label": "MODERATE RISK", "msg": "Some concerns detected. Small changes can help significantly."},
            2: {"class": "high", "emoji": "🆘", "label": "HIGH RISK", "msg": "Please speak with a mental health professional today."}
        }
        
        info = risk_info[pred]
        st.markdown(f"""
        <div class="result-{info['class']}">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{info['emoji']}</div>
            <div class="result-label">{info['label']}</div>
            <div class="result-msg">{info['msg']}</div>
            <div style="margin-top: 1rem; font-weight: 700; color: #000000;">PHQ-9: {phq_total}/27</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('---')
        st.subheader("📊 Prediction Confidence")
        c1, c2, c3 = st.columns(3)
        c1.metric("Low Risk", f"{probs[0]*100:.1f}%")
        c2.metric("Moderate Risk", f"{probs[1]*100:.1f}%")
        c3.metric("High Risk", f"{probs[2]*100:.1f}%")
        
        if os.path.exists("shap_1_global_importance.png"):
            with st.expander("🧬 Why This Result? (AI Reasoning)"):
                st.image("shap_1_global_importance.png", caption="Feature Importance")
                if os.path.exists("shap_2_summary_beeswarm.png"):
                    st.image("shap_2_summary_beeswarm.png")
    
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

st.markdown('---')
st.markdown('<p style="text-align: center; color: #000000; font-size: 0.8rem;">MindScan • DS4270 • Manipal University Jaipur</p>', unsafe_allow_html=True)
