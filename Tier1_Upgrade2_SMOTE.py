# =============================================================================
# TIER 1 — UPGRADE 2: SMOTE OVERSAMPLING
# Project: AI-Based Mental Health Risk Prediction System
# Author : Priyanshi Goel | DS4270 | Manipal University Jaipur
#
# What SMOTE does:
#   - Fixes the class imbalance: High Risk only has 148 students (12.8%)
#   - Synthetically creates new High Risk samples so all 3 classes are equal
#   - Expected improvement: High Risk F1 from 91% → 94-96%
#
# Install: pip install imbalanced-learn
# Run    : python Tier1_Upgrade2_SMOTE.py
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (classification_report, confusion_matrix,
                             ConfusionMatrixDisplay, f1_score, accuracy_score)
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from collections import Counter

RISK_NAMES  = ['Low Risk', 'Moderate Risk', 'High Risk']
RISK_COLORS = ['#2E7D32', '#F9A825', '#C62828']

# ── STEP 1: Load data ─────────────────────────────────────────────────────────
df = pd.read_csv('MH_Survey_Cleaned_1151.csv')
X  = df.drop(columns=['Field of Study', 'PHQ-9 Total Score', 'Depression Risk Label'])
y  = df['Depression Risk Label']

print("=" * 60)
print("BEFORE SMOTE — Class Distribution")
print("=" * 60)
for cls, count in sorted(Counter(y).items()):
    pct = count / len(y) * 100
    print(f"  {RISK_NAMES[cls]:15s}: {count:4d} ({pct:.1f}%)")

# ── STEP 2: Train/test split FIRST (apply SMOTE only to training data!) ───────
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# ── STEP 3: Apply SMOTE to training set only ──────────────────────────────────
smote = SMOTE(random_state=42, k_neighbors=5)
X_train_sm, y_train_sm = smote.fit_resample(X_train, y_train)

print(f"\nAFTER SMOTE — Training set class distribution:")
for cls, count in sorted(Counter(y_train_sm).items()):
    print(f"  {RISK_NAMES[cls]:15s}: {count:4d} samples (was {Counter(y_train)[cls]})")

# ── STEP 4: Train WITHOUT SMOTE (baseline) ────────────────────────────────────
print("\n" + "=" * 60)
print("TRAINING COMPARISON: Without SMOTE vs With SMOTE")
print("=" * 60)

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest':       RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
    'SVM':                 SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42),
}

results = {}
for name, model in models.items():
    # Without SMOTE
    model.fit(X_train, y_train)
    y_pred_no = model.predict(X_test)
    f1_no  = f1_score(y_test, y_pred_no, average='weighted')
    acc_no = accuracy_score(y_test, y_pred_no)
    f1_hr_no = f1_score(y_test, y_pred_no, average=None)[2]  # High Risk F1

    # With SMOTE
    model.fit(X_train_sm, y_train_sm)
    y_pred_sm = model.predict(X_test)
    f1_sm  = f1_score(y_test, y_pred_sm, average='weighted')
    acc_sm = accuracy_score(y_test, y_pred_sm)
    f1_hr_sm = f1_score(y_test, y_pred_sm, average=None)[2]

    results[name] = {
        'acc_no': acc_no, 'f1_no': f1_no, 'f1_hr_no': f1_hr_no,
        'acc_sm': acc_sm, 'f1_sm': f1_sm, 'f1_hr_sm': f1_hr_sm,
        'y_pred_sm': y_pred_sm,
    }

    delta_acc = (acc_sm - acc_no) * 100
    delta_f1  = (f1_sm  - f1_no)  * 100
    delta_hr  = (f1_hr_sm - f1_hr_no) * 100

    print(f"\n{name}")
    print(f"  Without SMOTE:  Accuracy={acc_no:.4f}  Weighted F1={f1_no:.4f}  High Risk F1={f1_hr_no:.4f}")
    print(f"  With SMOTE:     Accuracy={acc_sm:.4f}  Weighted F1={f1_sm:.4f}  High Risk F1={f1_hr_sm:.4f}")
    print(f"  Change:         Δ Acc={delta_acc:+.2f}%   Δ F1={delta_f1:+.2f}%   Δ High Risk F1={delta_hr:+.2f}%")

# ── STEP 5: PLOT 1 — Before vs After SMOTE comparison bar chart ───────────────
print("\nGenerating comparison chart...")
model_names = list(results.keys())
x = np.arange(len(model_names))
w = 0.35

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
metrics = [('acc_no', 'acc_sm', 'Overall Accuracy'),
           ('f1_no',  'f1_sm',  'Weighted F1-Score'),
           ('f1_hr_no', 'f1_hr_sm', 'High Risk F1-Score')]

