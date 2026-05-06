from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
import json
import os
from pathlib import Path

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
        model_path = Path(__file__).parent / "model_c45.pkl"
        encoders_path = Path(__file__).parent / "label_encoders.pkl"
        target_path = Path(__file__).parent / "target_encoder.pkl"
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(encoders_path, 'rb') as f:
            label_encoders = pickle.load(f)
        with open(target_path, 'rb') as f:
            target_encoder = pickle.load(f)
        
        return model, label_encoders, target_encoder
    except Exception as e:
        raise Exception(f"Error loading models: {str(e)}")

try:
    MODEL, LABEL_ENCODERS, TARGET_ENCODER = load_models()
    MODEL_LOADED = True
except Exception as e:
    print(f"Warning: {str(e)}")
    MODEL_LOADED = False
    MODEL = None

# ==================== PYDANTIC MODELS ====================
class PredictionInput(BaseModel):
    jenis_kelamin: str
    asal_sma: str
    nikah: str
    ukuran_program: str

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    probabilities: dict
    status: str

# ==================== ROUTES ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sistem Prediksi Kelulusan Mahasiswa - API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict (POST)",
            "info": "/info (GET)",
            "health": "/health (GET)"
        }
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
        "accuracy_test": 0.55,
        "feature_importance": {
            "AsalSMA": 0.2941,
            "UkuranProgram": 0.2910,
            "JenisKelamin": 0.2475,
            "Nikah": 0.1673
        }
    }

@app.post("/api/predict")
async def predict(input_data: PredictionInput) -> PredictionResponse:
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
        
        return PredictionResponse(
            prediction=prediction,
            confidence=confidence,
            probabilities=pred_proba_dict,
            status="success"
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.post("/predict-batch")
async def predict_batch(inputs: list[PredictionInput]):
    """Make batch predictions"""
    
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    results = []
    for input_data in inputs:
        try:
            encoded_data = {
                'JenisKelamin': LABEL_ENCODERS['JenisKelamin'].transform([input_data.jenis_kelamin])[0],
                'AsalSMA': LABEL_ENCODERS['AsalSMA'].transform([input_data.asal_sma])[0],
                'Nikah': LABEL_ENCODERS['Nikah'].transform([input_data.nikah])[0],
                'UkuranProgram': LABEL_ENCODERS['UkuranProgram'].transform([input_data.ukuran_program])[0]
            }
            
            X = pd.DataFrame([encoded_data])
            prediction_encoded = MODEL.predict(X)[0]
            prediction = TARGET_ENCODER.classes_[prediction_encoded]
            probabilities = MODEL.predict_proba(X)[0]
            confidence = float(max(probabilities) * 100)
            
            pred_proba_dict = {
                TARGET_ENCODER.classes_[i]: float(probabilities[i] * 100)
                for i in range(len(TARGET_ENCODER.classes_))
            }
            
            results.append({
                "input": input_data.dict(),
                "prediction": prediction,
                "confidence": confidence,
                "probabilities": pred_proba_dict
            })
        except Exception as e:
            results.append({
                "input": input_data.dict(),
                "error": str(e)
            })
    
    return {"results": results, "total": len(results)}

@app.get("/api/docs")
async def get_docs():
    """API documentation"""
    return {
        "title": "Sistem Prediksi Kelulusan Mahasiswa - API",
        "version": "1.0.0",
        "description": "API untuk prediksi status kelulusan mahasiswa menggunakan Decision Tree C4.5",
        "endpoints": {
            "GET /": "Root endpoint dengan informasi API",
            "GET /health": "Health check status",
            "GET /info": "Informasi model dan features",
            "POST /predict": "Melakukan prediksi single instance",
            "POST /predict-batch": "Melakukan prediksi batch"
        },
        "example_request": {
            "jenis_kelamin": "Laki-laki",
            "asal_sma": "SMA",
            "nikah": "Belum",
            "ukuran_program": "Reguler"
        }
    }

# ==================== ERROR HANDLERS ====================
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
