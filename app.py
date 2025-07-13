import streamlit as st  # Framework utama untuk membangun web app interaktif
import numpy as np  # Komputasi numerik & operasi matematika (untuk perhitungan optimasi)
import matplotlib.pyplot as plt  # Visualisasi data (grafik solusi optimal)
from io import BytesIO  # Menangani data biner (konversi gambar/PDF ke byte)
from PIL import Image, ImageDraw, ImageFont  # Manipulasi gambar (buat logo/header)
import base64  # Encode/decode gambar ke teks (untuk tampilkan di HTML)
from streamlit.components.v1 import html  # Embed HTML custom di Streamlit
from reportlab.pdfgen import canvas  # Generate PDF level rendah
from reportlab.lib.pagesizes import letter  # Ukuran halaman standar PDF
from reportlab.lib import colors  # Warna untuk PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage  # Generate PDF level tinggi
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # Style teks PDF
from reportlab.lib.units import inch  # Konversi satuan inci untuk layout PDF
import tempfile  # Membuat file sementara (untuk penyimpanan plot sementara)

# =============== FUNGSI UTILITAS ===============
def mermaid(code: str, height=300) -> None:
    """Render diagram Mermaid menggunakan komponen HTML"""
    html(rf"""
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
        draw.text((50, 25), "LINEAR PROGRAMMING", fill=(255,255,255), font=font, stroke_width=2, stroke_fill=(0,0,0))
        
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
        draw.text((100, 60), "APLIKASI MODEL LINEAR PROGRAMMING", fill=(255,255,0), font=font)
        
        # Add logo (jika logo berhasil dibuat)
        if LOGO_BASE64:
            try:
                logo_img = Image.open(BytesIO(base64.b64decode(LOGO_BASE64)))
                logo_img = logo_img.resize((150,60))
                img.paste(logo_img, (800, 20), logo_img)
            except:
                pass
        
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        st.error(f"Error creating header: {e}")
        return ""

@st.cache_data
def create_pdf_report(optimal_point, optimal_value, parameters, plot_bytes):
    """Membuat laporan PDF dari hasil optimasi"""
    try:
        # Buat file PDF sementara
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading2']
        body_style = styles['BodyText']
        
        # Konten PDF
        content = []
        
        # Judul
        content.append(Paragraph("Laporan Optimasi Produksi", title_style))
        content.append(Spacer(1, 0.25*inch))
        
        # Informasi Parameter
        content.append(Paragraph("Parameter Produksi:", heading_style))
        param_text = f"""
        <b>Produk 1:</b><br/>
        - Keuntungan/unit: Rp{parameters['p1']:,}<br/>
        - Waktu produksi: {parameters['t1']} jam<br/>
        - Maksimal permintaan: {parameters['max1']} unit<br/><br/>
        
        <b>Produk 2:</b><br/>
        - Keuntungan/unit: Rp{parameters['p2']:,}<br/>
        - Waktu produksi: {parameters['t2']} jam<br/>
        - Maksimal permintaan: {parameters['max2']} unit<br/><br/>
        
        <b>Total waktu tersedia:</b> {parameters['total_time']} jam
        """
        content.append(Paragraph(param_text, body_style))
        content.append(Spacer(1, 0.25*inch))
        
        # Hasil Optimasi
        content.append(Paragraph("Hasil Optimasi:", heading_style))
        result_text = f"""
        <b>Solusi Optimal:</b><br/>
        - Produk 1 (x₁): {optimal_point[0]:.0f} unit<br/>
        - Produk 2 (x₂): {optimal_point[1]:.0f} unit<br/>
        - Keuntungan Maksimum: Rp{optimal_value:,.0f}
        """
        content.append(Paragraph(result_text, body_style))
        content.append(Spacer(1, 0.25*inch))
        
        # Tambahkan plot ke PDF
        if plot_bytes:
            try:
                temp_img = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                temp_img.write(plot_bytes.getvalue())
                temp_img.close()
                
                img = RLImage(temp_img.name, width=5*inch, height=3*inch)
                content.append(Paragraph("Visualisasi Solusi:", heading_style))
                content.append(img)
            except Exception as e:
                st.error(f"Error adding plot to PDF: {e}")
        
        # Build PDF
        doc.build(content)
        
        return pdf_buffer.getvalue()
    except Exception as e:
        st.error(f"Error generating PDF: {e}")
        return None

# =============== KONFIGURASI APLIKASI ===============
# Pindahkan inisialisasi LOGO_BASE64 dan HEADER_BASE64 setelah definisi fungsi
try:
    LOGO_BASE64 = create_logo()
    HEADER_BASE64 = create_header()
except:
    LOGO_BASE64 = ""
    HEADER_BASE64 = ""

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
    st.button("📚 Pengertian Optimasi", on_click=change_page, args=("Pengertian",), use_container_width=True)
    st.button("📊 Optimasi Produksi", on_click=change_page, args=("Optimasi",), use_container_width=True)
    
    st.markdown("---")
    st.info("""
    **Versi 2.2.1**  
    Dikembangkan oleh:  
    *Megatama Setiaji*  
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
    5. **Export PDF**: Unduh hasil perhitungan dalam format PDF
    """)
    
    st.markdown("---")
    st.subheader("🎯 Fitur Utama")
    st.markdown("""
    - Analisis produksi optimal dengan **Linear Programming**
    - Visualisasi grafik interaktif
    - Contoh kasus siap pakai
    - Penjelasan langkah demi langkah
    - **Ekspor hasil ke PDF**
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
                p1 = st.number_input("Keuntungan/unit (Rp)", min_value=0, key="p1")
                t1 = st.number_input("Waktu produksi (jam)", min_value=0, key="t1")
                max1 = st.number_input("Maksimal permintaan", min_value=0, key="max1")
            with col2:
                st.subheader("Produk 2")
                p2 = st.number_input("Keuntungan/unit (Rp)", min_value=0, key="p2")
                t2 = st.number_input("Waktu produksi (jam)", min_value=0, key="t2")
                max2 = st.number_input("Maksimal permintaan", min_value=0, key="max2")
            
            total_time = st.number_input("Total waktu tersedia (jam)", min_value=0, key="total")

        if st.button("🧮 HITUNG SOLUSI DETAIL", type="primary", use_container_width=True):
            with st.spinner('Menghitung solusi optimal...'):
                # Validasi input
                if p1 == 0 and p2 == 0:
                    st.error("Keuntungan produk tidak boleh 0 semua")
                    st.stop()
                if t1 == 0 and t2 == 0:
                    st.error("Waktu produksi tidak boleh 0 semua")
                    st.stop()
                if total_time == 0:
                    st.error("Total waktu tersedia tidak boleh 0")
                    st.stop()
                
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
                    x = np.linspace(0, max1*1.2 if max1 > 0 else 40, 100)
                    y = (total_time - t1*x)/t2 if t2 != 0 else np.zeros_like(x)
                    ax.plot(x, y, 'b-', linewidth=2, label=f'{t1}x₁ + {t2}x₂ ≤ {total_time}')
                    ax.fill_between(x, 0, np.minimum(y, max2 if max2 > 0 else np.inf), where=(x<=max1 if max1 > 0 else True), color='lightblue', alpha=0.3)
                    
                    # Plot constraints
                    if max1 > 0:
                        ax.axvline(max1, color='red', linestyle='--', label=f'x₁ ≤ {max1}')
                    if max2 > 0:
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
                    
                    # Simpan plot ke buffer untuk PDF
                    plot_buffer = BytesIO()
                    plt.savefig(plot_buffer, format='png', bbox_inches='tight', dpi=300)
                    plt.close()
                    st.pyplot(fig)
                    
                    st.markdown("""
                    **Keterangan Grafik:**
                    - **Area biru**: Kombinasi produksi yang memungkinkan
                    - **Titik merah**: Solusi optimal
                    - **Garis putus-putus**: Batas permintaan pasar
                    """)

                # Buat dan tampilkan tombol download PDF
                st.markdown("---")
                st.subheader("📤 Ekspor Hasil")
                
                # Siapkan data untuk PDF
                parameters = {
                    'p1': p1,
                    'p2': p2,
                    't1': t1,
                    't2': t2,
                    'max1': max1,
                    'max2': max2,
                    'total_time': total_time
                }
                
                # Generate PDF
                pdf_bytes = create_pdf_report(optimal_point, optimal_value, parameters, plot_buffer)
                
                if pdf_bytes:
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_bytes,
                        file_name="optimasi_produksi.pdf",
                        mime="application/pdf",
                        help="Klik untuk mengunduh laporan lengkap dalam format PDF",
                        use_container_width=True
                    )
                    st.success("PDF siap diunduh! Klik tombol di atas untuk mengunduh laporan lengkap.")

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
    .stDownloadButton>button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)
