import streamlit as st
import pandas as pd
import numpy as np


# ===== Konfigurasi Halaman =====
st.set_page_config(
    page_title="Katalog Paket Internet",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CSS untuk Tema Gelap + Kartu =====
st.markdown("""
    <style>
        .stApp {
            background-color: #1e1e1e;
            color: #f0f0f0;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3 {
            color: #ffffff;
        }
        .sidebar .sidebar-content {
            background-color: #2c2c2c;
        }
        .card {
            background-color: #2c2c2c;
            border-radius: 12px;
            padding: 16px;
            margin: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            color: #ffffff;
        }
        .card-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 4px;
        }
        .card-subtitle {
            font-size: 16px;
            margin-bottom: 8px;
            color: #bbbbbb;
        }
        .card-info {
            font-size: 14px;
            margin-bottom: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# ===== Sidebar =====
st.sidebar.title("🌐 Menu Navigasi")
menu = st.sidebar.radio("Pilih Halaman", ["🏠 Beranda", "🛒 Katalog Paket", "📈 Analisis & Kalkulator", "ℹ️ Tentang"])

# ===== Data Paket Internet =====
data_paket = {
    "Provider": ["Icon net", "Indihome", "Biznet", "Icon net", "Indihome", "Biznet"],
    "Nama Paket": ["Basic", "Speedy", "Pro", "Ultra", "Max", "Super"],
    "Kecepatan (Mbps)": [10, 20, 30, 50, 75, 100],
    "Harga (Rp/bulan)": [180000, 250000, 320000, 450000, 600000, 750000]
}
df = pd.DataFrame(data_paket)

# ===== Halaman Beranda =====
if menu == "🏠 Beranda":
    st.title("Hitung Harga kebutuhan internet anda")
    st.write("Selamat datang! .")

# ===== Halaman Katalog Paket Internet =====
elif menu == "🛒 Katalog Paket":
    st.title("🛒 Katalog Paket Internet")

    # Filter Provider dan Kecepatan
    col1, col2 = st.columns(2)
    with col1:
        kecepatan_min = st.slider("🔧 Kecepatan Minimum (Mbps)", 1, 100, 10)
    with col2:
        provider_filter = st.multiselect("🏢 Pilih Provider", df["Provider"].unique().tolist(), default=df["Provider"].unique().tolist())

    # Filter data
    filtered = df[(df["Kecepatan (Mbps)"] >= kecepatan_min) & (df["Provider"].isin(provider_filter))]

    if filtered.empty:
        st.warning("⚠️ Tidak ada paket dengan filter yang dipilih.")
    else:
        # Tampilkan dalam bentuk katalog
        for i in range(0, len(filtered), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(filtered):
                    row = filtered.iloc[i + j]
                    with cols[j]:
                        harga_formatted = f"{row['Harga (Rp/bulan)']:,}".replace(",", ".")
                        st.markdown(f"""
                            <div class="card">
                                <div class="card-title">{row['Nama Paket']} 📶</div>
                                <div class="card-subtitle">{row['Provider']}</div>
                                <div class="card-info">💨 Kecepatan: {row['Kecepatan (Mbps)']} Mbps</div>
                                <div class="card-info">💰 Harga: Rp {harga_formatted}</div>
                            </div>
                        """, unsafe_allow_html=True)


# ===== Halaman Tentang =====
elif menu == "ℹ️ Tentang":
    st.title("ℹ️ Tentang Aplikasi")
    st.markdown("""
    Aplikasi ini menampilkan paket internet dalam bentuk katalog seperti e-commerce.  
   
    **Dibuat oleh:**
    - IRFAN MAULANA (312210346)  
    - LUTVI ALVIANSYAH (312210365)  
    - BAGOES BALYAN IZZUL FURQON  (312210415)  

    Dibangun menggunakan **Python + Streamlit**.
    """)

# ===== Halaman Analisis & Kalkulator =====
elif menu == "📈 Analisis & Kalkulator":
    st.title("📈 Analisis dan Kalkulator Internet")

    # === 1. Kalkulator Total Biaya ===
    st.subheader("📏 Kalkulator Total Biaya Langganan")
    nama_paket = st.selectbox("Pilih Paket:", df["Nama Paket"])
    durasi = st.number_input("Durasi (bulan):", min_value=1, max_value=36, value=6)

    harga = df[df["Nama Paket"] == nama_paket]["Harga (Rp/bulan)"].values[0]
    total = harga * durasi

    st.success(f"Total biaya untuk {durasi} bulan: **Rp {total:,}**".replace(",", "."))

    # === 2. Statistik Harga per Mbps dan Visualisasi ===
    st.subheader("📊 Statistik & Grafik Harga vs Kecepatan")

    df["Harga per Mbps"] = df["Harga (Rp/bulan)"] / df["Kecepatan (Mbps)"]
    avg_harga_per_mbps = np.mean(df["Harga per Mbps"])

    st.info(f"💡 Rata-rata harga per Mbps: **Rp {avg_harga_per_mbps:,.0f}**".replace(",", "."))

    fig, ax = plt.subplots(figsize=(8, 5))
    scatter = ax.scatter(
        df["Kecepatan (Mbps)"],
        df["Harga (Rp/bulan)"],
        c=df["Harga per Mbps"],
        cmap="viridis",
        s=100,
        edgecolors="white"
    )
    for i, row in df.iterrows():
        ax.annotate(row["Nama Paket"], (row["Kecepatan (Mbps)"], row["Harga (Rp/bulan)"] + 10000), color="white")

    ax.set_facecolor("#2c2c2c")
    fig.patch.set_facecolor('#2c2c2c')
    ax.set_title("Harga vs Kecepatan Paket Internet", color="white")
    ax.set_xlabel("Kecepatan (Mbps)", color="white")
    ax.set_ylabel("Harga (Rp/bulan)", color="white")
    ax.tick_params(colors='white')

    cbar = fig.colorbar(scatter)
    cbar.set_label("Harga per Mbps", color="white")
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    st.pyplot(fig)

# ===== Footer =====
st.markdown("<hr style='border:1px solid gray;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:12px;'>© 2025 Aplikasi Paket Internet </p>", unsafe_allow_html=True)
