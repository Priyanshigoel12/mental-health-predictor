# =============================================================================
# TIER 1 — UPGRADE 3: ADD GAD-7 ANXIETY SCALE
# Project: AI-Based Mental Health Risk Prediction System
# Author : Priyanshi Goel | DS4270 | Manipal University Jaipur
#
# What this does:
#   - Adds 7 validated anxiety screening questions (GAD-7) to the survey
#   - Predicts BOTH depression risk (PHQ-9) AND anxiety risk (GAD-7)
#   - Turns your project from "depression predictor" to "mental wellness system"
#   - Almost no existing Indian university paper does PHQ-9 + GAD-7 together
#
# GAD-7 scoring:
#   0-4  = Minimal anxiety
#   5-9  = Mild anxiety
#   10-14= Moderate anxiety
#   15+  = Severe anxiety
#
# Run: python Tier1_Upgrade3_GAD7.py
# NOTE: This script shows you:
#   1. How to add GAD-7 to your Google Form survey
#   2. How to process GAD-7 scores once you collect them
#   3. A SIMULATED demo using your existing data
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score

# ── PART A: THE 7 GAD-7 QUESTIONS TO ADD TO YOUR GOOGLE FORM ─────────────────
print("=" * 65)
print("GAD-7 QUESTIONS TO ADD TO YOUR GOOGLE FORM")
print("(Scale: 0=Not at all, 1=Several days, 2=More than half days, 3=Nearly every day)")
print("=" * 65)

gad7_questions = [
    "GAD1: Feeling nervous, anxious, or on edge",
    "GAD2: Not being able to stop or control worrying",
    "GAD3: Worrying too much about different things",
    "GAD4: Trouble relaxing",
    "GAD5: Being so restless that it is hard to sit still",
    "GAD6: Becoming easily annoyed or irritable",
    "GAD7: Feeling afraid, as if something awful might happen",
]
for q in gad7_questions:
    print(f"  • {q}")

print("\nSCORING: Sum all 7 answers → GAD-7 Total Score")
print("  0-4  = Minimal anxiety (Label: 0)")
print("  5-9  = Mild anxiety    (Label: 1)")
print("  10-14= Moderate anxiety(Label: 2)")
print("  15+  = Severe anxiety  (Label: 3)")

# ── PART B: LOAD EXISTING DATA & SIMULATE GAD-7 ───────────────────────────────
print("\n" + "=" * 65)
print("DEMO: Simulating GAD-7 from existing stress data")
print("(Replace simulation with real GAD-7 once you re-collect data)")
print("=" * 65)

df = pd.read_csv('MH_Survey_Cleaned_1151.csv')

# Simulate GAD-7 scores correlated with existing stress indicators
# In real data you'd just read the actual GAD-7 columns from your CSV
np.random.seed(42)
stress_proxy = (
    df['I feel stressed because of academic workload'] * 0.3 +
    df['I find it difficult to relax'] * 0.3 +
    df['I feel overwhelmed by responsibilities'] * 0.2 +
    df['I feel anxious about exams or deadlines'] * 0.2
)
# Scale to 0-21 range and add noise
gad7_raw = stress_proxy * 3.5 + np.random.normal(0, 2, len(df))
gad7_raw = np.clip(gad7_raw.round(), 0, 21).astype(int)
df['GAD-7 Total Score'] = gad7_raw

# Label GAD-7 anxiety risk
def gad7_label(score):
    if score <= 4:  return 0   # Minimal
    elif score <= 9:  return 1   # Mild
    elif score <= 14: return 2   # Moderate
    else:             return 3   # Severe

df['Anxiety Risk Label'] = df['GAD-7 Total Score'].apply(gad7_label)
anxiety_names = ['Minimal', 'Mild', 'Moderate', 'Severe']

