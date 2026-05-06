# ✅ CHECKLIST VERCEL DEPLOYMENT

## 📋 Pre-Deployment Checklist

### 1. Code Files ✓
- [ ] `api/index.py` - FastAPI untuk Vercel
- [ ] `main.py` - FastAPI untuk local development
- [ ] `public/index.html` - Frontend
- [ ] `requirements.txt` - Dependencies (updated for FastAPI)
- [ ] `vercel.json` - Vercel configuration

### 2. Model Files ✓
- [ ] `model_c45.pkl` - Trained model
- [ ] `label_encoders.pkl` - Feature encoders
- [ ] `target_encoder.pkl` - Target encoder

### 3. Documentation ✓
- [ ] `DEPLOYMENT_GUIDE.md` - Step-by-step deployment
- [ ] `VERCEL_README.md` - Quick reference
- [ ] `README.md` - Project overview

### 4. Scripts ✓
- [ ] `RUN_SERVER.bat` - Run local development server
- [ ] `test_deployment.bat` - Test deployment setup
- [ ] `test_deployment.sh` - Test script for Unix

### 5. Configuration ✓
- [ ] `.gitignore` - Git ignore rules
- [ ] `vercel.json` - Vercel build config

---

## 🧪 Testing Steps

### Local Testing
1. Open Command Prompt / PowerShell
2. Navigate to project folder
3. Run: `test_deployment.bat`
4. Expected output:
   ```
   [1/6] Checking Python... OK
   [2/6] Installing dependencies... OK
   [3/6] Checking model files... OK
   [4/6] Checking API files... OK
   [5/6] Checking Vercel config... OK
   [6/6] Testing Python imports... OK
   ✓ All tests passed!
   ```

### Start Development Server
1. Run: `RUN_SERVER.bat`
2. Open browser: `http://localhost:8000/public/index.html`
3. Test form submission
4. Check console for errors
5. Stop server with CTRL+C

---

## 📤 Deployment Steps

### Step 1: Git Setup
```bash
git add .
git commit -m "Setup FastAPI for Vercel deployment"
git push -u origin main
```

### Step 2: Vercel Deploy
**Option A: Via Web Dashboard**
1. Go to https://vercel.com/dashboard
2. Click "New Project"
3. Select your repository
4. Click "Import"
5. Click "Deploy"

**Option B: Via CLI**
```bash
npm install -g vercel
vercel --prod
```

### Step 3: Verify Deployment
```bash
# Check health
curl https://YOUR_DOMAIN.vercel.app/api/health

# Test prediction
curl -X POST https://YOUR_DOMAIN.vercel.app/api/predict \
  -H "Content-Type: application/json" \
  -d '{"jenis_kelamin":"Laki-laki","asal_sma":"SMA","nikah":"Belum","ukuran_program":"Reguler"}'
```

### Step 4: Share
- Frontend: `https://YOUR_DOMAIN.vercel.app/public/index.html`
- API Docs: `https://YOUR_DOMAIN.vercel.app/docs`
- ReDoc: `https://YOUR_DOMAIN.vercel.app/redoc`

---

## 🆘 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution**: 
```bash
pip install -r requirements.txt
```

### Issue: "pickle.UnpicklingError"
**Solution**:
- Ensure model files are in root directory
- Files must be committed to Git for Vercel
- Re-run `model.py` if needed

### Issue: API returns 503 - Model not loaded
**Solution**:
- Check model files exist
- Check Vercel build logs
- Redeploy with fresh build

### Issue: CORS error from frontend
**Solution**:
- Already configured in `api/index.py`
- Check browser console for specific error
- Test with curl first

### Issue: Slow response time
**Solution**:
- First request may be slow (cold start)
- Subsequent requests are fast
- This is normal for serverless

---

## 📊 File Checklist

Run this to verify all files:

```bash
# Windows PowerShell or CMD
if exist "api\index.py" echo ✓ api/index.py
if exist "main.py" echo ✓ main.py
if exist "public\index.html" echo ✓ public/index.html
if exist "requirements.txt" echo ✓ requirements.txt
if exist "vercel.json" echo ✓ vercel.json
if exist "model_c45.pkl" echo ✓ model_c45.pkl
if exist "label_encoders.pkl" echo ✓ label_encoders.pkl
if exist "target_encoder.pkl" echo ✓ target_encoder.pkl
if exist "DEPLOYMENT_GUIDE.md" echo ✓ DEPLOYMENT_GUIDE.md
if exist "VERCEL_README.md" echo ✓ VERCEL_README.md
if exist "RUN_SERVER.bat" echo ✓ RUN_SERVER.bat
if exist "test_deployment.bat" echo ✓ test_deployment.bat
if exist ".gitignore" echo ✓ .gitignore
```

---

## 🎯 Success Criteria

✅ Deployment is successful if:
- [ ] Application loads without errors
- [ ] Frontend form is visible
- [ ] Can submit prediction from frontend
- [ ] Result displays correctly
- [ ] API health check returns 200 OK
- [ ] API predict endpoint works
- [ ] No CORS errors in console
- [ ] Response time is < 2 seconds

---

## 🚀 Post-Deployment

### 1. Monitor Performance
- Check Vercel dashboard for metrics
- Monitor error rates
- Check response times

### 2. Share Application
- Share frontend link
- Document API for developers
- Create usage guide

### 3. Maintenance
- Update model as needed
- Push commits to trigger redeploy
- Check logs regularly

### 4. Improvements
- Optimize API response time
- Add caching if needed
- Implement rate limiting
- Add authentication

---

## 📞 Quick Reference

```bash
# Local Development
python main.py                    # Start dev server

# Testing
test_deployment.bat               # Run all tests

# Git Operations
git add .                         # Stage changes
git commit -m "message"           # Commit
git push                          # Push to GitHub

# Vercel
vercel --prod                     # Deploy to production
vercel logs [url]                 # View logs
vercel env list                   # List env vars
```

---

## ✨ Ready to Deploy?

1. ✓ All files present?
2. ✓ Tests passing?
3. ✓ Git commits done?
4. ✓ GitHub account ready?
5. ✓ Vercel account ready?

**If all YES → You're ready to deploy! 🚀**

---

**Status**: ✅ Vercel Compatible  
**Last Checked**: May 2026  
**Version**: 1.0.0
