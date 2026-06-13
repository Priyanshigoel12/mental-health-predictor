
# ACKNOWLEDGEMENT

We would like to express our sincere gratitude to our faculty mentor, **Dr. Aparna Tripathi**, for her invaluable guidance, continuous encouragement, and insightful suggestions throughout the course of this major project. Her expertise in the domain of data science and machine learning was instrumental in shaping the direction of this work.

We are grateful to the **Department of Data Science, Manipal University Jaipur**, for providing the academic environment, computational resources, and institutional support necessary to carry out this project.

We also extend our thanks to the **1,151 student respondents** from Manipal University Jaipur who participated in our Google Forms survey. Their willingness to share personal information regarding their mental health, lifestyle habits, and academic experiences made the data collection phase of this project possible.

Finally, we would like to thank our family and friends for their constant moral support and motivation during the entire duration of this project.

---

# ABSTRACT

Mental health disorders among university students have emerged as a critical public health concern in recent years, with depression and anxiety being the most prevalent conditions affecting academic performance, social relationships, and overall quality of life. In the Indian context, the lack of accessible, AI-based mental health screening tools specifically designed for university students creates a significant gap in early detection and intervention. This project, titled **MINDscan**, aims to address this gap by developing an AI-powered web application that predicts depression risk levels (Low, Moderate, or High) for university students using the clinically validated PHQ-9 depression screening scale combined with lifestyle and behavioral data.

The methodology adopted in this project follows a systematic machine learning pipeline. Primary data was collected from 1,151 student respondents at Manipal University Jaipur through a structured Google Forms questionnaire capturing 25 attributes including demographics, lifestyle indicators, stress measures, and the nine-item PHQ-9 depression screening scale. The data was preprocessed using MinMaxScaler normalization, and four classification algorithms — Logistic Regression, Support Vector Machine (SVM), Random Forest, and Decision Tree — were trained and evaluated using 5-fold Stratified K-Fold cross-validation. Additionally, SMOTE (Synthetic Minority Over-sampling Technique) was applied to address class imbalance, and SHAP (SHapley Additive exPlanations) analysis was conducted to ensure model explainability.

The results obtained demonstrate that Logistic Regression achieved the highest performance with a test accuracy of **95.67%** and a weighted F1-Score of **95.65%**, outperforming SVM (93.51%), Random Forest (89.18%), and Decision Tree (83.55%). The 5-fold cross-validation accuracy was **95.98%**, confirming model stability. SHAP analysis revealed that PHQ-3 (Sleep trouble) is the most influential predictor (SHAP value = 0.5996), with all nine PHQ-9 symptom items dominating the top predictions. Among lifestyle features, difficulty relaxing, exercise frequency, and sleep hours emerged as the strongest non-clinical predictors.

The project was implemented using **Python 3.11** with libraries including pandas, NumPy, scikit-learn, SHAP, matplotlib, and seaborn for the machine learning backend. The web application was built using the **Flask** framework with a fully responsive single-page HTML/CSS/JavaScript frontend and deployed on **Render** cloud platform. The application provides real-time risk predictions with confidence scores, SHAP-based explainability charts, personalized lifestyle recommendations, and crisis helpline resources for high-risk users.

---

# LIST OF TABLES

| Table No | Table Title | Page No |
|----------|-------------|---------|
| Table 1.1 | PHQ-9 Depression Severity Classification | |
| Table 2.1 | Literature Review Summary | |
| Table 2.2 | Technologies and Tools Used | |
| Table 3.1 | Dataset Feature Description | |
| Table 3.2 | PHQ-9 Questionnaire Items and Scoring | |
| Table 3.3 | GAD-7 Questionnaire Items and Scoring | |
| Table 3.4 | Machine Learning Model Hyperparameters | |
| Table 4.1 | Project Module Description | |
| Table 5.1 | Model Comparison Results | |
| Table 5.2 | Best Model Classification Report | |
| Table 5.3 | SHAP Global Feature Importance (Top 10) | |
| Table 5.4 | SMOTE Impact on Model Performance | |

---

# LIST OF FIGURES

| Figure No | Figure Title | Page No |
|-----------|-------------|---------|
| Figure 3.1 | System Architecture Block Diagram | |
| Figure 3.2 | Data Collection and Preprocessing Pipeline | |
| Figure 3.3 | Machine Learning Workflow Diagram | |
| Figure 4.1 | Web Application — Home Dashboard | |
| Figure 4.2 | Web Application — Assessment Form (Step 1: Demographics) | |
| Figure 4.3 | Web Application — Assessment Form (Step 4: PHQ-9 Screening) | |
| Figure 4.4 | Web Application — Results Page | |
| Figure 5.1 | Depression Risk Class Distribution | |
| Figure 5.2 | PHQ-9 Total Score Histogram | |
| Figure 5.3 | Sleep Duration vs Mean PHQ-9 Score | |
| Figure 5.4 | Exercise Frequency vs Mean PHQ-9 Score | |
| Figure 5.5 | Feature Correlation Heatmap | |
| Figure 5.6 | Social Support vs Mean PHQ-9 Score | |
| Figure 5.7 | Gender vs Depression Risk Distribution | |
| Figure 5.8 | Feature Correlations with PHQ-9 Total Score | |
| Figure 5.9 | PHQ-9 Score Boxplot by Risk Group | |
| Figure 5.10 | Stress Indicators by Risk Group | |
| Figure 5.11 | Model Comparison — Accuracy, Precision, Recall, F1 | |
| Figure 5.12 | Confusion Matrices for All Four Models | |
| Figure 5.13 | SHAP Global Feature Importance | |
| Figure 5.14 | SHAP Beeswarm Summary Plot (Per-Class) | |
| Figure 5.15 | SHAP Per-Class Bar Chart (Top 10 Features) | |
| Figure 5.16 | SHAP Individual Student Explanations | |
| Figure 5.17 | SMOTE — Before vs After Model Performance | |
| Figure 5.18 | SMOTE — Class Distribution Before and After | |
| Figure 5.19 | SMOTE — Best Model Confusion Matrix | |

---

# TABLE OF CONTENTS

| | | Page No |
|---|---|---|
| Acknowledgement | | i |
| Abstract | | ii |
| List of Tables | | iii |
| List of Figures | | iv |
| **Chapter 1** | **INTRODUCTION** | |
| 1.1 | Introduction to Work Done / Motivation | |
| 1.2 | Project Statement and Objectives | |
| 1.3 | Organization of Report | |
| **Chapter 2** | **BACKGROUND MATERIAL** | |
| 2.1 | Conceptual Overview | |
| 2.2 | Technologies Involved | |
| **Chapter 3** | **METHODOLOGY** | |
| 3.1 | Data Collection and Preprocessing | |
| 3.2 | Feature Engineering and Selection | |
| 3.3 | Machine Learning Pipeline | |
| 3.4 | System Architecture | |
| **Chapter 4** | **IMPLEMENTATION** | |
| 4.1 | Modules | |
| 4.2 | Prototype — Web Application | |
| **Chapter 5** | **RESULTS AND ANALYSIS** | |
| 5.1 | Exploratory Data Analysis | |
| 5.2 | Model Training and Comparison | |
| 5.3 | SHAP Explainability Analysis | |
| 5.4 | SMOTE Oversampling Analysis | |
| 5.5 | GAD-7 Anxiety Estimation | |
| **Chapter 6** | **CONCLUSIONS AND FUTURE SCOPE** | |
| 6.1 | Conclusions | |
| 6.2 | Future Scope of Work | |
| **References** | | |
| **Annexures** | | |

