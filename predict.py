import pickle
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

# ==================== LOAD SAVED MODEL ====================
print("=" * 60)
print("PREDICTION MODULE - C4.5 DECISION TREE")
print("=" * 60)

with open(MODELS_DIR / 'model_c45.pkl', 'rb') as f:
    model = pickle.load(f)
with open(MODELS_DIR / 'label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)
with open(MODELS_DIR / 'target_encoder.pkl', 'rb') as f:
    target_encoder = pickle.load(f)

print("\n[OK] Model loaded successfully")

# ==================== PREDICTION FUNCTION ====================
def predict_kelulusan(jenis_kelamin, asal_sma, nikah, ukuran_program):
    """
    Prediksi kelulusan berdasarkan input features
    
    Parameters:
    - jenis_kelamin: 'Laki-laki' atau 'Perempuan'
    - asal_sma: 'SMA' atau 'SMK'
    - nikah: 'Belum' atau 'Sudah'
    - ukuran_program: 'Reguler' atau 'Ekstensi'
    
    Returns:
    - prediction: 'Tepat' atau 'Terlambat'
    """
    
    # Encode input
    encoded_data = {
        'JenisKelamin': label_encoders['JenisKelamin'].transform([jenis_kelamin])[0],
        'AsalSMA': label_encoders['AsalSMA'].transform([asal_sma])[0],
        'Nikah': label_encoders['Nikah'].transform([nikah])[0],
        'UkuranProgram': label_encoders['UkuranProgram'].transform([ukuran_program])[0]
    }
    
    # Create DataFrame
    X = pd.DataFrame([encoded_data])
    
    # Predict
    prediction_encoded = model.predict(X)[0]
    prediction = target_encoder.classes_[prediction_encoded]
    
    # Get probability
    probabilities = model.predict_proba(X)[0]
    confidence = max(probabilities) * 100
    
    return prediction, confidence

# ==================== EXAMPLE PREDICTIONS ====================
print("\n" + "=" * 60)
print("EXAMPLE PREDICTIONS")
print("=" * 60)

test_cases = [
    ('Laki-laki', 'SMA', 'Belum', 'Reguler'),
    ('Perempuan', 'SMK', 'Sudah', 'Ekstensi'),
    ('Laki-laki', 'SMK', 'Belum', 'Reguler'),
    ('Perempuan', 'SMA', 'Sudah', 'Reguler'),
    ('Laki-laki', 'SMK', 'Sudah', 'Ekstensi'),
]

print("\n")
for jk, asal, nikah, prog in test_cases:
    prediction, confidence = predict_kelulusan(jk, asal, nikah, prog)
    print(f"Input: {jk:12} | {asal:4} | {nikah:5} | {prog:8}")
    print(f"  -> Prediksi: {prediction:12} (Confidence: {confidence:.2f}%)")
    print()

# ==================== INTERACTIVE PREDICTION ====================
print("=" * 60)
print("INTERACTIVE PREDICTION")
print("=" * 60)
print("\nFormat input sebagai: 'Jenis_Kelamin,AsalSMA,Nikah,UkuranProgram'")
print("Contoh: Laki-laki,SMA,Belum,Reguler")
print("Ketik 'quit' untuk keluar\n")

while True:
    user_input = input("Masukkan data (atau 'quit'): ").strip()
    
    if user_input.lower() == 'quit':
        print("Terima kasih!")
        break
    
    try:
        parts = user_input.split(',')
        if len(parts) != 4:
            print("Error: Masukkan 4 parameter yang dipisahkan koma")
            continue
        
        jk, asal, nikah, prog = [p.strip() for p in parts]
        prediction, confidence = predict_kelulusan(jk, asal, nikah, prog)
        
        print(f"[OK] Prediksi: {prediction} (Confidence: {confidence:.2f}%)")
        print()
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Pastikan input sesuai dengan format yang benar\n")
