import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned data
df = pd.read_csv("cleaned_jooble_jobs.csv")

st.set_page_config(page_title="Data Job Market in Canada", layout="wide")

st.title("📊 Canadian Data Job Trends - Last 7 Days (Jooble API)")
st.markdown("An interactive dashboard analyzing the latest data analyst, data engineer, and business analyst jobs in Canada.")

# Top KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs", len(df))
col2.metric("Unique Companies", df['Company'].nunique())
col3.metric("Top City", df['City'].mode()[0] if not df['City'].isna().all() else "N/A")

# Sidebar Filters
with st.sidebar:
    st.header("🔍 Filters")
    selected_city = st.selectbox("Filter by City", ["All"] + sorted(df['City'].dropna().unique().tolist()))
    selected_company = st.selectbox("Filter by Company", ["All"] + sorted(df['Company'].dropna().unique().tolist()))

filtered_df = df.copy()
if selected_city != "All":
    filtered_df = filtered_df[filtered_df['City'] == selected_city]
if selected_company != "All":
    filtered_df = filtered_df[filtered_df['Company'] == selected_company]

# Top job titles
st.subheader("📌 Top 10 Job Titles")
top_titles = filtered_df['Job_Title'].value_counts().head(10)
st.bar_chart(top_titles)

# Top cities
st.subheader("📍 Top Hiring Cities")
top_cities = filtered_df['City'].value_counts().head(10)
st.bar_chart(top_cities)

# Top companies
st.subheader("🏢 Top Hiring Companies")
top_companies = filtered_df['Company'].value_counts().head(10)
st.bar_chart(top_companies)

# Full table
st.subheader("🗂 Full Job Listings (Filtered)")
st.dataframe(filtered_df[['Job_Title', 'Company', 'City', 'Salary', 'Job_Type', 'Posted_On', 'Job_Link']])