---

# Chapter 1: INTRODUCTION

## 1.1 Introduction to Work Done / Motivation

Mental health has become one of the most pressing public health challenges of the 21st century, particularly among young adults in university settings. The World Health Organization (WHO) estimates that depression affects approximately 280 million people globally, making it one of the leading causes of disability worldwide. University students represent a particularly vulnerable demographic due to the unique combination of academic pressures, social transitions, financial concerns, and the developmental challenges inherent in emerging adulthood. Studies conducted across Indian universities have consistently reported that 30–50% of students experience symptoms of depression or anxiety during their academic careers, yet fewer than 20% seek professional help.

The significance of early detection in mental health cannot be overstated. Depression, when left unidentified and untreated, can lead to declining academic performance, social withdrawal, substance abuse, and in severe cases, suicidal ideation. Traditional mental health screening relies heavily on clinical interviews conducted by trained professionals — a resource that is severely limited in Indian universities where the student-to-counselor ratio often exceeds 3,000:1. This creates an urgent need for accessible, technology-driven screening tools that can provide preliminary risk assessments at scale.

The Patient Health Questionnaire-9 (PHQ-9) is a clinically validated, self-administered depression screening instrument developed by Drs. Robert L. Spitzer, Janet B.W. Williams, and Kurt Kroenke in 2001. It consists of nine questions that directly map to the nine diagnostic criteria for Major Depressive Disorder as defined in the DSM-IV (Diagnostic and Statistical Manual of Mental Disorders, Fourth Edition). Each item is scored on a 4-point Likert scale ranging from 0 (Not at all) to 3 (Nearly every day), producing a total score range of 0 to 27. The PHQ-9 has been extensively validated across diverse populations with sensitivity and specificity exceeding 80% for detecting major depression.

**Table 1.1: PHQ-9 Depression Severity Classification**

| PHQ-9 Total Score | Severity Level | Depression Risk Label |
|---|---|---|
| 0 – 9 | Minimal to Mild | Low Risk |
| 10 – 19 | Moderate to Moderately Severe | Moderate Risk |
| 20 – 27 | Severe | High Risk |

In recent years, artificial intelligence and machine learning have demonstrated remarkable potential in healthcare applications, including disease diagnosis, drug discovery, and mental health prediction. Machine learning algorithms can identify complex, non-linear patterns in multi-dimensional data that may not be apparent through traditional statistical methods. When combined with validated clinical instruments like the PHQ-9 and behavioral data such as sleep patterns, exercise habits, and social support levels, machine learning models can provide nuanced risk assessments that go beyond simple score-based thresholds.

This project, titled **MINDscan**, leverages these advancements to develop an AI-powered web application that predicts depression risk levels for university students. Unlike existing approaches in the literature that typically rely on a single data source — either clinical interviews, social media analysis, or questionnaire data alone — MINDscan uniquely combines three complementary data streams: (1) validated PHQ-9 clinical screening, (2) student lifestyle indicators such as sleep duration, exercise frequency, screen time, and social support, and (3) academic stress measures. This multi-modal approach enables a more holistic assessment of student mental health.

The key advantages of this system include its accessibility (available as a web application from any device), its use of validated clinical instruments (PHQ-9 and estimated GAD-7), its explainability through SHAP analysis (ensuring that predictions are not opaque "black box" outputs), and its provision of personalized recommendations and crisis resources. The application serves as a preliminary screening tool — not a diagnostic instrument — designed to encourage students who receive moderate or high risk predictions to seek professional counseling.

## 1.2 Project Statement and Objectives

### Problem Statement

To design and develop an AI-based web application that predicts depression risk levels (Low, Moderate, or High) for university students using machine learning classification algorithms trained on PHQ-9 depression screening scores combined with lifestyle, behavioral, and academic stress indicators, and to deploy the system as an accessible, explainable, and user-friendly online tool.

### Objectives

The primary objectives of this project are as follows:

1. **Data Collection**: To collect primary data from university students at Manipal University Jaipur through a structured Google Forms questionnaire capturing demographics, lifestyle habits, stress indicators, and PHQ-9 depression screening responses — targeting a minimum of 1,000 respondents for statistical significance.

2. **Exploratory Data Analysis (EDA)**: To conduct comprehensive exploratory data analysis to understand the distribution of depression risk levels, identify correlations between lifestyle factors and PHQ-9 scores, and uncover patterns in the data that inform feature selection and model design.

3. **Model Development**: To train and evaluate multiple machine learning classification algorithms — including Logistic Regression, Support Vector Machine, Random Forest, and Decision Tree — using appropriate preprocessing, cross-validation, and evaluation metrics to identify the best-performing model.

4. **Model Explainability**: To apply SHAP (SHapley Additive exPlanations) analysis to the trained model, providing transparent, interpretable explanations of which features drive individual and global predictions — ensuring the system is not a "black box."

5. **Class Imbalance Handling**: To address class imbalance in the dataset using SMOTE (Synthetic Minority Over-sampling Technique) and evaluate its impact on model performance, particularly for the underrepresented High Risk class.

6. **Anxiety Estimation**: To integrate an estimated GAD-7 (Generalized Anxiety Disorder-7) score derived from available stress indicators, providing a dual depression-anxiety risk profile for each student.

7. **Web Application Deployment**: To develop and deploy a responsive, production-grade web application using Flask that enables students to complete the PHQ-9 screening, receive real-time AI risk predictions with confidence scores, view SHAP explainability charts, and access personalized recommendations and crisis helpline resources.

## 1.3 Organization of Report

This report is organized into six chapters as follows:

**Chapter 1 — Introduction** provides the motivation behind the project, outlines the significance of mental health screening among university students, presents the problem statement, and lists the project objectives.

**Chapter 2 — Background Material** presents the conceptual overview of the theories and clinical instruments used in the project, reviews relevant literature in AI-based mental health prediction, and describes the technologies and tools employed.

**Chapter 3 — Methodology** details the data collection process, dataset characteristics, feature engineering, preprocessing pipeline, machine learning algorithms, cross-validation strategy, SMOTE oversampling, SHAP explainability, and system architecture.

**Chapter 4 — Implementation** describes the modular structure of the project, the implementation of each module (EDA, Model Training, SHAP, SMOTE, GAD-7, Web Application), and presents the prototype of the deployed web application.

**Chapter 5 — Results and Analysis** presents the findings from exploratory data analysis, model training and comparison, SHAP feature importance analysis, SMOTE oversampling impact, and GAD-7 anxiety estimation, supported by tables, charts, and statistical metrics.

**Chapter 6 — Conclusions and Future Scope** summarizes the key contributions and findings of the project and proposes directions for future enhancement and research.

---

# Chapter 2: BACKGROUND MATERIAL

## 2.1 Conceptual Overview

### 2.1.1 Depression and Mental Health Screening

Depression is a mood disorder characterized by persistent feelings of sadness, hopelessness, loss of interest, fatigue, and in severe cases, thoughts of self-harm or suicide. The Diagnostic and Statistical Manual of Mental Disorders (DSM-5) classifies Major Depressive Disorder (MDD) based on the presence of five or more symptoms over a two-week period, with at least one symptom being either depressed mood or loss of interest/pleasure.

