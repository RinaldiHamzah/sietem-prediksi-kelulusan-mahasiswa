# 📋 ALTERNATIVE VERCEL.JSON CONFIGURATIONS

Jika runtime format `python@3.11` masih error, coba salah satu konfigurasi di bawah.

---

## ✅ CONFIGURATION 1 (Currently Using)

**File:** `vercel.json`
```json
{
  "buildCommand": "pip install -r requirements.txt",
  "installCommand": "pip install -r requirements.txt",
  "functions": {
    "api/index.py": {
      "runtime": "python@3.11"
    }
  },
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/index.py" }
  ],
  "env": {
    "PYTHONUNBUFFERED": "1"
  }
}
```
**Status:** Currently deployed
**Try this first!**

---

## 🔄 CONFIGURATION 2 (Alternative - Without Functions)

If Configuration 1 fails, try this:

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "installCommand": "pip install -r requirements.txt",
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/index.py" }
  ],
  "env": {
    "PYTHONUNBUFFERED": "1"
  }
}
```

**Explanation:** Let Vercel auto-detect Python functions without explicit runtime specification.

**When to use:** If Configuration 1 gives runtime format error.

---

## 🔄 CONFIGURATION 3 (With Python Version in Path)

If both above fail:

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "installCommand": "pip install -r requirements.txt",
  "functions": {
    "api/index.py": {
      "runtime": "python:3.11"
    }
  },
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/index.py" }
  ],
  "env": {
    "PYTHONUNBUFFERED": "1"
  }
}
```

**Difference:** Uses `python:3.11` instead of `python@3.11`

---

## 🔄 CONFIGURATION 4 (Minimal Setup)

Most minimal configuration:

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/index.py" }
  ]
}
```

**Warning:** Only use if others fail - minimal error checking.

---

## 🔄 CONFIGURATION 5 (With Source Map)

If you need more control:

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "installCommand": "pip install -r requirements.txt",
  "functions": {
    "api/*.py": {
      "runtime": "python@3.11"
    }
  },
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/index.py" }
  ],
  "env": {
    "PYTHONUNBUFFERED": "1",
    "PYTHONPATH": "."
  }
}
```

**Difference:** Uses glob pattern for all .py files in api folder

---

## 📋 WHICH ONE TO USE?

### Step 1: Try Current Configuration
**Configuration 1** (`python@3.11`)
- Most standard format
- Should work with modern Vercel
- **Try this first**

### Step 2: If fails, try these in order:
1. **Configuration 2** - Without explicit runtime
2. **Configuration 3** - With `:` instead of `@`
3. **Configuration 4** - Minimal setup
4. **Configuration 5** - With glob pattern

---

## 🛠️ HOW TO SWITCH CONFIGURATION

If current doesn't work:

1. **Backup current vercel.json:**
   ```bash
   copy vercel.json vercel.json.backup
   ```

2. **Edit vercel.json** with alternative configuration

3. **Commit and push:**
   ```bash
   git add vercel.json
   git commit -m "Switch to alternative Vercel configuration"
   git push
   ```

4. **Wait 2-5 minutes** for auto-redeploy

5. **Check status** in Vercel dashboard

---

## 🔍 HOW TO CHECK WHAT'S WRONG

In Vercel Dashboard:
1. Go to Project
2. Click latest **Deployment**
3. Go to **"Logs"** tab
4. Look for error messages
5. Match error to troubleshooting below

---

## 🚨 COMMON ERRORS & SOLUTIONS

### Error: "Function Runtimes must have a valid version"
**Try:** Configuration 2 (without functions field)
**Or:** Configuration 3 (with `:` instead of `@`)

### Error: "ModuleNotFoundError: No module named 'fastapi'"
**Solution:**
- Ensure `requirements.txt` has fastapi
- Check buildCommand runs correctly
- Verify Python packages install

### Error: "File not found: api/index.py"
**Solution:**
- Verify file exists in repository
- Check file path spelling
- Ensure file is committed to git

### Error: "No module named 'models'"
**Solution:**
- Model files (.pkl) must be in root directory
- Check they're committed to git
- Add to vercel.json if needed

### Error: "CORS error on frontend"
**Solution:**
- CORS already configured in api/index.py
- Check browser console for exact error
- Verify API URL matches actual domain

---

## ✅ VERIFICATION AFTER FIX

Once deployment succeeds, test:

```bash
# 1. Health check
curl https://YOUR-DOMAIN.vercel.app/api/health

# 2. Get info
curl https://YOUR-DOMAIN.vercel.app/api/info

# 3. Make prediction
curl -X POST https://YOUR-DOMAIN.vercel.app/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "jenis_kelamin": "Laki-laki",
    "asal_sma": "SMA",
    "nikah": "Belum",
    "ukuran_program": "Reguler"
  }'

# 4. Open web interface
# https://YOUR-DOMAIN.vercel.app/public/index.html
```

---

## 📞 GETTING MORE HELP

If none of these work:

1. Check Vercel documentation: https://vercel.com/docs/functions/serverless-functions/python
2. Review build logs in dashboard
3. Check requirements.txt for syntax errors
4. Ensure all files are properly committed

---

## 💡 NOTES

- Configuration 1 is recommended for modern Vercel
- All configurations serve the same API
- Difference is only in how Vercel interprets the config
- Once working, don't change unless you hit issues

---

**Current Status:** Configuration 1 deployed (`python@3.11`)

If this fails, use FIX_DEPLOYMENT_ERROR.md for step-by-step recovery.
