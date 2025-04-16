import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("cleaned_jooble_jobs.csv")

# Convert date
df["Posted_On"] = pd.to_datetime(df["Posted_On"])

# Sidebar filters
st.sidebar.title("🔍 Filter Jobs")
job_filter = st.sidebar.multiselect("Select Job Titles", sorted(df["Job_Title_Cleaned"].unique()), default=df["Job_Title_Cleaned"].unique())
city_filter = st.sidebar.multiselect("Select Cities", sorted(df["City"].unique()), default=df["City"].unique())
level_filter = st.sidebar.multiselect("Select Job Level", sorted(df["Job_Level"].unique()), default=df["Job_Level"].unique())

# Filter logic
filtered_df = df[
    (df["Job_Title_Cleaned"].isin(job_filter)) &
    (df["City"].isin(city_filter)) &
    (df["Job_Level"].isin(level_filter))
]

# Dashboard title
st.title("📊 Live Job Market Analytics Dashboard")
st.markdown("Showing live job insights based on the latest **Jooble** data. Filter by job title, city, and experience level.")

# Metric Cards
col1, col2, col3 = st.columns(3)
col1.metric("🔢 Total Jobs", len(filtered_df))
col2.metric("🏙️ Top City", filtered_df["City"].mode()[0] if not filtered_df["City"].isna().all() else "N/A")
col3.metric("💼 Top Role", filtered_df["Job_Title_Cleaned"].mode()[0] if not filtered_df["Job_Title_Cleaned"].isna().all() else "N/A")

st.divider()

# Pie Chart - Job Title Distribution
st.subheader("📌 Job Title Distribution")
title_counts = filtered_df["Job_Title_Cleaned"].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(title_counts, labels=title_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# Bar Chart - Jobs by City
st.subheader("🌆 Jobs by City")
city_counts = filtered_df["City"].value_counts().head(10)
fig2, ax2 = plt.subplots()
ax2.bar(city_counts.index, city_counts.values)
ax2.set_ylabel("Number of Jobs")
ax2.set_xlabel("City")
plt.xticks(rotation=45)
st.pyplot(fig2)

# Bar Chart - Job Level
st.subheader("📈 Job Level Breakdown")
level_counts = filtered_df["Job_Level"].value_counts()
fig3, ax3 = plt.subplots()
ax3.bar(level_counts.index, level_counts.values)
ax3.set_ylabel("Number of Jobs")
ax3.set_xlabel("Level")
st.pyplot(fig3)

# Latest Jobs Table
st.subheader("📄 Latest Jobs")
st.dataframe(filtered_df[[
    "Job_Title_Cleaned", "Company", "City", "Salary", "Job_Type", "Job_Level", "Posted_On", "Job_Link"
]].sort_values(by="Posted_On", ascending=False).reset_index(drop=True))

st.caption("Data source: Jooble API | Built with ❤️ by Adwaith Raj")
