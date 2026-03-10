import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Brooklyn Housing EDA", layout="wide")

st.title("Brooklyn Residential Housing Prices EDA")
st.markdown("This app performs EDA on the merged Brooklyn housing dataset (2009-2022).")

@st.cache_data
def load_data():
    # Check if merged file exists, otherwise merge on the fly
    if os.path.exists('merged_brooklyn_housing.csv'):
        df = pd.read_csv('merged_brooklyn_housing.csv')
    else:
        # Fallback logic from join_data.py
        years = range(2009, 2023)
        df_list = []
        for year in years:
            file_path = f"brooklyn_{year}.csv"
            if os.path.exists(file_path):
                df_list.append(pd.read_csv(file_path))
        if not df_list:
            return None
        df = pd.concat(df_list, ignore_index=True)
    return df

df = load_data()

if df is not None:
    # Sidebar filters
    st.sidebar.header("Filters")
    if 'NEIGHBORHOOD' in df.columns:
        neighborhoods = st.sidebar.multiselect("Select Neighborhood", options=df['NEIGHBORHOOD'].unique())
        if neighborhoods:
            df = df[df['NEIGHBORHOOD'].isin(neighborhoods)]

    # Basic Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df))
    if 'SALE PRICE' in df.columns:
        # Simple cleaning for numeric analysis
        df['SALE PRICE'] = pd.to_numeric(df['SALE PRICE'], errors='coerce')
        col2.metric("Avg Sale Price", f"${df['SALE PRICE'].mean():,.2f}")

    # Data Preview
    st.subheader("Data Preview")
    st.dataframe(df.head(100))

    # Visualizations
    st.subheader("Visualizations")
    if 'SALE PRICE' in df.columns and 'SALE DATE' in df.columns:
        df['SALE DATE'] = pd.to_datetime(df['SALE DATE'])
        fig = px.histogram(df, x='SALE PRICE', title="Distribution of Sale Prices")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.error("No data found. Please ensure the CSV files are in the directory.")