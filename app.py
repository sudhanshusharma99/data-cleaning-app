import streamlit as st
import pandas as pd
import numpy as np
import io

# -------------------------------
# Title & Description
# -------------------------------
st.set_page_config(page_title="Data Cleaning App", page_icon="🧹", layout="centered")

st.title("🧹 Data Cleaning Service")
st.write("Upload your CSV/Excel file and clean it interactively by removing columns and handling missing values.")

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload your file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Read file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📊 Original Data Preview")
        st.dataframe(df.head())

        cleaned_df = df.copy()

        # -------------------------------
        # 1. Ask user to remove unwanted columns
        # -------------------------------
        st.subheader("🗑️ Remove Unwanted Columns")
        cols_to_remove = st.multiselect(
            "Select columns you want to remove:",
            options=cleaned_df.columns.tolist()
        )

        if cols_to_remove:
            cleaned_df.drop(columns=cols_to_remove, inplace=True)
            st.success(f"Removed columns: {', '.join(cols_to_remove)}")

        # -------------------------------
        # 2. Handle Missing Values
        # -------------------------------
        st.subheader("🩹 Handle Missing Values")

        fill_option = st.selectbox(
            "Choose how to fill missing values:",
            [
                "Do nothing",
                "Fill with column mean (numeric only)",
                "Fill with column median (numeric only)",
                "Fill with mode",
                "Fill with 0 (numeric only)",
                "Fill with 'Unknown' (for text)",
                "Drop rows with missing values"
            ]
        )

        if fill_option != "Do nothing":
            for col in cleaned_df.columns:
                if cleaned_df[col].isnull().sum() > 0:
                    if fill_option == "Fill with column mean (numeric only)" and cleaned_df[col].dtype in [np.float64, np.int64]:
                        cleaned_df[col].fillna(cleaned_df[col].mean(), inplace=True)

                    elif fill_option == "Fill with column median (numeric only)" and cleaned_df[col].dtype in [np.float64, np.int64]:
                        cleaned_df[col].fillna(cleaned_df[col].median(), inplace=True)

                    elif fill_option == "Fill with mode":
                        cleaned_df[col].fillna(cleaned_df[col].mode()[0], inplace=True)

                    elif fill_option == "Fill with 0 (numeric only)" and cleaned_df[col].dtype in [np.float64, np.int64]:
                        cleaned_df[col].fillna(0, inplace=True)

                    elif fill_option == "Fill with 'Unknown' (for text)" and cleaned_df[col].dtype == object:
                        cleaned_df[col].fillna("Unknown", inplace=True)

                    elif fill_option == "Drop rows with missing values":
                        cleaned_df.dropna(inplace=True)

            st.success(f"Missing values handled using: {fill_option}")

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