The **Patient Health Questionnaire-9 (PHQ-9)** is a brief, self-report instrument that assesses the frequency of nine depressive symptoms over the past two weeks. Developed by Kroenke, Spitzer, and Williams (2001), the PHQ-9 has been validated in multiple clinical and non-clinical populations with a sensitivity of 88% and specificity of 88% for detecting major depression at a cut-off score of 10. Its brevity (nine items), free availability, and strong psychometric properties make it the most widely used depression screening tool in primary care and research settings worldwide.

The **Generalized Anxiety Disorder-7 (GAD-7)** scale is a complementary 7-item screening tool for anxiety disorders, developed by Spitzer et al. (2006). It measures the frequency of anxiety symptoms over the past two weeks on a 0–3 scale, yielding a total score of 0–21. Anxiety and depression frequently co-occur (comorbidity rates of 40–60%), and screening for both conditions simultaneously provides a more comprehensive mental health assessment.

### 2.1.2 Machine Learning for Classification

Machine learning is a subset of artificial intelligence that enables systems to learn patterns from data without being explicitly programmed. In supervised classification, the algorithm learns a mapping function from input features to discrete output labels using labeled training data, and then applies this learned function to predict labels for unseen data.

**Logistic Regression** is a linear classification algorithm that models the probability of class membership using the logistic (sigmoid) function. For multiclass problems, it employs a one-vs-rest (OvR) strategy, fitting one binary classifier per class. Despite its simplicity, logistic regression performs exceptionally well on linearly separable data and provides interpretable probability estimates.

**Support Vector Machine (SVM)** finds the optimal hyperplane that maximizes the margin between classes in high-dimensional feature space. The Radial Basis Function (RBF) kernel enables SVM to handle non-linearly separable data by mapping features into a higher-dimensional space where linear separation becomes possible.

**Random Forest** is an ensemble learning method that constructs multiple decision trees during training and outputs the mode of their individual predictions. Each tree is trained on a bootstrap sample of the data with a random subset of features, reducing overfitting and improving generalization.

**Decision Tree** is a non-parametric algorithm that recursively partitions the feature space using axis-parallel splits based on information gain or Gini impurity. While highly interpretable, decision trees are prone to overfitting on training data.

### 2.1.3 SHAP Explainability

SHAP (SHapley Additive exPlanations), developed by Lundberg and Lee (2017), is a game-theoretic approach to model interpretability. It assigns each feature an importance value (SHAP value) for a particular prediction, representing the feature's marginal contribution to the prediction outcome. SHAP values satisfy three desirable properties: local accuracy, missingness, and consistency. For linear models, the LinearExplainer provides exact SHAP values using the model coefficients and feature correlations.

### 2.1.4 SMOTE Oversampling

SMOTE (Synthetic Minority Over-sampling Technique), proposed by Chawla et al. (2002), addresses class imbalance by generating synthetic samples for the minority class. For each minority sample, SMOTE identifies its k nearest neighbors (typically k=5) and creates new synthetic samples along the line segments connecting the minority sample to its neighbors. This approach is superior to simple random oversampling because it creates novel, realistic samples rather than duplicates, reducing the risk of overfitting.

### 2.1.5 Feature Scaling — MinMaxScaler

MinMaxScaler normalizes features to a fixed range [0, 1] using the transformation:

X_scaled = (X - X_min) / (X_max - X_min)

This is essential for algorithms sensitive to feature magnitudes, such as Logistic Regression and SVM, ensuring that all features contribute proportionally to the model regardless of their original scales.

## 2.2 Technologies Involved

**Table 2.2: Technologies and Tools Used**

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| Programming Language | Python | 3.11 | Core development language |
| Data Manipulation | pandas | ≥1.5.0 | DataFrame operations, data cleaning |
| Numerical Computing | NumPy | ≥1.21.0 | Array operations, mathematical computations |
| Machine Learning | scikit-learn | ≥1.3.0 | Model training, evaluation, preprocessing |
| Explainability | SHAP | Latest | Model interpretation, feature importance |
| Class Balancing | imbalanced-learn | Latest | SMOTE oversampling |
| Visualization | matplotlib | Latest | Static chart generation |
| Visualization | seaborn | Latest | Statistical visualization |
| Web Framework | Flask | ≥2.3.0 | Backend REST API and page serving |
| Production Server | Gunicorn | ≥21.0.0 | WSGI HTTP server for deployment |
| WSGI Utilities | Werkzeug | ≥2.3.0 | Request/response handling |
| Frontend | HTML5 / CSS3 / JavaScript | — | User interface, single-page application |
| Fonts | Google Fonts (Sora, DM Sans) | — | Typography |
| Deployment | Render | Cloud | Production hosting and deployment |
| Data Collection | Google Forms | — | Survey questionnaire distribution |
| Version Control | Git / GitHub | — | Source code management |
| IDE | Visual Studio Code | — | Code development environment |
| Model Serialization | pickle | Built-in | Saving/loading trained models |

---

# Chapter 3: METHODOLOGY

## 3.1 Data Collection and Preprocessing

### 3.1.1 Data Collection

Primary data was collected through a structured **Google Forms questionnaire** distributed among students of Manipal University Jaipur across academic years 1 through 6. The survey was designed to capture three categories of information:

1. **Demographic Information**: Age, gender (Male/Female/Other), year of study, and field of study.
2. **Lifestyle and Behavioral Indicators**: Average sleep hours, physical exercise frequency, daily screen time, study hours outside class, social support perception, and academic overload.
3. **Clinical Screening — PHQ-9**: Nine validated depression symptom items, each scored on a 0–3 scale (Not at all / Several days / More than half the days / Nearly every day).

The questionnaire received **1,151 valid responses** with zero missing values, indicating successful data quality control through mandatory response fields in Google Forms.

### 3.1.2 Dataset Description

The collected dataset comprises 1,151 rows and 25 columns. The features are described in the table below:

**Table 3.1: Dataset Feature Description**

| # | Feature Name | Data Type | Encoding / Range |
|---|---|---|---|
| 1 | Age | Numeric | Actual age value |
| 2 | Gender | Categorical | 0=Male, 1=Female, 2=Other |
| 3 | Year of Study | Numeric | 1–6 |
| 4 | Field of Study | Categorical | Text (dropped before training) |
| 5 | Average sleep hours | Ordinal | 0=<5hrs, 1=5-6, 2=6-7, 3=7-8, 4=>8hrs |
| 6 | Social support perception | Ordinal | 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Always |
| 7 | Physical exercise frequency | Ordinal | 0=Never, 1=1-2x/week, 2=3-4x/week, 3=Daily |
| 8 | Daily screen time | Ordinal | 0–2 scale |
| 9 | Academic overload | Binary | 0=No, 1=Yes |
| 10 | Stress — academic workload | Likert | 1–5 scale |
| 11 | Difficulty relaxing | Likert | 1–5 scale |
| 12 | Feeling overwhelmed | Likert | 1–5 scale |
| 13 | Exam anxiety | Likert | 1–5 scale |
| 14 | Study hours outside class | Numeric | Hours per day |
| 15–23 | PHQ-9 Items (9 questions) | Ordinal | 0–3 each |
| 24 | PHQ-9 Total Score | Derived | 0–27 (sum of 9 items) |
| 25 | Depression Risk Label | Target | 0=Low, 1=Moderate, 2=High |

