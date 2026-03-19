# =============================================================================
# PHASE 4 — MODEL TRAINING & EVALUATION
# Project: AI-Based Mental Health Risk Prediction System for University Students
# Author : Priyanshi Goel | DS4270 | Manipal University Jaipur
# Dataset: MH_Survey_Cleaned_1151.csv
# IDE    : VS Code  |  Run: python Phase4_Model_Training.py
# =============================================================================

# ── STEP 0: Install libraries (run once in terminal) ─────────────────────────
# pip install pandas numpy matplotlib seaborn scikit-learn

# ── STEP 1: Imports ───────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, ConfusionMatrixDisplay
)
import pickle   # to save the best model

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

RISK_NAMES = ['Low Risk', 'Moderate Risk', 'High Risk']

# =============================================================================
# STEP 2: LOAD DATA
# =============================================================================
df = pd.read_csv('MH_Survey_Cleaned_1151.csv')
print("=" * 60)
print("PHASE 4 — MODEL TRAINING")
print("=" * 60)
print(f"Dataset shape: {df.shape}")

# =============================================================================
# STEP 3: PREPARE FEATURES (X) AND TARGET (y)
# =============================================================================
# Drop non-numeric and non-feature columns
DROP_COLS = ['Field of Study', 'PHQ-9 Total Score', 'Depression Risk Label']

X = df.drop(columns=DROP_COLS)
y = df['Depression Risk Label']

print(f"\nFeatures used ({X.shape[1]}):")
for col in X.columns:
    print(f"  • {col}")
print(f"\nTarget classes: {y.value_counts().sort_index().to_dict()}")

# =============================================================================
# STEP 4: NORMALIZE FEATURES (Min-Max Scaling)
# =============================================================================
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
print("\nFeature normalization applied (Min-Max Scaler).")

# =============================================================================
# STEP 5: TRAIN / TEST SPLIT  (80% train, 20% test)
# =============================================================================
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y,
    test_size=0.2,
    random_state=42,
    stratify=y          # keeps class proportions equal in both splits
)
print(f"\nTrain set : {X_train.shape[0]} samples")
print(f"Test set  : {X_test.shape[0]} samples")

# =============================================================================
# STEP 6: DEFINE MODELS
# =============================================================================
models = {
    'Logistic Regression': LogisticRegression(
        max_iter=1000, random_state=42
    ),
    'Decision Tree': DecisionTreeClassifier(
        max_depth=8, random_state=42
    ),
    'Random Forest': RandomForestClassifier(
        n_estimators=200, max_depth=10, random_state=42, n_jobs=-1
    ),
    'SVM': SVC(
        kernel='rbf', C=1.0, gamma='scale', random_state=42, probability=True
    ),
}

# =============================================================================
# STEP 7: TRAIN + EVALUATE ALL MODELS
# =============================================================================
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
results = {}

print("\n" + "=" * 60)
print("TRAINING & CROSS-VALIDATION RESULTS")
print("=" * 60)

for name, model in models.items():
    # 5-Fold Cross-Validation on training data
    cv_scores = cross_val_score(model, X_train, y_train,
                                cv=cv, scoring='accuracy')

    # Train on full training set
    model.fit(X_train, y_train)

    # Predict on test set
    y_pred = model.predict(X_test)

    # Metrics
    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec  = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1   = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    results[name] = {
        'model':    model,
        'cv_mean':  cv_scores.mean(),
        'cv_std':   cv_scores.std(),
        'accuracy': acc,
        'precision': prec,
        'recall':   rec,
        'f1':       f1,
        'y_pred':   y_pred,
    }

    print(f"\n{name}")
    print(f"  CV Accuracy   : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print(f"  Test Accuracy : {acc:.4f}")
    print(f"  Precision     : {prec:.4f}")
    print(f"  Recall        : {rec:.4f}")
    print(f"  F1-Score      : {f1:.4f}")

# =============================================================================
# STEP 8: COMPARISON TABLE
# =============================================================================
print("\n" + "=" * 60)
print("MODEL COMPARISON TABLE")
print("=" * 60)
print(f"{'Model':<22} {'CV Acc':>8} {'Test Acc':>10} {'Precision':>11} {'Recall':>8} {'F1':>8}")
print("-" * 72)
for name, r in results.items():
    print(f"{name:<22} {r['cv_mean']:>8.4f} {r['accuracy']:>10.4f} "
          f"{r['precision']:>11.4f} {r['recall']:>8.4f} {r['f1']:>8.4f}")

# =============================================================================
# STEP 9: PLOT — MODEL COMPARISON BAR CHART
# =============================================================================
metrics    = ['accuracy', 'precision', 'recall', 'f1']
met_labels = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
model_names = list(results.keys())
colors = ['#1565C0', '#2E7D32', '#F9A825', '#C62828']

fig, axes = plt.subplots(1, 4, figsize=(14, 4.5), sharey=False)
for ax, metric, label in zip(axes, metrics, met_labels):
    vals  = [results[m][metric] for m in model_names]
    short = ['LR', 'DT', 'RF', 'SVM']
    bars  = ax.bar(short, vals, color=colors, width=0.55,
                   edgecolor='white', linewidth=1)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.005,
                f'{val:.3f}', ha='center', va='bottom',
                fontsize=9, fontweight='bold')
    ax.set_title(label, fontsize=12, fontweight='bold')
    ax.set_ylim(0, 1.1)
    ax.set_axisbelow(True)
    ax.grid(alpha=0.3, linestyle='--', axis='y')
