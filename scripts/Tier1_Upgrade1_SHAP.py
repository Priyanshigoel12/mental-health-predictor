# =============================================================================
# TIER 1 — UPGRADE 1: SHAP EXPLAINABILITY
# Project: AI-Based Mental Health Risk Prediction System
# Author : Priyanshi Goel | DS4270 | Manipal University Jaipur
#
# What SHAP does:
#   - Explains WHY the model predicted Low / Moderate / High for each student
#   - Shows which features matter most GLOBALLY (summary plot)
#   - Shows which features drove a SINGLE student's prediction (force plot)
#   - Produces publication-ready charts for your research paper
#
# Install: pip install shap
# Run    : python Tier1_Upgrade1_SHAP.py
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import shap
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression

# ── STEP 1: Load & prepare data ───────────────────────────────────────────────
df = pd.read_csv('MH_Survey_Cleaned_1151.csv')

X = df.drop(columns=['Field of Study', 'PHQ-9 Total Score', 'Depression Risk Label'])
y = df['Depression Risk Label']

# Short feature names for cleaner plots
SHORT_NAMES = {
    'Age':                                                          'Age',
    'Gender':                                                       'Gender',
    'Year of Study':                                                'Year of study',
    'Average sleep hours':                                          'Sleep hours',
    'How often do you feel supported by friends or family?':        'Social support',
    'Physical exercise frequency':                                  'Exercise freq',
    'Daily screen time':                                            'Screen time',
    'Do you feel academically overloaded?':                         'Acad. overload',
    'I feel stressed because of academic workload':                 'Stress (workload)',
    'I find it difficult to relax':                                 'Difficulty relaxing',
    'I feel overwhelmed by responsibilities':                       'Overwhelmed',
    'I feel anxious about exams or deadlines':                      'Exam anxiety',
    'How many hours per day do you spend studying outside class?':  'Study hours',
    '[Little interest or pleasure in doing things]':                'PHQ1: Low interest',
    '[Feeling down, depressed, or hopeless]':                       'PHQ2: Depressed mood',
    '[Trouble falling or staying asleep, or sleeping too much]':    'PHQ3: Sleep trouble',
    '[Feeling tired or having little energy]':                      'PHQ4: Low energy',
    '[Poor appetite or overeating]':                                'PHQ5: Appetite change',
    '[Feeling bad about yourself — or that you are a failure]':     'PHQ6: Worthlessness',
    '[Trouble concentrating on things]':                            'PHQ7: Concentration',
    '[Moving or speaking slowly OR being restless/fidgety]':        'PHQ8: Psychomotor',
    '[Thoughts that you would be better off dead or hurting yourself]': 'PHQ9: Self-harm thoughts',
}

X_named = X.rename(columns=SHORT_NAMES)
feature_names = list(X_named.columns)

RISK_LABELS = {0: 'Low Risk', 1: 'Moderate Risk', 2: 'High Risk'}
RISK_COLORS = ['#2E7D32', '#F9A825', '#C62828']

# ── STEP 2: Train model ───────────────────────────────────────────────────────
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_named)
X_scaled_df = pd.DataFrame(X_scaled, columns=feature_names)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled_df, y, test_size=0.2, random_state=42, stratify=y
)

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)
print(f"Model accuracy: {model.score(X_test, y_test):.4f}")

# ── STEP 3: Compute SHAP values ───────────────────────────────────────────────
print("\nComputing SHAP values (this takes ~30 seconds)...")

# Use LinearExplainer for Logistic Regression (fast + accurate)
explainer = shap.LinearExplainer(model, X_train, feature_perturbation="interventional")
shap_values = explainer.shap_values(X_test)

# shap_values from LinearExplainer (multiclass) is (n_samples, n_features, n_classes)
print(f"SHAP values computed. Shape: {shap_values.shape}")

# ── STEP 4: PLOT 1 — Global Feature Importance (Mean |SHAP|) ─────────────────
# Shows which features matter most across ALL predictions
print("\nGenerating Plot 1: Global Feature Importance...")

# Mean absolute SHAP across all classes and all samples
mean_shap_per_feature = np.mean(np.abs(shap_values), axis=(0, 2))
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'SHAP Importance': mean_shap_per_feature
}).sort_values('SHAP Importance', ascending=True)

fig, ax = plt.subplots(figsize=(9, 8))
colors = ['#C62828' if v > 0.04 else '#1565C0' if v > 0.02 else '#546E7A'
          for v in importance_df['SHAP Importance']]
