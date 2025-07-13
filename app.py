import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64

# =============== GENERATE LOGO & HEADER ===============
def create_logo():
    img = Image.new('RGBA', (200, 80), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    for i in range(80):
        draw.line([(0,i), (200,i)], fill=(0, 100+i, 200))
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    draw.text((50, 25), "APLIKASI MODEL MATEMATIKA", fill=(255,255,255), font=font, stroke_width=2, stroke_fill=(0,0,0))
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def create_header():
    img = Image.new('RGB', (1000, 200), (70, 130, 180))
    draw = ImageDraw.Draw(img)
    for i in range(-200, 1000, 30):
        draw.line([(i,0), (i+200,200)], fill=(100,150,200), width=2)
    try:
        font = ImageFont.truetype("arial.ttf", 50)
    except:
        font = ImageFont.load_default()
    draw.text((100, 60), "APLIKASI MODEL MATEMATIKA INDUSTRI", fill=(255,255,0), font=font)
    logo_img = Image.open(BytesIO(base64.b64decode(LOGO_BASE64)))
    logo_img = logo_img.resize((150,60))
    img.paste(logo_img, (800, 20), logo_img)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

LOGO_BASE64 = create_logo()
HEADER_BASE64 = create_header()

# =============== KONFIGURASI ===============
st.set_page_config(layout="wide", page_title="Aplikasi Model Optimasi Produksi", page_icon="📈")

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Pengertian"

def change_page(page_name):
    st.session_state.current_page = page_name

# =============== SIDEBAR ===============
with st.sidebar:
    st.image(f"data:image/png;base64,{LOGO_BASE64}", use_container_width=True)
    st.title("MENU NAVIGASI")
    st.button("📘 Pengertian Model", on_click=change_page, args=("Pengertian",), use_container_width=True)
    st.button("🧮 Optimasi Produksi", on_click=change_page, args=("Optimasi",), use_container_width=True)
    st.button("🔧 Cara Penggunaan", on_click=change_page, args=("Panduan",), use_container_width=True)
    st.markdown("---")
    st.info("""
    **Versi 3.0.0**  
    Dikembangkan oleh:  
    *Megatama Setiaji*  
    🇮🇩 © 2025
    """)

# =============== HALAMAN PENGERTIAN ===============
if st.session_state.current_page == "Pengertian":
    st.title("📘 PENGERTIAN MODEL OPTIMASI PRODUKSI")
    st.image(f"data:image/jpeg;base64,{HEADER_BASE64}", use_container_width=True)
    st.markdown("""
    Model optimasi produksi digunakan untuk menentukan kombinasi terbaik dari produk yang akan diproduksi agar **memaksimalkan keuntungan** atau **meminimalkan biaya** berdasarkan **kendala sumber daya** seperti waktu, bahan baku, atau tenaga kerja.

    ### Rumus Umum:
    Fungsi Objektif:
    $$\text{Maksimalkan } Z = c_1x_1 + c_2x_2 + \dots + c_nx_n$$

    Kendala:
    $$a_{11}x_1 + a_{12}x_2 + \dots + a_{1n}x_n \le b_1$$
    $$a_{21}x_1 + a_{22}x_2 + \dots + a_{2n}x_n \le b_2$$

    dan seterusnya...

    Dengan syarat:
    $$x_i \ge 0$$
    """)

# =============== HALAMAN OPTIMASI ===============
elif st.session_state.current_page == "Optimasi":
    st.title("🧮 OPTIMASI PRODUKSI")

    with st.expander("📚 Contoh Soal", expanded=True):
        st.markdown("""
        **PT Kayu Indah** memproduksi **Meja** dan **Kursi**:
        - Meja: keuntungan Rp120.000/unit, waktu produksi 3 jam
        - Kursi: keuntungan Rp80.000/unit, waktu produksi 2 jam
        - Total waktu tersedia: 120 jam
        - Maksimal permintaan: 30 meja dan 40 kursi per minggu
        """)

    with st.expander("🔧 Input Parameter", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            p1 = st.number_input("Keuntungan Meja (Rp/unit)", 120000)
            t1 = st.number_input("Waktu Meja (jam)", 3)
            m1 = st.number_input("Maksimum Meja", 30)
        with col2:
            p2 = st.number_input("Keuntungan Kursi (Rp/unit)", 80000)
            t2 = st.number_input("Waktu Kursi (jam)", 2)
            m2 = st.number_input("Maksimum Kursi", 40)
        waktu_total = st.number_input("Total Waktu Tersedia (jam)", 120)

    if st.button("🚀 HITUNG OPTIMAL", type="primary"):
        titik = [
            (0,0),
            (m1, 0),
            (0, min(waktu_total/t2, m2)),
            (m1, min((waktu_total - t1*m1)/t2, m2)),
            (min((waktu_total - t2*m2)/t1, m1), m2)
        ]
        nilai = [p1*x + p2*y for x,y in titik]
        idx = np.argmax(nilai)
        optimal = titik[idx]

        st.subheader("📈 Hasil Optimasi")
        st.success(f"Produksi Meja: {optimal[0]:.0f}, Kursi: {optimal[1]:.0f}\nTotal Keuntungan: Rp{nilai[idx]:,.0f}")

        fig, ax = plt.subplots(figsize=(8,6))
        x = np.linspace(0, m1*1.2, 200)
        y = (waktu_total - t1*x) / t2
        ax.plot(x, y, label=f"{t1}x + {t2}y ≤ {waktu_total}", color="blue")
        ax.axvline(m1, label=f"x ≤ {m1}", color="red")
        ax.axhline(m2, label=f"y ≤ {m2}", color="green")
        ax.plot(optimal[0], optimal[1], 'ro', label="Titik Optimal")
        ax.fill_between(x, 0, np.minimum(y, m2), where=(x<=m1), alpha=0.1)
        ax.set_xlabel("Meja (x)")
        ax.set_ylabel("Kursi (y)")
        ax.set_title("Wilayah Solusi Feasible")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

# =============== HALAMAN PANDUAN ===============
elif st.session_state.current_page == "Panduan":
    st.title("📖 CARA PENGGUNAAN APLIKASI")
    st.markdown("""
    ### Langkah-langkah:
    1. Pilih menu "🧮 Optimasi Produksi"
    2. Masukkan parameter seperti keuntungan, waktu kerja, dan batasan
    3. Klik tombol "HITUNG OPTIMAL"
    4. Lihat hasil dan grafik solusi
    5. Gunakan hasil untuk keputusan produksi
    """)

# =============== CUSTOM STYLE ===============
st.markdown("""
<style>
    .stButton>button {
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    .st-emotion-cache-1qg05tj {
        font-family: "Arial", sans-serif;
    }
</style>
""", unsafe_allow_html=True)
