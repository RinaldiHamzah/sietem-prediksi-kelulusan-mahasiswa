# 🎓 Aplikasi Prediksi Kelulusan Mahasiswa - Decision Tree C4.5

## 📋 Deskripsi Aplikasi

Aplikasi web berbasis **Streamlit** yang memudahkan pengguna non-IT untuk memprediksi status kelulusan mahasiswa menggunakan algoritma Machine Learning **Decision Tree C4.5**.


---

## 🚀 Cara Menjalankan Aplikasi

### Opsi 1: Menggunakan Terminal
```bash
cd "c:\Users\ADVAN\OneDrive - Universitas Teknologi Yogyakarta\Decition Tree"
streamlit run app.py
```

### Opsi 2: Menggunakan Tombol Run di VS Code
- Buka file `app.py`
- Klik tombol "Run" atau tekan `Ctrl+F5`

Aplikasi akan berjalan di: **http://localhost:8501**

---

## 📱 Fitur-Fitur Aplikasi

### 1. 🏠 **Halaman Beranda (Home)**
   - **Informasi Aplikasi**: Penjelasan tentang algoritma C4.5
   - **Faktor Prediksi**: Menunjukkan 4 faktor yang digunakan
   - **Performa Model**: Menampilkan akurasi dan metrik lainnya
   - **Output Prediksi**: Hasil yang bisa didapatkan (Tepat/Terlambat)

### 2. 🔮 **Halaman Prediksi (Prediction)**
   Fitur utama untuk melakukan prediksi:
   - **Input Data Interaktif**: 4 dropdown untuk memilih:
     - 👤 Jenis Kelamin (Laki-laki/Perempuan)
     - 🏫 Asal Sekolah (SMA/SMK)
     - 💍 Status Pernikahan (Belum/Sudah)
     - 📚 Ukuran Program (Reguler/Ekstensi)
   - **Tombol Prediksi**: Menjalankan prediksi dengan 1 klik
   - **Hasil Prediksi**: 
     - ✅ Status kelulusan (Tepat/Terlambat)
     - 📊 Tingkat kepercayaan (Confidence %)
     - 🎯 Probabilitas untuk setiap kelas
     - 📥 Data input yang digunakan

### 3. 📊 **Halaman Analisis Model (Model Analysis)**
   Visualisasi mendalam tentang performa model:
   
   **Tab 1: 🌳 Struktur Tree**
   - Menampilkan seluruh struktur decision tree
   - Menunjukkan node splitting criteria
   - Visualisasi lengkap dari root hingga leaf nodes

   **Tab 2: 📈 Feature Importance**
   - Grafik kepentingan setiap fitur
   - AsalSMA: 39.19% (paling penting)
   - JenisKelamin: 27.26%
   - Nikah: 18.96%
   - UkuranProgram: 14.58%

   **Tab 3: 🔲 Confusion Matrix**
   - Matriks untuk analisis performa testing
   - Menunjukkan True Positives, False Positives, dll

   **Metrik Performa**:
   - Training Accuracy: 100.00%
   - Testing Accuracy: 100.00%
   - Precision, Recall, F1-Score

### 4. ℹ️ **Halaman Tentang (About)**
   - 🤖 Penjelasan algoritma C4.5
   - 📚 Informasi tentang dataset
   - 👨‍💻 Stack teknologi yang digunakan
   - 🎯 Tutorial cara penggunaan

---

## 🎨 Desain & UX

### Fitur Desain
- ✨ **Gradient Header**: Header dengan gradient biru-ungu yang menarik
- 🎯 **Color-coded Results**: 
  - ✅ Hijau untuk prediksi "Tepat"
  - ⏰ Kuning untuk prediksi "Terlambat"
- 📱 **Responsive Layout**: Beradaptasi dengan berbagai ukuran layar
- 🧭 **Navigasi Sidebar**: Menu navigasi yang jelas dan terstruktur
- 📊 **Metric Cards**: Kartu-kartu informasi yang terorganisir dengan baik

### Emoji Usage
- Setiap halaman memiliki emoji yang konsisten
- Memudahkan pengenalan visual untuk pengguna non-teknis
- Membuat interface lebih friendly dan approachable

---

## 📊 Model & Data

### Dataset
- **Jumlah Records**: 160 mahasiswa
- **Features**: 4 (JenisKelamin, AsalSMA, Nikah, UkuranProgram)
- **Target**: 2 kelas (Tepat, Terlambat)
- **Distribution**: Tepat 68.75%, Terlambat 31.25%
- **Train/Test Split**: 80% / 20%

### Algoritma: Decision Tree C4.5
- **Criterion**: Entropy (Information Gain)
- **Tree Depth**: 4
- **Number of Leaves**: 10
- **Karakteristik**:
  - Mudah diinterpretasi
  - Cocok untuk data categorical
  - Tidak memerlukan normalisasi
  - Robust terhadap outliers

