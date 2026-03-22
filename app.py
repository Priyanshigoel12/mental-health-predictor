# =============================================================================
# MindScan — AI Mental Health Risk Assessment
# Flask backend serving HTML frontend + ML prediction API
# =============================================================================

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle
import os

app = Flask(__name__)

# ── Load AI Model ─────────────────────────────────────────────────────────────
def load_model():
    try:
        with open('best_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open('feature_names.pkl', 'rb') as f:
            features = pickle.load(f)
        return model, scaler, features
    except FileNotFoundError as e:
        print(f"⚠️ Model file missing: {e}")
        return None, None, None

model, scaler, FEATURES = load_model()

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    data = request.get_json()

    # Map frontend keys to model feature names
    input_dict = {
        'Age': data.get('age', 21),
        'Gender': data.get('gender', 0),
        'Year of Study': data.get('year', 4),
        'Average sleep hours': data.get('sleep', 3),
        'How often do you feel supported by friends or family?': data.get('support', 3),
        'Physical exercise frequency': data.get('exercise', 2),
        'Daily screen time': data.get('screen', 1),
        'Do you feel academically overloaded?': data.get('overload', 0),
        'I feel stressed because of academic workload': data.get('workload', 3),
        'I find it difficult to relax': data.get('relax', 3),
        'I feel overwhelmed by responsibilities': data.get('overwhelm', 3),
        'I feel anxious about exams or deadlines': data.get('exam', 3),
        'How many hours per day do you spend studying outside class?': data.get('study', 1),
        '[Little interest or pleasure in doing things]': data['phq'][0],
        '[Feeling down, depressed, or hopeless]': data['phq'][1],
        '[Trouble falling or staying asleep, or sleeping too much]': data['phq'][2],
        '[Feeling tired or having little energy]': data['phq'][3],
        '[Poor appetite or overeating]': data['phq'][4],
        '[Feeling bad about yourself — or that you are a failure]': data['phq'][5],
        '[Trouble concentrating on things]': data['phq'][6],
        '[Moving or speaking slowly OR being restless/fidgety]': data['phq'][7],
        '[Thoughts that you would be better off dead or hurting yourself]': data['phq'][8],
    }

    # Build DataFrame in correct feature order, scale, and predict
    input_df = pd.DataFrame([input_dict])[FEATURES]
    input_scaled = scaler.transform(input_df)
    input_scaled_df = pd.DataFrame(input_scaled, columns=FEATURES)

    pred_class = int(model.predict(input_scaled_df)[0])
    probs = model.predict_proba(input_scaled_df)[0].tolist()

    phq_total = sum(data['phq'])
    stability = max(10, 100 - int(phq_total * 2.5 + (data.get('workload', 3) - 1) * 5))
    gad_estimate = min(21, round(
        (data.get('workload', 3) + data.get('relax', 3) + data.get('exam', 3)) * 1.2
        + (2 if data.get('screen', 1) > 1 else 0)
    ))

    return jsonify({
        'prediction': pred_class,
        'probabilities': probs,
        'phq_total': phq_total,
        'stability': stability,
        'gad_estimate': gad_estimate,
    })


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)