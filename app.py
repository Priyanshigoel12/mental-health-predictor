# =============================================================================
# MindScan — AI Mental Health Risk Assessment
# Professional redesign — mobile-first, production-ready
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

# ── Custom CSS for Professional UI ────────────────────────────────────────────
st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }
.block-container { padding: 1.5rem 1rem 3rem; max-width: 780px; }
.stApp { background: #F0F4FF; }

.hero {
    background: #1A237E;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 1.8rem;
}
.hero-icon { font-size: 3rem; margin-bottom: 0.5rem; }
.hero h1 {
    color: #FFFFFF;
    font-size: clamp(1.5rem, 4vw, 2.2rem);
    font-weight: 800;
    margin: 0 0 0.4rem;
}
.hero-sub { color: #90CAF9; font-size: clamp(0.85rem, 2.5vw, 1rem); margin: 0; }
.hero-tag { color: #64B5F6; font-size: 0.78rem; margin-top: 0.6rem; }

.section-card {
    background: white;
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    border: 1px solid #E8EAF6;
}
.section-title {
    font-size: 1.15rem; font-weight: 700; color: #1565C0;
    margin-bottom: 1.2rem; display: flex; align-items: center; gap: 0.6rem;
}

.result-box {
    border-radius: 16px; padding: 2rem; text-align: center; margin-top: 1rem;
    box-shadow: 0 6px 16px rgba(0,0,0,0.06);
}
.result-low { background: #E8F5E9; border: 2px solid #2E7D32; }
.result-mod { background: #FFFDE7; border: 2px solid #F9A825; }
.result-high { background: #FFEBEE; border: 2px solid #C62828; }
.res-title { font-size: 1.8rem; font-weight: 800; margin-bottom: 0.4rem; }

.btn-primary button {
    background: linear-gradient(135deg, #1565C0, #0D47A1) !important;
    color: white !important; font-weight: 700 !important;
    border-radius: 12px !important; padding: 0.75rem !important;
    font-size: 1.1rem !important; border: none !important;
    box-shadow: 0 4px 10px rgba(21, 101, 192, 0.3) !important;
}
.btn-primary button:hover { transform: translateY(-1px); box-shadow: 0 6px 14px rgba(21, 101, 192, 0.4) !important; }
</style>
""", unsafe_allow_html=True)

# ── Load AI Model ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    # Try loading SMOTE model first (better recall for high risk), fallback to standard
    try:
        with open('best_model_smote.pkl', 'rb') as f: model = pickle.load(f)
    except FileNotFoundError:
        try:
            with open('best_model.pkl', 'rb') as f: model = pickle.load(f)
        except FileNotFoundError:
            return None, None, None
            
    with open('scaler.pkl',        'rb') as f: scaler = pickle.load(f)
    with open('feature_names.pkl', 'rb') as f: features = pickle.load(f)
    return model, scaler, features

model, scaler, FEATURES = load_model()

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-icon">🧠</div>
    <h1>MindScan</h1>
    <p class="hero-sub">AI-Powered Mental Health Risk Assessment for Students</p>
    <p class="hero-tag">CONFIDENTIAL · ANONYMOUS · INSTANT RESULTS</p>
</div>
""", unsafe_allow_html=True)

if model is None:
    st.error("⚠️ **System Error:** Model files missing. Please contact administrator.")
    st.stop()

# ── Input Form ────────────────────────────────────────────────────────────────
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👤 Your Profile</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: age = st.number_input("Age", 17, 30, 20)
    with c2: 
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        gender_val = {"Male": 0, "Female": 1, "Other": 2}[gender]
    with c3: year_of_study = st.selectbox("Year of Study", [1, 2, 3, 4, 5, 6], index=2)
    
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌙 Lifestyle & Habits</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        sleep_raw = st.selectbox("Sleep Duration (avg/night)", 
            ["Less than 5 hrs", "5–6 hrs", "6–7 hrs", "7–8 hrs", "More than 8 hrs"], index=2)
        sleep_val = {"Less than 5 hrs": 0, "5–6 hrs": 1, "6–7 hrs": 2, "7–8 hrs": 3, "More than 8 hrs": 4}[sleep_raw]
        
        screen_raw = st.selectbox("Daily Screen Time", 
            ["Less than 2 hrs", "2–4 hrs", "More than 4 hrs"], index=1)
        screen_val = {"Less than 2 hrs": 0, "2–4 hrs": 1, "More than 4 hrs": 2}[screen_raw]

    with c2:
        exercise_raw = st.selectbox("Exercise Frequency", 
            ["Never", "1–2 times/week", "3–4 times/week", "Daily"], index=1)
        exercise_val = {"Never": 0, "1–2 times/week": 1, "3–4 times/week": 2, "Daily": 3}[exercise_raw]
        
        study_hours_raw = st.selectbox("Study Hours (outside class)", 
            ["0–1 hrs", "1–2 hrs", "2–3 hrs", "More than 3 hrs"], index=1)
        study_hours_val = {"0–1 hrs": 0, "1–2 hrs": 1, "2–3 hrs": 2, "More than 3 hrs": 3}[study_hours_raw]

    st.markdown('</div>', unsafe_allow_html=True) # End section-card

    # Academic & Stress
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📚 Academic Stress & Support</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        support_raw = st.selectbox("Support from friends/family", 
            ["Never", "Rarely", "Sometimes", "Often", "Always"], index=2)
        support_val = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3, "Always": 4}[support_raw]
        
        overload_raw = st.radio("Feel academically overloaded?", ["No", "Yes"], horizontal=True)
        overload_val = 1 if overload_raw == "Yes" else 0

    with c2:
        st.markdown("**Stress Indicators (1=Never, 5=Always)**")
        stress_workload = st.slider("Stressed by workload", 1, 5, 3)
        diff_relax     = st.slider("Difficulty relaxing", 1, 5, 3)
        overwhelmed    = st.slider("Overwhelmed by responsibility", 1, 5, 3)
        exam_anxiety   = st.slider("Anxious about exams", 1, 5, 3)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # PHQ-9
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔬 Wellness Check (PHQ-9)</div>', unsafe_allow_html=True)
    st.caption("Over the last 2 weeks, how often have you been bothered by:")
    
    phq_labels = [
        "Little interest/pleasure in doing things",
        "Feeling down, depressed, or hopeless",
        "Trouble falling/staying asleep, or sleeping too much",
        "Feeling tired or having little energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself / failure",
        "Trouble concentrating",
        "Moving slowly OR restlessness",
        "Thoughts of self-harm"
    ]
    
    phq_responses = []
    for i, label in enumerate(phq_labels):
        val = st.select_slider(f"{i+1}. {label}", options=[0, 1, 2, 3], value=0,
            format_func=lambda x: ["Not at all", "Several days", "More than half days", "Nearly every day"][x])
        phq_responses.append(val)
    
    phq_total = sum(phq_responses)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Prediction Logic ──────────────────────────────────────────────────────────
st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
if st.button("🚀 Analyze My Mental Health Risk"):
    # Prepare input
    input_dict = {
        'Age': age, 'Gender': gender_val, 'Year of Study': year_of_study,
        'Average sleep hours': sleep_val, 'How often do you feel supported by friends or family?': support_val,
        'Physical exercise frequency': exercise_val, 'Daily screen time': screen_val,
        'Do you feel academically overloaded?': overload_val,
        'I feel stressed because of academic workload': stress_workload,
        'I find it difficult to relax': diff_relax,
        'I feel overwhelmed by responsibilities': overwhelmed,
        'I feel anxious about exams or deadlines': exam_anxiety,
        'How many hours per day do you spend studying outside class?': study_hours_val,
        '[Little interest or pleasure in doing things]': phq_responses[0],
        '[Feeling down, depressed, or hopeless]': phq_responses[1],
        '[Trouble falling or staying asleep, or sleeping too much]': phq_responses[2],
        '[Feeling tired or having little energy]': phq_responses[3],
        '[Poor appetite or overeating]': phq_responses[4],
        '[Feeling bad about yourself — or that you are a failure]': phq_responses[5],
        '[Trouble concentrating on things]': phq_responses[6],
        '[Moving or speaking slowly OR being restless/fidgety]': phq_responses[7],
        '[Thoughts that you would be better off dead or hurting yourself]': phq_responses[8],
    }
    
    # Predict
    input_df = pd.DataFrame([input_dict])[FEATURES]
    input_scaled = scaler.transform(input_df)
    input_scaled_df = pd.DataFrame(input_scaled, columns=FEATURES)
    
    pred_class = model.predict(input_scaled_df)[0]
    probs = model.predict_proba(input_scaled_df)[0]
    
    # ── Display Results ───────────────────────────────────────────────────────
    risk_map = {
        0: {"label": "Low Risk", "class": "result-low", "color": "#2E7D32", "msg": "You're doing great! Keep maintaining your healthy habits."},
        1: {"label": "Moderate Risk", "class": "result-mod", "color": "#F9A825", "msg": "Some risk detected. Consider adjusting your sleep and stress management."},
        2: {"label": "High Risk", "class": "result-high", "color": "#C62828", "msg": "High risk detected. We strongly recommend speaking to a counselor."}
    }
    res = risk_map[pred_class]
    
    st.markdown(f"""
    <div class="result-box {res['class']}">
        <div class="res-title" style="color:{res['color']}">{res['label']}</div>
        <p>{res['msg']}</p>
        <p style="font-size:0.9rem; color:#666; margin-top:0.5rem">PHQ-9 Score: <strong>{phq_total}/27</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Probabilities
    c1, c2, c3 = st.columns(3)
    c1.metric("Low Risk", f"{probs[0]*100:.1f}%")
    c2.metric("Moderate Risk", f"{probs[1]*100:.1f}%")
    c3.metric("High Risk", f"{probs[2]*100:.1f}%")
    
    # Explainability (SHAP)
    with st.expander("🧠 Why did the AI make this prediction?", expanded=True):
        st.write("Top factors influencing the model globally:")
        if os.path.exists("shap_1_global_importance.png"):
            st.image("shap_1_global_importance.png", use_column_width=True)
        if os.path.exists("shap_2_summary_beeswarm.png"):
            st.image("shap_2_summary_beeswarm.png", caption="Feature Impact Direction", use_column_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; margin-top:3rem; padding-top:1rem; border-top:1px solid #eee; color:#999; font-size:0.8rem;">
    MindScan AI System · Priyanshi Goel · DS4270 · Manipal University Jaipur
</div>
""", unsafe_allow_html=True)