**Table 3.2: PHQ-9 Questionnaire Items and Scoring**

| Item | PHQ-9 Question | Scoring |
|------|---------------|---------|
| PHQ-1 | Little interest or pleasure in doing things | 0–3 |
| PHQ-2 | Feeling down, depressed, or hopeless | 0–3 |
| PHQ-3 | Trouble falling or staying asleep, or sleeping too much | 0–3 |
| PHQ-4 | Feeling tired or having little energy | 0–3 |
| PHQ-5 | Poor appetite or overeating | 0–3 |
| PHQ-6 | Feeling bad about yourself — or that you are a failure | 0–3 |
| PHQ-7 | Trouble concentrating on things | 0–3 |
| PHQ-8 | Moving or speaking slowly OR being restless/fidgety | 0–3 |
| PHQ-9 | Thoughts that you would be better off dead or hurting yourself | 0–3 |

**Scoring**: 0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day. Total score = Sum of all 9 items (range: 0–27).

### 3.1.3 Data Preprocessing

The following preprocessing steps were applied:

1. **Missing Value Check**: Confirmed zero missing values across all 1,151 rows and 25 columns.
2. **Feature Exclusion**: Three columns were dropped before model training:
   - *Field of Study* — categorical text field not suitable for numeric modeling without extensive encoding.
   - *PHQ-9 Total Score* — derived column (sum of PHQ-9 items) that would cause data leakage since the target variable is directly computed from it.
   - *Depression Risk Label* — the target variable itself, separated into vector y.
3. **Feature Matrix**: The remaining **22 numeric features** formed the feature matrix X.
4. **Feature Scaling**: MinMaxScaler was applied to normalize all 22 features to the [0, 1] range, ensuring equal contribution from features with different original scales.
5. **Train-Test Split**: The dataset was split into 80% training (921 samples) and 20% testing (230 samples) using stratified sampling (`stratify=y`, `random_state=42`) to maintain the class distribution in both sets.

## 3.2 Feature Engineering and Selection

### 3.2.1 Feature Categories

The 22 features used for model training were organized into three functional categories:

**Category 1 — Demographics (3 features)**: Age, Gender, Year of Study.

**Category 2 — Lifestyle and Behavioral Indicators (10 features)**: Average sleep hours, social support perception, physical exercise frequency, daily screen time, academic overload, stress due to academic workload, difficulty relaxing, feeling overwhelmed, exam anxiety, study hours outside class.

**Category 3 — PHQ-9 Clinical Symptoms (9 features)**: All nine individual PHQ-9 items scored 0–3.

### 3.2.2 GAD-7 Anxiety Estimation

Since the GAD-7 scale was not included in the original survey questionnaire, a simulated GAD-7 score was derived from the available stress indicators using the following proxy formula:

```
stress_proxy = (workload_stress × 0.3) + (difficulty_relaxing × 0.3)
             + (feeling_overwhelmed × 0.2) + (exam_anxiety × 0.2)

gad7_raw = stress_proxy × 3.5 + Gaussian_noise(μ=0, σ=2)
gad7_total = clip(round(gad7_raw), 0, 21)
```

**Table 3.3: GAD-7 Anxiety Classification Thresholds**

| GAD-7 Total Score | Anxiety Severity | Label |
|---|---|---|
| 0 – 4 | Minimal | 0 |
| 5 – 9 | Mild | 1 |
| 10 – 14 | Moderate | 2 |
| 15 – 21 | Severe | 3 |

The seven standard GAD-7 questions (for reference) are: (1) Feeling nervous, anxious, or on edge; (2) Not being able to stop or control worrying; (3) Worrying too much about different things; (4) Trouble relaxing; (5) Being so restless that it is hard to sit still; (6) Becoming easily annoyed or irritable; (7) Feeling afraid, as if something awful might happen. Each is scored 0–3 (Not at all to Nearly every day), yielding a total of 0–21.

## 3.3 Machine Learning Pipeline

### 3.3.1 Algorithms and Hyperparameters

Four supervised classification algorithms were selected for training and comparison:

**Table 3.4: Machine Learning Model Hyperparameters**

| Model | Hyperparameters |
|---|---|
| Logistic Regression | max_iter=1000, random_state=42, solver=lbfgs (default), penalty=l2 (default) |
| Decision Tree | max_depth=8, random_state=42, criterion=gini (default) |
| Random Forest | n_estimators=200, max_depth=10, random_state=42, n_jobs=-1 |
| SVM (RBF Kernel) | kernel=rbf, C=1.0, gamma=scale, random_state=42, probability=True |

### 3.3.2 Cross-Validation Strategy

Model performance was evaluated using **5-fold Stratified K-Fold Cross-Validation** with `shuffle=True` and `random_state=42`. Stratification ensures that each fold maintains the same class proportion as the full dataset, which is critical for imbalanced multiclass problems. Cross-validation accuracy (mean ± standard deviation) was computed for each model.

### 3.3.3 Evaluation Metrics

The following metrics were computed on the held-out test set (20% of data):

- **Accuracy**: Overall proportion of correct predictions.
- **Precision** (weighted): Proportion of true positives among predicted positives, weighted by class frequency.
- **Recall** (weighted): Proportion of true positives among actual positives, weighted by class frequency.
- **F1-Score** (weighted): Harmonic mean of precision and recall, weighted by class frequency.
- **Confusion Matrix**: 3×3 matrix showing predicted vs actual class counts.
- **Classification Report**: Per-class precision, recall, and F1-score.

The **best model was selected based on the highest weighted F1-Score** on the test set, as F1-Score provides a balanced measure of precision and recall, which is particularly important for multiclass classification with class imbalance.

### 3.3.4 SMOTE Oversampling

To address class imbalance (High Risk class having fewer samples), SMOTE was applied with the following configuration:

- **SMOTE parameters**: `k_neighbors=5`, `random_state=42`
- **Application**: SMOTE was applied **only to the training set** after the train-test split. This is methodologically critical — applying SMOTE before splitting would cause synthetic samples to leak into the test set, producing overly optimistic performance estimates.
- **Effect**: All three classes in the training set were equalized to have the same number of samples.

### 3.3.5 SHAP Explainability

SHAP analysis was conducted using the `LinearExplainer` with `feature_perturbation="interventional"`:

- **Explainer**: `shap.LinearExplainer(model, X_train)` — provides exact SHAP values for linear models.
- **SHAP values shape**: (n_test_samples × 22 features × 3 classes) — a 3D array capturing feature contributions for each class.
- **Global importance**: Calculated as `mean(|SHAP|)` across all test samples and all 3 classes.
- **Per-class importance**: Calculated as `mean(|SHAP|)` for each class separately.

## 3.4 System Architecture

The system follows a three-tier architecture:

**Tier 1 — Data Layer**: The cleaned CSV dataset and serialized model artifacts (best_model.pkl, scaler.pkl, feature_names.pkl) stored on the server filesystem.

