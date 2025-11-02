import streamlit as st
import pandas as pd
import io

# --- Konfigurasi Halaman (Opsional tapi bagus) ---
# Mengatur judul tab browser dan layout halaman
st.set_page_config(page_title="Dashboard Data Penjualan", layout="wide")

# --- Judul Aplikasi ---
st.title("Dashboard Analisis Data CSV 📊")
st.write("Aplikasi ini memuat dan menganalisis file `Copy of finalProj_df - df.csv`.")

# --- Path File ---
file_path = 'Copy of finalProj_df - df.csv'

# --- Fungsi untuk memuat data (dengan cache) ---
# @st.cache_data digunakan agar Streamlit tidak perlu memuat ulang data
# setiap kali ada interaksi, sehingga lebih cepat.
@st.cache_data
def load_data(path):
    """Fungsi untuk memuat data CSV dan menanganani error."""
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        st.error(f"Error: File tidak ditemukan di lokasi '{path}'")
        st.info("Pastikan file CSV Anda berada di folder yang sama dengan file `app.py` ini.")
        return None
    except Exception as e:
        st.error(f"Terjadi error saat memuat data: {e}")
        return None

# --- Muat Data ---
df = load_data(file_path)

# --- Tampilkan Data jika berhasil dimuat ---
# Kode di bawah ini hanya berjalan jika 'df' tidak None (artinya data berhasil dimuat)
if df is not None:
    st.success(f"Berhasil memuat **{df.shape[0]} baris** dan **{df.shape[1]} kolom**.")

    # --- Tampilkan Data Mentah (Opsional) ---
    if st.checkbox("Tampilkan seluruh data mentah (raw data)"):
        st.subheader("Data Mentah")
        # st.dataframe lebih interaktif (bisa di-sort) daripada st.write
        st.dataframe(df) 

    # --- Tampilkan 5 Baris Pertama ---
    st.subheader("5 Baris Pertama Data")
    st.dataframe(df.head())

    # --- Tampilkan Info Dasar & Contoh Visualisasi (dalam kolom) ---
    st.subheader("Ringkasan dan Visualisasi Data")
    
    # Bagi layout jadi 2 kolom
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Informasi Kolom (Tipe Data):**")
        # Menangkap output df.info() agar bisa ditampilkan di Streamlit
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_string = buffer.getvalue()
        st.text(info_string)

    with col2:
        st.write("**Distribusi Kategori Produk:**")
        # Cek apakah kolom 'category' ada di data Anda
        if 'category' in df.columns:
            # Hitung jumlah unik di kolom 'category'
            category_counts = df['category'].value_counts().head(10) # Ambil 10 teratas
            st.bar_chart(category_counts)
        else:
            st.warning("Kolom 'category' tidak ditemukan. Visualisasi ini dilewati.")

else:
    # Pesan jika data gagal dimuat
    st.error("Data tidak dapat dimuat. Silakan periksa pesan error di atas.")
