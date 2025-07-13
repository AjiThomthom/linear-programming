import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64
from streamlit.components.v1 import html
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import tempfile

# =============== FUNGSI UTILITAS ===============
def mermaid(code: str, height=300) -> None:
    html(rf"""
    <div class="mermaid" style="text-align: center;">
        {code}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{startOnLoad:true}});</script>
    """, height=height)

@st.cache_data
def create_logo():
    try:
        img = Image.new('RGBA', (200, 80), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        for i in range(80):
            draw.line([(0,i), (200,i)], fill=(0, 100+i, 200))
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
    try:
        img = Image.new('RGB', (1000, 200), (70, 130, 180))
        draw = ImageDraw.Draw(img)
        for i in range(-200, 1000, 30):
            draw.line([(i,0), (i+200,200)], fill=(100,150,200), width=2)
        try:
            font = ImageFont.truetype("arial.ttf", 50)
        except:
            font = ImageFont.load_default()
        draw.text((100, 60), "APLIKASI MODEL LINEAR PROGRAMMING", fill=(255,255,0), font=font)
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
    try:
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        content = []
        
        content.append(Paragraph("Laporan Optimasi Produksi", styles['Title']))
        content.append(Spacer(1, 0.25*inch))
        
        # Parameter Produksi
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
        content.append(Paragraph("Parameter Produksi:", styles['Heading2']))
        content.append(Paragraph(param_text, styles['BodyText']))
        content.append(Spacer(1, 0.25*inch))
        
        # Hasil Optimasi
        result_text = f"""
        <b>Solusi Optimal:</b><br/>
        - Produk 1 (x₁): {optimal_point[0]:.0f} unit<br/>
        - Produk 2 (x₂): {optimal_point[1]:.0f} unit<br/>
        - Keuntungan Maksimum: Rp{optimal_value:,.0f}
        """
        content.append(Paragraph("Hasil Optimasi:", styles['Heading2']))
        content.append(Paragraph(result_text, styles['BodyText']))
        content.append(Spacer(1, 0.25*inch))
        
        # Plot
        if plot_bytes:
            try:
                temp_img = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                temp_img.write(plot_bytes.getvalue())
                temp_img.close()
                img = RLImage(temp_img.name, width=5*inch, height=3*inch)
                content.append(Paragraph("Visualisasi Solusi:", styles['Heading2']))
                content.append(img)
            except Exception as e:
                st.error(f"Error adding plot to PDF: {e}")
        
        doc.build(content)
        return pdf_buffer.getvalue()
    except Exception as e:
        st.error(f"Error generating PDF: {e}")
        return None

# =============== KONFIGURASI APLIKASI ===============
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
    **Versi 2.2.2**  
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
    - **Solusi yang selalu feasible** (tidak melanggar kendala)
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
        - **Solusi**: Kombinasi optimal yang feasible
        """)

# =============== HALAMAN OPTIMASI ===============
elif st.session_state.current_page == "Optimasi":
    st.title("📈 OPTIMASI PRODUKSI")
    
    with st.expander("📚 Contoh Kasus: Bakery Enak", expanded=True):
        st.markdown("""
        **Studi Kasus:**
        - **Kue Coklat (x₁):** Rp50.000/loyang, 2 jam/loyang, maks 20 loyang
        - **Kue Keju (x₂):** Rp70.000/loyang, 3 jam/loyang, maks 15 loyang
        - **Total waktu:** 60 jam/minggu
        
        **Solusi Optimal Manual:**
        - Produksi 15 Kue Coklat + 10 Kue Keju
        - Keuntungan: Rp1.450.000
        """)
        
        if st.button("💡 Gunakan Contoh", type="secondary"):
            st.session_state.p1 = 50000
            st.session_state.t1 = 2
            st.session_state.max1 = 20
            st.session_state.p2 = 70000
            st.session_state.t2 = 3
            st.session_state.max2 = 15
            st.session_state.total = 60

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
            
            # Fungsi untuk mengecek feasibility
            def is_feasible(x1, x2):
                return (t1*x1 + t2*x2 <= total_time + 1e-9 and 
                        x1 <= max1 + 1e-9 and 
                        x2 <= max2 + 1e-9 and
                        x1 >= -1e-9 and x2 >= -1e-9)
            
            # Langkah 1: Hitung titik pojok
            titik_A = (0, 0)
            titik_B = (max1, 0) if is_feasible(max1, 0) else (0, 0)
            titik_C = (max1, min((total_time - t1*max1)/t2, max2)) if t2 != 0 else (0, 0)
            titik_D = (min((total_time - t2*max2)/t1, max1), max2) if t1 != 0 else (0, 0)
            titik_E = (0, min(total_time/t2, max2)) if t2 != 0 else (0, 0)
            
            # Hanya ambil titik yang feasible
            feasible_points = []
            for point in [titik_A, titik_B, titik_C, titik_D, titik_E]:
                if is_feasible(point[0], point[1]):
                    feasible_points.append(point)
            
            if not feasible_points:
                st.error("Tidak ada solusi feasible dengan parameter saat ini!")
                st.stop()
            
            # Hitung nilai Z untuk setiap titik feasible
            nilai_Z = [p1*p[0] + p2*p[1] for p in feasible_points]
            optimal_idx = np.argmax(nilai_Z)
            optimal_point = feasible_points[optimal_idx]
            optimal_value = nilai_Z[optimal_idx]
            
            # Tampilkan proses perhitungan
            with st.expander("🔍 Proses Perhitungan", expanded=True):
                cols = st.columns(2)
                with cols[0]:
                    st.markdown("""
                    **Titik Pojok yang Feasible:**
                    """)
                    for i, point in enumerate(feasible_points):
                        st.write(f"Poin {chr(65+i)}: ({point[0]:.1f}, {point[1]:.1f}) = Rp{p1*point[0] + p2*point[1]:,.0f}")
                
                with cols[1]:
                    st.markdown(f"""
                    **Solusi Optimal:**
                    - **Produk 1 (x₁):** {optimal_point[0]:.0f} unit
                    - **Produk 2 (x₂):** {optimal_point[1]:.0f} unit
                    - **Keuntungan:** Rp{optimal_value:,.0f}
                    """)
            
            # Visualisasi Grafik
            st.markdown("---")
            st.header("📊 Visualisasi Solusi")
            
            fig, ax = plt.subplots(figsize=(10,6))
            x = np.linspace(0, max(1, max1*1.2), 100)
            y = np.where(t2 != 0, (total_time - t1*x)/t2, np.zeros_like(x))
            ax.plot(x, y, 'b-', linewidth=2, label=f'{t1}x₁ + {t2}x₂ ≤ {total_time}')
            
            # Area feasible
            y_feasible = np.minimum(y, max2)
            ax.fill_between(x, 0, y_feasible, where=(x <= max1), color='lightblue', alpha=0.3)
            
            # Garis kendala
            if max1 > 0:
                ax.axvline(max1, color='r', linestyle='--', label=f'x₁ ≤ {max1}')
            if max2 > 0:
                ax.axhline(max2, color='g', linestyle='--', label=f'x₂ ≤ {max2}')
            
            # Titik optimal
            ax.plot(optimal_point[0], optimal_point[1], 'ro', markersize=10, label='Solusi Optimal')
            ax.annotate(f'Optimal\n({optimal_point[0]:.0f}, {optimal_point[1]:.0f})', 
                        xy=optimal_point, 
                        xytext=(optimal_point[0]+1, optimal_point[1]+1),
                        arrowprops=dict(facecolor='black', arrowstyle='->'))
            
            ax.set_xlabel('Produk 1 (x₁)')
            ax.set_ylabel('Produk 2 (x₂)')
            ax.legend()
            ax.grid(True)
            
            plot_buffer = BytesIO()
            plt.savefig(plot_buffer, format='png', bbox_inches='tight', dpi=300)
            plt.close()
            st.pyplot(fig)
            
            # Generate PDF
            st.markdown("---")
            st.subheader("📤 Ekspor Hasil")
            
            parameters = {
                'p1': p1,
                'p2': p2,
                't1': t1,
                't2': t2,
                'max1': max1,
                'max2': max2,
                'total_time': total_time
            }
            
            pdf_bytes = create_pdf_report(optimal_point, optimal_value, parameters, plot_buffer)
            
            if pdf_bytes:
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name="optimasi_produksi.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

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
    .mermaid {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid #e1e1e1;
    }
    .stDownloadButton>button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)
