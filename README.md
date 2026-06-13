# 🧠 AI-Based Mental Health Risk Prediction System

**🔴 Live App:** [mental-health-predictor-0oat.onrender.com](https://mental-health-predictor-0oat.onrender.com)

---

## About

An AI-powered web application that predicts depression risk levels (**Low / Moderate / High**) for university students using the validated PHQ-9 depression screening scale combined with lifestyle and behavioral data.

**Course:** Major Project DS4270  
**Institution:** Manipal University Jaipur  
**Author:** Priyanshi Goel  
**Faculty Mentor:** Dr. Aparna Tripathi

---

## Key Results

| Metric | Value |
|--------|-------|
| Dataset | 1,151 student responses |
| Features | 22 behavioral + PHQ-9 indicators |
| Best Model | Logistic Regression |
| Test Accuracy | **95.67%** |
| Weighted F1-Score | **95.65%** |
| Low Risk F1 | **97%** |
| Moderate Risk F1 | **95%** |
| High Risk F1 | **91%** |
| Cross-Validation Accuracy | **95.98%** |

---

## App Features

- **PHQ-9 Depression Screening** — validated 9-item questionnaire (0–3 scale)
- **Lifestyle Assessment** — sleep duration, exercise frequency, screen time, social support
- **Stress Indicators** — academic workload, exam anxiety, difficulty relaxing, overwhelm
- **3-Class Risk Prediction** — Low / Moderate / High depression risk
- **Prediction Confidence** — probability scores for all 3 risk classes
- **SHAP Explainability** — global feature importance + per-class feature impact charts
- **Personalised Recommendations** — tailored lifestyle advice per risk level
- **Crisis Resources** — Indian helpline numbers displayed for High Risk users

---

## SHAP Explainability

The app includes full SHAP (SHapley Additive exPlanations) analysis showing:
- **Global Feature Importance** — which features matter most across all predictions
- **Per-class Bar Charts** — top 10 features driving each risk class separately

Top findings from SHAP analysis:
- PHQ-3 (Sleep trouble) is the single most influential feature (SHAP = 0.5996)
- All 9 PHQ-9 symptom items dominate the top predictions
- Lifestyle features (difficulty relaxing, exercise, sleep hours) are the strongest non-PHQ predictors

---

## Tech Stack

```
Python 3.11
pandas · numpy · scikit-learn
shap · matplotlib · seaborn
Flask (deployed on Render)
```

---

## Project Structure

```
mental-health-predictor/
│
├── README.md                           # Project documentation
├── requirements.txt                    # Python dependencies
├── MH_Survey_Cleaned_1151.csv          # Cleaned dataset (1,151 responses)
│
├── scripts/                            # All Python implementation scripts
│   ├── Phase3_EDA.py                   #   → Exploratory Data Analysis
│   ├── Phase4_Model_Training.py        #   → Model Training & Comparison
│   ├── Tier1_Upgrade1_SHAP.py          #   → SHAP Explainability Analysis
│   ├── Tier1_Upgrade2_SMOTE.py         #   → SMOTE Class Balancing
│   ├── Tier1_Upgrade3_GAD7.py          #   → GAD-7 Anxiety Estimation
│   ├── build_dashboard.py              #   → Dashboard Builder
│   └── test_prediction.py             #   → Model Testing Script
│
├── models/                             # Trained model artifacts
│   ├── best_model.pkl                  #   → Final Logistic Regression model
│   ├── best_model_smote.pkl            #   → SMOTE-balanced model
│   ├── scaler.pkl                      #   → MinMax feature scaler
│   └── feature_names.pkl              #   → Feature column names
│
├── outputs/                            # Generated visualizations
│   ├── eda/                            #   → EDA plots (Phase 3)
│   │   ├── eda_1_risk_distribution.png
│   │   ├── eda_2_phq_histogram.png
│   │   ├── eda_3_sleep_phq.png
│   │   ├── eda_4_exercise_phq.png
│   │   ├── eda_5_correlation_heatmap.png
│   │   ├── eda_6_social_support_phq.png
│   │   ├── eda_7_gender_risk.png
│   │   ├── eda_8_feature_correlations.png
│   │   ├── eda_9_phq_boxplot.png
│   │   └── eda_10_stress_by_risk.png
│   ├── model/                          #   → Model comparison (Phase 4)
│   │   ├── model_comparison.png
│   │   └── confusion_matrices.png
│   ├── shap/                           #   → SHAP explainability
│   │   ├── shap_1_global_importance.png
│   │   ├── shap_2_summary_beeswarm.png
│   │   ├── shap_3_per_class_bar.png
│   │   └── shap_4_individual_explanations.png
│   └── smote/                          #   → SMOTE analysis
│       ├── smote_1_comparison.png
│       ├── smote_2_class_distribution.png
│       └── smote_3_confusion_matrix.png
│
├── app.py                              # Flask web application backend
├── Procfile                            # Render deployment config
├── runtime.txt                         # Python version for Render
├── templates/                          # HTML templates
│   └── index.html
└── static/                             # Static web assets
    └── images/
        └── (SHAP images for web display)
```

---

## How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/Priyanshigoel12/mental-health-predictor.git
cd mental-health-predictor

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
# Opens at http://localhost:5000
```

---

## Dataset

Primary data collected via **Google Forms** survey — **1,151 student respondents** across academic years 1–6, Manipal University Jaipur, 2026.

Features collected:
- **Demographics:** Age, gender, year of study, field of study
- **Lifestyle:** Sleep hours, exercise frequency, screen time, study hours outside class
- **Stress Scale:** 4 Likert-scale items (academic stress, relaxation, overwhelm, exam anxiety)
- **PHQ-9:** 9 validated depression symptom items + total score
- **Target:** Depression Risk Label — Low (PHQ 0–9), Moderate (PHQ 10–19), High (PHQ 20+)

---

## Models Compared

| Model | CV Accuracy | Test Accuracy | F1-Score |
|-------|------------|--------------|----------|
| **Logistic Regression** | **95.98%** | **95.67%** | **95.65%** |
| SVM | 94.24% | 93.51% | 93.48% |
| Random Forest | 92.39% | 89.18% | 89.15% |
| Decision Tree | 80.54% | 83.55% | 83.48% |

---

## Research Context

This project addresses the lack of AI-based mental health screening tools specifically designed for Indian university students. Existing literature uses single data sources (clinical interviews OR social media OR questionnaires). This system uniquely combines:

1. Student lifestyle indicators (sleep, exercise, screen time, social support)
2. Validated PHQ-9 clinical depression screening
3. Machine learning classification with SHAP explainability

---

## Disclaimer

This tool is for **educational and research purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment.

**Crisis Helplines (India):**
- **iCall:** 9152987821 *(free, confidential)*
- **Vandrevala Foundation:** 1860-2662-345 *(24/7)*
- **NIMHANS:** 080-46110007

---

## Citation

```bibtex
@misc{goel2026mentalhealth,
  author    = {Priyanshi Goel},
  title     = {AI-Based Mental Health Risk Prediction System for University Students},
  year      = {2026},
  note      = {Major Project DS4270, Manipal University Jaipur},
  url       = {https://mental-health-riskpredictor.streamlit.app}
}
```

---

## Acknowledgements

Special thanks to **Dr. Aparna Tripathi** for her guidance and mentorship throughout this project.
