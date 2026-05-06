import pickle
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

# Load model
with open(MODELS_DIR / 'model_c45.pkl', 'rb') as f:
    model = pickle.load(f)
with open(MODELS_DIR / 'label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)
with open(MODELS_DIR / 'target_encoder.pkl', 'rb') as f:
    target_encoder = pickle.load(f)

def predict_kelulusan(jenis_kelamin, asal_sma, nikah, ukuran_program):
    encoded_data = {
        'JenisKelamin': label_encoders['JenisKelamin'].transform([jenis_kelamin])[0],
        'AsalSMA': label_encoders['AsalSMA'].transform([asal_sma])[0],
        'Nikah': label_encoders['Nikah'].transform([nikah])[0],
        'UkuranProgram': label_encoders['UkuranProgram'].transform([ukuran_program])[0]
    }
    X = pd.DataFrame([encoded_data])
    prediction_encoded = model.predict(X)[0]
    prediction = target_encoder.classes_[prediction_encoded]
    probabilities = model.predict_proba(X)[0]
    confidence = max(probabilities) * 100
    return prediction, confidence

if __name__ == "__main__":
    print("=" * 60)
    print("PREDICTION EXAMPLES")
    print("=" * 60)

    test_cases = [
        ('Laki-laki', 'SMA', 'Belum', 'Reguler'),
        ('Perempuan', 'SMK', 'Sudah', 'Ekstensi'),
        ('Laki-laki', 'SMK', 'Belum', 'Reguler'),
        ('Perempuan', 'SMA', 'Sudah', 'Reguler'),
        ('Laki-laki', 'SMK', 'Sudah', 'Ekstensi'),
    ]

    print()
    for jk, asal, nikah, prog in test_cases:
        prediction, confidence = predict_kelulusan(jk, asal, nikah, prog)
        print(f"Input: {jk:12} | {asal:4} | {nikah:5} | {prog:8}")
        print(f"  -> Prediksi: {prediction:12} (Confidence: {confidence:.2f}%)")
        print()

    print("=" * 60)
