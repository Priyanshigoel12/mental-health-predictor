from app import app, model, scaler, FEATURES
import pandas as pd

# Test data
test_input = {
    'Age': 21,
    'Gender': 0,
    'Year of Study': 4,
    'Average sleep hours': 3,
    'How often do you feel supported by friends or family?': 3,
    'Physical exercise frequency': 2,
    'Daily screen time': 1,
    'Do you feel academically overloaded?': 0,
    'I feel stressed because of academic workload': 3,
    'I find it difficult to relax': 3,
    'I feel overwhelmed by responsibilities': 3,
    'I feel anxious about exams or deadlines': 3,
    'How many hours per day do you spend studying outside class?': 1,
    '[Little interest or pleasure in doing things]': 0,
    '[Feeling down, depressed, or hopeless]': 0,
    '[Trouble falling or staying asleep, or sleeping too much]': 0,
    '[Feeling tired or having little energy]': 0,
    '[Poor appetite or overeating]': 0,
    '[Feeling bad about yourself — or that you are a failure]': 0,
    '[Trouble concentrating on things]': 0,
    '[Moving or speaking slowly OR being restless/fidgety]': 0,
    '[Thoughts that you would be better off dead or hurting yourself]': 0,
}

print(f"Test input keys: {len(test_input)}")
print(f"Model expects: {len(FEATURES)}")

try:
    test_df = pd.DataFrame([test_input])[FEATURES]
    print(f"✓ DataFrame created: {test_df.shape}")
    
    test_scaled = scaler.transform(test_df)
    test_scaled_df = pd.DataFrame(test_scaled, columns=FEATURES)
    
    pred = model.predict(test_scaled_df)[0]
    probs = model.predict_proba(test_scaled_df)[0]
    
    print(f"✓ Prediction successful!")
    print(f"  Prediction: {pred}")
    print(f"  Probabilities: {probs}")
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