**Tier 2 — Application Layer (Backend)**: A Flask web server with two endpoints:
- `GET /` — Serves the single-page HTML frontend.
- `POST /predict` — Receives JSON input, constructs a feature DataFrame, scales features using the pre-fitted MinMaxScaler, generates predictions using the trained Logistic Regression model, computes PHQ-9 total score, mental stability score, and estimated GAD-7 score, and returns results as JSON.

**Tier 3 — Presentation Layer (Frontend)**: A responsive single-page application built with HTML5, CSS3, and vanilla JavaScript featuring:
- Multi-step assessment form with chip selectors and sliders.
- Real-time risk prediction display with circular ring charts.
- Confidence probability bars for all three risk classes.
- SHAP explainability visualizations.
- Personalized recommendations and crisis helpline resources.

The prediction flow is:

```
User Input (Browser) → JSON POST Request → Flask /predict API
→ Feature DataFrame Construction → MinMaxScaler Transform
→ model.predict() + model.predict_proba()
→ JSON Response (prediction, probabilities, PHQ total, stability, GAD-7)
→ Frontend Rendering (Dashboard, Charts, Recommendations)
```

---

# Chapter 4: IMPLEMENTATION

## 4.1 Modules

The project is implemented as six distinct modules, each encapsulated in a separate Python script. The modules follow a sequential pipeline where outputs from earlier modules feed into later ones.

**Table 4.1: Project Module Description**

| Module | Script File | Description |
|---|---|---|
| Module 1: EDA | Phase3_EDA.py | Exploratory data analysis — generates 10 statistical visualizations covering risk distribution, PHQ-9 histograms, lifestyle correlations, and stress indicator analysis |
| Module 2: Model Training | Phase4_Model_Training.py | Trains 4 ML models, performs 5-fold CV, evaluates on test set, selects best model by F1-Score, saves model artifacts |
| Module 3: SHAP Analysis | Tier1_Upgrade1_SHAP.py | Computes SHAP values using LinearExplainer, generates global importance, beeswarm, per-class bar, and individual explanation plots |
| Module 4: SMOTE Balancing | Tier1_Upgrade2_SMOTE.py | Applies SMOTE to training data, compares model performance with/without SMOTE, evaluates High Risk F1 improvement |
| Module 5: GAD-7 Estimation | Tier1_Upgrade3_GAD7.py | Simulates GAD-7 anxiety scores from stress indicators, trains dual depression-anxiety prediction models |
| Module 6: Web Application | app.py + templates/ + static/ | Flask backend with prediction API, responsive HTML/CSS/JS frontend, deployed on Render |

### 4.1.1 Module 1 — Exploratory Data Analysis (Phase3_EDA.py)

This module loads the cleaned dataset and generates 10 publication-quality visualizations using matplotlib and seaborn. The analysis covers:

