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
        draw.text((50, 25), "OPTIMASI PRODUKSI", fill=(255,255,255), font=font, stroke_width=2, stroke_fill=(0,0,0))
        
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
        draw.text((100, 60), "APLIKASI OPTIMASI PRODUKSI", fill=(255,255,0), font=font)
        
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
    page_title="Optimasi Produksi",
    page_icon="📊"
)

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Beranda"

def change_page(page_name):
    st.session_state.current_page = page_name

# =============== NAVIGASI SIDEBAR ===============
with st.sidebar:
    st.image(f"data:image/png;base64,{LOGO_BASE64}", use_container_width=True)
    st.title("MENU NAVIGASI")
    
    st.button("🏠 Beranda", on_click=change_page, args=("Beranda",), use_container_width=True)
    st.button("📊 Optimasi", on_click=change_page, args=("Optimasi",), use_container_width=True)
    
    st.markdown("---")
    
    with st.expander("📚 Teori Optimasi", expanded=False):
        st.markdown("""
        **Apa itu Optimasi Produksi?**
        Metode untuk menentukan alokasi sumber daya terbatas (waktu, bahan) guna memaksimalkan keuntungan.
        
        **Komponen Penting:**
        - Variabel keputusan (x₁, x₂)
        - Fungsi tujuan (Z)
        - Kendala produksi
        """)
    
    with st.expander("🧮 Rumus Dasar", expanded=False):
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
        st.markdown("""
        - **Z**: Keuntungan total
        - **c₁, c₂**: Keuntungan per unit
        - **a₁, a₂**: Waktu produksi
        - **b**: Total waktu tersedia
        """)
    
    st.markdown("---")
    st.info("""
    **Panduan Cepat:**
    1. Isi parameter produksi
    2. Klik tombol hitung
    3. Analisis grafik solusi
    """)

# =============== HALAMAN BERANDA ===============
if st.session_state.current_page == "Beranda":
    st.title("Optimasi Produksi dengan Linear Programming")
    st.image(f"data:image/jpeg;base64,{HEADER_BASE64}", use_container_width=True)
    
    st.markdown("""
    ## Selamat Datang di Aplikasi Optimasi Produksi!
    Aplikasi ini membantu Anda menentukan kombinasi produksi optimal dengan metode **Linear Programming**.
    """)
    
    cols = st.columns(2)
    with cols[0]:
        st.subheader("📋 Cara Menggunakan")
        st.markdown("""
        1. Masuk ke halaman **📊 Optimasi**
        2. Input parameter produksi:
           - Keuntungan per unit
           - Waktu produksi
           - Batas permintaan
        3. Klik **Hitung Solusi**
        4. Lihat hasil di grafik dan tabel
        """)
    
    with cols[1]:
        st.subheader("🎯 Contoh Kasus")
        st.markdown("""
        **Perusahaan Meubel:**
        - Produk: Meja (Rp120k) dan Kursi (Rp80k)
        - Waktu produksi: 3 jam dan 2 jam
        - Total waktu: 120 jam/minggu
        - Permintaan maks: 30 meja, 40 kursi
        """)
        st.image("https://via.placeholder.com/400x200?text=Contoh+Grafik+Optimasi", use_container_width=True)
    
    st.markdown("---")
    st.subheader("📊 Prinsip Dasar Optimasi")
    st.markdown("""
    ```mermaid
    graph LR
    A[Variabel Keputusan] --> B(Fungsi Tujuan)
    C[Kendala Produksi] --> B
    B --> D[Solusi Optimal]
    ```
    """)

