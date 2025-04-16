import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(
    page_title="Job Market Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Load Data ---
df = pd.read_csv("cleaned_jooble_jobs.csv")
df["Posted_On"] = pd.to_datetime(df["Posted_On"])
df["Posted_On"] = df["Posted_On"].dt.date

# --- Filters Data Prep ---
top_titles = df["Job_Title_Cleaned"].value_counts().nlargest(5).index.tolist()
top_cities = df["City"].value_counts().nlargest(5).index.tolist()
top_levels = df["Job_Level"].value_counts().nlargest(5).index.tolist()

# --- FILTERS SECTION ---
with st.expander("🔍 Filter Jobs", expanded=False):
    colF1, colF2, colF3 = st.columns(3)
    with colF1:
        job_filter = st.multiselect("Job Titles", top_titles, default=top_titles)
    with colF2:
        city_filter = st.multiselect("Cities", top_cities, default=top_cities)
    with colF3:
        level_filter = st.multiselect("Experience Level", top_levels, default=top_levels)

# --- Filtered Data ---
filtered_df = df[
    (df["Job_Title_Cleaned"].isin(job_filter)) &
    (df["City"].isin(city_filter)) &
    (df["Job_Level"].isin(level_filter))
].copy()

# --- Header ---
st.title("📊 Job Market Analytics Dashboard")
st.markdown("**Live data from Jooble API – Data Analyst, Business Analyst, and Data Engineer roles across Canada and USA**")

# --- Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("🔢 Total Jobs", len(filtered_df))
col2.metric("🏙️ Top City", filtered_df["City"].mode()[0] if not filtered_df.empty else "N/A")
col3.metric("💼 Top Role", filtered_df["Job_Title_Cleaned"].mode()[0] if not filtered_df.empty else "N/A")

st.markdown("---")

# --- Row 1: Job Title & Job Level ---
colA, colB = st.columns(2)

with colA:
    st.subheader("📌 Job Title Distribution")
    title_counts = filtered_df["Job_Title_Cleaned"].value_counts().head(5)
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.pie(title_counts, labels=title_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

with colB:
    st.subheader("🧠 Job Levels")
    level_counts = filtered_df["Job_Level"].value_counts().head(5)
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    wedges, texts, autotexts = ax2.pie(
        level_counts, labels=level_counts.index, autopct='%1.1f%%',
        startangle=140, wedgeprops=dict(width=0.5)
    )
    ax2.axis('equal')
    st.pyplot(fig2)

st.markdown("---")

# --- Row 2: Top Cities & Companies ---
colC, colD = st.columns(2)

with colC:
    st.subheader("🌆 Top Cities")
    city_counts = filtered_df["City"].value_counts().head(5)
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    ax3.bar(city_counts.index, city_counts.values)
    ax3.set_ylabel("Jobs")
    ax3.set_xlabel("City")
    plt.xticks(rotation=30)
    st.pyplot(fig3)

with colD:
    st.subheader("🏢 Top Hiring Companies")
    company_counts = filtered_df["Company"].value_counts().head(5)
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    ax4.barh(company_counts.index, company_counts.values)
    ax4.set_xlabel("Jobs")
    ax4.set_ylabel("Company")
    st.pyplot(fig4)

st.markdown("---")

# --- Timeline Chart ---
st.subheader("📅 Job Posting Trend")
trend = filtered_df.groupby(filtered_df["Posted_On"]).size()
fig5, ax5 = plt.subplots(figsize=(12, 4))
ax5.plot(trend.index, trend.values, marker='o', linestyle='-')
ax5.set_xlabel("Date")
ax5.set_ylabel("Jobs Posted")
plt.xticks(rotation=45)
st.pyplot(fig5)

# --- Job Listings Table ---
st.subheader("🧾 Latest Job Listings")

latest_jobs = filtered_df[[
    "Job_Title_Cleaned", "Company", "City", "Job_Level", "Posted_On", "Job_Link"
]].sort_values(by="Posted_On", ascending=False).head(50).reset_index(drop=True)

latest_jobs.columns = ["Job Title", "Company", "City", "Experience Level", "Date Posted", "Apply"]
latest_jobs["Apply"] = latest_jobs["Apply"].apply(lambda x: f"<a href='{x}' target='_blank'>Apply</a>")

# Build and render HTML Table
table_html = "<table><thead><tr>"
for col in latest_jobs.columns:
    table_html += f"<th style='text-align:left;padding:8px'>{col}</th>"
table_html += "</tr></thead><tbody>"

for _, row in latest_jobs.iterrows():
    table_html += "<tr>"
    for col in latest_jobs.columns:
        table_html += f"<td style='text-align:left;padding:8px'>{row[col]}</td>"
    table_html += "</tr>"

table_html += "</tbody></table>"
st.markdown(table_html, unsafe_allow_html=True)

st.markdown("---")
st.caption(" Built by Adwaith Raj · Powered by Jooble API · Hosted on Streamlit")
