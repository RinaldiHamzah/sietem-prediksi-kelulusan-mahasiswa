from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# ==================== INIT FASTAPI ====================
app = FastAPI(title="Prediksi Kelulusan API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== LOAD MODEL ====================
def load_models():
    """Load model dan encoders"""
    try:
        # Try different paths for Vercel deployment
        parent_dir = Path(__file__).parent.parent
        
        model_path = parent_dir / "model_c45.pkl"
        encoders_path = parent_dir / "label_encoders.pkl"
        target_path = parent_dir / "target_encoder.pkl"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(encoders_path, 'rb') as f:
            label_encoders = pickle.load(f)
        with open(target_path, 'rb') as f:
            target_encoder = pickle.load(f)
        
        return model, label_encoders, target_encoder
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        return None, None, None

MODEL, LABEL_ENCODERS, TARGET_ENCODER = load_models()
MODEL_LOADED = MODEL is not None

# ==================== PYDANTIC MODELS ====================
class PredictionInput(BaseModel):
    jenis_kelamin: str
    asal_sma: str
    nikah: str
    ukuran_program: str

# ==================== ROUTES ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sistem Prediksi Kelulusan Mahasiswa - API",
        "version": "1.0.0",
        "status": "ok"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "model_loaded": MODEL_LOADED
    }

@app.get("/api/info")
async def get_info():
    """Get model information"""
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model": "Decision Tree C4.5",
        "features": {
            "jenis_kelamin": ["Laki-laki", "Perempuan"],
            "asal_sma": ["SMA", "SMK"],
            "nikah": ["Belum", "Sudah"],
            "ukuran_program": ["Reguler", "Ekstensi"]
        },
        "target_classes": list(TARGET_ENCODER.classes_),
        "accuracy_train": 0.65,
        "accuracy_test": 0.55
    }

@app.post("/api/predict")
async def predict(input_data: PredictionInput):
    """Make prediction based on input features"""
    
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Encode input
        encoded_data = {
            'JenisKelamin': LABEL_ENCODERS['JenisKelamin'].transform([input_data.jenis_kelamin])[0],
            'AsalSMA': LABEL_ENCODERS['AsalSMA'].transform([input_data.asal_sma])[0],
            'Nikah': LABEL_ENCODERS['Nikah'].transform([input_data.nikah])[0],
            'UkuranProgram': LABEL_ENCODERS['UkuranProgram'].transform([input_data.ukuran_program])[0]
        }
        
        # Create DataFrame
        X = pd.DataFrame([encoded_data])
        
        # Predict
        prediction_encoded = MODEL.predict(X)[0]
        prediction = TARGET_ENCODER.classes_[prediction_encoded]
        
        # Get probabilities
        probabilities = MODEL.predict_proba(X)[0]
        confidence = float(max(probabilities) * 100)
        
        # Create probability dict
        pred_proba_dict = {
            TARGET_ENCODER.classes_[i]: float(probabilities[i] * 100)
            for i in range(len(TARGET_ENCODER.classes_))
        }
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "probabilities": pred_proba_dict,
            "status": "success"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

# Export app for Vercel
# Vercel will automatically detect this as an ASGI app