# =============== HALAMAN OPTIMASI ===============
elif st.session_state.current_page == "Optimasi":
    st.title("📊 OPTIMASI PRODUKSI")
    st.image(f"data:image/jpeg;base64,{HEADER_BASE64}", use_container_width=True)
    
    with st.expander("📚 Contoh Kasus & Pembahasan", expanded=True):
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
                st.subheader("Penyelesaian Matematis")
                st.latex(r"""
                \begin{aligned}
                \text{Maks } Z &= 120x_1 + 80x_2 \\
                \text{s.t. } &3x_1 + 2x_2 \leq 120 \\
                &x_1 \leq 30 \\
                &x_2 \leq 40 \\
                &x_1, x_2 \geq 0
                \end{aligned}
                """)
            
            with cols[1]:
                st.subheader("Solusi Optimal")
                st.markdown("""
                - **Produksi Meja:** 30 unit
                - **Produksi Kursi:** 15 unit
                - **Keuntungan Maks:** Rp4.800.000
                """)
                
                # Contoh grafik
                fig, ax = plt.subplots(figsize=(8,5))
                x = np.linspace(0, 50, 100)
                y = (120 - 3*x)/2
                ax.plot(x, y, 'b-', label='3x₁ + 2x₂ ≤ 120')
                ax.fill_between(x, 0, np.minimum(y, 40), where=(x<=30), alpha=0.2)
                ax.plot(30, 15, 'ro', markersize=8)
                ax.set_xlabel('Meja (x₁)')
                ax.set_ylabel('Kursi (x₂)')
                ax.legend()
                st.pyplot(fig)
    
    with st.expander("🔧 PARAMETER PRODUKSI", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Produk 1")
            p1 = st.number_input("Keuntungan per unit (Rp)", value=120000, key="p1")
            t1 = st.number_input("Waktu produksi (jam)", value=3, key="t1")
            max1 = st.number_input("Maksimal permintaan", value=30, key="max1")
        
        with col2:
            st.subheader("Produk 2")
            p2 = st.number_input("Keuntungan per unit (Rp)", value=80000, key="p2")
            t2 = st.number_input("Waktu produksi (jam)", value=2, key="t2")
            max2 = st.number_input("Maksimal permintaan", value=40, key="max2")
        
        total_time = st.number_input("Total waktu tersedia (jam)", value=120, key="total")

    if st.button("🧮 HITUNG SOLUSI OPTIMAL", type="primary", use_container_width=True):
        # Hitung titik pojok
        titik_A = (0, 0)
        titik_B = (max1, 0)
        titik_C = (max1, min((total_time - t1*max1)/t2, max2))
        titik_D = (min((total_time - t2*max2)/t1, max1), max2)
        titik_E = (0, min(total_time/t2, max2))
        
        # Hitung keuntungan di setiap titik
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

        st.markdown("---")
        st.header("📝 HASIL PERHITUNGAN")
        
        # Tampilkan hasil
        cols = st.columns(2)
        with cols[0]:
            st.subheader("Solusi Optimal")
            st.markdown(f"""
            - **Produk 1 (x₁):** {optimal_point[0]:.0f} unit
            - **Produk 2 (x₂):** {optimal_point[1]:.0f} unit
            - **Keuntungan Maksimum:** Rp{optimal_value:,.0f}
            """)
            
            st.subheader("Titik Pojok")
            st.write(f"A(0,0) = Rp{nilai_Z[0]:,.0f}")
            st.write(f"B({max1},0) = Rp{nilai_Z[1]:,.0f}")
            st.write(f"C({titik_C[0]:.0f},{titik_C[1]:.0f}) = Rp{nilai_Z[2]:,.0f}")
            st.write(f"D({titik_D[0]:.0f},{max2}) = Rp{nilai_Z[3]:,.0f}")
            st.write(f"E(0,{titik_E[1]:.0f}) = Rp{nilai_Z[4]:,.0f}")
        
        with cols[1]:
            st.subheader("Visualisasi Grafik")
            fig, ax = plt.subplots(figsize=(10,6))
            
            # Plot feasible region
            x = np.linspace(0, max1*1.2, 100)
            y = (total_time - t1*x)/t2
            ax.plot(x, y, 'b-', linewidth=2, label=f'{t1}x₁ + {t2}x₂ ≤ {total_time}')
            ax.fill_between(x, 0, np.minimum(y, max2), where=(x<=max1), color='lightblue', alpha=0.3, label='Area Feasible')
            
            # Plot constraints
            ax.axvline(max1, color='red', linestyle='--', label=f'x₁ ≤ {max1}')
            ax.axhline(max2, color='green', linestyle='--', label=f'x₂ ≤ {max2}')
            
            # Highlight optimal point
            ax.plot(optimal_point[0], optimal_point[1], 'ro', markersize=10, label='Solusi Optimal')
            ax.annotate(f'Optimal\n({optimal_point[0]:.0f}, {optimal_point[1]:.0f})', 
                        xy=optimal_point, 
                        xytext=(optimal_point[0]+5, optimal_point[1]+5),
                        arrowprops=dict(facecolor='black', arrowstyle='->'))
            
            # Customize plot
            ax.set_xlabel('Produk 1 (x₁)', fontsize=12)
            ax.set_ylabel('Produk 2 (x₂)', fontsize=12)
            ax.set_title('Grafik Solusi Optimasi', fontsize=14)
            ax.legend(loc='upper right')
            ax.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            st.pyplot(fig)
        
        # Penjelasan grafik
        st.markdown("""
        ### 🔍 Cara Membaca Grafik:
        1. **Area Biru Muda**: Kombinasi produksi yang memungkinkan
        2. **Titik Merah**: Solusi optimal dengan keuntungan tertinggi
        3. **Garis Putus-Putus**: Batas permintaan pasar
        4. **Sumbu X**: Jumlah Produk 1
        5. **Sumbu Y**: Jumlah Produk 2
        """)

# =============== STYLE CUSTOM ===============
st.markdown("""
<style>
    .stButton>button {
        transition: all 0.3s;
        border: 1px solid #4CAF50;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .st-emotion-cache-1qg05tj {
        font-family: "Arial", sans-serif;
    }
    .stMarkdown h1 {
        color: #2e86c1;
    }
</style>
""", unsafe_allow_html=True)