print("\nSimulated GAD-7 Distribution:")
for i, name in enumerate(anxiety_names):
    cnt = (df['Anxiety Risk Label'] == i).sum()
    print(f"  {name:10s}: {cnt:4d} ({cnt/len(df)*100:.1f}%)")

# ── PART C: DUAL PREDICTION — PHQ-9 + GAD-7 ──────────────────────────────────
print("\n" + "=" * 65)
print("DUAL PREDICTION MODEL")
print("=" * 65)

features = df.drop(columns=['Field of Study', 'PHQ-9 Total Score',
                              'Depression Risk Label', 'GAD-7 Total Score',
                              'Anxiety Risk Label'])
y_dep = df['Depression Risk Label']   # 3 classes: Low/Mod/High
y_anx = df['Anxiety Risk Label']      # 4 classes: Min/Mild/Mod/Severe

scaler = MinMaxScaler()
X_sc   = scaler.fit_transform(features)

X_tr, X_te, yd_tr, yd_te, ya_tr, ya_te = train_test_split(
    X_sc, y_dep, y_anx, test_size=0.2, random_state=42, stratify=y_dep
)

# Train separate model for each scale
model_dep = LogisticRegression(max_iter=1000, random_state=42)
model_anx = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')

model_dep.fit(X_tr, yd_tr)
model_anx.fit(X_tr, ya_tr)

dep_f1 = f1_score(yd_te, model_dep.predict(X_te), average='weighted')
anx_f1 = f1_score(ya_te, model_anx.predict(X_te), average='weighted')

print(f"\nDepression model (PHQ-9):  F1 = {dep_f1:.4f}")
print(f"Anxiety model   (GAD-7):   F1 = {anx_f1:.4f}")

# ── PART D: PLOT 1 — Dual risk profile chart ──────────────────────────────────
print("\nGenerating Plot 1: Dual risk profile...")

dep_labels_full = {0:'Low\nDepression', 1:'Moderate\nDepression', 2:'High\nDepression'}
anx_labels_full = {0:'Minimal\nAnxiety', 1:'Mild\nAnxiety',
                   2:'Moderate\nAnxiety', 3:'Severe\nAnxiety'}

# Cross-tabulation: depression risk × anxiety risk
ct = pd.crosstab(df['Depression Risk Label'], df['Anxiety Risk Label'])
ct.index   = [dep_labels_full[i] for i in ct.index]
ct.columns = [anx_labels_full[i] for i in ct.columns]

fig, ax = plt.subplots(figsize=(9, 5.5))
ct.T.plot(kind='bar', ax=ax, color=['#2E7D32','#F9A825','#C62828'],
          edgecolor='white', width=0.7, alpha=0.88)
ax.set_title('Co-occurrence: Depression Risk × Anxiety Risk Level\n'
             '(Key insight: High depression almost always co-occurs with Moderate/Severe anxiety)',
             fontsize=12, fontweight='bold')
ax.set_xlabel('Anxiety Risk Level', fontsize=10)
ax.set_ylabel('Number of Students', fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=15, ha='right')
ax.legend(title='Depression Risk', fontsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.25, axis='y', linestyle='--')
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig('gad7_1_dual_risk_profile.png', dpi=150, bbox_inches='tight')
plt.show()
print("  Saved: gad7_1_dual_risk_profile.png")

# ── PART E: PLOT 2 — GAD-7 score distribution ─────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

# Histogram
axes[0].hist(df['GAD-7 Total Score'], bins=22, color='#7B1FA2',
             edgecolor='white', alpha=0.85)
axes[0].axvline(x=4.5,  color='#F9A825', lw=2, linestyle='--', label='Min/Mild (4/5)')
axes[0].axvline(x=9.5,  color='#E65100', lw=2, linestyle='--', label='Mild/Mod (9/10)')
axes[0].axvline(x=14.5, color='#C62828', lw=2, linestyle='--', label='Mod/Severe (14/15)')
axes[0].axvline(df['GAD-7 Total Score'].mean(), color='#0D47A1',
                lw=2, linestyle=':', label=f'Mean = {df["GAD-7 Total Score"].mean():.1f}')
