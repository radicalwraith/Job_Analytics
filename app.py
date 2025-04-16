import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your cleaned data
df = pd.read_csv("cleaned_jooble_jobs.csv")

st.set_page_config(page_title="Data Job Market in Canada", layout="wide")

st.title("📊 Canadian Data Job Trends - Last 3 Days (Jooble API)")
st.markdown("An interactive dashboard analyzing the latest data roles in Canada.")

# Top KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs", len(df))
col2.metric("Unique Companies", df['Company'].nunique())
col3.metric("Top Location", df['Location'].mode()[0])

# Sidebar Filters
with st.sidebar:
    st.header("🔍 Filters")
    selected_city = st.selectbox("Filter by Location", ["All"] + sorted(df['Location'].dropna().unique().tolist()))
    selected_company = st.selectbox("Filter by Company", ["All"] + sorted(df['Company'].dropna().unique().tolist()))

filtered_df = df.copy()
if selected_city != "All":
    filtered_df = filtered_df[filtered_df['Location'] == selected_city]
if selected_company != "All":
    filtered_df = filtered_df[filtered_df['Company'] == selected_company]

# Top job titles
st.subheader("📌 Top 10 Job Titles")
top_titles = filtered_df['Job_Title'].value_counts().head(10)
st.bar_chart(top_titles)

# Top locations
st.subheader("📍 Top Hiring Cities")
top_locations = filtered_df['Location'].value_counts().head(10)
st.bar_chart(top_locations)

# Top companies
st.subheader("🏢 Top Hiring Companies")
top_companies = filtered_df['Company'].value_counts().head(10)
st.bar_chart(top_companies)

# Show full table
st.subheader("🗂 Full Job Listings (Filtered)")
st.dataframe(filtered_df[['Job_Title', 'Company', 'Location', 'Salary', 'Job_Type', 'Posted_On', 'Job_Link']])
