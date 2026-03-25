import streamlit as st
import numpy as np

# Konfigurasi Halaman
st.set_page_config(page_title="Kalkulator Makroekonomi", layout="centered")

st.title("Dashboard Elastisitas PDB & Tenaga Kerja Indonesia 🇮🇩")
st.write("Analisis data historis (1986-2025) untuk mengukur hubungan dua arah antara Pertumbuhan Ekonomi (PDB) dan Serapan Tenaga Kerja.")

st.markdown("---")

# Bagian Penjelasan Metode & Rumus
st.header("Metodologi & Rumus Pendekatan")

st.markdown("""
Analisis ini tidak sekadar menggunakan persentase deskriptif biasa, melainkan menggunakan pendekatan ekonometrika untuk mendapatkan parameter struktural yang stabil.

### 1. Sisi Permintaan (Elastisitas Kesempatan Kerja)
Mengukur berapa banyak lapangan kerja yang tercipta akibat pertumbuhan ekonomi. Kami menggunakan regresi linier OLS model *double-log*:

$$ \ln L = b_0 + b_1 \ln Y $$

* **L** = Jumlah Penduduk Bekerja
* **Y** = Indeks PDB
* **b₁** = Koefisien Elastisitas (Hasil data historis: **0,4065**)

**Kesimpulan:** Setiap pertumbuhan 1% PDB membuka **0,407%** lapangan kerja baru.

### 2. Sisi Penawaran (Fungsi Produksi Cobb-Douglas)
Mengukur seberapa besar kontribusi tenaga kerja terhadap penciptaan PDB itu sendiri. Kami menggunakan Fungsi Produksi Cobb-Douglas yang ditransformasi menjadi model log-linier berganda:

$$ \ln Y = \ln A + \alpha \ln K + \beta \ln L $$

* **K** = Kapital / Pembentukan Modal Tetap Bruto (PMTB)
* **β** = Elastisitas Output Tenaga Kerja (Hasil data historis: **1,7311**)

**Kesimpulan:** Setiap penambahan 1% jumlah pekerja berkontribusi pada pertumbuhan PDB sebesar **1,7311%** (dengan asumsi kapital konstan).
""")

st.markdown("---")

# Konstanta Data (Tahun 2025)
BASE_PEKERJA_2025 = 146540000
ELASTISITAS_L_TO_Y = 1.7311
ELASTISITAS_Y_TO_L = 0.4065

st.header("🧮 Kalkulator Simulasi Kebijakan")

# Kalkulator 1: Target Penciptaan Lapangan Kerja (CAGR)
st.subheader("1. Kalkulator Target Lapangan Kerja (Metode CAGR)")
st.write("Berapa target rata-rata pertumbuhan PDB tahunan yang dibutuhkan untuk mencapai target lapangan kerja dalam periode tertentu?")

col1, col2 = st.columns(2)
with col1:
    target_pekerja = st.number_input("Target Lapangan Kerja Baru (Jiwa):", min_value=100000, value=19000000, step=1000000)
with col2:
    tahun_target = st.number_input("Waktu Pencapaian (Tahun):", min_value=1, value=5, step=1)

if st.button("Hitung Kebutuhan PDB"):
    # Hitung persentase target dari populasi dasar
    persen_target_pekerja = (target_pekerja / BASE_PEKERJA_2025)
    
    # Hitung total PDB yang dibutuhkan
    total_pdb_dibutuhkan = persen_target_pekerja / ELASTISITAS_Y_TO_L
    
    # Hitung CAGR
    # Rumus CAGR: (Nilai Akhir / Nilai Awal)^(1/n) - 1
    # Nilai akhir rasio = 1 + total_pdb_dibutuhkan
    cagr_pdb = ((1 + total_pdb_dibutuhkan) ** (1 / tahun_target)) - 1
    
    st.success(f"Untuk menciptakan **{target_pekerja:,.0f}** lapangan kerja dalam **{tahun_target} tahun**, ekonomi Indonesia harus tumbuh konsisten sebesar **{cagr_pdb * 100:.2f}% per tahun**.")

st.markdown("---")

# Kalkulator 2: Dampak Tenaga Kerja ke Ekonomi
st.subheader("2. Kalkulator Kontribusi Pekerja ke PDB")
st.write("Jika lapangan kerja bertambah sekian jiwa, seberapa besar dorongannya terhadap PDB nasional?")

tambahan_pekerja = st.number_input("Jumlah Pekerja Baru (Jiwa):", min_value=100000, value=407000, step=100000)

if st.button("Hitung Kontribusi PDB"):
    # Hitung persentase kenaikan pekerja
    persen_kenaikan = tambahan_pekerja / BASE_PEKERJA_2025
    
    # Hitung dampak ke PDB menggunakan beta Cobb-Douglas
    dampak_pdb = persen_kenaikan * ELASTISITAS_L_TO_Y
    
    st.info(f"Masuknya **{tambahan_pekerja:,.0f}** pekerja baru (pertumbuhan tenaga kerja **{persen_kenaikan * 100:.3f}%**) akan mendorong pertumbuhan PDB sebesar **{dampak_pdb * 100:.3f}%** (ceteris paribus).")

st.markdown("---")
st.caption("Data Base Tahun 2025: 146.540.000 Pekerja | Dihitung dengan Python Statsmodels")
