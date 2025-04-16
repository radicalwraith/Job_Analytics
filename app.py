import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load and prepare data
df = pd.read_csv("cleaned_jooble_jobs.csv")
df["Posted_On"] = pd.to_datetime(df["Posted_On"])

# Filters – only top 5
top_titles = df["Job_Title_Cleaned"].value_counts().nlargest(5).index.tolist()
top_cities = df["City"].value_counts().nlargest(5).index.tolist()
top_levels = df["Job_Level"].value_counts().nlargest(5).index.tolist()

# Sidebar filters
st.sidebar.title("🔍 Filter Jobs")
job_filter = st.sidebar.multiselect("Job Titles", top_titles, default=top_titles)
city_filter = st.sidebar.multiselect("Cities", top_cities, default=top_cities)
level_filter = st.sidebar.multiselect("Experience Level", top_levels, default=top_levels)

# Filtered data
filtered_df = df[
    (df["Job_Title_Cleaned"].isin(job_filter)) &
    (df["City"].isin(city_filter)) &
    (df["Job_Level"].isin(level_filter))
]

# Header
st.title("📊 Job Market Analytics Dashboard")
st.markdown("**Data & Business Roles in Canada and USA – Live from Jooble**")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("🔢 Total Jobs", len(filtered_df))
col2.metric("🏙️ Top City", filtered_df["City"].mode()[0] if not filtered_df.empty else "N/A")
col3.metric("💼 Top Role", filtered_df["Job_Title_Cleaned"].mode()[0] if not filtered_df.empty else "N/A")

st.divider()

# --- Charts Grid ---

# Chart Row 1 – Title Pie + City Bar
colA, colB = st.columns(2)

with colA:
    st.subheader("📌 Job Title Distribution")
    title_counts = filtered_df["Job_Title_Cleaned"].value_counts().head(5)
    fig1, ax1 = plt.subplots(figsize=(4, 4))
    ax1.pie(title_counts, labels=title_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

with colB:
    st.subheader("🌆 Top Cities")
    city_counts = filtered_df["City"].value_counts().head(5)
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    ax2.bar(city_counts.index, city_counts.values)
    ax2.set_ylabel("Jobs")
    ax2.set_xlabel("City")
    plt.xticks(rotation=30)
    st.pyplot(fig2)

# Chart Row 2 – Donut (Level) + Company Horizontal
colC, colD = st.columns(2)

with colC:
    st.subheader("🧠 Job Levels")
    level_counts = filtered_df["Job_Level"].value_counts().head(5)
    fig3, ax3 = plt.subplots(figsize=(4, 4))
    wedges, texts, autotexts = ax3.pie(level_counts, labels=level_counts.index, autopct='%1.1f%%',
                                       startangle=140, wedgeprops=dict(width=0.5))
    ax3.axis('equal')
    st.pyplot(fig3)

with colD:
    st.subheader("🏢 Top Hiring Companies")
    company_counts = filtered_df["Company"].value_counts().head(5)
    fig4, ax4 = plt.subplots(figsize=(5, 4))
    ax4.barh(company_counts.index, company_counts.values)
    ax4.set_xlabel("Jobs")
    ax4.set_ylabel("Company")
    st.pyplot(fig4)

# Row 3 – Timeline
st.subheader("📅 Job Posting Trend")
trend = filtered_df.groupby(filtered_df["Posted_On"].dt.date).size()
fig5, ax5 = plt.subplots(figsize=(10, 4))
ax5.plot(trend.index, trend.values, marker='o', linestyle='-')
ax5.set_xlabel("Date")
ax5.set_ylabel("Jobs Posted")
plt.xticks(rotation=45)
st.pyplot(fig5)

# Job Table
st.subheader("📄 Latest Jobs")

# Make Job_Link clickable
df_display = filtered_df.copy()
df_display["Job_Link"] = df_display["Job_Link"].apply(lambda x: f"[Apply]({x})")

# Display table
st.dataframe(df_display[[
    "Job_Title_Cleaned", "Company", "City", "Salary", "Job_Type", "Job_Level", "Posted_On", "Job_Link"
]].sort_values(by="Posted_On", ascending=False).reset_index(drop=True))

st.caption("📡 Built by Adwaith Raj | Powered by Jooble API | Hosted on Streamlit")
