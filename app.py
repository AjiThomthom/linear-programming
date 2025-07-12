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
st.set_page_config(layout="wide", page_title="Aplikasi Model Industri", page_icon="🏭")

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Beranda"

def change_page(page_name):
    st.session_state.current_page = page_name

# =============== SIDEBAR ===============
with st.sidebar:
    st.image(f"data:image/png;base64,{LOGO_BASE64}", use_container_width=True)
    st.title("NAVIGASI")
    col1, col2 = st.columns(2)
    with col1:
        st.button("🏠 Beranda", on_click=change_page, args=("Beranda",), use_container_width=True)
        st.button("📊 Optimasi", on_click=change_page, args=("Optimasi",), use_container_width=True)
    st.markdown("---")
    st.info("""
    **Versi 2.2.1**  
    Dikembangkan oleh:  
    *Megatama Setiaji & Ronnan Ghazi*  
    🇮🇩 🇵🇸  
    © 2025
    """)

# =============== BERANDA ===============
if st.session_state.current_page == "Beranda":
    st.title("Selamat Datang di Aplikasi Model Matematika Industri")
    st.image(f"data:image/jpeg;base64,{HEADER_BASE64}", use_container_width=True)
    st.markdown("---")
    st.subheader("📚 Panduan Cepat")
    st.write("""
    1. Pilih menu di sidebar untuk mengakses fitur
    2. Masukkan parameter sesuai kasus Anda
    3. Klik tombol hitung untuk melihat hasil
    """)

# =============== OPTIMASI ===============
elif st.session_state.current_page == "Optimasi":
    st.title("📈 OPTIMASI PRODUKSI")

    with st.expander("🔧 PARAMETER PRODUKSI", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Produk 1")
            p1 = st.number_input("Keuntungan/unit (Rp)", 120000, key="p1")
            t1 = st.number_input("Waktu produksi (jam)", 3, key="t1")
            max1 = st.number_input("Maksimal permintaan", 30, key="max1")
        with col2:
            st.subheader("Produk 2")
            p2 = st.number_input("Keuntungan/unit (Rp)", 80000, key="p2")
            t2 = st.number_input("Waktu produksi (jam)", 2, key="t2")
            max2 = st.number_input("Maksimal permintaan", 40, key="max2")

        total_time = st.number_input("Total waktu tersedia (jam)", 120, key="total")

    if st.button("🧮 HITUNG SOLUSI DETAIL", type="primary", use_container_width=True):
        titik_A = (0, 0)
        titik_B = (max1, 0)
        titik_C = (max1, min((total_time - t1*max1)/t2, max2))
        titik_D = (min((total_time - t2*max2)/t1, max1), max2)
        titik_E = (0, min(total_time/t2, max2))
        nilai_Z = [
            p1*titik_A[0] + p2*titik_A[1],
            p1*titik_B[0] + p2*titik_B[1],
            p1*titik_C[0] + p2*titik_C[1],
            p1*titik_D[0] + p2*titik_D[1],
            p1*titik_E[0] + p2*titik_E[1]
        ]
        optimal_idx = np.argmax(nilai_Z)
        optimal_point = [titik_A, titik_B, titik_C, titik_D, titik_E][optimal_idx]
        optimal_value = nilai_Z[optimal_idx]

        st.header("📝 HASIL PERHITUNGAN")
        st.subheader("Fungsi Tujuan")
        st.latex(fr"Z = {p1}x_1 + {p2}x_2")
        st.subheader("Solusi Optimal")
        st.success(f"Produk 1: {optimal_point[0]:.0f} unit, Produk 2: {optimal_point[1]:.0f} unit\n\nKeuntungan Maksimum: Rp{optimal_value:,.0f}")

        fig, ax = plt.subplots(figsize=(8,6))
        x = np.linspace(0, max1*1.1, 100)
        y = (total_time - t1*x)/t2
        ax.plot(x, y, 'b-', label=f'{t1}x₁ + {t2}x₂ ≤ {total_time}')
        ax.fill_between(x, 0, np.minimum(y, max2), where=(x<=max1), alpha=0.1)
        ax.axvline(max1, color='r', label=f'x₁ ≤ {max1}')
        ax.axhline(max2, color='g', label=f'x₂ ≤ {max2}')
        ax.plot(optimal_point[0], optimal_point[1], 'ro', markersize=8)
        ax.set_xlabel('Produk 1 (x₁)')
        ax.set_ylabel('Produk 2 (x₂)')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

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
