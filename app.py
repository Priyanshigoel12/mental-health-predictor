# =============================================================================
# PHASE 6 — STREAMLIT DEPLOYMENT
# Project: AI-Based Mental Health Risk Prediction System for University Students
# Author : Priyanshi Goel | DS4270 | Manipal University Jaipur
# Run    : streamlit run app.py
# Install: pip install streamlit scikit-learn pandas numpy pickle5
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import warnings
import os
warnings.filterwarnings('ignore')

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mental Health Risk Predictor",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9ff; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    .header-box {
        background: linear-gradient(135deg, #1565C0, #0D47A1);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .header-box h1 { color: white; font-size: 1.9rem; margin: 0; }
    .header-box p  { color: #BBDEFB; font-size: 1rem; margin: 0.4rem 0 0; }

    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1565C0;
        border-left: 4px solid #1565C0;
        padding-left: 10px;
        margin: 1.5rem 0 0.8rem;
    }

    .result-low {
        background: #E8F5E9;
        border: 2px solid #2E7D32;
        border-radius: 14px;
        padding: 1.8rem;
        text-align: center;
        color: #0D1B2A !important;
    }
    .result-moderate {
        background: #FFFDE7;
        border: 2px solid #F9A825;
        border-radius: 14px;
        padding: 1.8rem;
        text-align: center;
        color: #0D1B2A !important;
    }
    .result-high {
        background: #FFEBEE;
        border: 2px solid #C62828;
        border-radius: 14px;
        padding: 1.8rem;
        text-align: center;
        color: #0D1B2A !important;
    }
    .result-title { font-size: 2rem; font-weight: 800; margin: 0; }
    .result-sub   { font-size: 1rem; margin-top: 0.3rem; }

    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    .metric-val { font-size: 1.5rem; font-weight: 700; color: #1565C0; }
    .metric-lbl { font-size: 0.8rem; color: #666; margin-top: 0.2rem; }

    .tip-box {
        background: #E3F2FD;
        border-left: 4px solid #1565C0;
        border-radius: 0 10px 10px 0;
        padding: 0.9rem 1.2rem;
        margin: 0.5rem 0;
        font-size: 0.92rem;
        color: #0D1B2A !important;
    }
    .footer {
        text-align: center;
        color: #999;
        font-size: 0.8rem;
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
    }
    div[data-testid="stButton"] button {
        width: 100%;
        background: linear-gradient(135deg, #1565C0, #0D47A1);
        color: white;
        font-size: 1.1rem;
        font-weight: 700;
        padding: 0.7rem;
        border-radius: 10px;
        border: none;
        margin-top: 1rem;
    }
    div[data-testid="stButton"] button:hover {
        background: linear-gradient(135deg, #1976D2, #1565C0);
    }
</style>
""", unsafe_allow_html=True)


# ── Load model, scaler, feature names ─────────────────────────────────────────
@st.cache_resource
def load_model():
    # Attempt to load SMOTE model first, fall back to standard if not found
    try:
        with open('best_model_smote.pkl', 'rb') as f: model = pickle.load(f)
    except FileNotFoundError:
        with open('best_model.pkl', 'rb') as f: model = pickle.load(f)
        
    with open('scaler.pkl',        'rb') as f: scaler = pickle.load(f)
    with open('feature_names.pkl', 'rb') as f: features = pickle.load(f)
    return model, scaler, features

try:
    model, scaler, FEATURES = load_model()
    model_loaded = True
except FileNotFoundError:
    model_loaded = False


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h1>🧠 Mental Health Risk Predictor</h1>
    <p>AI-Based Depression Risk Assessment for University Students</p>
    <p style="color:#90CAF9; font-size:0.85rem;">Manipal University Jaipur · DS4270 · Priyanshi Goel</p>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.error("⚠️ Model files not found. Make sure best_model_smote.pkl (or best_model.pkl), scaler.pkl, and feature_names.pkl are in the same folder.")
    st.stop()

# Model accuracy badge
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card"><div class="metric-val">95.67%</div><div class="metric-lbl">Model Accuracy</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><div class="metric-val">1,151</div><div class="metric-lbl">Students Trained On</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><div class="metric-val">Logistic Regression</div><div class="metric-lbl">Best Model</div></div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📋 Fill in your details below")
st.caption("All responses are anonymous and used only for prediction.")

# ── SECTION 1: Demographics ───────────────────────────────────────────────────
st.markdown('<div class="section-title">👤 Demographics</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    age = st.selectbox("Age", options=list(range(18, 28)), index=2)
with col2:
    gender = st.selectbox("Gender", options=["Male", "Female", "Other"], index=0)
    gender_val = {"Male": 0, "Female": 1, "Other": 2}[gender]
with col3:
    year_of_study = st.selectbox("Year of Study", options=[1, 2, 3, 4, 5, 6], index=2)

# ── SECTION 2: Lifestyle ──────────────────────────────────────────────────────
st.markdown('<div class="section-title">🌙 Lifestyle Habits</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    sleep_raw = st.selectbox(
        "Average sleep per night",
        options=["Less than 5 hrs", "5–6 hrs", "6–7 hrs", "7–8 hrs", "More than 8 hrs"],
        index=2
    )
    sleep_val = {"Less than 5 hrs": 0, "5–6 hrs": 1, "6–7 hrs": 2,
                 "7–8 hrs": 3, "More than 8 hrs": 4}[sleep_raw]

with col2:
    exercise_raw = st.selectbox(
        "Exercise frequency",
        options=["Never", "1–2 times/week", "3–4 times/week", "Daily"],
        index=1
    )
    exercise_val = {"Never": 0, "1–2 times/week": 1,
                    "3–4 times/week": 2, "Daily": 3}[exercise_raw]

with col3:
    screen_raw = st.selectbox(
        "Daily screen time",
        options=["Less than 2 hrs", "2–4 hrs", "More than 4 hrs"],
        index=1
    )
    screen_val = {"Less than 2 hrs": 0, "2–4 hrs": 1, "More than 4 hrs": 2}[screen_raw]

# ── SECTION 3: Academic ───────────────────────────────────────────────────────
st.markdown('<div class="section-title">📚 Academic & Social</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    support_raw = st.selectbox(
        "Social support from friends/family",
        options=["Never", "Rarely", "Sometimes", "Often", "Always"],
        index=2
    )
    support_val = {"Never": 0, "Rarely": 1, "Sometimes": 2,
                   "Often": 3, "Always": 4}[support_raw]

with col2:
    overload_raw = st.selectbox(
        "Feel academically overloaded?",
        options=["No", "Yes"],
        index=0
    )
    overload_val = {"No": 0, "Yes": 1}[overload_raw]

with col3:
    study_hours_raw = st.selectbox(
        "Study hours outside class/day",
        options=["0–1 hrs", "1–2 hrs", "2–3 hrs", "More than 3 hrs"],
        index=1
    )
    study_hours_val = {"0–1 hrs": 0, "1–2 hrs": 1,
                       "2–3 hrs": 2, "More than 3 hrs": 3}[study_hours_raw]

# ── SECTION 4: Stress Scale ───────────────────────────────────────────────────
st.markdown('<div class="section-title">😰 Stress Indicators  <span style="font-size:0.85rem; font-weight:400; color:#666">(1 = Never, 5 = Always)</span></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    stress_workload  = st.slider("I feel stressed due to academic workload",   1, 5, 3)
    diff_relax       = st.slider("I find it difficult to relax",               1, 5, 3)
with col2:
    overwhelmed      = st.slider("I feel overwhelmed by responsibilities",     1, 5, 3)
    exam_anxiety     = st.slider("I feel anxious about exams or deadlines",    1, 5, 3)

# ── SECTION 5: PHQ-9 Questions ────────────────────────────────────────────────
st.markdown('<div class="section-title">🔬 PHQ-9 Depression Screening  <span style="font-size:0.85rem; font-weight:400; color:#666">(0 = Not at all, 3 = Nearly every day)</span></div>', unsafe_allow_html=True)
st.caption("Over the **last 2 weeks**, how often have you been bothered by the following?")

phq_labels = [
    "Little interest or pleasure in doing things",
    "Feeling down, depressed, or hopeless",
    "Trouble falling or staying asleep, or sleeping too much",
    "Feeling tired or having little energy",
    "Poor appetite or overeating",
    "Feeling bad about yourself — or that you are a failure",
    "Trouble concentrating on things",
    "Moving or speaking slowly OR being restless/fidgety",
    "Thoughts that you would be better off dead or hurting yourself",
]
phq_responses = []
col1, col2 = st.columns(2)
for i, label in enumerate(phq_labels):
    col = col1 if i % 2 == 0 else col2
    with col:
        val = st.select_slider(
            label,
            options=[0, 1, 2, 3],
            value=0,
            format_func=lambda x: ["Not at all", "Several days",
                                   "More than half days", "Nearly every day"][x]
        )
        phq_responses.append(val)

phq_total = sum(phq_responses)

# ── PREDICT BUTTON ────────────────────────────────────────────────────────────
st.markdown("")
predict_clicked = st.button("🔍  Predict My Mental Health Risk")

if predict_clicked:
    # Build input row matching training feature order
    input_dict = {
        'Age':                                                          age,
        'Gender':                                                       gender_val,
        'Year of Study':                                                year_of_study,
        'Average sleep hours':                                          sleep_val,
        'How often do you feel supported by friends or family?':        support_val,
        'Physical exercise frequency':                                  exercise_val,
        'Daily screen time':                                            screen_val,
        'Do you feel academically overloaded?':                         overload_val,
        'I feel stressed because of academic workload':                 stress_workload,
        'I find it difficult to relax':                                 diff_relax,
        'I feel overwhelmed by responsibilities':                       overwhelmed,
        'I feel anxious about exams or deadlines':                      exam_anxiety,
        'How many hours per day do you spend studying outside class?':  study_hours_val,
        '[Little interest or pleasure in doing things]':                phq_responses[0],
        '[Feeling down, depressed, or hopeless]':                       phq_responses[1],
        '[Trouble falling or staying asleep, or sleeping too much]':    phq_responses[2],
        '[Feeling tired or having little energy]':                      phq_responses[3],
        '[Poor appetite or overeating]':                                phq_responses[4],
        '[Feeling bad about yourself — or that you are a failure]':     phq_responses[5],
        '[Trouble concentrating on things]':                            phq_responses[6],
        '[Moving or speaking slowly OR being restless/fidgety]':        phq_responses[7],
        '[Thoughts that you would be better off dead or hurting yourself]': phq_responses[8],
    }

    # Align to training feature order
    input_df  = pd.DataFrame([input_dict])[FEATURES]
    input_scaled = scaler.transform(input_df)

    prediction   = model.predict(input_scaled)[0]
    proba        = model.predict_proba(input_scaled)[0]

    # ── Result display ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 🎯 Your Result")

    risk_config = {
        0: {
            "class": "result-low",
            "emoji": "✅",
            "title": "Low Risk",
            "color": "#2E7D32",
            "sub": "Your responses suggest low depression risk. Keep up your healthy habits!",
            "tips": [
                "Maintain your current sleep schedule — it's working well.",
                "Continue regular physical activity to sustain mental wellness.",
                "Stay connected with your support network.",
                "Practice mindfulness or meditation during exam season."
            ]
        },
        1: {
            "class": "result-moderate",
            "emoji": "⚠️",
            "title": "Moderate Risk",
            "color": "#F9A825",
            "sub": "Your responses indicate moderate depression risk. Some lifestyle adjustments can help.",
            "tips": [
                "Try to get 7–8 hours of sleep each night consistently.",
                "Break large tasks into smaller steps to reduce overwhelm.",
                "Reach out to a friend, mentor, or counsellor to talk.",
                "Limit screen time before bed to improve sleep quality.",
                "Include at least 30 mins of physical activity 3x per week."
            ]
        },
        2: {
            "class": "result-high",
            "emoji": "🔴",
            "title": "High Risk",
            "color": "#C62828",
            "sub": "Your responses suggest high depression risk. Please consider speaking to a professional.",
            "tips": [
                "Reach out to your university counselling centre as soon as possible.",
                "Talk to a trusted person — a friend, family member, or faculty mentor.",
                "iCall helpline: 9152987821 (free, confidential mental health support).",
                "Vandrevala Foundation helpline: 1860-2662-345 (24/7).",
                "Remember: seeking help is a sign of strength, not weakness."
            ]
        }
    }

    cfg = risk_config[prediction]

    st.markdown(f"""
    <div class="{cfg['class']}">
        <div class="result-title" style="color:{cfg['color']}">{cfg['emoji']} {cfg['title']}</div>
        <div class="result-sub">{cfg['sub']}</div>
        <div style="margin-top:0.8rem; font-size:0.9rem; color:#666">
            PHQ-9 Total Score: <strong>{phq_total}</strong> / 27
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Confidence probabilities
    st.markdown("#### 📊 Prediction Confidence")
    prob_cols = st.columns(3)
    labels = ["Low Risk", "Moderate Risk", "High Risk"]
    prob_colors = ["#2E7D32", "#F9A825", "#C62828"]
    for col, label, prob, color in zip(prob_cols, labels, proba, prob_colors):
        with col:
            st.markdown(
                f'<div class="metric-card"><div class="metric-val" style="color:{color}">'
                f'{prob*100:.1f}%</div><div class="metric-lbl">{label}</div></div>',
                unsafe_allow_html=True
            )

    # Recommendations
    st.markdown("#### 💡 Personalised Recommendations")
    for tip in cfg["tips"]:
        st.markdown(f'<div class="tip-box">→ {tip}</div>', unsafe_allow_html=True)

    # ── SHAP Explainability ───────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🧠 How does the AI decide?")
    with st.expander("See Global Feature Importance (SHAP)", expanded=True):
        st.write("The charts below show which questions generally have the biggest impact on the AI's risk prediction.")
        
        if os.path.exists("shap_1_global_importance.png"):
            st.image("shap_1_global_importance.png", caption="Features ranked by their contribution to the prediction", use_column_width=True)
            
        if os.path.exists("shap_3_per_class_bar.png"):
            st.image("shap_3_per_class_bar.png", caption="Top features driving each risk class", use_column_width=True)

        if os.path.exists("shap_2_summary_beeswarm.png"):
            st.image("shap_2_summary_beeswarm.png", caption="Feature Impact Direction (Red = High Value, Blue = Low Value)", use_column_width=True)

    # Disclaimer
    st.info("⚕️ **Disclaimer:** This tool is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. If you are in distress, please contact a healthcare professional.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    AI-Based Mental Health Risk Prediction System · Priyanshi Goel · DS4270 · Manipal University Jaipur<br>
    Built with Python · scikit-learn · Streamlit
</div>
""", unsafe_allow_html=True)