fig.suptitle('Model Performance Comparison', fontsize=14,
             fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('model_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nSaved: model_comparison.png")

# =============================================================================
# STEP 10: CONFUSION MATRICES FOR ALL MODELS
# =============================================================================
fig, axes = plt.subplots(1, 4, figsize=(18, 4.5))
for ax, (name, r) in zip(axes, results.items()):
    cm  = confusion_matrix(y_test, r['y_pred'])
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                  display_labels=RISK_NAMES)
    disp.plot(ax=ax, cmap='Blues', colorbar=False)
    ax.set_title(name, fontsize=11, fontweight='bold')
    ax.set_xlabel('Predicted', fontsize=9)
    ax.set_ylabel('Actual', fontsize=9)
    plt.setp(ax.get_xticklabels(), rotation=20, ha='right', fontsize=8)
    plt.setp(ax.get_yticklabels(), fontsize=8)
plt.suptitle('Confusion Matrices — All Models', fontsize=13,
             fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('confusion_matrices.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: confusion_matrices.png")

# =============================================================================
# STEP 11: PICK BEST MODEL (by F1-Score)
# =============================================================================
best_name  = max(results, key=lambda m: results[m]['f1'])
best_model = results[best_name]['model']

print("\n" + "=" * 60)
print(f"BEST MODEL  →  {best_name}")
print(f"  F1-Score  : {results[best_name]['f1']:.4f}")
print(f"  Accuracy  : {results[best_name]['accuracy']:.4f}")
print("=" * 60)

# Full classification report for best model
print(f"\nDetailed Classification Report — {best_name}:")
print(classification_report(y_test, results[best_name]['y_pred'],
                             target_names=RISK_NAMES))

# =============================================================================
# STEP 12: FEATURE IMPORTANCE (if Random Forest is best)
# =============================================================================
if best_name == 'Random Forest':
    importances = best_model.feature_importances_
    feat_imp    = pd.Series(importances, index=X.columns).sort_values(ascending=True)
    top15       = feat_imp.tail(15)

    fig, ax = plt.subplots(figsize=(8, 6))
    colors  = ['#C62828' if v > 0.05 else '#1565C0' for v in top15.values]
    ax.barh(top15.index, top15.values, color=colors,
            height=0.6, edgecolor='white')
    ax.set_title(f'Feature Importances — {best_name}',
                 fontsize=14, fontweight='bold', pad=12)
    ax.set_xlabel('Importance Score', fontsize=11)
    ax.set_axisbelow(True)
    ax.grid(alpha=0.3, linestyle='--', axis='x')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Saved: feature_importance.png")
    print("\nTop 5 most important features:")
    for feat, imp in feat_imp.tail(5).items()[::-1]:
        print(f"  {feat:<45s}: {imp:.4f}")

# =============================================================================
# STEP 13: SAVE BEST MODEL + SCALER (for Phase 6 deployment)
# =============================================================================
with open('best_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

with open('feature_names.pkl', 'wb') as f:
    pickle.dump(list(X.columns), f)

print(f"\nModel saved  → best_model.pkl   ({best_name})")
print("Scaler saved → scaler.pkl")
print("Feature names saved → feature_names.pkl")
print("\nPhase 4 complete! Ready for Phase 5 (deployment).")
