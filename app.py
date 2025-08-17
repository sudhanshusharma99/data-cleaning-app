import streamlit as st
import pandas as pd
import numpy as np
import io

# -------------------------------
# Title & Description
# -------------------------------
st.set_page_config(page_title="Data Cleaning App", page_icon="🧹", layout="centered")

st.title("🧹 Data Cleaning Service")
st.write("Upload your CSV/Excel file and get a cleaned version with duplicates removed, "
         "missing values handled, and column names standardized.")

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload your file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📊 Original Data Preview")
        st.dataframe(df.head())

        # -------------------------------
        # Cleaning Process
        # -------------------------------
        cleaned_df = df.copy()

        # 1. Remove Duplicates
        cleaned_df = cleaned_df.drop_duplicates()

        # 2. Fill Missing Values
        for col in cleaned_df.columns:
            if cleaned_df[col].dtype in [np.float64, np.int64]:
                cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].mean())
            else:
                cleaned_df[col] = cleaned_df[col].fillna("Unknown")

        # 3. Standardize Column Names
        cleaned_df.columns = [c.strip().lower().replace(" ", "_") for c in cleaned_df.columns]

        # -------------------------------
        # Show Cleaned Data
        # -------------------------------
        st.subheader("✅ Cleaned Data Preview")
        st.dataframe(cleaned_df.head())

        # -------------------------------
        # Summary Stats
        # -------------------------------
        st.subheader("📈 Summary Statistics")
        st.write(cleaned_df.describe(include="all"))

        # -------------------------------
        # Download Button
        # -------------------------------
        buffer = io.BytesIO()
        cleaned_df.to_csv(buffer, index=False)
        buffer.seek(0)

        st.download_button(
            label="⬇️ Download Cleaned File (CSV)",
            data=buffer,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload a CSV or Excel file to start cleaning.")
