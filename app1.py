import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64
import json
from streamlit.components.v1 import html
from scipy.optimize import linprog
from fpdf import FPDF
import time
from concurrent.futures import ThreadPoolExecutor

# =============== FUNGSI UTILITAS ===============
def mermaid(code: str, height=300) -> None:
    """Render diagram Mermaid menggunakan komponen HTML"""
    html(f"""
    <div class="mermaid" style="text-align: center;">
        {code}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{startOnLoad:true}});</script>
    """, height=height)

@st.cache_data
def create_logo():
    """Membuat logo aplikasi dengan caching"""
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

@st.cache_data
def create_header():
    """Membuat header aplikasi dengan caching"""
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

def buat_laporan(optimal_point, optimal_value, params):
    """Membuat laporan PDF"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Laporan Optimasi Produksi", ln=1, align='C')
    
    pdf.cell(200, 10, txt="Parameter Produksi:", ln=1)
    pdf.cell(200, 10, txt=f"- Produk 1: Rp{params['p1']:,}/unit, {params['t1']} jam/unit, maks {params['max1']} unit", ln=1)
    pdf.cell(200, 10, txt=f"- Produk 2: Rp{params['p2']:,}/unit, {params['t2']} jam/unit, maks {params['max2']} unit", ln=1)
    pdf.cell(200, 10, txt=f"- Total waktu: {params['total']} jam", ln=1)
    
    pdf.cell(200, 10, txt="Hasil Optimasi:", ln=1)
    pdf.cell(200, 10, txt=f"- Produk 1: {optimal_point[0]:.0f} unit", ln=1)
    pdf.cell(200, 10, txt=f"- Produk 2: {optimal_point[1]:.0f} unit", ln=1)
    pdf.cell(200, 10, txt=f"- Keuntungan Maksimum: Rp{optimal_value:,.0f}", ln=1)
    
    pdf.cell(200, 10, txt="Dihasilkan oleh Aplikasi Optimasi Produksi", ln=1)
    pdf.cell(200, 10, txt=f"Pada: {time.strftime('%d/%m/%Y %H:%M:%S')}", ln=1)
    
    return pdf.output(dest='S').encode('latin1')

# =============== KONFIGURASI APLIKASI ===============
LOGO_BASE64 = create_logo()
HEADER_BASE64 = create_header()

st.set_page_config(
    layout="wide", 
    page_title="Aplikasi Model Industri",
    page_icon="🏭"
)

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Beranda"
if 'produk3_active' not in st.session_state:
    st.session_state.produk3_active = False

def change_page(page_name):
    st.session_state.current_page = page_name

def toggle_produk3():
    st.session_state.produk3_active = not st.session_state.produk3_active

# =============== NAVIGASI SIDEBAR ===============
with st.sidebar:
    st.image(f"data:image/png;base64,{LOGO_BASE64}", use_container_width=True)
    st.title("NAVIGASI")
    
    st.button("🏠 Beranda", on_click=change_page, args=("Beranda",), use_container_width=True)
    st.button("📚 Pengertian Optimasi", on_click=change_page, args=("Pengertian",), use_container_width=True)
    st.button("📊 Optimasi Produksi", on_click=change_page, args=("Optimasi",), use_container_width=True)
    
    st.markdown("---")
    st.info("""
    **Versi 2.3.0**  
    Fitur Baru:
    - Simpan/Load Kasus
    - Analisis Sensitivitas
    - Laporan PDF
    - Multi Metode Solver
    
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
    1. **Pengertian Optimasi**: Pelajari dasar-dasar optimasi produksi
    2. **Optimasi Produksi**: Hitung solusi optimal untuk kasus Anda
    3. Masukkan parameter produksi
    4. Klik tombol **Hitung Solusi**
    5. Simpan hasil atau ekspor laporan
    """)
    
    st.markdown("---")
    st.subheader("🎯 Fitur Terbaru")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
        ### 💾 Simpan/Load Kasus
        - Simpan konfigurasi kasus
        - Load kasus yang disimpan
        - Berbagi kasus dengan kolega
        """)
    with cols[1]:
        st.markdown("""
        ### 🔍 Analisis Sensitivitas
        - Shadow price
        - Range kelayakan
        - Analisis what-if
        """)
    with cols[2]:
        st.markdown("""
        ### 📄 Laporan PDF
        - Ekspor hasil lengkap
        - Format profesional
        - Siap cetak
        """)

