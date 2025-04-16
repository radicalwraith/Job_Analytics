import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("cleaned_jooble_jobs.csv")
df["Posted_On"] = pd.to_datetime(df["Posted_On"])

# Filters (Top 5)
top_titles = df["Job_Title_Cleaned"].value_counts().nlargest(5).index.tolist()
top_cities = df["City"].value_counts().nlargest(5).index.tolist()
top_levels = df["Job_Level"].value_counts().nlargest(5).index.tolist()

# Sidebar
st.sidebar.title("🔍 Filter Jobs")
job_filter = st.sidebar.multiselect("Select Top Job Titles", top_titles, default=top_titles)
city_filter = st.sidebar.multiselect("Select Top Cities", top_cities, default=top_cities)
level_filter = st.sidebar.multiselect("Select Top Job Levels", top_levels, default=top_levels)

# Filter Data
filtered_df = df[
    (df["Job_Title_Cleaned"].isin(job_filter)) &
    (df["City"].isin(city_filter)) &
    (df["Job_Level"].isin(level_filter))
]

# Dashboard Title
st.title("📊 Job Market Dashboard – Data & Business Roles")
st.markdown("Insights from Jooble job listings across Canada & USA")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("🔢 Total Jobs", len(filtered_df))
col2.metric("🏙️ Top City", filtered_df["City"].mode()[0] if not filtered_df.empty else "N/A")
col3.metric("💼 Top Role", filtered_df["Job_Title_Cleaned"].mode()[0] if not filtered_df.empty else "N/A")

st.divider()

# 1️⃣ Pie Chart – Job Titles
st.subheader("📌 Job Title Distribution")
title_counts = filtered_df["Job_Title_Cleaned"].value_counts().head(5)
fig1, ax1 = plt.subplots()
ax1.pie(title_counts, labels=title_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# 2️⃣ Bar Chart – Jobs by City
st.subheader("🌆 Top Cities Hiring")
city_counts = filtered_df["City"].value_counts().head(5)
fig2, ax2 = plt.subplots()
ax2.bar(city_counts.index, city_counts.values)
ax2.set_ylabel("Number of Jobs")
ax2.set_xlabel("City")
plt.xticks(rotation=45)
st.pyplot(fig2)

# 3️⃣ Donut Chart – Job Level Breakdown
st.subheader("🧠 Job Level Breakdown")
level_counts = filtered_df["Job_Level"].value_counts().head(5)
fig3, ax3 = plt.subplots()
wedges, texts, autotexts = ax3.pie(level_counts, labels=level_counts.index, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.5))
ax3.axis('equal')
st.pyplot(fig3)

# 4️⃣ Horizontal Bar – Top Hiring Companies
st.subheader("🏢 Top Hiring Companies")
company_counts = filtered_df["Company"].value_counts().head(5)
fig4, ax4 = plt.subplots()
ax4.barh(company_counts.index, company_counts.values)
ax4.set_xlabel("Jobs")
ax4.set_ylabel("Company")
st.pyplot(fig4)

# 5️⃣ Line Chart – Job Posting Trend
st.subheader("📅 Job Posting Trend Over Time")
trend = filtered_df.groupby(filtered_df["Posted_On"].dt.date).size()
fig5, ax5 = plt.subplots()
ax5.plot(trend.index, trend.values, marker='o', linestyle='-')
ax5.set_xlabel("Date")
ax5.set_ylabel("Jobs Posted")
plt.xticks(rotation=45)
st.pyplot(fig5)

# 📄 Data Table
st.subheader("🧾 Latest Job Listings")
st.dataframe(filtered_df[[
    "Job_Title_Cleaned", "Company", "City", "Salary", "Job_Type", "Job_Level", "Posted_On", "Job_Link"
]].sort_values(by="Posted_On", ascending=False).reset_index(drop=True))

st.caption("Built by Adwaith Raj · Data via Jooble API")
