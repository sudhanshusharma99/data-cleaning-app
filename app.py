import streamlit as st
import pandas as pd
import numpy as np
import io

st.set_page_config(page_title="Data Cleaning App", page_icon="🧹", layout="wide")

st.title("🧹 Interactive Data Cleaning App")

# -------------------------------
# Step 1: Upload File
# -------------------------------
uploaded_file = st.file_uploader("📂 Upload your CSV/Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Work on a copy
    cleaned_df = df.copy()

    # -------------------------------
    # Step 2: Show Raw File
    # -------------------------------
    st.subheader("📊 Step 2: Raw Dataset Preview")
    st.dataframe(cleaned_df.head())

    # -------------------------------
    # Step 3: Show Info + Null Summary
    # -------------------------------
    st.subheader("ℹ️ Step 3: Dataset Information")
    st.write("**Shape:** ", cleaned_df.shape)
    st.write("**Columns:** ", cleaned_df.columns.tolist())

    st.write("**Null Values Summary:**")
    st.write(cleaned_df.isnull().sum())

    st.write("**Statistical Description:**")
    st.write(cleaned_df.describe(include="all"))

    # -------------------------------
    # Step 4: Remove Unwanted Columns
    # -------------------------------
    st.subheader("🗑️ Step 4: Remove Unwanted Columns")
    cols_to_remove = st.multiselect(
        "Select columns you want to remove:",
        options=cleaned_df.columns.tolist()
    )
    if cols_to_remove:
        cleaned_df.drop(columns=cols_to_remove, inplace=True)
        st.success(f"Removed columns: {', '.join(cols_to_remove)}")
        st.dataframe(cleaned_df.head())

    # -------------------------------
    # Step 5: Handle Nulls & Inappropriate Values
    # -------------------------------
    st.subheader("🩹 Step 5: Handle Nulls & Inappropriate Values")

    st.write("🔎 Unique values per column (to detect inappropriate values):")
    for col in cleaned_df.columns:
        st.write(f"**{col}** → {cleaned_df[col].unique()}")

    col_to_fix = st.selectbox("Select column to clean:", options=cleaned_df.columns.tolist())

    if col_to_fix:
        st.write(f"Selected column: **{col_to_fix}**")

        # Show unique values of selected column
        st.write("Unique values in this column:")
        st.write(cleaned_df[col_to_fix].unique())

        # Choose handling method
        fill_option = st.selectbox(
            "Choose how to handle null/inappropriate values:",
            [
                "Do nothing",
                "Fill with Mean (numeric only)",
                "Fill with Median (numeric only)",
                "Fill with Mode",
                "Fill with 0 (numeric only)",
                "Fill with 'Unknown' (for text)",
                "Drop rows with null/inappropriate values"
            ]
        )

        if fill_option != "Do nothing":
            if fill_option == "Fill with Mean (numeric only)" and cleaned_df[col_to_fix].dtype in [np.float64, np.int64]:
                cleaned_df[col_to_fix].fillna(cleaned_df[col_to_fix].mean(), inplace=True)

            elif fill_option == "Fill with Median (numeric only)" and cleaned_df[col_to_fix].dtype in [np.float64, np.int64]:
                cleaned_df[col_to_fix].fillna(cleaned_df[col_to_fix].median(), inplace=True)

            elif fill_option == "Fill with Mode":
                cleaned_df[col_to_fix].fillna(cleaned_df[col_to_fix].mode()[0], inplace=True)

            elif fill_option == "Fill with 0 (numeric only)" and cleaned_df[col_to_fix].dtype in [np.float64, np.int64]:
                cleaned_df[col_to_fix].fillna(0, inplace=True)

            elif fill_option == "Fill with 'Unknown' (for text)" and cleaned_df[col_to_fix].dtype == object:
                cleaned_df[col_to_fix].fillna("Unknown", inplace=True)

            elif fill_option == "Drop rows with null/inappropriate values":
                cleaned_df = cleaned_df[cleaned_df[col_to_fix].notna()]

            st.success(f"✅ {fill_option} applied to column: {col_to_fix}")

    # -------------------------------
    # Step 6: Show Cleaned Dataset
    # -------------------------------
    st.subheader("✅ Step 6: Final Cleaned Dataset")
    st.dataframe(cleaned_df.head())

    # Download option
    buffer = io.BytesIO()
    cleaned_df.to_csv(buffer, index=False)
    buffer.seek(0)
    st.download_button(
        label="⬇️ Download Cleaned File (CSV)",
        data=buffer,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload a CSV or Excel file to begin.")
