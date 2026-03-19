# =============================================================================
# PHASE 3 — EXPLORATORY DATA ANALYSIS (EDA)
# Project: AI-Based Mental Health Risk Prediction System for University Students
# Author : Priyanshi Goel | DS4270 | Manipal University Jaipur
# Dataset: MH_Survey_Cleaned_1151.csv  (1151 responses, 25 columns)
# IDE    : VS Code  |  Run: python Phase3_EDA.py
# =============================================================================

# ── STEP 0: Install libraries (run once in terminal) ─────────────────────────
# pip install pandas numpy matplotlib seaborn

# ── STEP 1: Imports ───────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Global plot style
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--'
})

PALETTE  = ['#2E7D32', '#F9A825', '#C62828']   # Low / Moderate / High
RISK_MAP = {0: 'Low Risk', 1: 'Moderate Risk', 2: 'High Risk'}

# =============================================================================
# STEP 2: LOAD & INSPECT DATA
# =============================================================================
df = pd.read_csv('MH_Survey_Cleaned_1151.csv')   # <-- put CSV in same folder

print("=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)
print(f"Shape          : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Missing values : {df.isnull().sum().sum()}")
print("\nColumn dtypes:")
print(df.dtypes)
print("\nFirst 3 rows:")
print(df.head(3).to_string())
print("\nBasic statistics:")
print(df.describe().round(2).to_string())

# Map risk label to readable string
df['Risk'] = df['Depression Risk Label'].map(RISK_MAP)

# =============================================================================
# STEP 3: RISK DISTRIBUTION
# =============================================================================
print("\n--- Risk Label Distribution ---")
risk_counts = df['Depression Risk Label'].value_counts().sort_index()
for k, v in risk_counts.items():
    print(f"  {RISK_MAP[k]:15s}: {v:4d}  ({v/len(df)*100:.1f}%)")

fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(
    ['Low Risk\n(PHQ 0–9)', 'Moderate Risk\n(PHQ 10–19)', 'High Risk\n(PHQ 20+)'],
    risk_counts.values, color=PALETTE, width=0.55, edgecolor='white', linewidth=1.2
)
for bar, val in zip(bars, risk_counts.values):
    pct = val / len(df) * 100
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8,
            f'{val}\n({pct:.1f}%)', ha='center', va='bottom',
            fontsize=11, fontweight='bold')
ax.set_title('Depression Risk Distribution  (N=1,151)', fontsize=14,
             fontweight='bold', pad=12)