---

## 🛠️ Teknologi

### Backend & ML
```
✓ Python 3.x
✓ Scikit-learn (ML Library)
✓ Pandas (Data Processing)
✓ NumPy (Numerical Computation)
```

### Frontend
```
✓ Streamlit (Web Framework)
✓ Matplotlib (Visualisasi)
✓ Pillow (Image Processing)
```

### Model Files
```
✓ model_c45.pkl - Model terlatih
✓ label_encoders.pkl - Encoder untuk features
✓ target_encoder.pkl - Encoder untuk target
```

### Visualisasi Output
```
✓ decision_tree_visualization.png - Struktur tree
✓ feature_importance.png - Grafik importance
✓ confusion_matrix.png - Matriks confusion
```

---

## 📚 File-File Aplikasi

```
Decition Tree/
├── app.py                              # Aplikasi Streamlit utama
├── model.py                            # Script training model
├── predict.py                          # Module prediksi dengan input interaktif
├── test_predictions.py                 # Test script untuk prediksi
├── generate.py                         # Script generate dataset
├── requirements.txt                    # Dependencies
│
├── kelulusan.csv                       # Dataset (160 records)
├── model_c45.pkl                       # Model terlatih
├── label_encoders.pkl                  # Encoder features
├── target_encoder.pkl                  # Encoder target
│
├── decision_tree_visualization.png     # Visualisasi tree
├── feature_importance.png              # Grafik importance
└── confusion_matrix.png                # Matriks confusion
```

---

## 🎯 Cara Menggunakan Aplikasi

### Untuk Melakukan Prediksi:
1. **Buka aplikasi** dan pilih halaman "🔮 Prediksi"
2. **Isi form input**:
   - Pilih jenis kelamin mahasiswa
   - Pilih asal sekolah menengah
   - Pilih status pernikahan
   - Pilih ukuran program studi
3. **Klik tombol "🚀 Lakukan Prediksi"**
4. **Lihat hasil**:
   - Status kelulusan (Tepat/Terlambat)
   - Tingkat kepercayaan dalam persentase
   - Detail probabilitas untuk setiap kelas

### Untuk Melihat Analisis Model:
1. Buka halaman "📊 Analisis Model"
2. Pilih tab yang diinginkan:
   - **Struktur Tree**: Lihat bagaimana model membuat keputusan
   - **Feature Importance**: Pahami faktor mana yang paling berpengaruh
   - **Confusion Matrix**: Analisis performa model

### Untuk Pelajari Lebih Lanjut:
1. Buka halaman "ℹ️ Tentang"
2. Baca penjelasan tentang algoritma dan dataset
3. Ikuti tutorial penggunaan

---

## 📈 Interpretasi Hasil

### Tingkat Kepercayaan (Confidence)
- **70-100%**: Prediksi sangat yakin
- **60-69%**: Prediksi cukup yakin
- **50-59%**: Prediksi kurang yakin
- **<50%**: Prediksi tidak yakin

### Faktor Terpenting
Berdasarkan feature importance:
1. **Asal SMA** (39.19%): Tipe sekolah menengah sangat mempengaruhi
2. **Jenis Kelamin** (27.26%): Gender memiliki pengaruh signifikan
3. **Status Pernikahan** (18.96%): Status pernikahan cukup mempengaruhi
4. **Ukuran Program** (14.58%): Program reguler vs ekstensi tetap berpengaruh

---

## ❓ FAQ

### Q: Bagaimana cara menambah data training?
A: Edit file `kelulusan.csv` atau jalankan `generate.py` untuk generate data baru, kemudian jalankan `model.py` untuk retrain model.

### Q: Bisakah saya mengubah model?
A: Ya, edit `model.py` untuk mengubah parameter atau algoritma, lalu jalankan ulang untuk melatih model baru.

### Q: Bagaimana cara deploy ke production?
A: Gunakan Streamlit Cloud (streamlit.app) atau deploy ke server dengan Docker untuk production-ready deployment.

### Q: Apakah akurasi 100% bagus?
A: Pada dataset sintetis yang konsisten, 100% menunjukkan model berhasil mempelajari aturan data. Untuk data nyata, akurasi perlu divalidasi ulang dengan data real yang belum pernah dilihat model.

---

## 📞 Support

Jika ada pertanyaan atau masalah dalam menggunakan aplikasi:
1. Pastikan semua dependencies terinstall: `pip install -r requirements.txt`
2. Pastikan file model (.pkl) ada di folder yang sama
3. Restart aplikasi jika ada perubahan
4. Cek log di terminal untuk error messages

---

## 🎓 Aplikasi Prediksi Kelulusan Mahasiswa
**Universitas Teknologi Yogyakarta**  
*Powered by Streamlit & Machine Learning*

---

**Last Updated**: May 2026
