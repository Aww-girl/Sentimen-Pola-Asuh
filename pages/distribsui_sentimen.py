# File: 1_Distribusi_Sentimen.py (dalam folder pages)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Statistik Distribusi Sentimen")

src = st.sidebar.radio("Pilih Sumber Data:", ("Lokal", "Unggah"))
file_obj = None; path = None
if src == "Lokal":
    path = "polasuh1output.csv"
else:
    file_obj = st.sidebar.file_uploader("Unggah CSV", type="csv")

@st.cache_data
def load_data(source_type, local_file_path=None, uploaded_file_obj=None):
    try:
        if source_type == "Lokal":
            return pd.read_csv(local_file_path)
        elif source_type == "Unggah" and uploaded_file_obj:
            return pd.read_csv(uploaded_file_obj)
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
    return None

df = load_data(src, path, file_obj)

if df is None or 'sentimen_lexicon' not in df:
    st.warning("Data tidak valid atau kolom 'sentimen_lexicon' tidak ditemukan.")
    st.stop()

st.subheader("Jumlah Tweet per Sentimen")
sentimen_counts = df['sentimen_lexicon'].value_counts()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tweet", len(df))
col2.metric("Positif", sentimen_counts.get("positif", 0))
col3.metric("Negatif", sentimen_counts.get("negatif", 0))
col4.metric("Netral", sentimen_counts.get("netral", 0))

st.subheader("Distribusi Sentimen (Pie Chart)")
fig, ax = plt.subplots()
ax.pie(sentimen_counts, labels=sentimen_counts.index, autopct="%1.1f%%", startangle=90)
ax.axis("equal")
st.pyplot(fig)