bars = ax.barh(importance_df['Feature'], importance_df['SHAP Importance'],
               color=colors, height=0.65, edgecolor='white')
for bar, val in zip(bars, importance_df['SHAP Importance']):
    ax.text(val + 0.001, bar.get_y() + bar.get_height()/2,
            f'{val:.4f}', va='center', ha='left', fontsize=8.5, fontweight='bold')
ax.set_title('Global Feature Importance — Mean |SHAP| Value\n'
             '(How much each feature contributes to predictions on average)',
             fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Mean |SHAP Value|  (higher = more important)', fontsize=11)
high_p = mpatches.Patch(color='#C62828', label='High importance (>0.04)')
mid_p  = mpatches.Patch(color='#1565C0', label='Medium importance (>0.02)')
low_p  = mpatches.Patch(color='#546E7A', label='Lower importance')
ax.legend(handles=[high_p, mid_p, low_p], fontsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.25, axis='x', linestyle='--')
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig('shap_1_global_importance.png', dpi=150, bbox_inches='tight')
plt.show()
print("  Saved: shap_1_global_importance.png")

# ── STEP 5: PLOT 2 — SHAP Summary Plot (Beeswarm) per class ──────────────────
# Shows direction: does high sleep REDUCE or INCREASE risk?
print("Generating Plot 2: SHAP Summary (Beeswarm) plots...")

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
for i, (ax, class_name, color) in enumerate(
        zip(axes, ['Low Risk', 'Moderate Risk', 'High Risk'], RISK_COLORS)):
    # Sort features by mean |SHAP| for this class
    class_shap = shap_values[:, :, i]  # (n_samples, n_features)
    mean_abs = np.abs(class_shap).mean(axis=0)
    top_idx  = np.argsort(mean_abs)[-15:]  # top 15 features
    top_names = [feature_names[j] for j in top_idx]
    top_shap  = class_shap[:, top_idx]
    top_feat  = X_test.values[:, top_idx]

    # Beeswarm-style scatter
    for fi in range(len(top_idx)):
        y_pos    = fi
        sv       = top_shap[:, fi]
        fv       = top_feat[:, fi]
        # color by feature value (low=blue, high=red)
        norm_fv  = (fv - fv.min()) / (fv.max() - fv.min() + 1e-9)
        colors_pt = plt.cm.RdYlBu_r(norm_fv)
        jitter   = np.random.RandomState(42).uniform(-0.25, 0.25, len(sv))
        ax.scatter(sv, np.full_like(sv, y_pos) + jitter,
                   c=colors_pt, alpha=0.5, s=8, linewidths=0)
    ax.axvline(0, color='black', lw=0.8, alpha=0.5)
    ax.set_yticks(range(len(top_names)))
    ax.set_yticklabels(top_names, fontsize=8.5)
    ax.set_title(f'{class_name}', fontsize=12, fontweight='bold', color=color)
    ax.set_xlabel('SHAP value', fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=0.2, axis='x', linestyle='--')

# Shared colorbar
sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=plt.Normalize(0, 1))
sm.set_array([])
fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.02,
             pad=0.08, label='Feature value  (blue = low, red = high)')
fig.suptitle('SHAP Summary — Feature Impact on Each Risk Class\n'
             'Each dot = one student. Position = SHAP value. Color = feature value',
             fontsize=13, fontweight='bold')
plt.savefig('shap_2_summary_beeswarm.png', dpi=150, bbox_inches='tight')
plt.show()
print("  Saved: shap_2_summary_beeswarm.png")

# ── STEP 6: PLOT 3 — Class-specific Bar Plot (Top 10 features) ───────────────
print("Generating Plot 3: Top features per risk class...")

fig, axes = plt.subplots(1, 3, figsize=(15, 6), sharey=False)
for i, (ax, class_name, color) in enumerate(
        zip(axes, ['Low Risk', 'Moderate Risk', 'High Risk'], RISK_COLORS)):
    
    class_shap = shap_values[:, :, i]  # (n_samples, n_features)
    mean_abs = np.abs(class_shap).mean(axis=0)
    top_idx  = np.argsort(mean_abs)[-10:]
    top_names = [feature_names[j] for j in top_idx]
    top_vals  = mean_abs[top_idx]
    ax.barh(top_names, top_vals, color=color, alpha=0.82,
            height=0.6, edgecolor='white')
    for bar, val in zip(ax.patches, top_vals):
        ax.text(val + 0.001, bar.get_y() + bar.get_height()/2,
                f'{val:.3f}', va='center', ha='left', fontsize=8)
    ax.set_title(class_name, fontsize=12, fontweight='bold', color=color)
    ax.set_xlabel('Mean |SHAP|', fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=0.2, axis='x', linestyle='--')
