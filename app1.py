import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64

# =============== GENERATE LOGO & HEADER ===============
def create_logo():
    try:
        img = Image.new('RGBA', (200, 80), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        
        # Background gradient
        for i in range(80):
            draw.line([(0,i), (200,i)], fill=(0, 100+i, 200))
        
        # Text
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        draw.text((50, 25), "APLIKASI MODEL MATEMATIKA", fill=(255,255,255), font=font, stroke_width=2, stroke_fill=(0,0,0))
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        st.error(f"Error creating logo: {e}")
        return ""

def create_header():
    try:
        img = Image.new('RGB', (1000, 200), (70, 130, 180))
        draw = ImageDraw.Draw(img)
        
        # Diagonal pattern
        for i in range(-200, 1000, 30):
            draw.line([(i,0), (i+200,200)], fill=(100,150,200), width=2)
        
        # Main title
        try:
            font = ImageFont.truetype("arial.ttf", 50)
        except:
            font = ImageFont.load_default()
        draw.text((100, 60), "APLIKASI MODEL MATEMATIKA INDUSTRI", fill=(255,255,0), font=font)
        
        # Add logo
        logo_img = Image.open(BytesIO(base64.b64decode(LOGO_BASE64)))
        logo_img = logo_img.resize((150,60))
        img.paste(logo_img, (800, 20), logo_img)
        
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        st.error(f"Error creating header: {e}")
        return ""

LOGO_BASE64 = create_logo()
HEADER_BASE64 = create_header()

# =============== KONFIGURASI APLIKASI ===============
st.set_page_config(
    layout="wide", 
    page_title="Aplikasi Model Industri",
    page_icon="🏭"
)

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Beranda"

def change_page(page_name):
    st.session_state.current_page = page_name

# =============== NAVIGASI SIDEBAR ===============
with st.sidebar:
    st.image(f"data:image/png;base64,{LOGO_BASE64}", use_container_width=True)
    st.title("NAVIGASI")
    
    st.button("🏠 Beranda", on_click=change_page, args=("Beranda",), use_container_width=True)
    st.button("📊 Optimasi", on_click=change_page, args=("Optimasi",), use_container_width=True)
    
    with st.expander("📚 Pengertian Optimasi", expanded=False):
        st.markdown("""
        **Optimasi Produksi** adalah metode untuk menentukan alokasi sumber daya terbatas (waktu, bahan) guna memaksimalkan keuntungan.
        
        **Prinsip Dasar:**
        ```mermaid
        graph LR
        A[Variabel Keputusan] --> B(Fungsi Tujuan)
        C[Kendala Produksi] --> B
        B --> D[Solusi Optimal]
        ```
        
        **Rumus Dasar:**
        """)
        st.latex(r"""
        \text{Maksimalkan } Z = c_1x_1 + c_2x_2
        """)
        st.latex(r"""
        \begin{cases}
        a_1x_1 + a_2x_2 \leq b \\
        x_1 \leq d_1 \\
        x_2 \leq d_2 \\
        x_1, x_2 \geq 0
        \end{cases}
        """)
    
    st.markdown("---")
    st.info("""
    **Versi 2.2.1**  
    Dikembangkan oleh:  
    *Megatama Setiaji & Ronnan Ghazi*  
    🇮🇩 🇵🇸  
    © 2025
    """)

# =============== HALAMAN BERANDA ===============
if st.session_state.current_page == "Beranda":
    st.title("Selamat Datang di Aplikasi Optimasi Produksi")
    st.image(f"data:image/jpeg;base64,{HEADER_BASE64}", use_container_width=True)
    
    st.markdown("""
    ## 📋 Panduan Penggunaan
    1. Pilih menu **📊 Optimasi** di sidebar
    2. Masukkan parameter produksi:
       - Keuntungan per unit
       - Waktu produksi
       - Batas permintaan
    3. Klik tombol **Hitung Solusi**
    4. Analisis hasil di grafik dan tabel
    """)
    
    st.markdown("---")
    st.subheader("🎯 Rangkuman Optimasi Produksi")
    st.markdown("""
    - Digunakan untuk **maksimalkan keuntungan** atau **minimalkan biaya**
    - Menggunakan pendekatan **Linear Programming**
    - Solusi optimal diperoleh dengan **mengevaluasi titik pojok**
    - Hasil ditampilkan dalam **grafik interaktif**
    """)

# =============== HALAMAN OPTIMASI ===============
elif st.session_state.current_page == "Optimasi":
    st.title("📈 OPTIMASI PRODUKSI")
    
    with st.expander("📚 Contoh Soal & Pembahasan", expanded=True):
        st.subheader("Studi Kasus: Perusahaan Furniture")
        st.markdown("""
        | Produk | Keuntungan | Waktu Produksi | Maks Permintaan |
        |--------|------------|----------------|------------------|
        | Meja   | Rp120.000  | 3 jam          | 30 unit          |
        | Kursi  | Rp80.000   | 2 jam          | 40 unit          |
        **Total waktu tersedia:** 120 jam/minggu
        """)
        
        if st.button("💡 Lihat Solusi Contoh", type="secondary"):
            st.markdown("---")
            cols = st.columns(2)
            with cols[0]:
                st.subheader("Formulasi Matematis")
                st.latex(r"""
                \begin{aligned}
                \text{Maks } Z &= 120000x_1 + 80000x_2 \\
                \text{s.t. } &3x_1 + 2x_2 \leq 120 \\
                &x_1 \leq 30 \\
                &x_2 \leq 40 \\
                &x_1, x_2 \geq 0
                \end{aligned}
                """)
            
            with cols[1]:
                st.subheader("Langkah Penyelesaian")
                st.markdown("""
                1. Identifikasi titik pojok feasible region
                2. Hitung nilai Z di setiap titik
                3. Pilih titik dengan Z terbesar
                """)
                st.write("**Solusi Optimal:**")
                st.write("- Produksi Meja: 30 unit")
                st.write("- Produksi Kursi: 15 unit")
                st.write("- Keuntungan: Rp4.800.000")

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
        # Langkah 1: Hitung titik pojok
        st.markdown("---")
        st.subheader("🔍 Proses Perhitungan")
        
        with st.expander("Langkah 1: Identifikasi Titik Pojok", expanded=True):
            cols = st.columns(2)
            with cols[0]:
                st.markdown("""
                **Titik A (Origin):**
                """)
                st.latex(r"x_1 = 0, x_2 = 0")
                
                st.markdown("""
                **Titik B (Maks Produk 1):**
                """)
                st.latex(fr"x_1 = {max1}, x_2 = 0")
                
                st.markdown("""
                **Titik C (Interseksi Kendala):**
                """)
                st.latex(fr"{t1}x_1 + {t2}x_2 = {total_time}")
                st.latex(fr"x_1 = {max1}")
                st.latex(fr"x_2 = \frac{{{total_time} - {t1} \times {max1}}}{{{t2}}} = {(total_time - t1*max1)/t2:.1f}")
            
            with cols[1]:
                st.markdown("""
                **Titik D (Interseksi Kendala):**
                """)
                st.latex(fr"{t1}x_1 + {t2}x_2 = {total_time}")
                st.latex(fr"x_2 = {max2}")
                st.latex(fr"x_1 = \frac{{{total_time} - {t2} \times {max2}}}{{{t1}}} = {(total_time - t2*max2)/t1:.1f}")
                
                st.markdown("""
                **Titik E (Maks Produk 2):**
                """)
                st.latex(fr"x_1 = 0, x_2 = \min\left(\frac{{{total_time}}}{{{t2}}}, {max2}\right) = {min(total_time/t2, max2):.1f}")

        # Langkah 2: Hitung nilai Z
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
        
        with st.expander("Langkah 2: Hitung Nilai Fungsi Tujuan", expanded=True):
            cols = st.columns(2)
            with cols[0]:
                st.latex(fr"""
                \begin{{aligned}}
                Z_A &= {p1} \times 0 + {p2} \times 0 = \text{{Rp}}0 \\
                Z_B &= {p1} \times {max1} + {p2} \times 0 = \text{{Rp}}{p1*max1:,} \\
                Z_C &= {p1} \times {titik_C[0]:.1f} + {p2} \times {titik_C[1]:.1f} = \text{{Rp}}{nilai_Z[2]:,.0f}
                \end{{aligned}}
                """)
            with cols[1]:
                st.latex(fr"""
                \begin{{aligned}}
                Z_D &= {p1} \times {titik_D[0]:.1f} + {p2} \times {max2} = \text{{Rp}}{nilai_Z[3]:,.0f} \\
                Z_E &= {p1} \times 0 + {p2} \times {titik_E[1]:.1f} = \text{{Rp}}{nilai_Z[4]:,.0f}
                \end{{aligned}}
                """)

        # Langkah 3: Tentukan solusi optimal
        optimal_idx = np.argmax(nilai_Z)
        optimal_point = [titik_A, titik_B, titik_C, titik_D, titik_E][optimal_idx]
        optimal_value = nilai_Z[optimal_idx]
        
        with st.expander("Langkah 3: Tentukan Solusi Optimal", expanded=True):
            st.markdown(f"""
            **Titik Optimal**: Pekerjaan {['A','B','C','D','E'][optimal_idx]}  
            **Alasan**: Memberikan nilai Z tertinggi (Rp{optimal_value:,.0f})
            """)

        # Tampilkan hasil akhir
        st.markdown("---")
        st.header("📝 HASIL PERHITUNGAN")
        
        cols = st.columns(2)
        with cols[0]:
            st.subheader("Solusi Optimal")
            st.markdown(f"""
            - **Produk 1 (x₁):** {optimal_point[0]:.0f} unit
            - **Produk 2 (x₂):** {optimal_point[1]:.0f} unit
            - **Keuntungan Maksimum:** Rp{optimal_value:,.0f}
            """)
            
            st.subheader("Detail Titik Pojok")
            st.write(f"A(0,0) = Rp{nilai_Z[0]:,.0f}")
            st.write(f"B({max1},0) = Rp{nilai_Z[1]:,.0f}")
            st.write(f"C({titik_C[0]:.1f},{titik_C[1]:.1f}) = Rp{nilai_Z[2]:,.0f}")
            st.write(f"D({titik_D[0]:.1f},{max2}) = Rp{nilai_Z[3]:,.0f}")
            st.write(f"E(0,{titik_E[1]:.1f}) = Rp{nilai_Z[4]:,.0f}")
        
        with cols[1]:
            st.subheader("Visualisasi Grafik")
            fig, ax = plt.subplots(figsize=(10,6))
            
            # Plot feasible region
            x = np.linspace(0, max1*1.2, 100)
            y = (total_time - t1*x)/t2
            ax.plot(x, y, 'b-', linewidth=2, label=f'{t1}x₁ + {t2}x₂ ≤ {total_time}')
            ax.fill_between(x, 0, np.minimum(y, max2), where=(x<=max1), color='lightblue', alpha=0.3)
            
            # Plot constraints
            ax.axvline(max1, color='red', linestyle='--', label=f'x₁ ≤ {max1}')
            ax.axhline(max2, color='green', linestyle='--', label=f'x₂ ≤ {max2}')
            
            # Plot optimal point
            ax.plot(optimal_point[0], optimal_point[1], 'ro', markersize=10, label='Solusi Optimal')
            ax.annotate(f'Optimal\n({optimal_point[0]:.0f}, {optimal_point[1]:.0f})', 
                        xy=optimal_point, 
                        xytext=(optimal_point[0]+5, optimal_point[1]+5),
                        arrowprops=dict(facecolor='black', arrowstyle='->'))
            
            ax.set_xlabel('Produk 1 (x₁)', fontsize=12)
            ax.set_ylabel('Produk 2 (x₂)', fontsize=12)
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.6)
            st.pyplot(fig)
            
            st.markdown("""
            **Keterangan Grafik:**
            - **Area biru**: Kombinasi produksi yang memungkinkan
            - **Titik merah**: Solusi optimal
            - **Garis putus-putus**: Batas permintaan pasar
            """)

# =============== STYLE CUSTOM ===============
st.markdown("""
<style>
    .stButton>button {
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .st-emotion-cache-1qg05tj {
        font-family: "Arial", sans-serif;
    }
    .stMarkdown h3 {
        color: #2e86c1;
    }
</style>
""", unsafe_allow_html=True)
