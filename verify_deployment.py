#!/usr/bin/env python3
"""
Summary dan verification script untuk Vercel deployment
Jalankan script ini untuk verifikasi bahwa semua siap deploy
"""

import os
import sys
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    required_files = {
        'Code Files': {
            'api/index.py': 'FastAPI app for Vercel',
            'main.py': 'FastAPI app for local dev',
            'public/index.html': 'Frontend interface',
            'requirements.txt': 'Python dependencies',
            'vercel.json': 'Vercel configuration',
        },
        'Model Files': {
            'model_c45.pkl': 'Trained Decision Tree model',
            'label_encoders.pkl': 'Feature label encoders',
            'target_encoder.pkl': 'Target label encoder',
        },
        'Documentation': {
            'DEPLOYMENT_GUIDE.md': 'Step-by-step deployment guide',
            'VERCEL_README.md': 'Vercel-specific documentation',
            'DEPLOYMENT_CHECKLIST.md': 'Pre-deployment checklist',
            'README.md': 'Project overview',
        },
        'Scripts': {
            'RUN_SERVER.bat': 'Local development server launcher',
            'test_deployment.bat': 'Deployment test script',
        },
        'Configuration': {
            '.gitignore': 'Git ignore rules',
        }
    }
    
    print("\n" + "="*60)
    print("📋 FILE VERIFICATION")
    print("="*60)
    
    all_ok = True
    for category, files in required_files.items():
        print(f"\n{category}:")
        for filename, description in files.items():
            path = Path(filename)
            if path.exists():
                print(f"  ✓ {filename:<30} - {description}")
            else:
                print(f"  ✗ {filename:<30} - {description}")
                all_ok = False
    
    return all_ok

def check_requirements():
    """Check if requirements.txt has correct packages"""
    print("\n" + "="*60)
    print("📦 REQUIREMENTS VERIFICATION")
    print("="*60)
    
    required_packages = {
        'fastapi': 'Web framework',
        'uvicorn': 'ASGI server',
        'pandas': 'Data processing',
        'numpy': 'Numerical computing',
        'scikit-learn': 'Machine learning',
        'pydantic': 'Data validation',
    }
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        print("\nRequirements.txt content:")
        print(content)
        
        all_ok = True
        for package, description in required_packages.items():
            if package.lower() in content.lower():
                print(f"✓ {package:<20} - {description}")
            else:
                print(f"✗ {package:<20} - {description}")
                all_ok = False
        
        return all_ok
    except FileNotFoundError:
        print("✗ requirements.txt not found")
        return False

def check_vercel_config():
    """Check vercel.json configuration"""
    print("\n" + "="*60)
    print("⚙️  VERCEL CONFIGURATION")
    print("="*60)
    
    try:
        with open('vercel.json', 'r') as f:
            import json
            config = json.load(f)
        
        print("\nVercel configuration loaded successfully!")
        print("\nKey settings:")
        print(f"  - Runtime: {config.get('functions', {}).get('api/index.py', {}).get('runtime', 'N/A')}")
        print(f"  - Build Command: {config.get('buildCommand', 'Not set')}")
        print(f"  - Functions: {list(config.get('functions', {}).keys())}")
        print(f"  - Rewrites: {config.get('rewrites', [])}")
        
        return True
    except Exception as e:
        print(f"✗ Error reading vercel.json: {e}")
        return False

def check_api_structure():
    """Check API structure"""
    print("\n" + "="*60)
    print("🔌 API STRUCTURE")
    print("="*60)
    
    endpoints = {
        'GET /': 'Root endpoint',
        'GET /api/health': 'Health check',
        'GET /api/info': 'Model information',
        'POST /api/predict': 'Single prediction',
        'POST /api/predict-batch': 'Batch prediction',
        'GET /docs': 'Swagger UI',
        'GET /redoc': 'ReDoc documentation',
        'GET /public/index.html': 'Frontend interface',
    }
    
    print("\nAvailable endpoints:")
    for endpoint, description in endpoints.items():
        print(f"  {endpoint:<30} - {description}")
    
    return True

def main():
    """Main verification function"""
    print("\n" + "🚀 "*15)
    print("VERCEL DEPLOYMENT VERIFICATION")
    print("🚀 "*15)
    
    results = {
        'Files': check_files(),
        'Requirements': check_requirements(),
        'Vercel Config': check_vercel_config(),
        'API Structure': check_api_structure(),
    }
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    for check, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{check:<25} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL CHECKS PASSED - Ready for Vercel deployment!")
        print("="*60)
        print("\nNext steps:")
        print("1. Test locally: python main.py")
        print("2. Commit changes: git add . && git commit -m 'Ready for Vercel'")
        print("3. Push to GitHub: git push")
        print("4. Deploy on Vercel dashboard or CLI")
        print("5. Share your live application!")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - Please fix issues before deploying")
        print("="*60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