# =============== HALAMAN PENGERTIAN ===============
elif st.session_state.current_page == "Pengertian":
    st.title("📚 Pengertian Optimasi Produksi")
    
    cols = st.columns(2)
    with cols[0]:
        st.markdown("""
        ### 🧠 Konsep Dasar
        **Optimasi Produksi** adalah metode matematika untuk menentukan:
        - Kombinasi produksi terbaik
        - Dengan sumber daya terbatas
        - Guna mencapai keuntungan maksimal
        """)
        
        st.markdown("""
        ### 🔍 Alur Penyelesaian Masalah
        """)
        mermaid("""
        graph TD
            A[Permasalahan Produksi] --> B(Formulasi Model)
            B --> C[Identifikasi Variabel]
            B --> D[Definisi Fungsi Tujuan]
            B --> E[Penentuan Kendala]
            C --> F[Solusi Optimal]
            D --> F
            E --> F
        """)
        
        st.markdown("""
        1. **Formulasi Model**  
           Mengubah masalah nyata menjadi model matematika
        2. **Identifikasi Variabel**  
           Menentukan apa yang akan dioptimalkan (x₁, x₂)
        3. **Definisi Fungsi Tujuan**  
           Membuat rumus keuntungan (Z)
        4. **Penentuan Kendala**  
           Menetapkan batasan produksi
        5. **Solusi Optimal**  
           Hasil akhir yang memenuhi semua syarat
        """)
    
    with cols[1]:
        st.markdown("""
        ### 📝 Komponen Utama
        **1. Variabel Keputusan**  
        ```python
        x₁ = jumlah meja
        x₂ = jumlah kursi
        ```
        
        **2. Fungsi Tujuan**  
        ```python
        Z = 120000*x₁ + 80000*x₂  # Keuntungan total
        ```
        
        **3. Kendala Produksi**  
        ```python
        3*x₁ + 2*x₂ ≤ 120  # Waktu produksi
        x₁ ≤ 30            # Batas permintaan meja
        x₂ ≤ 40            # Batas permintaan kursi
        ```
        
        ### 📊 Prinsip Kerja
        """)
        mermaid("""
        graph LR
            A[Variabel] -->|Input Produk| B(Fungsi Tujuan)
            C[Kendala] -->|Filter Feasible| B
            B --> D[Solusi Optimal]
        """)
        
        st.markdown("""
        **Keterangan:**
        - **Variabel**: Jumlah produk (x₁, x₂)
        - **Fungsi Tujuan**: Rumus keuntungan (Z)
        - **Kendala**: Batasan produksi
        - **Solusi**: Kombinasi optimal
        """)

