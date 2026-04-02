import streamlit as st
import pandas as pd
import os
from extractor import process_invoice
from excel_utils import save_to_excel, load_excel, reset_excel

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Invoice Processing System",
    layout="wide",
    page_icon="📄"
)

# -----------------------------
# CUSTOM UI STYLE
# -----------------------------
st.markdown("""
    <style>
        .title {
            font-size: 34px;
            font-weight: 600;
            color: #2c3e50;
        }
        .sub {
            color: #6c757d;
            font-size: 14px;
            margin-bottom: 20px;
        }
        .box {
            padding: 20px;
            border-radius: 10px;
            background: white;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        }
        .stButton>button {
            background-color: #2c3e50;
            color: white;
            border-radius: 6px;
            padding: 8px 16px;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="title">Invoice Processing System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Upload invoice and extract structured data into Excel</div>', unsafe_allow_html=True)

# -----------------------------
# EXCEL CONTROLS
# -----------------------------
st.markdown("### Excel Controls")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Preview Excel"):
        df = load_excel()

        if df.empty:
            st.warning("Excel file is empty.")
        else:
            st.dataframe(df, use_container_width=True)

with col2:
    if st.button("🗑 Reset Excel"):
        reset_excel()
        st.success("Excel data cleared successfully!")

# -----------------------------
# FILE UPLOAD
# -----------------------------
st.markdown('<div class="box">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Invoice (PDF / Image)",
    type=["pdf", "png", "jpg", "jpeg"]
)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# PROCESS FILE
# -----------------------------
if uploaded_file:

    st.success("File uploaded successfully")

    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("🚀 Extract Data"):

        with st.spinner("Processing invoice..."):

            data = process_invoice(file_path)

            # -----------------------------
            # DISPLAY OUTPUT
            # -----------------------------
            st.markdown("### Extracted Information")

            df = pd.DataFrame(list(data.items()), columns=["Field", "Value"])
            st.dataframe(df, use_container_width=True)

            # -----------------------------
            # SAVE TO EXCEL
            # -----------------------------
            excel_path = save_to_excel(data)

            st.success("Data saved to Excel successfully!")

            # -----------------------------
            # DOWNLOAD BUTTON
            # -----------------------------
            with open(excel_path, "rb") as f:
                st.download_button(
                    "⬇ Download Excel",
                    f,
                    file_name="invoice_data.xlsx"
                )