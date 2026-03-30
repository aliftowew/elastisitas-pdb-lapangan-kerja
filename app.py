import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import base64

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="Kalkulator Makroekonomi", layout="wide")

# Fungsi untuk format angka ribuan (untuk output)
def format_indo(angka):
    return f"{angka:,.0f}".replace(",", ".")

# ==========================================
# 2. DATASET HISTORIS (1986-2025)
# ==========================================
data_mentah = """Tahun	PDB Growth (%)	Penduduk Bekerja (L)	Nilai PDB (Y) (basis 1986=100)	Pembentukan Modal Tetap Bruto (K)	ln Y	ln L	ln K
1986	5,88	65655030	105,88	26,2	4,6623	17,9999	3,2657
1987	4,93	67878350	111,10	31,42	4,7104	18,0332	3,4474
1988	5,78	69828230	117,52	38,36	4,7666	18,0615	3,6470
1989	7,46	70743560	126,29	47,71	4,8385	18,0745	3,8651
1990	7,24	75850000	135,43	59,76	4,9084	18,1442	4,0903
1991	8,93	76420000	147,52	67,49	4,9939	18,1517	4,2119
1992	6,52	78520000	157,15	72,77	5,0571	18,1788	4,2873
1993	7,96	79200000	169,65	86,67	5,1337	18,1874	4,4621
1994	7,54	82040000	182,44	105,38	5,2064	18,2227	4,6575
1995	8,22	80110000	197,44	129,22	5,2854	18,1989	4,8615
1996	7,82	85702000	212,87	157,65	5,3606	18,2663	5,0603
1997	4,70	87050000	222,88	177,69	5,4066	18,2819	5,1800
1998	-13,13	87672000	193,62	243,04	5,2659	18,2891	5,4932
1999	0,79	88817000	195,15	221,47	5,2737	18,3020	5,4002
2000	4,92	89837700	204,75	275,88	5,3218	18,3135	5,6199
2001	3,64	90807400	212,22	323,88	5,3576	18,3242	5,7803
2002	4,50	91647200	221,76	353,97	5,4016	18,3334	5,8692
2003	4,78	90784900	232,36	392,79	5,4483	18,3240	5,9732
2004	5,03	93722000	244,05	515,38	5,4973	18,3558	6,2449
2005	5,69	94453000	257,95	655,85	5,5527	18,3636	6,4859
2006	5,50	95317000	272,14	805,79	5,6063	18,3727	6,6918
2007	6,35	98757000	289,40	985,63	5,6678	18,4081	6,8932
2008	6,01	102301000	306,81	11370	5,7262	18,4434	7,2225
2009	4,70	104678000	321,23	1740	5,7721	18,4663	7,4616
2010	6,38	107807000	341,72	2130	5,8339	18,4958	7,6638
2011	6,17	110475000	362,80	2450	5,8938	18,5203	7,8038
2012	6,03	111806000	384,68	2820	5,9524	18,5322	7,9444
2013	5,56	110800000	406,06	3050	6,0065	18,5232	8,0228
2014	5,01	114610000	426,39	3440	6,0553	18,5570	8,1432
2015	4,88	114800000	447,18	3780	6,1029	18,5587	8,2374
2016	5,03	118410000	469,69	4040	6,1520	18,5896	8,3039
2017	5,07	121020000	493,50	4370	6,2015	18,6114	8,3825
2018	5,17	124010000	519,04	4790	6,2519	18,6358	8,4742
2019	5,02	126510000	545,09	5120	6,3009	18,6558	8,5409
2020	-2,07	128450000	533,83	4900	6,2800	18,6710	8,4969
2021	3,70	131050000	553,60	5230	6,3164	18,6910	8,5621
2022	5,31	135300000	582,98	5696	6,3681	18,7230	8,6475
2023	5,05	139850000	612,41	6090	6,4174	18,7560	8,7145
2024	5,03	144640000	643,22	6452	6,4664	18,7897	8,7722
2025	5,11	146540000	676,08	6852	6,5163	18,8028	8,8323"""

df = pd.read_csv(io.StringIO(data_mentah), sep='\t', decimal=',')
df['Tahun'] = df['Tahun'].astype(str)

# ==========================================
# 3. HEADER & PENJELASAN METODE
# ==========================================
st.title("Dashboard Elastisitas PDB & Tenaga Kerja Indonesia 🇮🇩")
st.write("Analisis data historis (1986-2025) untuk mengukur hubungan dua arah antara Pertumbuhan Ekonomi (PDB) dan Serapan Tenaga Kerja.")