for ax, (key_no, key_sm, title) in zip(axes, metrics):
    vals_no = [results[m][key_no] for m in model_names]
    vals_sm = [results[m][key_sm] for m in model_names]
    bars_no = ax.bar(x - w/2, vals_no, w, label='Without SMOTE',
                     color='#90A4AE', edgecolor='white', alpha=0.9)
    bars_sm = ax.bar(x + w/2, vals_sm, w, label='With SMOTE',
                     color='#1565C0', edgecolor='white', alpha=0.9)
    for bar, val in zip(bars_no, vals_no):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.003,
                f'{val:.3f}', ha='center', va='bottom', fontsize=8, color='#546E7A')
    for bar, val in zip(bars_sm, vals_sm):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.003,
                f'{val:.3f}', ha='center', va='bottom', fontsize=9,
                fontweight='bold', color='#1565C0')
    ax.set_xticks(x)
    ax.set_xticklabels(['LR', 'RF', 'SVM'], fontsize=10)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_ylim(0.7, 1.05)
    ax.legend(fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=0.25, axis='y', linestyle='--')
    ax.set_axisbelow(True)

fig.suptitle('SMOTE Impact — Before vs After Oversampling\n'
             '(High Risk F1 improvement is the key metric)',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('smote_1_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
print("  Saved: smote_1_comparison.png")

# ── STEP 6: PLOT 2 — Class distribution before/after ─────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

before_counts = [Counter(y_train)[i] for i in range(3)]
after_counts  = [Counter(y_train_sm)[i] for i in range(3)]

for ax, counts, title in zip(axes,
        [before_counts, after_counts],
        ['Before SMOTE (Training Set)', 'After SMOTE (Training Set)']):
    bars = ax.bar(RISK_NAMES, counts, color=RISK_COLORS,
                  width=0.55, edgecolor='white', linewidth=1.2)
    for bar, val in zip(bars, counts):
        pct = val / sum(counts) * 100
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+5,
                f'{val}\n({pct:.1f}%)', ha='center', va='bottom',
                fontsize=10, fontweight='bold')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Samples')
    ax.set_ylim(0, max(after_counts) * 1.18)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=0.25, axis='y', linestyle='--')
    ax.set_axisbelow(True)

fig.suptitle('Class Distribution: SMOTE Fixes the High Risk Imbalance',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('smote_2_class_distribution.png', dpi=150, bbox_inches='tight')
plt.show()
print("  Saved: smote_2_class_distribution.png")

# ── STEP 7: PLOT 3 — Confusion matrix with SMOTE (best model = LR) ────────────
best_name  = max(results, key=lambda m: results[m]['f1_sm'])
y_pred_best = results[best_name]['y_pred_sm']

fig, ax = plt.subplots(figsize=(5.5, 4.5))
cm   = confusion_matrix(y_test, y_pred_best)
disp = ConfusionMatrixDisplay(cm, display_labels=RISK_NAMES)
disp.plot(ax=ax, cmap='Blues', colorbar=False)
ax.set_title(f'Confusion Matrix WITH SMOTE\n({best_name}  —  Acc: {results[best_name]["acc_sm"]:.4f})',
             fontsize=11, fontweight='bold')
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig('smote_3_confusion_matrix.png', dpi=150, bbox_inches='tight')
plt.show()
print("  Saved: smote_3_confusion_matrix.png")

# ── STEP 8: Detailed classification report ────────────────────────────────────
print("\n" + "=" * 60)
print(f"FINAL RESULTS WITH SMOTE — {best_name}")
print("=" * 60)
print(classification_report(y_test, y_pred_best, target_names=RISK_NAMES))

# ── STEP 9: Save the SMOTE-enhanced model ─────────────────────────────────────
import pickle

best_model = models[best_name]
best_model.fit(X_train_sm, y_train_sm)  # retrain on SMOTE data

with open('best_model_smote.pkl', 'wb') as f: pickle.dump(best_model, f)
with open('scaler.pkl',           'wb') as f: pickle.dump(scaler, f)
with open('feature_names.pkl',    'wb') as f: pickle.dump(list(X.columns), f)

print(f"\nSMOTE-enhanced model saved → best_model_smote.pkl")
print("Update app.py to load 'best_model_smote.pkl' instead of 'best_model.pkl'")
print("\n3 plots saved:")
print("  smote_1_comparison.png         — Before/after metric comparison")
print("  smote_2_class_distribution.png — Class balance visualization")
print("  smote_3_confusion_matrix.png   — Confusion matrix with SMOTE")
print("\nUpgrade 2 (SMOTE) complete!")