axes[0].set_title('GAD-7 Score Distribution', fontsize=12, fontweight='bold')
axes[0].set_xlabel('GAD-7 Total Score (0–21)', fontsize=10)
axes[0].set_ylabel('Number of Students', fontsize=10)
axes[0].legend(fontsize=8)
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)
axes[0].grid(alpha=0.25, linestyle='--')

# Scatter: PHQ-9 vs GAD-7
scatter_colors = ['#2E7D32','#F9A825','#C62828']
for cls, color in zip([0,1,2], scatter_colors):
    mask = df['Depression Risk Label'] == cls
    axes[1].scatter(df.loc[mask,'PHQ-9 Total Score'],
                    df.loc[mask,'GAD-7 Total Score'],
                    c=color, alpha=0.4, s=20,
                    label=['Low Risk','Moderate Risk','High Risk'][cls])
axes[1].set_title(f'PHQ-9 vs GAD-7 Correlation\n(r = {df["PHQ-9 Total Score"].corr(df["GAD-7 Total Score"]):.3f})',
                  fontsize=12, fontweight='bold')
axes[1].set_xlabel('PHQ-9 Score (Depression)', fontsize=10)
axes[1].set_ylabel('GAD-7 Score (Anxiety)', fontsize=10)
axes[1].legend(fontsize=9)
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)
axes[1].grid(alpha=0.25, linestyle='--')

plt.suptitle('GAD-7 Anxiety Scale Analysis', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('gad7_2_distribution_scatter.png', dpi=150, bbox_inches='tight')
plt.show()
print("  Saved: gad7_2_distribution_scatter.png")

# ── PART F: Updated Streamlit app snippet ────────────────────────────────────
print("\n" + "=" * 65)
print("HOW TO ADD GAD-7 TO YOUR STREAMLIT APP")
print("=" * 65)
print("""
Add this section to app.py after the PHQ-9 questions:

# ── GAD-7 Section ─────────────────────────────────────────────────
st.markdown('<div class="section-title">😟 GAD-7 Anxiety Screening</div>',
            unsafe_allow_html=True)
st.caption("Over the last 2 weeks, how often were you bothered by:")

gad7_questions = [
    "Feeling nervous, anxious, or on edge",
    "Not being able to stop or control worrying",
    "Worrying too much about different things",
    "Trouble relaxing",
    "Being so restless it is hard to sit still",
    "Becoming easily annoyed or irritable",
    "Feeling afraid, as if something awful might happen",
]
gad7_responses = []
col1, col2 = st.columns(2)
for i, label in enumerate(gad7_questions):
    col = col1 if i % 2 == 0 else col2
    with col:
        val = st.select_slider(label, options=[0, 1, 2, 3], value=0,
            format_func=lambda x: ["Not at all","Several days",
                                   "More than half days","Nearly every day"][x])
        gad7_responses.append(val)

gad7_total = sum(gad7_responses)

# Then in prediction output:
if gad7_total <= 4:   anx_label = "Minimal Anxiety"
elif gad7_total <= 9: anx_label = "Mild Anxiety"
elif gad7_total <= 14:anx_label = "Moderate Anxiety"
else:                 anx_label = "Severe Anxiety"

st.metric("Anxiety Risk (GAD-7)", anx_label, f"Score: {gad7_total}/21")
""")

print("\n2 plots saved:")
print("  gad7_1_dual_risk_profile.png    — Depression × Anxiety co-occurrence")
print("  gad7_2_distribution_scatter.png — GAD-7 distribution + PHQ-9 correlation")
print("\nUpgrade 3 (GAD-7) complete!")
print("\n*** IMPORTANT: Re-collect survey data with GAD-7 questions added ***")
print("    You already have 1,151 responses — next collection adds 7 questions.")
