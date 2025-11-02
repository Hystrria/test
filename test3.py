import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Dashboard Penjualan", layout="wide")

st.title("Dashboard Analisis Penjualan 📈")

file_path = 'Copy of finalProj_df - df.csv'

@st.cache_data
def load_data(path):
    """Fungsi untuk memuat data CSV, menangani error, dan konversi tanggal."""
    try:
        df = pd.read_csv(path)
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

df = load_data(file_path)

if df is not None:
    
    df_valid = df[df['is_valid'] == 1].copy()

    if df_valid.empty:
        st.warning("Tidak ada data 'valid' (is_valid == 1) untuk dianalisis.")
    else:
        st.success(f"Berhasil memuat dan memfilter **{df_valid.shape[0]} transaksi valid**.")
        
        st.subheader("Ringkasan Performa Bisnis (KPI)")

        total_revenue = df_valid['after_discount'].sum()
        total_cogs = df_valid['cogs'].sum()
        total_profit = total_revenue - total_cogs
        total_quantity = df_valid['qty_ordered'].sum()
        total_customers = df_valid['customer_id'].nunique()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Pemasukan", f"Rp {total_revenue:,.0f}")
        col2.metric("Total Keuntungan", f"Rp {total_profit:,.0f}")
        col3.metric("Quantity Terjual", f"{total_quantity:,}")
        col4.metric("Total Customer", f"{total_customers:,}")
        
        st.divider() 

        st.subheader("Visualisasi Data Penjualan")

        viz1, viz2 = st.columns(2)

        with viz1:
            st.write("**Pemasukan per Bulan**")
            if 'order_date' in df_valid.columns:
                df_time = df_valid.set_index('order_date')
                sales_over_time = df_time.resample('MS')['after_discount'].sum()
                st.line_chart(sales_over_time)
            else:
                st.warning("Kolom 'order_date' tidak ditemukan untuk membuat line chart.")

        with viz2:
            st.write("**Pemasukan per Kategori (Top 10)**")
            if 'category' in df_valid.columns:
                category_sales = df_valid.groupby('category')['after_discount'].sum().sort_values(ascending=False).head(10)
                st.bar_chart(category_sales)
            else:
                st.warning("Kolom 'category' tidak ditemukan untuk membuat bar chart.")

        st.divider() 

    st.subheader("Detail Data")
    
    if st.checkbox("Tampilkan seluruh data mentah (valid)"):
        st.dataframe(df_valid)
    
    st.write("**5 Baris Pertama Data:**")
    st.dataframe(df.head())
    
    st.write("**Informasi Kolom Data (Asli):**")
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_string = buffer.getvalue()
    st.text(info_string)

else:
    st.error("Data tidak dapat dimuat. Silakan periksa pesan error di atas.")