st.markdown("---")
st.header("Metodologi & Rumus Pendekatan")
st.write("Berbeda dengan analisis persentase sederhana, *dashboard* ini menggunakan ekonometrika **Fungsi Produksi Cobb-Douglas Multivariat** (memperhitungkan peran Kapital/Investasi) untuk mendapatkan parameter struktural efek *murni* yang stabil.")

# Penambahan Box Informasi Definisi Lapangan Kerja
st.info("💡 **Catatan Definisi:** Yang dimaksud dengan tambahan **'Lapangan Kerja'** dalam analisis ini adalah jumlah **agregat (net/bersih) lapangan kerja baru yang terbentuk dibandingkan dengan tahun sebelumnya**, bukan total rekrutmen kotor (*gross hiring*) perusahaan yang sekadar menggantikan pekerja yang pensiun atau *resign*.")

col_teori1, col_teori2 = st.columns(2)

with col_teori1:
    st.subheader("1. Sisi Permintaan (Kebutuhan Pekerja)")
    st.write("Mengukur *efek murni* berapa banyak lapangan kerja yang dibutuhkan untuk menumbuhkan PDB secara spesifik, dengan mengasumsikan faktor mesin/investasi konstan:")
    st.latex(r"\ln L = c_0 + \beta_{inv} \ln Y + \alpha_{inv} \ln K")
    st.markdown("""
    * **L** = Jumlah Penduduk Bekerja
    * **Y** = Indeks PDB
    * **K** = Kapital / Investasi Mesin
    * **β_inv** = Elastisitas PDB terhadap Pekerja (**0,3966**)
    
    **Kesimpulan:** Secara teori, setiap menargetkan pertumbuhan 1% PDB membutuhkan **0,397%** lapangan kerja baru (asumsi *ceteris paribus*).
    """)

with col_teori2:
    st.subheader("2. Sisi Penawaran (Sumbangan ke PDB)")
    st.write("Mengukur *efek murni* kontribusi tenaga kerja terhadap penciptaan PDB. Menggunakan Fungsi Produksi log-linier berganda:")
    st.latex(r"\ln Y = \ln A + \alpha \ln K + \beta \ln L")
    st.markdown("""
    * **L** = Jumlah Penduduk Bekerja
    * **Y** = Indeks PDB
    * **K** = Kapital / Investasi Mesin
    * **β** = Elastisitas Output Tenaga Kerja (**1,7311**)
    
    **Kesimpulan:** Setiap penambahan 1% jumlah pekerja berkontribusi menaikkan PDB sebesar **1,7311%** (asumsi *ceteris paribus*).
    """)

st.markdown("---")

# ==========================================
# 4. TABEL DATA & GRAFIK
# ==========================================
st.header("📊 Data Historis & Visualisasi Regresi")
st.write("Tabel di bawah adalah data historis Indonesia selama 40 tahun terakhir yang menjadi dasar perhitungan ekonometrika di atas.")

st.dataframe(
    df.style.format({
        'Penduduk Bekerja (L)': '{:,.0f}',
        'PDB Growth (%)': '{:.2f}',
        'Nilai PDB (Y) (basis 1986=100)': '{:.2f}',
        'Pembentukan Modal Tetap Bruto (K)': '{:,.0f}'
    }), 
    height=250, 
    use_container_width=True
)

st.write("### Plot Korelasi Data")
st.write("Grafik Sebar (*Scatter Plot*) ini menunjukkan korelasi sangat kuat ($R^2 = 0.987$) antara logaritma PDB dan logaritma Tenaga Kerja historis.")

fig = px.scatter(df, x='ln Y', y='ln L', hover_data=['Tahun'], 
                 trendline="ols", trendline_color_override="red",
                 labels={'ln Y': 'Log Indeks PDB (ln Y)', 'ln L': 'Log Penduduk Bekerja (ln L)'})
fig.update_layout(xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True), margin=dict(l=20, r=20, t=30, b=20))
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.markdown("---")

# ==========================================
# 5. KALKULATOR INTERAKTIF DENGAN GRAFIK
# ==========================================
BASE_PEKERJA_2025 = 146540000
ELASTISITAS_L_TO_Y = 1.7311     # Metode 2: Beta Supply Side Cobb-Douglas
ELASTISITAS_Y_TO_L = 0.3966437  # Metode 3: Beta Demand Side Cobb-Douglas

st.header("🧮 Kalkulator Simulasi Kebijakan")

st.subheader("1. Kalkulator Target Lapangan Kerja (Metode CAGR)")
st.write("Jika suatu negara menargetkan membuka X juta lapangan kerja baru, berapa persen **efek murni** PDB harus ditumbuhkan setiap tahunnya? *(Tanpa bantuan penambahan mesin/investasi)*")

