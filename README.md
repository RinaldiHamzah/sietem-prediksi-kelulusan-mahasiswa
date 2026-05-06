# Sistem Prediksi Kelulusan Mahasiswa

Aplikasi web berbasis Streamlit untuk memprediksi status kelulusan mahasiswa menggunakan model Decision Tree C4.5. Project ini dibuat menggunkan model machine learning end-to-end: mulai dari pembuatan dataset, training model, evaluasi, visualisasi, hingga deployment aplikasi interaktif.

## Demo Singkat

Pengguna mengisi data mahasiswa melalui form, lalu aplikasi menampilkan:
[![Demo Aplikasi - Klik untuk menonton](demo/thumbnail.png)](https://drive.google.com/file/d/1fbE7ap9EmVNPDDgVLK6-n4-IXbfsXR2F/view?usp=sharing)

- status prediksi kelulusan: `Tepat` atau `Terlambat`
- confidence score
- probabilitas setiap kelas
- ringkasan input
- analisis model dan preview dataset

## Tech Stack

- Python
- Streamlit
- Pandas
- Scikit-learn
- Matplotlib
- Pillow

## Fitur Utama

- Prediksi status kelulusan mahasiswa secara real-time.
- Dashboard metrik model: accuracy, precision, dan F1-score.
- Visualisasi decision tree, feature importance, dan confusion matrix.
- Preview dan download dataset training.
- Struktur project rapi untuk portfolio dan deployment.

## Struktur Project

```text
.
├── app.py                         # Entry point aplikasi Streamlit
├── model.py                       # Script training dan evaluasi model
├── generate.py                    # Script generate dataset demo
├── predict.py                     # Script prediksi via terminal
├── test_predictions.py            # Contoh pengujian prediksi
├── requirements.txt               # Dependency Python untuk deployment
├── RUN_APLIKASI.bat               # Launcher lokal untuk Windows
├── README.md                      # Dokumentasi 
├── .gitignore
├── .streamlit/
│   └── config.toml                # Konfigurasi tema Streamlit
├── assets/
│   ├── confusion_matrix.png
│   ├── decision_tree_visualization.png
│   └── feature_importance.png
├── data/
│   └── kelulusan.csv
├── docs/
│   ├── PANDUAN_APLIKASI.md
│   └── README.html
└── models/
    ├── label_encoders.pkl
    ├── model_c45.pkl
    └── target_encoder.pkl
```

## Dataset

Dataset demo berada di `data/kelulusan.csv` dan memiliki 4 fitur kategorikal:

| Fitur | Nilai |
| --- | --- |
| JenisKelamin | Laki-laki, Perempuan |
| AsalSMA | SMA, SMK |
| Nikah | Belum, Sudah |
| UkuranProgram | Reguler, Ekstensi |

Target:

| Target | Keterangan |
| --- | --- |
| Tepat | Mahasiswa diprediksi lulus tepat waktu |
| Terlambat | Mahasiswa diprediksi lulus terlambat |

## Performa Model

Model yang digunakan adalah `DecisionTreeClassifier` dengan criterion `entropy`, sebagai pendekatan C4.5 berbasis information gain.

| Metrik | Nilai |
| --- | ---: |
| Training Accuracy | 100% |
| Testing Accuracy | 100% |
| Precision | 100% |
| F1-Score | 100% |

## Menjalankan Project Secara Lokal

1. Clone repository.

```bash
git clone <url-repository>
cd <nama-folder-project>
```

2. Install dependency.

```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi.

```bash
streamlit run app.py
```

4. Buka aplikasi di browser.

```text
http://localhost:8501
```

Untuk pengguna Windows, aplikasi juga bisa dijalankan dengan membuka:

```text
RUN_APLIKASI.bat
```

## Training Ulang Model

Training ulang model dan visualisasi:

```bash
python model.py
```

File hasil training akan tersimpan di:

- `models/model_c45.pkl`
- `models/label_encoders.pkl`
- `models/target_encoder.pkl`
- `assets/decision_tree_visualization.png`
- `assets/feature_importance.png`
- `assets/confusion_matrix.png`


## Pengujian

Jalankan pengecekan sintaks:

```bash
python -m py_compile app.py model.py generate.py predict.py test_predictions.py
```

Jalankan contoh prediksi:

```bash
python test_predictions.py
```

## Portfolio Highlights

Project ini menunjukkan kemampuan:

- membangun aplikasi machine learning end-to-end
- melakukan preprocessing data kategorikal
- menyimpan dan memuat model dengan pickle
- membuat dashboard interaktif dengan Streamlit
- menampilkan visualisasi evaluasi model
- menyiapkan struktur project untuk deployment

## Author

Project machine learning untuk prediksi kelulusan mahasiswa.