ax.set_ylabel('Number of Students', fontsize=11)
ax.set_ylim(0, 620)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig('eda_1_risk_distribution.png', dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# STEP 4: PHQ-9 SCORE DISTRIBUTION (HISTOGRAM)
# =============================================================================
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(df['PHQ-9 Total Score'], bins=28, color='#1565C0',
        edgecolor='white', alpha=0.85, linewidth=0.8)
ax.axvline(x=9.5,  color='#F9A825', lw=2, linestyle='--',
           label='Low / Moderate boundary (9/10)')
ax.axvline(x=19.5, color='#C62828', lw=2, linestyle='--',
           label='Moderate / High boundary (19/20)')
ax.axvline(x=df['PHQ-9 Total Score'].mean(), color='#0D47A1', lw=2,
           linestyle=':', label=f"Mean = {df['PHQ-9 Total Score'].mean():.1f}")
ax.set_title('Distribution of PHQ-9 Total Scores  (N=1,151)',
             fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('PHQ-9 Score', fontsize=11)
ax.set_ylabel('Number of Students', fontsize=11)
ax.legend(fontsize=9)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig('eda_2_phq_histogram.png', dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# STEP 5: SLEEP DURATION vs PHQ-9
# =============================================================================
sleep_map = {0: '<5 hrs', 1: '5–6 hrs', 2: '6–7 hrs', 3: '7–8 hrs', 4: '>8 hrs'}
df['Sleep Cat'] = df['Average sleep hours'].map(sleep_map)
sleep_order = ['<5 hrs', '5–6 hrs', '6–7 hrs', '7–8 hrs', '>8 hrs']

means  = df.groupby('Sleep Cat')['PHQ-9 Total Score'].mean().reindex(sleep_order)
sleep_counts = df.groupby('Sleep Cat').size().reindex(sleep_order)
bar_colors = ['#C62828', '#E65100', '#F9A825', '#388E3C', '#1B5E20']

fig, ax = plt.subplots(figsize=(8, 4.8))
bars = ax.bar(sleep_order, means.values, color=bar_colors,
              width=0.6, edgecolor='white', linewidth=1)
for bar, val, n in zip(bars, means.values, sleep_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f'{val:.1f}\n(n={n})', ha='center', va='bottom',
            fontsize=10, fontweight='bold')
ax.axhline(y=10, color='#F9A825', lw=1.8, linestyle='--',
           label='Moderate risk threshold (10)')
ax.axhline(y=20, color='#C62828', lw=1.8, linestyle='--',
           label='High risk threshold (20)')
ax.set_title('Average PHQ-9 Score by Sleep Duration',
             fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Average Sleep Hours per Night', fontsize=11)
ax.set_ylabel('Mean PHQ-9 Score', fontsize=11)
ax.set_ylim(0, 22)
ax.legend(fontsize=9)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig('eda_3_sleep_phq.png', dpi=150, bbox_inches='tight')
plt.show()

# Key insight
print(f"\nKey Insight (Sleep vs PHQ-9):")
print(f"  <5 hrs sleep → avg PHQ-9 = {means['<5 hrs']:.1f}")
print(f"  >8 hrs sleep → avg PHQ-9 = {means['>8 hrs']:.1f}")

# =============================================================================
# STEP 6: EXERCISE FREQUENCY vs PHQ-9
# =============================================================================
ex_map = {0: 'Never', 1: '1–2x/week', 2: '3–4x/week', 3: 'Daily'}
df['Exercise Cat'] = df['Physical exercise frequency'].map(ex_map)
ex_order   = ['Never', '1–2x/week', '3–4x/week', 'Daily']
ex_means   = df.groupby('Exercise Cat')['PHQ-9 Total Score'].mean().reindex(ex_order)
ex_counts  = df.groupby('Exercise Cat').size().reindex(ex_order)
ex_colors  = ['#C62828', '#E65100', '#388E3C', '#1B5E20']

fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(ex_order, ex_means.values, color=ex_colors,
              width=0.55, edgecolor='white', linewidth=1)
for bar, val, n in zip(bars, ex_means.values, ex_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f'{val:.1f}\n(n={n})', ha='center', va='bottom',
            fontsize=10, fontweight='bold')
ax.axhline(y=10, color='#F9A825', lw=1.8, linestyle='--', label='Moderate threshold')
ax.set_title('Average PHQ-9 Score by Exercise Frequency',
             fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Exercise Frequency', fontsize=11)
ax.set_ylabel('Mean PHQ-9 Score', fontsize=11)
ax.set_ylim(0, 19)
ax.legend(fontsize=9)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig('eda_4_exercise_phq.png', dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# STEP 7: SOCIAL SUPPORT vs PHQ-9
# =============================================================================
sup_map   = {0: 'Never', 1: 'Rarely', 2: 'Sometimes', 3: 'Often', 4: 'Always'}
df['Support Cat'] = df['How often do you feel supported by friends or family?'].map(sup_map)
sup_order  = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']
sup_means  = df.groupby('Support Cat')['PHQ-9 Total Score'].mean().reindex(sup_order)
sup_counts = df.groupby('Support Cat').size().reindex(sup_order)
sup_colors = ['#C62828', '#E65100', '#F9A825', '#388E3C', '#1B5E20']

fig, ax = plt.subplots(figsize=(8, 4.8))
bars = ax.bar(sup_order, sup_means.values, color=sup_colors,
              width=0.6, edgecolor='white', linewidth=1)
for bar, val, n in zip(bars, sup_means.values, sup_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f'{val:.1f}\n(n={n})', ha='center', va='bottom',
            fontsize=10, fontweight='bold')
ax.axhline(y=10, color='#F9A825', lw=1.8, linestyle='--', label='Moderate threshold (10)')
ax.set_title('Average PHQ-9 Score by Social Support Level',
             fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Frequency of Feeling Supported', fontsize=11)
ax.set_ylabel('Mean PHQ-9 Score', fontsize=11)
ax.set_ylim(0, 20)
ax.legend(fontsize=9)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig('eda_6_social_support_phq.png', dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# STEP 8: GENDER vs RISK (Stacked Percentage Bar)
# =============================================================================
gender_map = {0: 'Male', 1: 'Female', 2: 'Other'}
df['Gender Cat'] = df['Gender'].map(gender_map)
ct = pd.crosstab(df['Gender Cat'], df['Risk'], normalize='index') * 100
ct = ct[['Low Risk', 'Moderate Risk', 'High Risk']]

fig, ax = plt.subplots(figsize=(7, 4.5))
bottom = np.zeros(len(ct))
for col, color in zip(['Low Risk', 'Moderate Risk', 'High Risk'], PALETTE):
    ax.bar(ct.index, ct[col], bottom=bottom, color=color,
           label=col, width=0.55, edgecolor='white')
    for i, (val, bot) in enumerate(zip(ct[col], bottom)):
        if val > 5:
            ax.text(i, bot + val/2, f'{val:.0f}%', ha='center',
                    va='center', fontsize=10, fontweight='bold', color='white')
    bottom += ct[col]
ax.set_title('Risk Distribution by Gender (%)', fontsize=14,
             fontweight='bold', pad=12)
ax.set_ylabel('Percentage of Students (%)', fontsize=11)
ax.set_ylim(0, 105)
ax.legend(title='Risk Level', fontsize=9)
ax.set_axisbelow(True)
ax.grid(alpha=0.3, linestyle='--', axis='y')
plt.tight_layout()
plt.savefig('eda_7_gender_risk.png', dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# STEP 9: FEATURE CORRELATION WITH PHQ-9 (Horizontal Bar Chart)
# =============================================================================
feature_cols = [
    'Average sleep hours', 'Physical exercise frequency',
    'How often do you feel supported by friends or family?',
    'Daily screen time', 'Do you feel academically overloaded?',
    'I feel stressed because of academic workload',
    'I find it difficult to relax',
    'I feel overwhelmed by responsibilities',
    'I feel anxious about exams or deadlines',
]
short_names = {
    'Average sleep hours':                                   'Sleep hours',
    'Physical exercise frequency':                           'Exercise freq',
    'How often do you feel supported by friends or family?': 'Social support',
    'Daily screen time':                                     'Screen time',
    'Do you feel academically overloaded?':                  'Acad. overload',
    'I feel stressed because of academic workload':          'Stress (workload)',
    'I find it difficult to relax':                          'Difficulty relaxing',
    'I feel overwhelmed by responsibilities':                'Overwhelmed',
    'I feel anxious about exams or deadlines':               'Exam anxiety',
}
corrs = {short_names[f]: df[f].corr(df['PHQ-9 Total Score'])
         for f in feature_cols}
corrs = dict(sorted(corrs.items(), key=lambda x: x[1]))

print("\n--- Pearson Correlations with PHQ-9 Score ---")
for name, val in corrs.items():
    direction = "positive (risk ↑)" if val > 0 else "negative (protective)"
    print(f"  {name:25s}: {val:+.3f}  → {direction}")

fig, ax = plt.subplots(figsize=(8, 5))
bar_colors = ['#C62828' if v > 0 else '#1565C0' for v in corrs.values()]
bars = ax.barh(list(corrs.keys()), list(corrs.values()),
               color=bar_colors, height=0.6, edgecolor='white')
for bar, val in zip(bars, corrs.values()):
    x  = val + 0.01 if val >= 0 else val - 0.01
    ha = 'left'       if val >= 0 else 'right'
    ax.text(x, bar.get_y() + bar.get_height()/2, f'{val:.3f}',
            va='center', ha=ha, fontsize=9, fontweight='bold')
ax.axvline(x=0, color='black', lw=0.8)
ax.set_title('Feature Correlation with PHQ-9 Score',
             fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Pearson Correlation Coefficient', fontsize=11)
ax.set_xlim(-0.65, 0.55)
red_patch  = plt.Rectangle((0,0), 1, 1, color='#C62828',
                             label='Positive — risk increases')
blue_patch = plt.Rectangle((0,0), 1, 1, color='#1565C0',
                             label='Negative — protective factor')
ax.legend(handles=[red_patch, blue_patch], fontsize=9)
ax.set_axisbelow(True)
ax.grid(alpha=0.3, linestyle='--', axis='x')
plt.tight_layout()
plt.savefig('eda_8_feature_correlations.png', dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# STEP 10: FULL CORRELATION HEATMAP
# =============================================================================
heatmap_cols = feature_cols + ['PHQ-9 Total Score', 'Depression Risk Label']
sub = df[heatmap_cols].rename(columns={**short_names,
    'PHQ-9 Total Score': 'PHQ-9 Score',
    'Depression Risk Label': 'Risk Label'})
corr_matrix = sub.corr()

fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
            cmap='RdYlGn_r', center=0, vmin=-1, vmax=1, ax=ax,
            annot_kws={'size': 8}, linewidths=0.5, square=True,
            cbar_kws={'shrink': 0.7})
ax.set_title('Feature Correlation Heatmap', fontsize=14, fontweight='bold', pad=14)
plt.xticks(rotation=35, ha='right', fontsize=9)
plt.yticks(rotation=0, fontsize=9)
plt.tight_layout()
plt.savefig('eda_5_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# STEP 11: PHQ-9 BOX PLOT BY RISK GROUP
# =============================================================================
risk_order = ['Low Risk', 'Moderate Risk', 'High Risk']
data_by_risk = [df[df['Risk'] == r]['PHQ-9 Total Score'].values for r in risk_order]

fig, ax = plt.subplots(figsize=(8, 4.8))
bp = ax.boxplot(data_by_risk, patch_artist=True, notch=False,
                medianprops={'color': 'white', 'linewidth': 2.5},
                whiskerprops={'linewidth': 1.5},
                capprops={'linewidth': 1.5},
                flierprops={'marker': 'o', 'markersize': 3, 'alpha': 0.4})
for patch, color in zip(bp['boxes'], PALETTE):
    patch.set_facecolor(color)
    patch.set_alpha(0.8)
ax.set_xticklabels(risk_order, fontsize=11)
ax.set_title('PHQ-9 Score Distribution by Risk Group',
             fontsize=14, fontweight='bold', pad=12)
ax.set_ylabel('PHQ-9 Total Score', fontsize=11)
ax.set_axisbelow(True)
ax.grid(alpha=0.3, linestyle='--', axis='y')
for i, (data, color) in enumerate(zip(data_by_risk, PALETTE), 1):
    ax.text(i, -2.5, f'n={len(data)}\nμ={np.mean(data):.1f}',
            ha='center', va='top', fontsize=9, color=color, fontweight='bold')
plt.tight_layout()
plt.savefig('eda_9_phq_boxplot.png', dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# STEP 12: STRESS INDICATORS BY RISK GROUP (Grouped Bar)
# =============================================================================
stress_cols  = [
    'I feel stressed because of academic workload',
    'I find it difficult to relax',
    'I feel overwhelmed by responsibilities',
    'I feel anxious about exams or deadlines',
]
stress_short = ['Stressed\n(workload)', 'Difficulty\nrelaxing',
                'Overwhelmed', 'Exam\nanxiety']

fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(stress_cols))
width = 0.25
for i, (label, color) in enumerate(zip(['Low Risk', 'Moderate Risk', 'High Risk'],
                                        PALETTE)):
    sub  = df[df['Risk'] == label]
    means = [sub[c].mean() for c in stress_cols]
    ax.bar(x + (i-1)*width, means, width, label=label,
           color=color, alpha=0.85, edgecolor='white')
ax.set_xticks(x)
ax.set_xticklabels(stress_short, fontsize=10)
ax.set_title('Mean Stress Indicator Scores by Risk Group',
             fontsize=14, fontweight='bold', pad=12)
ax.set_ylabel('Mean Score (1–5 scale)', fontsize=11)
ax.set_ylim(0, 5.8)
ax.legend(fontsize=9, loc='upper left')
ax.set_axisbelow(True)
ax.grid(alpha=0.3, linestyle='--', axis='y')
plt.tight_layout()
plt.savefig('eda_10_stress_by_risk.png', dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# STEP 13: PRINT FINAL EDA SUMMARY
# =============================================================================
print("\n" + "=" * 60)
print("EDA SUMMARY — KEY FINDINGS")
print("=" * 60)
print(f"Total responses       : {len(df)}")
print(f"Low Risk (0)          : {risk_counts[0]} ({risk_counts[0]/len(df)*100:.1f}%)")
print(f"Moderate Risk (1)     : {risk_counts[1]} ({risk_counts[1]/len(df)*100:.1f}%)")
print(f"High Risk (2)         : {risk_counts[2]} ({risk_counts[2]/len(df)*100:.1f}%)")
print(f"Mean PHQ-9 Score      : {df['PHQ-9 Total Score'].mean():.1f}")
print(f"\nStrongest protective factors  (negative correlation with PHQ-9):")
neg = {k:v for k,v in corrs.items() if v < 0}
for k,v in sorted(neg.items(), key=lambda x: x[1]):
    print(f"  {k:25s}: r = {v:.3f}")
print(f"\nStrongest risk factors (positive correlation with PHQ-9):")
pos = {k:v for k,v in corrs.items() if v > 0}
for k,v in sorted(pos.items(), key=lambda x: -x[1]):
    print(f"  {k:25s}: r = {v:.3f}")
print("\nAll 10 plots saved as PNG files in the current folder.")
