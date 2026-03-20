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
st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', 'Inter', sans-serif; color: #000000; }
.stApp, .stApp * { color: #000000 !important; opacity: 1 !important; }
.stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown label,
.stText, .stCaption, .stSubheader, .stHeader,
div[data-testid="stMarkdownContainer"],
div[data-testid="stMarkdownContainer"] * {
    color: #000000 !important;
    opacity: 1 !important;
}
.block-container { padding: 1.5rem 1rem 3rem; max-width: 780px; }
.stApp { background: #F0F4FF; }

.hero {
    background: linear-gradient(145deg, #6C3CE1 0%, #9B59B6 50%, #C471ED 100%);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 1.8rem;
}
.hero-icon { font-size: 3rem; margin-bottom: 0.5rem; }
.hero h1 {
    color: #000000;
    font-size: clamp(1.5rem, 4vw, 2.2rem);
    font-weight: 800;
    margin: 0 0 0.4rem;
}
.hero-sub { color: #000000; font-size: clamp(0.85rem, 2.5vw, 1rem); margin: 0; }
.hero-tag { color: #000000; font-size: 0.78rem; margin-top: 0.6rem; }

.section-card {
    background: white;
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    border: 1px solid #E8EAF6;
}
.section-title {
    font-size: 1.15rem; font-weight: 700; color: #000000;
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
    background: linear-gradient(135deg, #F2E8FF, #DCC7FF) !important;
    color: #FFFFFF !important; font-weight: 700 !important;
    border-radius: 12px !important; padding: 0.75rem !important;
    font-size: 1.1rem !important; border: 1px solid #C4A6FF !important;
    box-shadow: 0 8px 20px rgba(137, 99, 219, 0.22) !important;
}
.btn-primary button:hover { transform: translateY(-1px); background: linear-gradient(135deg, #E9DBFF, #CFB3FF) !important; box-shadow: 0 10px 22px rgba(137,99,219,0.28) !important; }
.btn-primary button * { color: #FFFFFF !important; }

div[data-testid="stExpander"] details summary,
div[data-testid="stExpander"] details summary * {
    color: #FFFFFF !important;
}
div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] > div { display: flex !important; flex-wrap: wrap !important; gap: 8px !important; margin-top: 4px !important; }
div[data-testid="stRadio"] > div > label {
    background: #F7F3FF !important; border: 1.5px solid #DDD6FE !important;
    border-radius: 50px !important; padding: 7px 15px !important;
    font-size: 0.85rem !important; font-weight: 500 !important;
    color: #000000 !important; cursor: pointer !important;
}
div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: #EDE9FE !important; border-color: #6C3CE1 !important;
    color: #000000 !important; font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(108,60,225,0.3) !important;
}
.stSlider > div > div > div > div { background: #6C3CE1 !important; }

</style>
""")

# ── Load AI Model ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    # Try loading SMOTE model first (better recall for high risk), fallback to standard
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
    st.markdown('<div class="section-title">👤 Your Profile</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Age**")
        age_r = st.radio("Age", ["18","19","20","21","22","23","24","25+"], horizontal=True, label_visibility="collapsed", key="age_r")
        age = int(age_r.replace("+","")) if "+" not in age_r else 25
    with c2: 
        st.markdown("**Gender**")
        gender = st.radio("Gender", ["Male","Female","Other"], horizontal=True, label_visibility="collapsed", key="gender_r")
        gender_val = {"Male": 0, "Female": 1, "Other": 2}[gender]
    with c3:
        st.markdown("**Year of Education**")
        yr = st.radio("Year", ["1", "2", "3", "4", "Masters", "PhD"], horizontal=True, label_visibility="collapsed", key="yr_r")
        year_of_study = {"1": 1, "2": 2, "3": 3, "4": 4, "Masters": 5, "PhD": 6}[yr]
    
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌙 Lifestyle & Habits</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Sleep per night**")
        sleep_raw = st.radio("sleep", ["<5 hrs","5-6 hrs","6-7 hrs","7-8 hrs",">8 hrs"], horizontal=True, label_visibility="collapsed", key="sl_r")
        sleep_val = {"<5 hrs":0,"5-6 hrs":1,"6-7 hrs":2,"7-8 hrs":3,">8 hrs":4}[sleep_raw]
        
        st.markdown("**Screen time/day**")
        screen_raw = st.radio("screen", ["<2 hrs","2-4 hrs",">4 hrs"], horizontal=True, label_visibility="collapsed", key="sc_r")
        screen_val = {"<2 hrs":0,"2-4 hrs":1,">4 hrs":2}[screen_raw]

    with c2:
        st.markdown("**Exercise frequency**")
        exercise_raw = st.radio("exercise", ["Never","1-2x/week","3-4x/week","Daily"], horizontal=True, label_visibility="collapsed", key="ex_r")
        exercise_val = {"Never":0,"1-2x/week":1,"3-4x/week":2,"Daily":3}[exercise_raw]
        
        st.markdown("**Study hours outside class**")
        study_hours_raw = st.radio("study", ["0-1 hr","1-2 hrs","2-3 hrs","3+ hrs"], horizontal=True, label_visibility="collapsed", key="st_r")
        study_hours_val = {"0-1 hr":0,"1-2 hrs":1,"2-3 hrs":2,"3+ hrs":3}[study_hours_raw]

    # Academic & Stress
    st.markdown('<div class="section-title">📚 Academic Stress & Support</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Support from friends/family**")
        support_raw = st.radio("support", ["Never","Rarely","Sometimes","Often","Always"], horizontal=True, label_visibility="collapsed", key="su_r")
        support_val = {"Never":0,"Rarely":1,"Sometimes":2,"Often":3,"Always":4}[support_raw]
        
        overload_raw = st.radio("Feel academically overloaded?", ["No", "Yes"], horizontal=True)
        overload_val = 1 if overload_raw == "Yes" else 0

    with c2:
        st.markdown("**Stress Indicators (1=Never, 5=Always)**")
        stress_workload = st.slider("Stressed by workload", 1, 5, 3)
        diff_relax     = st.slider("Difficulty relaxing", 1, 5, 3)
        overwhelmed    = st.slider("Overwhelmed by responsibility", 1, 5, 3)
        exam_anxiety   = st.slider("Anxious about exams", 1, 5, 3)
    
    # PHQ-9
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
        0: {"label": "Low Risk", "class": "result-low", "color": "#000000", "msg": "You're doing great! Keep maintaining your healthy habits."},
        1: {"label": "Moderate Risk", "class": "result-mod", "color": "#000000", "msg": "Some risk detected. Consider adjusting your sleep and stress management."},
        2: {"label": "High Risk", "class": "result-high", "color": "#000000", "msg": "High risk detected. We strongly recommend speaking to a counselor."}
    }
    res = risk_map[pred_class]
    
    st.markdown(f"""
    <div class="result-box {res['class']}">
        <div class="res-title" style="color:{res['color']}">{res['label']}</div>
        <p>{res['msg']}</p>
        <p style="font-size:0.9rem; color:#000000; margin-top:0.5rem">PHQ-9 Score: <strong>{phq_total}/27</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Confidence bars
    st.markdown("#### Prediction confidence")
    for lbl, p, col in [("Low Risk",probs[0],"#10B981"),("Moderate Risk",probs[1],"#F59E0B"),("High Risk",probs[2],"#EF4444")]:
        st.markdown(f'''<div style="margin:8px 0">
            <div style="display:flex;justify-content:space-between;font-size:0.85rem;font-weight:600;color:#000000;margin-bottom:4px">
                <span>{lbl}</span><span style="color:#000000">{p*100:.1f}%</span>
            </div>
            <div style="background:#F3F4F6;border-radius:6px;height:10px;overflow:hidden">
                <div style="background:{col};width:{p*100:.1f}%;height:100%;border-radius:6px"></div>
            </div></div>''', unsafe_allow_html=True)
    
    # ── Personalised recommendations based on actual input values ──────────
    st.markdown("#### 💡 Your Personalised Recommendations")
    st.caption("Based on your specific responses — not generic advice.")

    tips = []

    # ── SLEEP ──────────────────────────────────────────────────────────────
    if sleep_val == 0:       # < 5 hrs
        tips.append(("🌙", "Critical: Sleep", "You are sleeping fewer than 5 hours — this is the strongest driver of your risk score. Aim for at least 7 hours tonight as a first priority."))
    elif sleep_val == 1:     # 5-6 hrs
        tips.append(("🌙", "Sleep needs improvement", "You are getting 5–6 hours which is below the recommended 7–8. Try going to bed 45 minutes earlier this week and see how you feel."))
    elif sleep_val in [2,3]: # 6-8 hrs — good range
        tips.append(("✅", "Sleep is on track", "Your sleep duration is in a healthy range. Protect this — keep a consistent bedtime even on weekends."))
    else:                    # > 8 hrs
        tips.append(("🌙", "Oversleeping check", "Sleeping more than 8 hours can sometimes signal low energy or low mood. If you still feel tired, mention it to a doctor."))

    # ── EXERCISE ───────────────────────────────────────────────────────────
    if exercise_val == 0:    # Never
        tips.append(("🏃", "Start moving — it matters more than you think", "You currently don't exercise. Even a 20-minute walk 3 times a week reduces depression risk significantly. Start small — no gym needed."))
    elif exercise_val == 1:  # 1-2x/week
        tips.append(("🏃", "Increase exercise slightly", "You exercise 1–2 times a week — good start. Try adding one more session. Research shows 3x/week is the threshold where mental health benefits become strong."))
    else:                    # 3-4x or daily — good
        tips.append(("✅", "Exercise habit is strong", "Your exercise frequency is excellent. This is one of the most protective factors for mental health — keep it up."))

    # ── SCREEN TIME ────────────────────────────────────────────────────────
    if screen_val == 2:      # > 4 hrs
        tips.append(("📱", "Reduce screen time before bed", "You are spending more than 4 hours on screens daily. Try a 60-minute phone-free wind-down before bed — this alone can improve sleep quality and reduce anxiety."))
    elif screen_val == 1:    # 2-4 hrs
        tips.append(("📱", "Screen time is moderate", "Your screen time is manageable. Just avoid using your phone in the 30 minutes before sleep to protect your sleep quality."))
    # screen_val == 0 → no tip needed, it's fine

    # ── SOCIAL SUPPORT ─────────────────────────────────────────────────────
    if support_val in [0, 1]:  # Never / Rarely
        tips.append(("🤝", "Build your support network — urgently", "You rarely feel supported by friends or family. Social isolation is one of the strongest predictors of depression. Reach out to one person today — even a short conversation helps."))
    elif support_val == 2:     # Sometimes
        tips.append(("🤝", "Strengthen social connections", "You sometimes feel supported. Try to identify 1–2 people you can talk to regularly. Strong social bonds are the #1 protective factor against depression."))
    else:                       # Often / Always — good
        tips.append(("✅", "Social support is strong", "You feel well-supported by friends and family — this is one of the most protective factors for mental health. Nurture these relationships."))

    # ── ACADEMIC OVERLOAD ──────────────────────────────────────────────────
    if overload_val == 1:
        tips.append(("📚", "Managing academic overload", "You feel academically overloaded. Break your workload into a daily task list — 3 tasks maximum per day. Talk to a faculty member or advisor if the load feels unmanageable."))

    # ── STRESS INDICATORS ──────────────────────────────────────────────────
    if stress_workload >= 4:
        tips.append(("😰", "Academic stress is high", "Your stress from workload is very high. Use the Pomodoro technique — 25 minutes focused work, 5-minute break. It reduces overwhelm and increases output."))
    if diff_relax >= 4:
        tips.append(("🧘", "Difficulty relaxing — try this", "You find it very hard to relax. Try 4-7-8 breathing: inhale 4 seconds, hold 7, exhale 8. Do this 3 times. It activates the parasympathetic nervous system within minutes."))
    if overwhelmed >= 4:
        tips.append(("📋", "Reducing overwhelm", "You feel frequently overwhelmed. Write down everything on your mind in one list, then pick just ONE thing to do next. This reduces the cognitive load your brain is carrying."))
    if exam_anxiety >= 4:
        tips.append(("📝", "Exam anxiety management", "Your exam anxiety is high. Preparation is the antidote — make a 2-week revision plan and stick to it. Each completed session builds confidence."))

    # ── PHQ-9 SPECIFIC ITEMS ───────────────────────────────────────────────
    if phq_responses[2] >= 2:  # Sleep trouble item
        tips.append(("🛌", "Sleep quality needs attention", "Your PHQ-9 responses show sleep trouble. Try keeping a fixed wake-up time 7 days a week — even weekends. Consistent wake times reset your sleep cycle faster than bedtimes."))
    if phq_responses[3] >= 2:  # Low energy
        tips.append(("⚡", "Low energy patterns", "You are experiencing low energy frequently. Check your water intake, meal regularity and iron levels. Simple nutritional gaps are a common and overlooked cause."))
    if phq_responses[6] >= 2:  # Concentration
        tips.append(("🎯", "Improving concentration", "You have trouble concentrating. Try single-tasking — close all tabs except the one you need. Studies show multitasking reduces effective IQ by up to 10 points."))

    # ── HIGH RISK — always add crisis resources ─────────────────────────────
    if pred_class == 2:
        tips.append(("🆘", "Please reach out today", "iCall: 9152987821 (free, Mon–Sat 8am–10pm) · Vandrevala Foundation: 1860-2662-345 (24/7) · NIMHANS: 080-46110007. Speaking to someone is the most important step you can take right now."))

    # ── RENDER TIPS ────────────────────────────────────────────────────────
    TIP_COLORS = {
        "✅": "#10B981", "🌙": "#6C3CE1", "🏃": "#3B82F6",
        "📱": "#F59E0B", "🤝": "#8B5CF6", "📚": "#0EA5E9",
        "😰": "#EF4444", "🧘": "#14B8A6", "📋": "#F97316",
        "📝": "#EC4899", "🛌": "#6366F1", "⚡": "#EAB308",
        "🎯": "#06B6D4", "🆘": "#DC2626",
    }
    for icon, title, body in tips:
        color = TIP_COLORS.get(icon, "#6C3CE1")
        border = "#FEE2E2" if icon == "🆘" else "#F3F0FF"
        bg     = "#FFF5F5" if icon == "🆘" else "white"
        st.markdown(f'''
        <div style="background:{bg};border:1px solid {border};border-left:4px solid {color};
                    border-radius:12px;padding:14px 16px;margin:8px 0;
                    box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                <span style="font-size:1rem">{icon}</span>
                <span style="font-size:0.85rem;font-weight:700;color:#000000;">{title}</span>
            </div>
            <div style="font-size:0.88rem;color:#000000;line-height:1.6;padding-left:28px;">{body}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.caption(f"📊 {len(tips)} personalised recommendations generated based on your responses.")
    
    # Explainability (SHAP)
    with st.expander("🧠 Why did the AI make this prediction?", expanded=True):
        st.write("Top factors influencing the model globally:")
        if os.path.exists("shap_1_global_importance.png"):
            st.image("shap_1_global_importance.png", use_container_width=True)
        if os.path.exists("shap_3_per_class_bar.png"):
            st.image("shap_3_per_class_bar.png", caption="Top features per risk class", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; margin-top:3rem; padding-top:1rem; border-top:1px solid #eee; color:#000000; font-size:0.8rem;">
    MindScan AI System · Priyanshi Goel · DS4270 · Manipal University Jaipur
</div>
""", unsafe_allow_html=True)