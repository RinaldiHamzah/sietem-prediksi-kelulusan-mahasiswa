import os
import pickle
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "model_c45.pkl"
LABEL_ENCODER_PATH = BASE_DIR / "models" / "label_encoders.pkl"
TARGET_ENCODER_PATH = BASE_DIR / "models" / "target_encoder.pkl"
DATASET_PATH = BASE_DIR / "data" / "kelulusan.csv"
ASSETS_DIR = BASE_DIR / "assets"

MODEL_METRICS = {
    "Akurasi Training": "100%",
    "Akurasi Testing": "100%",
    "Precision": "100%",
    "F1-Score": "100%",
}

FEATURE_IMPORTANCE = {
    "Asal SMA": 39.19,
    "Jenis Kelamin": 27.26,
    "Status Pernikahan": 18.96,
    "Ukuran Program": 14.58,
}


st.set_page_config(
    page_title="Prediksi Kelulusan Mahasiswa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        .stApp {
            background: #f6f8fb;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        [data-testid="stSidebar"] {
            background: #102033;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label {
            color: #f8fafc !important;
        }

        .hero {
            background: linear-gradient(135deg, #174ea6 0%, #0f766e 100%);
            border-radius: 8px;
            color: white;
            padding: 28px 30px;
            margin-bottom: 20px;
        }

        .hero h1 {
            color: white;
            font-size: 34px;
            line-height: 1.2;
            margin: 0 0 8px 0;
        }

        .hero p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 16px;
            margin: 0;
        }

        .section-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
            padding: 20px;
            margin-bottom: 16px;
        }

        .section-card h3 {
            color: #172033;
            margin-top: 0;
            margin-bottom: 10px;
        }

        .section-card p,
        .section-card li {
            color: #4b5563;
            font-size: 15px;
            line-height: 1.6;
        }

        .result-success {
            background: #ecfdf3;
            border: 1px solid #86efac;
            border-radius: 8px;
            padding: 22px;
        }

        .result-warning {
            background: #fffbeb;
            border: 1px solid #fcd34d;
            border-radius: 8px;
            padding: 22px;
        }

        .result-title {
            color: #172033;
            font-size: 34px;
            font-weight: 800;
            margin: 0;
        }

        .muted {
            color: #667085;
            font-size: 14px;
        }

        .intro-badge {
            background: #e0f2fe;
            border-radius: 999px;
            color: #075985;
            display: inline-block;
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 14px;
            padding: 6px 10px;
        }

        .feature-list {
            display: grid;
            gap: 10px;
            margin-top: 14px;
        }

        .feature-item {
            align-items: center;
            background: #f8fafc;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            display: flex;
            gap: 12px;
            padding: 12px;
        }

        .feature-icon {
            align-items: center;
            background: #dbeafe;
            border-radius: 8px;
            color: #174ea6;
            display: flex;
            flex: 0 0 34px;
            font-size: 17px;
            font-weight: 800;
            height: 34px;
            justify-content: center;
            width: 34px;
        }

        .feature-text {
            color: #344054;
            font-size: 14px;
            font-weight: 600;
            line-height: 1.4;
        }

        .dataset-stats {
            display: grid;
            gap: 10px;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            margin: 16px 0;
        }

        .dataset-stat {
            background: #f8fafc;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 12px;
        }

        .dataset-label {
            color: #667085;
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .dataset-value {
            color: #172033;
            font-size: 28px;
            font-weight: 800;
            line-height: 1.1;
        }

        .class-row {
            margin-top: 14px;
        }

        .class-head {
            align-items: center;
            display: flex;
            justify-content: space-between;
            margin-bottom: 6px;
        }

        .class-name {
            color: #172033;
            font-size: 14px;
            font-weight: 800;
        }

        .class-count {
            color: #667085;
            font-size: 13px;
            font-weight: 700;
        }

        .class-track {
            background: #eef2f7;
            border-radius: 999px;
            height: 10px;
            overflow: hidden;
        }

        .class-fill {
            border-radius: 999px;
            height: 10px;
        }

        .fill-tepat {
            background: #16a34a;
        }

        .fill-terlambat {
            background: #f59e0b;
        }

        .footer {
            border-top: 1px solid #e5e7eb;
            color: #667085;
            font-size: 13px;
            margin-top: 24px;
            padding-top: 16px;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model_files():
    missing_files = [
        str(path.name)
        for path in [MODEL_PATH, LABEL_ENCODER_PATH, TARGET_ENCODER_PATH]
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(", ".join(missing_files))

    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)
    with open(LABEL_ENCODER_PATH, "rb") as file:
        label_encoders = pickle.load(file)
    with open(TARGET_ENCODER_PATH, "rb") as file:
        target_encoder = pickle.load(file)

    return model, label_encoders, target_encoder


@st.cache_data
def load_dataset():
    if DATASET_PATH.exists():
        return pd.read_csv(DATASET_PATH)
    return pd.DataFrame()


def predict_kelulusan(model, label_encoders, target_encoder, input_data):
    encoded_data = {
        column: label_encoders[column].transform([value])[0]
        for column, value in input_data.items()
    }

    features = pd.DataFrame([encoded_data])
    prediction_encoded = model.predict(features)[0]
    prediction = target_encoder.classes_[prediction_encoded]
    probabilities = model.predict_proba(features)[0]
    probability_map = {
        target_encoder.classes_[index]: probabilities[index] * 100
        for index in range(len(target_encoder.classes_))
    }
    confidence = max(probability_map.values())

    return prediction, confidence, probability_map


def render_header():
    st.markdown(
        """
        <div class="hero">
            <h1>Sistem Prediksi Kelulusan Mahasiswa</h1>
            <p>Dashboard prediksi berbasis Decision Tree C4.5 untuk membantu membaca potensi kelulusan mahasiswa.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metrics():
    cols = st.columns(4)
    for col, (label, value) in zip(cols, MODEL_METRICS.items()):
        col.metric(label, value)


def render_feature_importance():
    for feature, value in FEATURE_IMPORTANCE.items():
        left, right = st.columns([3, 1])
        left.progress(value / 100, text=feature)
        right.write(f"**{value:.2f}%**")


def render_image(path, caption):
    image_path = ASSETS_DIR / path
    if image_path.exists():
        st.image(Image.open(image_path), caption=caption, use_container_width=True)
    else:
        st.warning(f"File {path} belum tersedia. Jalankan `python model.py` untuk membuat visualisasi.")


def render_home(df):
    render_header()

    render_metrics()
    st.write("")

    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.markdown(
            """
            <div class="section-card">
                <div class="intro-badge">Aplikasi Akademik</div>
                <h3>Tentang Aplikasi</h3>
                <p>
                    Aplikasi ini memprediksi status kelulusan mahasiswa menjadi dua kelas:
                    <b>Tepat</b> atau <b>Terlambat</b>. Pengguna cukup memilih empat data profil,
                    lalu sistem menampilkan prediksi, confidence, dan probabilitas kelas secara langsung.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-card">
                <h3>Fitur yang Tersedia</h3>
                <div class="feature-list">
                    <div class="feature-item">
                        <div class="feature-icon">1</div>
                        <div class="feature-text">Prediksi status kelulusan secara langsung dari form mahasiswa.</div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">2</div>
                        <div class="feature-text">Menampilkan confidence dan probabilitas untuk setiap kelas hasil.</div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">3</div>
                        <div class="feature-text">Visualisasi struktur decision tree, feature importance, dan confusion matrix.</div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">4</div>
                        <div class="feature-text">Preview serta download dataset training dari halaman analisis.</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        if df.empty:
            st.markdown(
                """
                <div class="section-card">
                    <h3>Ringkasan Dataset</h3>
                    <p>Dataset belum ditemukan.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            counts = df["Kelulusan"].value_counts()
            total = len(df)
            tepat_count = int(counts.get("Tepat", 0))
            terlambat_count = int(counts.get("Terlambat", 0))
            tepat_percent = tepat_count / total * 100 if total else 0
            terlambat_percent = terlambat_count / total * 100 if total else 0

            st.markdown(
                f"""
                <div class="section-card">
                    <div class="intro-badge">Dataset Training</div>
                    <h3>Ringkasan Dataset</h3>
                    <p>Data training yang digunakan model saat ini terdiri dari fitur kategorikal dan target kelulusan.</p>
                    <div class="dataset-stats">
                        <div class="dataset-stat">
                            <div class="dataset-label">Jumlah Data</div>
                            <div class="dataset-value">{total}</div>
                        </div>
                        <div class="dataset-stat">
                            <div class="dataset-label">Jumlah Fitur</div>
                            <div class="dataset-value">4</div>
                        </div>
                        <div class="dataset-stat">
                            <div class="dataset-label">Target Class</div>
                            <div class="dataset-value">2</div>
                        </div>
                    </div>
                    <h3 style="font-size: 18px; margin-top: 18px;">Distribusi Kelas</h3>
                    <div class="class-row">
                        <div class="class-head">
                            <div class="class-name">Tepat</div>
                            <div class="class-count">{tepat_count} data · {tepat_percent:.2f}%</div>
                        </div>
                        <div class="class-track">
                            <div class="class-fill fill-tepat" style="width: {tepat_percent}%;"></div>
                        </div>
                    </div>
                    <div class="class-row">
                        <div class="class-head">
                            <div class="class-name">Terlambat</div>
                            <div class="class-count">{terlambat_count} data · {terlambat_percent:.2f}%</div>
                        </div>
                        <div class="class-track">
                            <div class="class-fill fill-terlambat" style="width: {terlambat_percent}%;"></div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_prediction(model, label_encoders, target_encoder):
    render_header()
    st.subheader("Prediksi Status Kelulusan")

    form_col, result_col = st.columns([1, 1.1])

    with form_col:
        with st.form("prediction_form"):
            st.markdown("### Data Mahasiswa")
            jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
            asal_sma = st.selectbox("Asal Sekolah Menengah", ["SMA", "SMK"])
            nikah = st.selectbox("Status Pernikahan", ["Belum", "Sudah"])
            ukuran_program = st.selectbox("Ukuran Program Studi", ["Reguler", "Ekstensi"])
            submitted = st.form_submit_button("Lakukan Prediksi", use_container_width=True)

        if submitted:
            input_data = {
                "JenisKelamin": jenis_kelamin,
                "AsalSMA": asal_sma,
                "Nikah": nikah,
                "UkuranProgram": ukuran_program,
            }
            prediction, confidence, probability_map = predict_kelulusan(
                model, label_encoders, target_encoder, input_data
            )
            st.session_state["prediction_result"] = {
                "prediction": prediction,
                "confidence": confidence,
                "probability_map": probability_map,
                "display_input": {
                    "Jenis Kelamin": jenis_kelamin,
                    "Asal SMA": asal_sma,
                    "Status Pernikahan": nikah,
                    "Ukuran Program": ukuran_program,
                },
            }
            st.rerun()

    with result_col:
        with st.container(border=True):
            st.markdown("### Hasil")
            result = st.session_state.get("prediction_result")

            if not result:
                st.info("Isi data mahasiswa lalu klik tombol prediksi. Hasil akan muncul di panel ini.")
                return

            prediction = result["prediction"]
            confidence = result["confidence"]
            result_class = "result-success" if prediction == "Tepat" else "result-warning"
            description = (
                "Mahasiswa diprediksi Lulus tepat waktu"
                if prediction == "Tepat"
                else "Mahasiswa diprediksi terlambat Lulus"
            )

            st.markdown(
                f"""
                <div class="{result_class}">
                    <p class="muted">Status Prediksi</p>
                    <p class="result-title">{prediction}</p>
                    <p>{description}</p>
                    <p><b>Confidence:</b> {confidence:.2f}%</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")
            st.markdown("#### Probabilitas Kelas")
            for class_name, probability in result["probability_map"].items():
                st.write(f"**{class_name}**: {probability:.2f}%")
                st.progress(probability / 100)

            with st.expander("Ringkasan Input"):
                st.dataframe(
                    pd.DataFrame(
                        [
                            {"Atribut": key, "Nilai": value}
                            for key, value in result["display_input"].items()
                        ]
                    ),
                    hide_index=True,
                    use_container_width=True,
                )

            if st.button("Reset Prediksi", use_container_width=True):
                st.session_state.pop("prediction_result", None)
                st.rerun()


def render_analysis(df):
    render_header()
    st.subheader("Analisis Model")
    render_metrics()
    st.write("")

    tab_tree, tab_importance, tab_confusion, tab_dataset = st.tabs(
        ["Struktur Tree", "Feature Importance", "Confusion Matrix", "Dataset"]
    )

    with tab_tree:
        render_image("decision_tree_visualization.png", "Struktur Decision Tree C4.5")

    with tab_importance:
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.markdown("### Nilai Importance")
            render_feature_importance()
        with col2:
            render_image("feature_importance.png", "Grafik Feature Importance")

    with tab_confusion:
        render_image("confusion_matrix.png", "Confusion Matrix Testing Set")

    with tab_dataset:
        if df.empty:
            st.warning("Dataset tidak ditemukan.")
        else:
            st.dataframe(df, hide_index=True, use_container_width=True)
            st.download_button(
                "Download Dataset CSV",
                df.to_csv(index=False).encode("utf-8"),
                "kelulusan.csv",
                "text/csv",
                use_container_width=True,
            )


def render_about():
    render_header()
    st.subheader("Tentang Sistem")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="section-card">
                <h3>Algoritma</h3>
                <p>
                    Decision Tree C4.5 menggunakan entropy dan information gain untuk menentukan
                    pemisahan fitur terbaik. Model ini mudah dijelaskan karena hasilnya berbentuk pohon keputusan.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="section-card">
                <h3>Teknologi</h3>
                <p>
                    Aplikasi dibuat dengan Streamlit, Scikit-learn, Pandas, Matplotlib, dan Pillow.
                    Seluruh file model disimpan sebagai pickle agar aplikasi dapat memuat model dengan cepat.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="section-card">
            <h3>Cara Menggunakan</h3>
            <ol>
                <li>Buka halaman Prediksi.</li>
                <li>Pilih data mahasiswa pada form.</li>
                <li>Klik tombol Lakukan Prediksi.</li>
                <li>Baca hasil, confidence, dan probabilitas kelas.</li>
                <li>Buka Analisis Model untuk melihat visualisasi dan dataset.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    try:
        model, label_encoders, target_encoder = load_model_files()
    except FileNotFoundError as error:
        st.error(f"File model belum lengkap: {error}. Jalankan `python model.py` terlebih dahulu.")
        st.stop()

    df = load_dataset()

    with st.sidebar:
        st.title("Prediksi Kelulusan")
        st.caption("Decision Tree C4.5")
        page = st.radio(
            "Menu",
            ["Beranda", "Prediksi", "Analisis Model", "Tentang"],
        )
        st.divider()
        st.success("Model aktif")
        st.caption(f"Lokasi project: {BASE_DIR}")

    if page == "Beranda":
        render_home(df)
    elif page == "Prediksi":
        render_prediction(model, label_encoders, target_encoder)
    elif page == "Analisis Model":
        render_analysis(df)
    else:
        render_about()

    st.markdown(
        """
        <div class="footer">
            Sistem Prediksi Kelulusan Mahasiswa - Universitas Teknologi Yogyakarta
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