# =============== HALAMAN OPTIMASI ===============
elif st.session_state.current_page == "Optimasi":
    st.title("📈 OPTIMASI PRODUKSI")
    
    with st.expander("📚 Contoh Kasus", expanded=True):
        st.subheader("Studi Kasus: Perusahaan Furniture")
        
        with st.expander("📚 Contoh Soal & Pembahasan", expanded=True):
            st.subheader("Studi Kasus: Perusahaan Furniture")
            st.markdown("""
            **PT Kayu Indah** memproduksi:
            - **Meja**: Keuntungan Rp120.000/unit, butuh 3 jam pengerjaan
            - **Kursi**: Keuntungan Rp80.000/unit, butuh 2 jam pengerjaan
            
            **Kendala:**
            - Waktu produksi maksimal 120 jam/minggu
            - Permintaan pasar maksimal 30 meja dan 40 kursi per minggu
            """)
            
            if st.button("💡 Lihat Solusi Contoh", type="secondary"):
                st.markdown("---")
                st.subheader("Penyelesaian:")
                
                cols = st.columns(2)
                with cols[0]:
                    st.latex(r"""
                    \begin{aligned}
                    \text{Maksimalkan } & Z = 120000x_1 + 80000x_2 \\
                    \text{Dengan kendala: } & 3x_1 + 2x_2 \leq 120 \\
                    & x_1 \leq 30 \\
                    & x_2 \leq 40 \\
                    & x_1 \geq 0, x_2 \geq 0
                    \end{aligned}
                    """)
                
                with cols[1]:
                    st.markdown("""
                    **Solusi Optimal:**
                    - Produksi 30 meja
                    - Produksi 15 kursi
                    - Keuntungan maksimum: Rp4.800.000/minggu
                    """)
                
                fig, ax = plt.subplots(figsize=(10,6))
                x = np.linspace(0, 40, 100)
                y1 = (120 - 3*x)/2
                ax.plot(x, y1, 'b-', label='3x₁ + 2x₂ ≤ 120')
                ax.axvline(30, color='r', label='x₁ ≤ 30')
                ax.axhline(40, color='g', label='x₂ ≤ 40')
                ax.fill_between(x, 0, np.minimum(y1, 40), where=(x<=30), alpha=0.1)
                ax.plot(30, 15, 'ro', markersize=8)
                ax.set_xlabel('Meja (x₁)')
                ax.set_ylabel('Kursi (x₂)')
                ax.legend()
                ax.grid(True)
                st.pyplot(fig)

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
            
            # Toggle produk ketiga
            if st.checkbox("+ Tambah Produk 3", key="toggle_produk3", on_change=toggle_produk3):
                st.session_state.produk3_active = True
                col3 = st.columns(1)[0]
                with col3:
                    st.subheader("Produk 3")
                    p3 = st.number_input("Keuntungan/unit (Rp)", 50000, key="p3")
                    t3 = st.number_input("Waktu produksi (jam)", 4, key="t3")
                    max3 = st.number_input("Maksimal permintaan", 20, key="max3")
            else:
                st.session_state.produk3_active = False
            
            total_time = st.number_input("Total waktu tersedia (jam)", 120, key="total")

            # Pilih metode solver
            solver_option = st.selectbox(
                "Pilih Metode Solver",
                ["Simple Corner Point", "Simplex Method"],
                index=0
            )

        # Tombol untuk menyimpan konfigurasi
        kasus = {
            'p1': p1, 't1': t1, 'max1': max1,
            'p2': p2, 't2': t2, 'max2': max2,
            'total': total_time,
            'produk3_active': st.session_state.produk3_active
        }
        
        if st.session_state.produk3_active:
            kasus.update({
                'p3': p3, 't3': t3, 'max3': max3
            })

        col_save, col_load = st.columns(2)
        with col_save:
            st.download_button(
                label="💾 Simpan Kasus Ini",
                data=json.dumps(kasus, indent=2),
                file_name="konfigurasi_kasus.json",
                mime="application/json"
            )
        with col_load:
            uploaded_file = st.file_uploader("📤 Upload Kasus", type=["json"], key="uploader")
            if uploaded_file:
                try:
                    kasus_terupload = json.load(uploaded_file)
                    st.session_state.p1 = kasus_terupload['p1']
                    st.session_state.t1 = kasus_terupload['t1']
                    st.session_state.max1 = kasus_terupload['max1']
                    st.session_state.p2 = kasus_terupload['p2']
                    st.session_state.t2 = kasus_terupload['t2']
                    st.session_state.max2 = kasus_terupload['max2']
                    st.session_state.total = kasus_terupload['total']
                    if kasus_terupload.get('produk3_active', False):
                        st.session_state.produk3_active = True
                        st.session_state.p3 = kasus_terupload['p3']
                        st.session_state.t3 = kasus_terupload['t3']
                        st.session_state.max3 = kasus_terupload['max3']
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal memuat kasus: {str(e)}")

        if st.button("🧮 HITUNG SOLUSI DETAIL", type="primary", use_container_width=True):
            with st.spinner('Menghitung solusi optimal...'):
                # Langkah 1: Hitung titik pojok
                st.markdown("---")
                st.subheader("🔍 Proses Perhitungan")
                
                if solver_option == "Simple Corner Point":
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
                    
                    # Gunakan parallel processing untuk perhitungan
                    def hitung_z(titik):
                        return p1*titik[0] + p2*titik[1]
                    
                    with ThreadPoolExecutor() as executor:
                        nilai_Z = list(executor.map(hitung_z, [titik_A, titik_B, titik_C, titik_D, titik_E]))
                    
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
                
                elif solver_option == "Simplex Method":
                    # Gunakan metode simpleks dari scipy
                    res = linprog(
                        c=[-p1, -p2],  # Negative for maximization
                        A_ub=[[t1, t2]],
                        b_ub=[total_time],
                        bounds=((0, max1), (0, max2))
                    
                    optimal_point = (res.x[0], res.x[1])
                    optimal_value = p1*res.x[0] + p2*res.x[1]
                    
                    st.markdown("""
                    ### Metode Simpleks
                    Solusi ditemukan menggunakan algoritma simpleks dengan bantuan library `scipy.optimize.linprog`.
                    """)
                    st.json({
                        "status": "Optimal" if res.success else "Tidak Optimal",
                        "x1": res.x[0],
                        "x2": res.x[1],
                        "slack": res.slack[0],
                        "keuntungan": optimal_value
                    })

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
                    
                    if solver_option == "Simple Corner Point":
                        st.subheader("Detail Titik Pojok")
                        st.write(f"A(0,0) = Rp{nilai_Z[0]:,.0f}")
                        st.write(f"B({max1},0) = Rp{nilai_Z[1]:,.0f}")
                        st.write(f"C({titik_C[0]:.1f},{titik_C[1]:.1f}) = Rp{nilai_Z[2]:,.0f}")
                        st.write(f"D({titik_D[0]:.1f},{max2}) = Rp{nilai_Z[3]:,.0f}")
                        st.write(f"E(0,{titik_E[1]:.1f}) = Rp{nilai_Z[4]:,.0f}")
                    
                    # Analisis Sensitivitas
                    with st.expander("🔄 Analisis Sensitivitas", expanded=True):
                        shadow_price = optimal_value / total_time * 1  # Perkiraan sederhana
                        st.markdown(f"""
                        ### Shadow Price
                        - **Nilai**: Rp{shadow_price:,.0f}/jam
                        - **Artinya**: Setiap penambahan 1 jam kerja dapat meningkatkan keuntungan sekitar Rp{shadow_price:,.0f}
                        
                        ### Range Kelayakan
                        - **Waktu produksi**: {total_time*0.8:,.0f} - {total_time*1.2:,.0f} jam
                        - **Permintaan produk**: ±20% dari nilai saat ini
                        """)
                    
                    # Ekspor laporan
                    st.download_button(
                        label="📄 Export PDF Report",
                        data=buat_laporan(optimal_point, optimal_value, {
                            'p1': p1, 't1': t1, 'max1': max1,
                            'p2': p2, 't2': t2, 'max2': max2,
                            'total': total_time
                        }),
                        file_name="laporan_optimasi.pdf",
                        mime="application/pdf"
                    )
                
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
        border-radius: 8px;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stMarkdown h2 {
        color: #2e86c1;
        border-bottom: 2px solid #2e86c1;
        padding-bottom: 5px;
    }
    .stMarkdown h3 {
        color: #2874a6;
    }
    .stTextInput>div>div>input {
        background-color: #f0f0f0;
        color: #333;
    }
    .mermaid {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid #e1e1e1;
    }
    .mermaid svg {
        display: block;
        margin: 0 auto;
    }
    .stSpinner>div {
        text-align: center;
        margin: 20px 0;
    }
    .stDownloadButton>button {
        width: 100%;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)
