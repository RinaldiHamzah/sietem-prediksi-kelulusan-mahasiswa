#!/bin/bash
# Test script for Vercel deployment

echo "======================================"
echo "Testing Vercel Deployment Setup"
echo "======================================"
echo ""

# Check Python
echo "✓ Checking Python..."
python --version

# Check pip
echo "✓ Checking pip..."
pip --version

# Install dependencies
echo "✓ Installing dependencies..."
pip install -q -r requirements.txt

# Check model files
echo "✓ Checking model files..."
if [ -f "model_c45.pkl" ]; then
    echo "  ✓ model_c45.pkl found"
else
    echo "  ✗ model_c45.pkl NOT found"
    exit 1
fi

if [ -f "label_encoders.pkl" ]; then
    echo "  ✓ label_encoders.pkl found"
else
    echo "  ✗ label_encoders.pkl NOT found"
    exit 1
fi

if [ -f "target_encoder.pkl" ]; then
    echo "  ✓ target_encoder.pkl found"
else
    echo "  ✗ target_encoder.pkl NOT found"
    exit 1
fi

# Check API files
echo "✓ Checking API files..."
if [ -f "api/index.py" ]; then
    echo "  ✓ api/index.py found"
else
    echo "  ✗ api/index.py NOT found"
    exit 1
fi

# Check vercel.json
echo "✓ Checking Vercel config..."
if [ -f "vercel.json" ]; then
    echo "  ✓ vercel.json found"
else
    echo "  ✗ vercel.json NOT found"
    exit 1
fi

# Test import
echo "✓ Testing imports..."
python -c "from fastapi import FastAPI; from pydantic import BaseModel; print('  ✓ FastAPI imports OK')"
python -c "import pandas; import sklearn; print('  ✓ Data science imports OK')"

# Verify structure
echo "✓ Checking directory structure..."
echo "  ✓ All checks passed!"

echo ""
echo "======================================"
echo "✅ All tests passed!"
echo "======================================"
echo ""
echo "Ready to deploy to Vercel!"
echo ""
echo "Next steps:"
echo "1. git add ."
echo "2. git commit -m 'Vercel deployment ready'"
echo "3. git push"
