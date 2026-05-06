from itertools import product
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATASET_PATH = DATA_DIR / "kelulusan.csv"

jenis_kelamin = ["Laki-laki", "Perempuan"]
asal_sma = ["SMA", "SMK"]
nikah = ["Belum", "Sudah"]
ukuran_program = ["Reguler", "Ekstensi"]


def tentukan_kelulusan(jk, asal, status_nikah, program):
    skor = 0

    if asal == "SMA":
        skor += 1
    if program == "Reguler":
        skor += 1
    if status_nikah == "Belum":
        skor += 1
    if jk == "Perempuan":
        skor += 1

    return "Tepat" if skor >= 2 else "Terlambat"


def generate_dataset():
    kombinasi = list(product(jenis_kelamin, asal_sma, nikah, ukuran_program))
    data = []

    for _ in range(10):
        for jk, asal, status_nikah, program in kombinasi:
            data.append(
                {
                    "JenisKelamin": jk,
                    "AsalSMA": asal,
                    "Nikah": status_nikah,
                    "UkuranProgram": program,
                    "Kelulusan": tentukan_kelulusan(jk, asal, status_nikah, program),
                }
            )

    df = pd.DataFrame(data)
    return df.sample(frac=1, random_state=42).reset_index(drop=True)


if __name__ == "__main__":
    DATA_DIR.mkdir(exist_ok=True)
    dataset = generate_dataset()
    dataset.to_csv(DATASET_PATH, index=False)

    print("[OK] Dataset berhasil dibuat dengan aturan label yang konsisten")
    print(f"[OK] Total baris: {len(dataset)}")
    print("\nSample 5 baris pertama:")
    print(dataset.head())
    print("\nDistribusi Kelulusan:")
    print(dataset["Kelulusan"].value_counts())
