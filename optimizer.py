import numpy as np
from scipy.optimize import linprog
import pandas as pd

def optimize_3_products(p1, p2, p3, t1, t2, t3, max1, max2, max3, total_time):
    """Solver Linear Programming untuk 3 produk"""
    c = [-p1, -p2, -p3]  # Koefisien fungsi tujuan (minimisasi -Z)
    A = [[t1, t2, t3]]    # Koefisien kendala waktu
    b = [total_time]       # Total waktu
    bounds = [
        (0, max1),         # Batas x₁
        (0, max2),         # Batas x₂
        (0, max3)          # Batas x₃
    ]
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds)
    return {
        "optimal_point": res.x,
        "optimal_value": -res.fun,
        "is_feasible": res.success
    }

def generate_report(solution, params):
    """Generate laporan dalam format DataFrame"""
    report = {
        "Parameter": ["Keuntungan/unit", "Waktu Produksi", "Batas Maksimal"],
        "Produk 1": [params["p1"], params["t1"], params["max1"]],
        "Produk 2": [params["p2"], params["t2"], params["max2"]],
        "Produk 3": [params["p3"], params["t3"], params["max3"]],
        "Total Waktu": [params["total_time"], "-", "-"]
    }
    return pd.DataFrame(report)