col_calc1, col_calc2 = st.columns(2)
with col_calc1:
    target_pekerja_str = st.text_input("Target Lapangan Kerja Baru (Jiwa):", value="5.000.000")
    try:
        target_pekerja = int(target_pekerja_str.replace('.', ''))
    except ValueError:
        target_pekerja = 5000000 
        st.error("Mohon masukkan angka yang valid.")
with col_calc2:
    tahun_target = st.number_input("Waktu Pencapaian (Tahun):", min_value=1, value=1, step=1)

# Tombol kosmetik
st.button("Hitung Kebutuhan PDB & Buat Grafik Proyeksi")

# Kalkulasi
persen_target_pekerja = (target_pekerja / BASE_PEKERJA_2025)
total_pdb_dibutuhkan = persen_target_pekerja / ELASTISITAS_Y_TO_L
cagr_pdb = ((1 + total_pdb_dibutuhkan) ** (1 / tahun_target)) - 1

st.success(f"📌 Untuk menciptakan **{format_indo(target_pekerja)}** lapangan kerja murni dari pertumbuhan (tanpa disubstitusi investasi baru) dalam **{tahun_target} tahun**, PDB Indonesia harus tumbuh konsisten sebesar **{cagr_pdb * 100:.2f}% per tahun**.")

tahun_list = [f"Tahun {i}" for i in range(tahun_target + 1)]
proyeksi_pdb = [100 * ((1 + cagr_pdb) ** i) for i in range(tahun_target + 1)]

fig_cagr = go.Figure()
fig_cagr.add_trace(go.Scatter(x=tahun_list, y=proyeksi_pdb, mode='lines+markers', name='Proyeksi PDB', line=dict(color='green', width=3)))
fig_cagr.update_layout(title=f"Proyeksi Eksponensial PDB ({cagr_pdb * 100:.2f}% per tahun)", yaxis_title="Indeks PDB (Tahun 0 = 100)", xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
st.plotly_chart(fig_cagr, use_container_width=True, config={'displayModeBar': False})

st.markdown("---")

st.subheader("2. Kalkulator Kontribusi Pekerja ke PDB")
st.write("Jika terserap sekian juta lapangan kerja, seberapa besar **efek murni** dorongannya menaikkan PDB nasional?")

tambahan_pekerja_str = st.text_input("Jumlah Pekerja Baru (Jiwa):", value="5.000.000")
try:
    tambahan_pekerja = int(tambahan_pekerja_str.replace('.', ''))
except ValueError:
    tambahan_pekerja = 5000000

# Tombol kosmetik
st.button("Hitung Kontribusi & Lihat Bar Chart")

# Kalkulasi
persen_kenaikan = tambahan_pekerja / BASE_PEKERJA_2025
dampak_pdb = persen_kenaikan * ELASTISITAS_L_TO_Y

st.info(f"📌 Masuknya **{format_indo(tambahan_pekerja)}** pekerja baru (pertumbuhan tenaga kerja **{persen_kenaikan * 100:.3f}%**) akan memberikan efek murni pada pertumbuhan PDB sebesar **{dampak_pdb * 100:.3f}%** (ceteris paribus).")

fig_bar = go.Figure(data=[
    go.Bar(name='Pertumbuhan Pekerja (%)', x=['Indikator'], y=[persen_kenaikan * 100], marker_color='blue'),
    go.Bar(name='Sumbangan murni ke PDB (%)', x=['Indikator'], y=[dampak_pdb * 100], marker_color='orange')
])
fig_bar.update_layout(barmode='group', title="Efek Multiplier Tenaga Kerja terhadap Output", yaxis_title="Persentase (%)", xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# ==========================================
# 7. INJEKSI CSS UNTUK FOOTER DENGAN BACKGROUND LOKAL
# ==========================================

def get_base64_image(file_name):
    try:
        with open(file_name, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

bg_image_base64 = get_base64_image("image5.png")

st.markdown(
    f"""
    <style>
    .block-container {{
        padding-bottom: 0rem !important;
    }}
    
    .math-footer-bg {{
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        margin-top: 50px;
        background: linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)), url("data:image/png;base64,{bg_image_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: repeat;
        padding: 80px 20px; 
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    
    .tagline-box {{
        background-color: #ffffff;
        padding: 15px 50px;
        border-radius: 30px; 
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.15); 
        text-align: center;
        z-index: 10;
    }}
    
    .footer-text {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #555555;
        margin: 0;
        line-height: 1.4;
        font-size: 14px;
    }}
    
    .tagline-title {{
        font-size: 18px;
        font-weight: 800;
        color: #000000;
    }}
    </style>
    
    <div class="math-footer-bg">
        <div class="tagline-box">
            <p class="footer-text">
                <span class="tagline-title">💡 Semua Bisa Dihitung</span><br>
                by Alif Towew
            </p>
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)
