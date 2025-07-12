# app.py
import streamlit as st
from scipy.optimize import linprog

st.title("🛠️ Aplikasi Optimasi (Model Industri)")

st.sidebar.header("Parameter Optimasi Linear")

# Input koefisien fungsi tujuan
c1 = st.sidebar.number_input("K_1 (target)", value=1.0)
c2 = st.sidebar.number_input("K_2 (target)", value=1.0)

# Input batasan
st.sidebar.subheader("Batasan (≤):")
a11 = st.sidebar.number_input("a11", value=1.0)
a12 = st.sidebar.number_input("a12", value=1.0)
b1 = st.sidebar.number_input("b1", value=10.0)

a21 = st.sidebar.number_input("a21", value=1.0)
a22 = st.sidebar.number_input("a22", value=1.0)
b2 = st.sidebar.number_input("b2", value=15.0)

# Setup optimasi (minimasi digunakan; untuk maksimasi, tinggal ubah tanda koefisien tujuan)
c = [c1, c2]
A = [[a11, a12], [a21, a22]]
b = [b1, b2]

st.write("### Fungsi Tujuan")
st.latex(r"\min\; " + f"{c1} x_1 + {c2} x_2")

st.write("### Kendala")
st.latex(r"\begin{cases}")
st.latex(f"{a11} x_1 + {a12} x_2 \\le {b1} \\")
st.latex(f"{a21} x_1 + {a22} x_2 \\le {b2}")
st.latex(r"\end{cases}")

if st.button("🔍 Hitung Solusi"):
    res = linprog(c, A_ub=A, b_ub=b, method="highs")
    if res.success:
        st.success("💡 Solusi ditemukan!")
        st.write(f"**x₁ = {res.x[0]:.4f}**, **x₂ = {res.x[1]:.4f}**")
        st.write(f"Nilai tujuan: **{res.fun:.4f}**")
    else:
        st.error("❌ Optimasi gagal: " + res.message)
