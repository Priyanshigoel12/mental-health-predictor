# 🧠 AI-Based Mental Health Risk Prediction System

**Live App:** [Click here to try it](https://mental-health-riskpredictor.streamlit.app)  
*(Update this link after deployment)*

---

## About

An AI-powered web application that predicts depression risk levels (Low / Moderate / High) for university students using PHQ-9 validated screening and lifestyle behavioral data.

**Built for:** Major Project DS4270 | Manipal University Jaipur  
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
| High Risk F1 | **91.23%** |

---

## Features

- **PHQ-9 Depression Screening** — validated 9-item questionnaire
- **Lifestyle Assessment** — sleep, exercise, screen time, social support
- **Stress Indicators** — academic workload, anxiety, overwhelm
- **3-Class Risk Prediction** — Low / Moderate / High
- **Confidence Scores** — probability for each risk class
- **SHAP Explainability** — shows WHY the model made its prediction
- **Personalised Recommendations** — tailored advice per risk level
- **Crisis Resources** — helpline numbers for High Risk users

---

## Tech Stack

```
Python · pandas · scikit-learn · SHAP · Streamlit · Matplotlib · Seaborn
```

---

## Project Structure

```
mental health/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
│
├── best_model.pkl                  # Trained Logistic Regression model
├── scaler.pkl                      # MinMax feature scaler
├── feature_names.pkl               # Feature column names
│
├── shap_1_global_importance.png    # SHAP global feature importance chart
├── shap_3_per_class_bar.png        # SHAP per-class feature importance
│
└── README.md
```

---

## How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/mental-health-predictor.git
cd mental-health-predictor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

---

## Dataset

Primary data collected via Google Forms survey — 1,151 student respondents across academic years 1–6, Manipal University Jaipur, 2026. Features include demographics, lifestyle indicators, validated PHQ-9 depression screening scale, and stress assessment items.

---

## Disclaimer

This tool is for **educational purposes only** and is not a substitute for professional medical advice, diagnosis, or treatment. If you are in distress, please contact a healthcare professional.

**Helplines (India):**
- iCall: 9152987821
- Vandrevala Foundation: 1860-2662-345 (24/7)

---

## Citation

If you use this work, please cite:
```
Goel, P. (2026). AI-Based Mental Health Risk Prediction System for University Students.
Major Project DS4270, Manipal University Jaipur.
```
