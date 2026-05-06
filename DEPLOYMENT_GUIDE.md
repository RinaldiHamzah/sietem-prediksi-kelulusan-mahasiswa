# PANDUAN DEPLOYMENT KE VERCEL

## ✅ Prasyarat

Pastikan Anda memiliki:
1. **Git** terinstall di komputer
2. **GitHub Account** (untuk push kode)
3. **Vercel Account** (gratis di https://vercel.com)
4. Model files sudah ada:
   - `model_c45.pkl`
   - `label_encoders.pkl`
   - `target_encoder.pkl`

---

## 📝 Step 1: Setup Repository GitHub

### Opsi 1: Dari Repository yang Ada (Jika sudah ada GitHub repo)

```bash
# Navigate to project folder
cd "c:\Users\ADVAN\OneDrive - Universitas Teknologi Yogyakarta\Decition Tree"

# Cek status Git
git status

# Tambah semua file
git add .

# Commit perubahan
git commit -m "Setup FastAPI for Vercel deployment"

# Push ke GitHub
git push -u origin main
```

### Opsi 2: Buat Repository Baru

```bash
# Navigate to project folder
cd "c:\Users\ADVAN\OneDrive - Universitas Teknologi Yogyakarta\Decition Tree"

# Initialize Git
git init

# Tambah remote (ganti YOUR_USERNAME dan REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/sietem-prediksi-kelulusan-mahasiswa.git

# Tambah semua file
git add .

# Commit
git commit -m "Initial commit: FastAPI Vercel deployment setup"

# Push ke GitHub (ganti dengan branch name jika berbeda)
git branch -M main
git push -u origin main
```

---

## 🚀 Step 2: Deploy ke Vercel

### Via Vercel Web Dashboard (Paling Mudah)

1. **Buka** https://vercel.com/dashboard
2. **Login** dengan GitHub account
3. **Klik** "New Project"
4. **Select Repository** → Pilih `sietem-prediksi-kelulusan-mahasiswa`
5. **Klik** "Import"
6. **Configure Project**:
   - Framework Preset: **Other**
   - Root Directory: `.` (default)
   - Build Command: `pip install -r requirements.txt` (sudah di vercel.json)
   - Output Directory: (kosongkan)
7. **Environment Variables**: (optional, tidak perlu untuk setup awal)
8. **Klik** "Deploy"

Tunggu 2-5 menit hingga deployment selesai.

### Via Vercel CLI (Alternative)

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod

# Atau
vercel deploy --prod
```

---

## ✔️ Verifikasi Deployment

Setelah deployment berhasil:

1. **Klik link yang diberikan Vercel**
   - Format: `https://sietem-prediksi-kelulusan-mahasiswa.vercel.app`

2. **Test API Endpoints**:
   ```
   GET  https://[YOUR_DOMAIN].vercel.app/api/health
   GET  https://[YOUR_DOMAIN].vercel.app/api/info
   POST https://[YOUR_DOMAIN].vercel.app/api/predict
   ```

3. **Test Web Interface**:
   ```
   https://[YOUR_DOMAIN].vercel.app/public/index.html
   ```

---

## 🔧 File Structure untuk Vercel

```
.
├── api/
│   └── index.py              # ← FastAPI app untuk Vercel
├── public/
│   └── index.html            # ← Frontend HTML
├── model_c45.pkl             # ← Model file (PENTING!)
├── label_encoders.pkl        # ← Encoder file (PENTING!)
├── target_encoder.pkl        # ← Target encoder (PENTING!)
├── requirements.txt          # ← Python dependencies
├── vercel.json              # ← Vercel config
├── main.py                  # ← Local FastAPI server
└── README.md
```

---

## 📋 Troubleshooting

### Problem: "No python entrypoint found"
**Solution**: Pastikan `api/index.py` ada dan `vercel.json` sudah dikonfigurasi dengan benar.

### Problem: "Model files not found"
**Solution**: 
- Pastikan 3 file pkl sudah di-commit ke Git:
  ```bash
  git add model_c45.pkl label_encoders.pkl target_encoder.pkl
  git commit -m "Add model files"
  git push
  ```

### Problem: "500 Internal Server Error"
**Solution**:
- Cek logs di Vercel dashboard
- Pastikan Python packages di `requirements.txt` sudah benar
- Test locally: `python main.py` atau `uvicorn main:app --reload`

### Problem: API tidak bisa diakses dari frontend
**Solution**:
- Pastikan CORS middleware aktif di `api/index.py`
- Frontend sudah menggunakan URL yang benar
- Check browser console untuk error messages

---

## 🧪 Test Local Sebelum Deploy

### Setup Local Development

```bash
# Create virtual environment
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
python main.py

# Atau dengan uvicorn:
uvicorn main:app --reload
```

### Test API dengan curl atau Postman

```bash
# Test health
curl http://localhost:8000/api/health

# Test predict
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"jenis_kelamin":"Laki-laki","asal_sma":"SMA","nikah":"Belum","ukuran_program":"Reguler"}'

# Open frontend
# Browser: http://localhost:8000/public/index.html
```

---

## 📊 API Documentation

Setelah deploy, akses API docs:
```
https://[YOUR_DOMAIN].vercel.app/docs      # Swagger UI
https://[YOUR_DOMAIN].vercel.app/redoc     # ReDoc
```

---

## 🔄 Update Kode Setelah Deploy

Setiap kali ada perubahan:

```bash
git add .
git commit -m "Your commit message"
git push

# Vercel otomatis akan redeploy!
```

---

## 📞 Common Commands

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/sietem-prediksi-kelulusan-mahasiswa.git

# Check git status
git status

# View git log
git log --oneline

# Pull latest changes
git pull origin main

# Create new branch
git checkout -b feature/nama-fitur

# Merge branch
git merge feature/nama-fitur
```

---

## ✨ Selesai!

Aplikasi Anda sudah live di Vercel! 🎉

Sharing link:
```
https://[YOUR_DOMAIN].vercel.app
```

---

**Notes:**
- Domain default: `[PROJECT_NAME].vercel.app`
- Bisa custom domain dengan upgrade akun
- Setiap push ke `main` branch otomatis redeploy
- Build logs bisa dilihat di Vercel dashboard
- Environment variables bisa diatur di Project Settings

Untuk bantuan lebih lanjut: https://vercel.com/docs