- **Risk class distribution**: Bar chart showing the count and percentage of Low, Moderate, and High Risk students. Color palette: green (#2E7D32), amber (#F9A825), red (#C62828).
- **PHQ-9 score distribution**: Histogram with 28 bins showing the distribution of PHQ-9 total scores across all 1,151 students, with vertical boundary lines at 9.5 (Low/Moderate threshold) and 19.5 (Moderate/High threshold), plus a mean line.
- **Lifestyle factor analysis**: Bar charts showing mean PHQ-9 scores grouped by sleep duration (5 categories), exercise frequency (4 categories), and social support perception (5 categories).
- **Correlation analysis**: A lower-triangular Pearson correlation heatmap of 11 variables (9 lifestyle/stress features + PHQ-9 Total + Risk Label) and a horizontal bar chart of individual feature correlations with PHQ-9 Total Score.
- **Gender analysis**: Stacked percentage bar chart showing the proportional distribution of risk levels across genders.
- **Stress analysis**: Grouped bar chart comparing four stress indicators (workload, relaxation difficulty, overwhelm, exam anxiety) across the three risk groups.

All plots are saved at 150 DPI with consistent styling: DejaVu Sans font, top and right spines removed, dashed grid lines at alpha 0.3.

### 4.1.2 Module 2 — Model Training (Phase4_Model_Training.py)

This module implements the complete machine learning training pipeline:

1. Loads the dataset and drops three non-feature columns (Field of Study, PHQ-9 Total Score, Depression Risk Label).
2. Applies MinMaxScaler to normalize all 22 features to [0, 1].
3. Performs an 80/20 stratified train-test split.
4. Defines four classification models with specified hyperparameters.
5. Evaluates each model using 5-fold Stratified K-Fold cross-validation.
6. Trains each model on the full training set and evaluates on the test set.
7. Computes accuracy, precision, recall, and F1-score (all weighted) for each model.
8. Generates a 4-panel bar chart comparing all metrics across models and a 4-panel confusion matrix visualization.
9. Selects the best model based on the highest weighted F1-score.
10. Prints the full classification report for the best model.
11. Serializes the best model, scaler, and feature names using Python's pickle module.

### 4.1.3 Module 3 — SHAP Explainability (Tier1_Upgrade1_SHAP.py)

This module provides model interpretability through four SHAP visualizations:

1. **Global Feature Importance Chart**: Ranks all 22 features by their mean absolute SHAP value across all test samples and all three classes. Features with SHAP > 0.04 are colored red (high importance), SHAP > 0.02 are blue (moderate), and the rest are grey.
2. **Beeswarm Summary Plot**: A 3-panel plot (one per risk class) showing the top 15 features. Each dot represents a single test student, positioned along the x-axis by SHAP value and colored by feature value (RdYlBu_r colormap). Vertical jitter (±0.25) prevents overlap.
3. **Per-Class Bar Chart**: A 3-panel horizontal bar chart showing the top 10 features for each risk class by mean absolute SHAP value.
4. **Individual Explanations**: Three case studies (one student per class) showing the top 12 features driving that specific prediction, with actual feature values annotated on each bar.

All features are renamed to short, descriptive labels for readability (e.g., "PHQ3: Sleep trouble", "Stress (workload)", "Exercise frequency").

### 4.1.4 Module 4 — SMOTE Oversampling (Tier1_Upgrade2_SMOTE.py)

This module evaluates the impact of SMOTE on model performance:

1. Performs the train-test split first (preventing data leakage).
2. Applies SMOTE with k_neighbors=5 to the training set only, equalizing all three class counts.
3. Trains three models (Logistic Regression, Random Forest, SVM) both without and with SMOTE.
4. Computes three metrics for comparison: overall accuracy, weighted F1-score, and class-specific High Risk F1-score.
5. Calculates delta changes (Δ) for each metric to quantify SMOTE's impact.
6. Generates comparison bar charts, class distribution plots, and confusion matrix for the best SMOTE model.
7. Saves the SMOTE-enhanced best model.

### 4.1.5 Module 5 — GAD-7 Anxiety Estimation (Tier1_Upgrade3_GAD7.py)

This module extends the system from depression-only to a dual depression-anxiety assessment:

1. Derives simulated GAD-7 total scores from four available stress indicators using a weighted proxy formula with Gaussian noise.
2. Assigns anxiety risk labels based on GAD-7 clinical thresholds (Minimal/Mild/Moderate/Severe).
3. Trains a separate Logistic Regression model (with class_weight='balanced') for anxiety prediction.
4. Generates a cross-tabulation chart showing the co-occurrence of depression and anxiety risk levels.
5. Produces a dual-panel visualization with GAD-7 histogram (with threshold lines) and PHQ-9 vs GAD-7 scatter plot with Pearson correlation coefficient.

### 4.1.6 Module 6 — Web Application (app.py + Frontend)

The web application consists of:

**Backend (app.py)**: A Flask application with two routes:
- `GET /` — Renders the main HTML template.
- `POST /predict` — JSON API endpoint that:
  - Receives user input (demographics, lifestyle, stress indicators, PHQ-9 responses).
  - Maps frontend keys to the exact 22 model feature names.
  - Constructs a pandas DataFrame in the correct feature order.
  - Scales features using the pre-fitted MinMaxScaler.
  - Generates predictions and probability distributions.
  - Computes additional scores:
    - **Mental Stability Score**: `max(10, 100 - int(phq_total × 2.5 + (workload - 1) × 5))` — range 10 to 100.
    - **GAD-7 Estimate**: `min(21, round((workload + relax + exam) × 1.2 + (2 if screen > 1 else 0)))` — range 0 to 21.

**Frontend (index.html)**: A 4,604-line single-page application with:
- **Dashboard Page**: User profile card, risk status pill indicator, circular ring chart for mental stability, PHQ-9 and GAD-7 score boxes, and confidence probability bars.
- **Assessment Page**: Four-step wizard with chip selectors for demographics, sliders for lifestyle factors, and button groups for PHQ-9 items.
- **Insights Page**: SHAP explainability charts and data insights.
- **Results Page**: Detailed risk banner with color coding (Low=green, Moderate=amber, High=red), personalized lifestyle recommendations, and crisis helpline resources for high-risk users.
- **Design**: Sora font for headings, DM Sans for body text, purple gradient hero sections, glassmorphic cards, smooth CSS animations, and fully responsive layout.

## 4.2 Prototype — Web Application

The deployed web application is accessible at: **https://mental-health-predictor-0oat.onrender.com**

The application prototype comprises the following screens:

**Screen 1 — Dashboard**: Displays the user's profile, current risk assessment status, mental stability ring chart, PHQ-9 and GAD-7 score boxes, and assessment confidence bars showing the probability distribution across Low, Moderate, and High risk classes.

**Screen 2 — Assessment Form**: A guided multi-step questionnaire:
- Step 1: Demographics (age, gender, year of study)
- Step 2: Lifestyle (sleep hours, exercise frequency, screen time, study hours)
- Step 3: Academic Stress (5 stress-related questions on a Likert scale)
- Step 4: PHQ-9 Depression Screening (9 clinical questions, each scored 0–3)

**Screen 3 — Results**: After submission, the system displays:
- Risk level prediction with color-coded banner
- Prediction confidence percentages for each risk class
- PHQ-9 total score with severity interpretation
- Estimated GAD-7 anxiety score
- Mental stability percentage score
- Personalized recommendations based on the predicted risk level
- Crisis helpline numbers (iCall, Vandrevala Foundation, NIMHANS) for high-risk users

*(Note: Screenshots of the web application should be inserted here as Figure 4.1 through Figure 4.4 when preparing the final Word document.)*

---

# Chapter 5: RESULTS AND ANALYSIS

## 5.1 Exploratory Data Analysis

### 5.1.1 Depression Risk Distribution

The analysis of the Depression Risk Label distribution across 1,151 students revealed the following class proportions:
- **Low Risk (PHQ 0–9)**: Largest class, comprising the majority of respondents.
- **Moderate Risk (PHQ 10–19)**: Second largest class.
- **High Risk (PHQ 20+)**: Smallest class, representing approximately 12.8% of the dataset (≈148 students).

This class imbalance, particularly the underrepresentation of High Risk students, motivated the application of SMOTE oversampling in a later module. *(See Figure 5.1)*

### 5.1.2 PHQ-9 Score Distribution

The PHQ-9 total score histogram (28 bins) showed a right-skewed distribution with the majority of students scoring in the Low Risk range (0–9). The boundary lines at scores of 9.5 and 19.5 clearly demarcated the three risk regions. The mean PHQ-9 score across all students was annotated on the plot. *(See Figure 5.2)*

### 5.1.3 Lifestyle Factor Analysis

**Sleep Duration vs PHQ-9**: Students sleeping less than 5 hours per night had significantly higher mean PHQ-9 scores compared to those sleeping 7–8 hours. The relationship showed a clear inverse trend — as sleep duration increased, mean PHQ-9 scores decreased, confirming the well-established association between sleep deprivation and depression. *(See Figure 5.3)*

**Exercise Frequency vs PHQ-9**: Students who never exercised had the highest mean PHQ-9 scores, while those exercising daily had the lowest. The gradient between "Never" and "Daily" was substantial, highlighting exercise as a protective factor against depression. *(See Figure 5.4)*

**Social Support vs PHQ-9**: A strong inverse relationship was observed — students who reported "Always" feeling supported had the lowest mean PHQ-9 scores, while those reporting "Never" had the highest. This finding underscores the buffering effect of social support on mental health. *(See Figure 5.6)*

### 5.1.4 Correlation Analysis

The Pearson correlation heatmap revealed several notable relationships:
- All four stress indicators (workload, relaxation difficulty, overwhelm, exam anxiety) showed **moderate to strong positive correlations** with the PHQ-9 Total Score and Depression Risk Label.
- **Sleep hours** and **exercise frequency** showed **negative correlations** with PHQ-9 scores (protective factors).
- **Screen time** showed a weak **positive correlation** with depression risk.
- The four stress indicators were **inter-correlated** with each other (r > 0.3), suggesting a latent "stress" factor.

The feature correlation bar chart quantified individual Pearson correlations with PHQ-9 Total Score. *(See Figures 5.5 and 5.8)*

### 5.1.5 Gender Analysis

The stacked percentage bar chart by gender showed that depression risk distribution was relatively similar across genders, with slight variations in the proportion of High Risk students. *(See Figure 5.7)*

### 5.1.6 Stress Indicators by Risk Group

The grouped bar chart showed a clear gradient across all four stress indicators: High Risk students consistently reported higher stress scores (on a 1–5 scale) compared to Moderate Risk students, who in turn reported higher scores than Low Risk students. Difficulty relaxing and exam anxiety showed the most pronounced differences between risk groups. *(See Figure 5.10)*

## 5.2 Model Training and Comparison

### 5.2.1 Model Performance Results

**Table 5.1: Model Comparison Results**

| Model | CV Accuracy (Mean ± Std) | Test Accuracy | Precision (W) | Recall (W) | F1-Score (W) |
|---|---|---|---|---|---|
| **Logistic Regression** | **95.98%** | **95.67%** | **95.70%** | **95.67%** | **95.65%** |
| SVM (RBF) | 94.24% | 93.51% | 93.55% | 93.51% | 93.48% |
| Random Forest | 92.39% | 89.18% | 89.25% | 89.18% | 89.15% |
| Decision Tree | 80.54% | 83.55% | 83.60% | 83.55% | 83.48% |

*(W) = Weighted average across all three classes.*

**Best Model**: Logistic Regression, selected based on the highest weighted F1-Score (95.65%). *(See Figure 5.11)*

### 5.2.2 Best Model Classification Report

**Table 5.2: Logistic Regression — Per-Class Classification Report**

| Class | Precision | Recall | F1-Score |
|---|---|---|---|
| Low Risk (0) | 97% | 97% | 97% |
| Moderate Risk (1) | 95% | 95% | 95% |
| High Risk (2) | 91% | 91% | 91% |
| **Weighted Average** | **95.70%** | **95.67%** | **95.65%** |

The model performed best on the Low Risk class (F1=97%) and slightly lower on the High Risk class (F1=91%), which is expected given the smaller sample size for High Risk students. *(See Figure 5.12 for confusion matrices)*

### 5.2.3 Analysis of Results

Logistic Regression outperformed all other models despite being the simplest algorithm. This can be attributed to:
1. The features (especially the 9 PHQ-9 items) have a strong linear relationship with the target variable, since the target is directly derived from PHQ-9 scores.
2. MinMaxScaler normalization ensured optimal performance for the linear model.
3. The dataset is relatively clean with zero missing values and well-encoded features.
4. The 95.98% cross-validation accuracy (very close to the 95.67% test accuracy) indicates minimal overfitting and strong generalization.

Decision Tree performed the worst (83.55%) due to its tendency to overfit training data despite the max_depth=8 constraint. Random Forest improved upon the Decision Tree (89.18%) through ensemble averaging but was still outperformed by the linear models. SVM achieved strong performance (93.51%) but was slightly below Logistic Regression.

## 5.3 SHAP Explainability Analysis

### 5.3.1 Global Feature Importance

**Table 5.3: SHAP Global Feature Importance (Top 10 Features)**

| Rank | Feature | Mean |SHAP| Value |
|---|---|---|
| 1 | PHQ-3: Sleep trouble | 0.5996 |
| 2 | PHQ-2: Feeling down/hopeless | High |
| 3 | PHQ-1: Low interest/pleasure | High |
| 4 | PHQ-4: Fatigue/low energy | High |
| 5 | PHQ-6: Feeling like a failure | High |
| 6 | PHQ-5: Appetite changes | High |
| 7 | PHQ-7: Concentration trouble | High |
| 8 | PHQ-9: Self-harm thoughts | Moderate-High |
| 9 | PHQ-8: Psychomotor changes | Moderate-High |
| 10 | Difficulty relaxing | Moderate |

**Key Finding**: PHQ-3 (Sleep trouble) emerged as the single most influential feature with a SHAP value of 0.5996, meaning it has the largest marginal contribution to predictions across all students and all risk classes. All nine PHQ-9 items dominated the top 9 positions, confirming that the clinical depression symptoms are the primary predictors. Among the lifestyle features, "Difficulty relaxing," "Exercise frequency," and "Sleep hours" were the strongest non-PHQ predictors. *(See Figure 5.13)*

### 5.3.2 Per-Class SHAP Analysis

The beeswarm and per-class bar charts revealed distinct patterns for each risk class:

- **Low Risk**: PHQ-3 (Sleep trouble) and PHQ-2 (Feeling down) had the highest SHAP contributions. Low values on these features (i.e., absence of symptoms) strongly pushed predictions toward the Low Risk class.
- **Moderate Risk**: A combination of moderate PHQ-9 symptom severity and lifestyle stressors (difficulty relaxing, exam anxiety) drove predictions toward this class.
- **High Risk**: PHQ-9 (Self-harm thoughts) and PHQ-6 (Feeling like a failure) had elevated importance for this class, consistent with clinical understanding that these symptoms are markers of severe depression. *(See Figures 5.14 and 5.15)*

### 5.3.3 Individual Student Explanations

Three representative case studies (one per risk class) demonstrated how SHAP provides personalized, interpretable explanations for individual predictions. The waterfall-style bar charts showed the top 12 features for each student with their actual feature values annotated, enabling clinicians to understand exactly why the model assigned a particular risk level. *(See Figure 5.16)*

## 5.4 SMOTE Oversampling Analysis

### 5.4.1 Class Distribution Before and After SMOTE

Before SMOTE, the High Risk class had approximately 148 samples in the training set (≈12.8%), compared to much larger counts for Low and Moderate Risk. After applying SMOTE with k_neighbors=5, all three classes were equalized to have the same number of training samples. *(See Figure 5.18)*

### 5.4.2 Impact on Model Performance

**Table 5.4: SMOTE Impact on Model Performance**

| Model | Metric | Without SMOTE | With SMOTE | Δ Change |
|---|---|---|---|---|
| Logistic Regression | Accuracy | High | Comparable | Minimal |
| Logistic Regression | Weighted F1 | High | Comparable | Minimal |
| Logistic Regression | High Risk F1 | Lower | Improved | Positive |
| Random Forest | High Risk F1 | Lower | Improved | Positive |
| SVM | High Risk F1 | Lower | Improved | Positive |

The primary benefit of SMOTE was observed in the **High Risk F1-Score**, which improved across all three models. This is the most clinically important metric — correctly identifying students at high risk for depression is more critical than maximizing overall accuracy. Overall accuracy and weighted F1-Score remained comparable, indicating that SMOTE did not degrade performance on the majority classes while improving minority class detection. *(See Figures 5.17 and 5.19)*

## 5.5 GAD-7 Anxiety Estimation

The GAD-7 simulation module revealed a strong positive correlation between estimated GAD-7 scores and PHQ-9 scores, consistent with the well-documented comorbidity between anxiety and depression. The Pearson correlation coefficient (r) between PHQ-9 and simulated GAD-7 was high, confirming that the stress-based proxy formula captures meaningful anxiety-related variance.

The cross-tabulation analysis showed that students with High Depression Risk were disproportionately likely to also have Moderate or Severe anxiety, while students with Low Depression Risk predominantly had Minimal or Mild anxiety. This dual-risk profiling provides clinicians with a more comprehensive view of each student's mental health status.

---

# Chapter 6: CONCLUSIONS AND FUTURE SCOPE

## 6.1 Conclusions

This project successfully designed, developed, and deployed **MINDscan** — an AI-based mental health risk prediction system for university students. The key conclusions drawn from this work are:

1. **High Predictive Accuracy**: The Logistic Regression model achieved a test accuracy of 95.67% and weighted F1-Score of 95.65%, demonstrating that machine learning can effectively predict depression risk levels from a combination of PHQ-9 scores and lifestyle indicators. The 5-fold cross-validation accuracy of 95.98% confirms strong generalization capability with minimal overfitting.

2. **Clinical Feature Dominance**: SHAP explainability analysis confirmed that the nine PHQ-9 clinical symptom items are the primary drivers of prediction, with PHQ-3 (Sleep trouble) being the single most influential feature (SHAP = 0.5996). This aligns with clinical literature that identifies sleep disturbance as both a symptom and a risk factor for depression.

3. **Lifestyle Factor Significance**: Among non-clinical features, difficulty relaxing, exercise frequency, and sleep duration emerged as meaningful predictors. These are modifiable behavioral factors, suggesting actionable intervention targets for university counseling services.

4. **Effective Class Imbalance Handling**: SMOTE oversampling improved the High Risk F1-Score without degrading overall model performance, ensuring that the underrepresented but clinically critical High Risk class is accurately identified.

5. **Dual Risk Assessment**: The integration of estimated GAD-7 anxiety scores alongside PHQ-9 depression screening provides a more holistic mental health profile, reflecting the high comorbidity between depression and anxiety disorders.

6. **Accessible Deployment**: The Flask web application, deployed on Render, makes the screening tool accessible to any student with a web browser, lowering barriers to mental health self-assessment. The inclusion of personalized recommendations and crisis helpline resources adds practical value beyond mere risk classification.

7. **Model Explainability**: The SHAP-based explanations ensure that the system is not a "black box" — students and counselors can understand which specific factors contribute to a given risk prediction, fostering trust and clinical utility.

## 6.2 Future Scope of Work

The following directions are proposed for future enhancement of this project:

1. **Longitudinal Data Collection**: The current system uses cross-sectional data (single time-point). Future work should collect longitudinal data — tracking the same students over multiple semesters — to model temporal changes in mental health risk and enable early warning systems that detect deteriorating trends.

2. **Actual GAD-7 Integration**: The current GAD-7 anxiety score is estimated from proxy stress indicators. A future version of the questionnaire should include the full seven-item GAD-7 scale, enabling validated dual depression-anxiety screening rather than simulated estimates.

3. **Deep Learning Models**: While Logistic Regression performed well on this dataset, future work could explore deep learning architectures (e.g., feedforward neural networks, attention-based models) on larger datasets to capture more complex non-linear feature interactions.

4. **Natural Language Processing (NLP)**: Integrating free-text responses (e.g., journal entries, open-ended questions about stressors) using NLP techniques such as sentiment analysis and topic modeling could provide richer, more nuanced mental health assessments.

5. **Multi-University Generalization**: The current model is trained on data from a single university (Manipal University Jaipur). Validating and retraining the model on data from multiple institutions across different regions would improve generalizability and account for cultural and institutional variations.

6. **Mobile Application Development**: Converting the web application into a native mobile application (Android/iOS) with push notification reminders for periodic self-assessments would improve accessibility and encourage regular mental health monitoring.

7. **Integration with University Counseling Services**: Future versions could include a secure referral pathway that, with the student's consent, shares risk assessment results directly with the university counseling center, enabling proactive outreach to high-risk students.

---

# REFERENCES

[1] K. Kroenke, R. L. Spitzer, and J. B. W. Williams, "The PHQ-9: Validity of a brief depression severity measure," *Journal of General Internal Medicine*, vol. 16, no. 9, pp. 606–613, Sep. 2001.

[2] R. L. Spitzer, K. Kroenke, J. B. W. Williams, and B. Löwe, "A brief measure for assessing generalized anxiety disorder: The GAD-7," *Archives of Internal Medicine*, vol. 166, no. 10, pp. 1092–1097, May 2006.

[3] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 30, 2017, pp. 4765–4774.

[4] N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, "SMOTE: Synthetic minority over-sampling technique," *Journal of Artificial Intelligence Research*, vol. 16, pp. 321–357, Jun. 2002.

[5] World Health Organization, "Depression and other common mental disorders: Global health estimates," WHO, Geneva, Tech. Rep., 2017.

[6] F. Pedregosa *et al.*, "Scikit-learn: Machine learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, Oct. 2011.

[7] A. Priya, S. Garg, and N. P. Tigga, "Predicting anxiety, depression and stress in modern life using machine learning algorithms," *Procedia Computer Science*, vol. 167, pp. 1258–1267, 2020.

[8] M. M. Islam, S. Karray, R. Alhajj, and J. Zeng, "A review on deep learning techniques for the diagnosis of novel coronavirus (COVID-19)," *IEEE Access*, vol. 9, pp. 30551–30572, 2021.

[9] G. Sahu, R. Kumar, and S. Kumar, "Mental health prediction using machine learning: A systematic review," *International Journal of Advanced Computer Science and Applications*, vol. 13, no. 5, pp. 150–160, 2022.

[10] T. Nguyen, D. Phung, B. Dao, S. Venkatesh, and M. Berk, "Affective and content analysis of online depression communities," *IEEE Transactions on Affective Computing*, vol. 5, no. 3, pp. 217–226, Jul. 2014.

[11] A. C. Müller and S. Guido, *Introduction to Machine Learning with Python: A Guide for Data Scientists*. Sebastopol, CA, USA: O'Reilly Media, 2016.

[12] J. Brownlee, "SMOTE for imbalanced classification with Python," *Machine Learning Mastery*, 2020. [Online]. Available: https://machinelearningmastery.com/smote-oversampling-for-imbalanced-classification/

[13] S. M. Lundberg, G. G. Erion, and S.-I. Lee, "Consistent individualized feature attribution for tree ensembles," arXiv preprint arXiv:1802.03888, 2018.

[14] American Psychiatric Association, *Diagnostic and Statistical Manual of Mental Disorders*, 5th ed. Arlington, VA, USA: APA, 2013.

[15] R. C. Kessler *et al.*, "Lifetime prevalence and age-of-onset distributions of DSM-IV disorders in the National Comorbidity Survey Replication," *Archives of General Psychiatry*, vol. 62, no. 6, pp. 593–602, Jun. 2005.

---

# ANNEXURES

## Annexure A: Project File Structure

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
│   ├── eda/                            #   → 10 EDA plots
│   ├── model/                          #   → Model comparison charts
│   ├── shap/                           #   → 4 SHAP explainability plots
│   └── smote/                          #   → 3 SMOTE analysis plots
│
├── app.py                              # Flask web application backend
├── Procfile                            # Render deployment config
├── runtime.txt                         # Python version
├── templates/index.html                # Frontend HTML (4,604 lines)
└── static/images/                      # Static web assets
```

## Annexure B: Python Dependencies (requirements.txt)

```
Flask>=2.3.0
pandas>=1.5.0
numpy>=1.21.0
scikit-learn>=1.3.0
gunicorn>=21.0.0
Werkzeug>=2.3.0
```

Additional dependencies used during development (not required for deployment):
- `shap` — SHAP explainability analysis
- `matplotlib` — Plot generation
- `seaborn` — Statistical visualization
- `imbalanced-learn` — SMOTE oversampling

## Annexure C: Sample Dataset Records

| Age | Gender | Year | Sleep | Exercise | PHQ-1 | PHQ-2 | PHQ-3 | ... | PHQ-9 | Total | Risk |
|-----|--------|------|-------|----------|-------|-------|-------|-----|-------|-------|------|
| 21 | 1 | 4 | 3 | 2 | 0 | 0 | 1 | ... | 0 | 4 | 0 |
| 19 | 0 | 2 | 1 | 0 | 2 | 2 | 3 | ... | 1 | 16 | 1 |
| 22 | 1 | 5 | 0 | 0 | 3 | 3 | 3 | ... | 2 | 23 | 2 |

## Annexure D: Prediction API — Sample Request and Response

**Request (POST /predict)**:
```json
{
  "age": 21,
  "gender": 0,
  "year": 4,
  "sleep": 3,
  "support": 3,
  "exercise": 2,
  "screen": 1,
  "overload": 0,
  "workload": 3,
  "relax": 3,
  "overwhelm": 3,
  "exam": 3,
  "study": 1,
  "phq": [0, 0, 0, 0, 0, 0, 0, 0, 0]
}
```

**Response**:
```json
{
  "prediction": 0,
  "probabilities": [0.94, 0.05, 0.01],
  "phq_total": 0,
  "stability": 90,
  "gad_estimate": 13
}
```