fig.suptitle('Top 10 Features Driving Each Risk Class',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('shap_3_per_class_bar.png', dpi=150, bbox_inches='tight')
plt.show()
print("  Saved: shap_3_per_class_bar.png")

# ── STEP 7: PLOT 4 — Individual Force Plot (3 example students) ──────────────
# Shows exactly WHY a specific student got their prediction
print("Generating Plot 4: Individual student explanations...")

# Find one example of each risk class in test set
examples = {}
for cls in [0, 1, 2]:
    idx_list = [i for i, v in enumerate(y_test.values) if v == cls]
    if idx_list:
        examples[cls] = idx_list[0]

fig, axes = plt.subplots(3, 1, figsize=(14, 9))
for cls, (ax, class_name, bg_color) in zip(
        [0, 1, 2], zip(axes,
                       ['Low Risk Student', 'Moderate Risk Student', 'High Risk Student'],
                       ['#E8F5E9', '#FFFDE7', '#FFEBEE'])):
    if cls not in examples:
        ax.axis('off')
        continue

    idx       = examples[cls]
    # mean across classes for this sample
    sv        = np.mean(shap_values[idx], axis=1)
    # class-specific SHAP values for this sample
    sv_cls    = shap_values[idx, :, cls]
    feat_vals = X_test.iloc[idx].values

    # Sort by absolute SHAP for this class
    order = np.argsort(np.abs(sv_cls))[-12:]
    names = [feature_names[j] for j in order]
    vals  = sv_cls[order]
    fvals = feat_vals[order]

    bar_colors = ['#C62828' if v > 0 else '#1565C0' for v in vals]
    ax.set_facecolor(bg_color)
    bars = ax.barh(names, vals, color=bar_colors, height=0.6, edgecolor='white')
    for bar, sv_val, fv in zip(bars, vals, fvals):
        ax.text(sv_val + (0.002 if sv_val >= 0 else -0.002),
                bar.get_y() + bar.get_height()/2,
                f'{sv_val:+.3f}  (val={fv:.1f})',
                va='center', ha='left' if sv_val >= 0 else 'right',
                fontsize=8)
    ax.axvline(0, color='black', lw=1)
    pred_class = RISK_LABELS[model.predict(X_test.iloc[[idx]])[0]]
    ax.set_title(f'{class_name}  →  Predicted: {pred_class}',
                 fontsize=11, fontweight='bold',
                 color=['#2E7D32', '#F9A825', '#C62828'][cls])
    ax.set_xlabel('SHAP value  (red = pushes toward this class, blue = pushes away)', fontsize=8.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=0.2, axis='x', linestyle='--')

fig.suptitle('Individual Student Explanations — Why Did the Model Predict This Risk Level?',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('shap_4_individual_explanations.png', dpi=150, bbox_inches='tight')
plt.show()
print("  Saved: shap_4_individual_explanations.png")

# ── STEP 8: Print key insights ────────────────────────────────────────────────
print("\n" + "=" * 65)
print("SHAP KEY INSIGHTS")
print("=" * 65)
print("\nTop 5 most important features globally (by mean |SHAP|):")
top5 = importance_df.tail(5).iloc[::-1]
for _, row in top5.iterrows():
    print(f"  {row['Feature']:35s}: {row['SHAP Importance']:.5f}")

print("\nFor HIGH RISK prediction, the most influential feature is:")
hr_mean = np.abs(shap_values[:, :, 2]).mean(axis=0)
top_hr  = np.argmax(hr_mean)
print(f"  {feature_names[top_hr]}  (mean |SHAP| = {hr_mean[top_hr]:.5f})")

print("\n4 plots saved:")
print("  shap_1_global_importance.png  — Use in PPT slide & research paper")
print("  shap_2_summary_beeswarm.png   — Use in research paper methodology")
print("  shap_3_per_class_bar.png      — Use in results section")
print("  shap_4_individual_explanations.png — Use in Streamlit app")
print("\nUpgrade 1 (SHAP) complete!")
