import streamlit as st
import pandas as pd
import io

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Dashboard Penjualan", layout="wide")

# --- Judul Aplikasi ---
st.title("Dashboard Analisis Penjualan 📈")

# --- Path File ---
file_path = 'Copy of finalProj_df - df.csv'

# --- Fungsi untuk memuat data (dengan cache) ---
@st.cache_data
def load_data(path):
    """Fungsi untuk memuat data CSV, menangani error, dan konversi tanggal."""
    try:
        df = pd.read_csv(path)
        # Konversi kolom 'order_date' menjadi format datetime
        # Ini sangat penting untuk analisis data berbasis waktu
        if 'order_date' in df.columns:
            df['order_date'] = pd.to_datetime(df['order_date'])
        return df
    except FileNotFoundError:
        st.error(f"Error: File tidak ditemukan di lokasi '{path}'")
        st.info("Pastikan file 'Copy of finalProj_df - df.csv' berada di folder yang sama dengan file `app.py` ini.")
        return None
    except Exception as e:
        st.error(f"Terjadi error saat memuat data: {e}")
        return None

# --- Muat Data ---
df = load_data(file_path)

# --- Tampilkan Dashboard jika data berhasil dimuat ---
if df is not None:
    
    # --- Filter data untuk analisis (hanya ambil transaksi valid) ---
    # Asumsi: is_valid == 1 berarti transaksi berhasil dan sah
    df_valid = df[df['is_valid'] == 1].copy()

    if df_valid.empty:
        st.warning("Tidak ada data 'valid' (is_valid == 1) untuk dianalisis.")
    else:
        st.success(f"Berhasil memuat dan memfilter **{df_valid.shape[0]} transaksi valid**.")
        
        # --- 1. Tampilkan Metrik Utama (KPI) ---
        st.subheader("Ringkasan Performa Bisnis (KPI)")

        # Hitung KPI
        total_revenue = df_valid['after_discount'].sum()
        total_cogs = df_valid['cogs'].sum()
        total_profit = total_revenue - total_cogs
        total_quantity = df_valid['qty_ordered'].sum()
        total_customers = df_valid['customer_id'].nunique()

        # Tampilkan KPI dalam 4 kolom
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Pemasukan", f"Rp {total_revenue:,.0f}")
        col2.metric("Total Keuntungan", f"Rp {total_profit:,.0f}")
        col3.metric("Quantity Terjual", f"{total_quantity:,}")
        col4.metric("Total Customer", f"{total_customers:,}")
        
        st.divider() # Garis pemisah

        # --- 2. Tampilkan Visualisasi ---
        st.subheader("Visualisasi Data Penjualan")

        viz1, viz2 = st.columns(2)

        with viz1:
            # --- Line Chart: Penjualan per Waktu (Bulan) ---
            st.write("**Pemasukan per Bulan**")
            if 'order_date' in df_valid.columns:
                # Set order_date sebagai index untuk resampling
                df_time = df_valid.set_index('order_date')
                # Resample data per bulan (MS = Month Start) dan jumlahkan 'after_discount'
                sales_over_time = df_time.resample('MS')['after_discount'].sum()
                st.line_chart(sales_over_time)
            else:
                st.warning("Kolom 'order_date' tidak ditemukan untuk membuat line chart.")

        with viz2:
            # --- Bar Chart: Kategori Terjual ---
            st.write("**Pemasukan per Kategori (Top 10)**")
            if 'category' in df_valid.columns:
                # Hitung total pemasukan per kategori
                category_sales = df_valid.groupby('category')['after_discount'].sum().sort_values(ascending=False).head(10)
                st.bar_chart(category_sales)
            else:
                st.warning("Kolom 'category' tidak ditemukan untuk membuat bar chart.")

        st.divider() # Garis pemisah

    # --- 3. Tampilkan Detail Data (Seperti sebelumnya) ---
    st.subheader("Detail Data")
    
    # Opsi untuk menampilkan seluruh data mentah
    if st.checkbox("Tampilkan seluruh data mentah (valid)"):
        st.dataframe(df_valid)
    
    # Tampilkan 5 baris pertama
    st.write("**5 Baris Pertama Data (Asli):**")
    st.dataframe(df.head())
    
    # Tampilkan Info Data
    st.write("**Informasi Kolom Data (Asli):**")
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_string = buffer.getvalue()
    st.text(info_string)

else:
    # Pesan jika data gagal dimuat
    st.error("Data tidak dapat dimuat. Silakan periksa pesan error di atas.")
