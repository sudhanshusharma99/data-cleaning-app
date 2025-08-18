import streamlit as st
import pandas as pd

st.title("🧹 Data Cleaning Web App")

# -------------------------------
# STEP 1: Upload File
# -------------------------------
st.header("📂 Step 1: Upload Your File")
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # -------------------------------
    # STEP 2: Show Raw File
    # -------------------------------
    st.header("👀 Step 2: Raw Dataset")
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    st.write(df.head())

    # -------------------------------
    # STEP 3: Show Info & Description
    # -------------------------------
    st.header("📊 Step 3: File Information")
    buffer = []
    df.info(buf=buffer)
    info_str = "\n".join(buffer)
    st.text("ℹ️ Dataset Info:")
    st.text(info_str)

    st.write("🧾 Summary Statistics:")
    st.write(df.describe(include="all"))

    # -------------------------------
    # STEP 4: Remove Columns
    # -------------------------------
    st.header("✂️ Step 4: Remove Unwanted Columns")
    cols_to_remove = st.multiselect("Select columns to remove", df.columns)
    if cols_to_remove:
        df = df.drop(columns=cols_to_remove)
        st.success(f"Removed columns: {cols_to_remove}")
    st.write(df.head())

    # -------------------------------
    # STEP 5: Handle Missing/Inappropriate Values
    # -------------------------------
    st.header("🩹 Step 5: Handle Missing/Inappropriate Values")

    st.subheader("🔎 Unique values per column")
    for col in df.columns:
        uniques = df[col].unique()
        # Fix display for datetime
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            uniques = df[col].dt.strftime("%Y-%m-%d").unique()
        else:
            uniques = uniques.astype(str)
        st.write(f"**{col}** → {uniques}")

    st.subheader("⚙️ Choose filling approach for each column")
    cleaned_df = df.copy()

    for col in df.columns:
        st.markdown(f"**Column: {col}**")
        if df[col].isnull().sum() > 0 or any(df[col].astype(str).str.lower().isin(["nan", "none", "null"])):
            method = st.selectbox(
                f"Choose method to handle missing/inappropriate values in '{col}'",
                ["Do Nothing", "Fill with Mean", "Fill with Median", "Fill with Mode", 
                 "Fill with Zero", "Fill with 'Unknown'", "Drop rows"],
                key=f"fill_{col}"
            )

            if method == "Fill with Mean" and pd.api.types.is_numeric_dtype(df[col]):
                cleaned_df[col] = df[col].fillna(df[col].mean())
            elif method == "Fill with Median" and pd.api.types.is_numeric_dtype(df[col]):
                cleaned_df[col] = df[col].fillna(df[col].median())
            elif method == "Fill with Mode":
                cleaned_df[col] = df[col].fillna(df[col].mode()[0])
            elif method == "Fill with Zero" and pd.api.types.is_numeric_dtype(df[col]):
                cleaned_df[col] = df[col].fillna(0)
            elif method == "Fill with 'Unknown'":
                cleaned_df[col] = df[col].fillna("Unknown")
            elif method == "Drop rows":
                cleaned_df = cleaned_df.dropna(subset=[col])

    # -------------------------------
    # STEP 6: Show Clean Dataset
    # -------------------------------
    st.header("✅ Step 6: Cleaned Dataset")
    st.write(cleaned_df.head())

    # Download option
    st.download_button(
        label="📥 Download Cleaned File (CSV)",
        data=cleaned_df.to_csv(index=False).encode("utf-8"),
        file_name="cleaned_dataset.csv",
        mime="text/csv",
    )
