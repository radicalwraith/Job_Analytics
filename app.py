import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("cleaned_jooble_jobs.csv")
df["Posted_On"] = pd.to_datetime(df["Posted_On"])

# Limit filters to top 5 values only
top_titles = df["Job_Title_Cleaned"].value_counts().nlargest(5).index.tolist()
top_cities = df["City"].value_counts().nlargest(5).index.tolist()
top_levels = df["Job_Level"].value_counts().nlargest(5).index.tolist()

# Sidebar filters
st.sidebar.title("🔍 Filter Jobs")
job_filter = st.sidebar.multiselect("Select Top Job Titles", top_titles, default=top_titles)
city_filter = st.sidebar.multiselect("Select Top Cities", top_cities, default=top_cities)
level_filter = st.sidebar.multiselect("Select Top Job Levels", top_levels, default=top_levels)

# Apply filters
filtered_df = df[
    (df["Job_Title_Cleaned"].isin(job_filter)) &
    (df["City"].isin(city_filter)) &
    (df["Job_Level"].isin(level_filter))
]

# Main dashboard
st.title("📊 Live Job Market Analytics Dashboard")
st.markdown("View trends in Data Analyst, Engineer & Business roles in Canada + USA")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("🔢 Total Jobs", len(filtered_df))
col2.metric("🏙️ Top City", filtered_df["City"].mode()[0] if not filtered_df.empty else "N/A")
col3.metric("💼 Top Role", filtered_df["Job_Title_Cleaned"].mode()[0] if not filtered_df.empty else "N/A")

st.divider()

# Pie Chart - Job Titles
st.subheader("📌 Top 5 Job Titles")
title_counts = filtered_df["Job_Title_Cleaned"].value_counts().head(5)
fig1, ax1 = plt.subplots()
ax1.pie(title_counts, labels=title_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# Bar Chart - Top 5 Cities
st.subheader("🌆 Top 5 Cities")
city_counts = filtered_df["City"].value_counts().head(5)
fig2, ax2 = plt.subplots()
ax2.bar(city_counts.index, city_counts.values)
ax2.set_ylabel("Number of Jobs")
ax2.set_xlabel("City")
plt.xticks(rotation=45)
st.pyplot(fig2)

# Bar Chart - Job Levels
st.subheader("📈 Job Level Distribution")
level_counts = filtered_df["Job_Level"].value_counts().head(5)
fig3, ax3 = plt.subplots()
ax3.bar(level_counts.index, level_counts.values)
ax3.set_ylabel("Jobs")
ax3.set_xlabel("Level")
st.pyplot(fig3)

# Latest Jobs Table
st.subheader("📄 Latest Jobs")
st.dataframe(filtered_df[[
    "Job_Title_Cleaned", "Company", "City", "Salary", "Job_Type", "Job_Level", "Posted_On", "Job_Link"
]].sort_values(by="Posted_On", ascending=False).reset_index(drop=True))

st.caption("Built by Adwaith Raj | Powered by Jooble API")
