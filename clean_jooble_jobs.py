import pandas as pd
import re
import html
from bs4 import BeautifulSoup

# Load the raw Jooble API data
df = pd.read_csv("jooble_data_jobs_last7_days.csv")

# Keep only relevant columns
columns = ["title", "location", "company", "salary", "type", "updated", "snippet", "link", "Country"]
df = df[columns]

# Rename for clarity
df.rename(columns={
    "title": "Job_Title",
    "location": "Location",
    "company": "Company",
    "salary": "Salary",
    "type": "Job_Type",
    "updated": "Posted_On",
    "snippet": "Description",
    "link": "Job_Link",
    "Country": "Country"
}, inplace=True)

# --- Cleaners ---
def clean_description(text):
    if pd.isna(text): return ""
    soup = BeautifulSoup(text, "html.parser")
    cleaned = soup.get_text()
    cleaned = html.unescape(cleaned)
    return re.sub(r'\s+', ' ', cleaned).strip()

def clean_text(text):
    if pd.isna(text): return ""
    return re.sub(r'\s+', ' ', html.unescape(str(text))).strip()

def extract_city(location):
    if pd.isna(location): return "Unknown"
    if ',' in location:
        return location.split(',')[0].strip()
    return location.strip()

def get_level(title):
    title = title.lower()
    if "senior" in title or "sr" in title:
        return "Senior"
    elif "junior" in title or "jr" in title or "entry" in title:
        return "Entry"
    else:
        return "Mid"

# Apply all cleaners
for col in ["Job_Title", "Company", "Location", "Salary", "Job_Type"]:
    df[col] = df[col].apply(clean_text)

df["Description"] = df["Description"].apply(clean_description)
df["City"] = df["Location"].apply(extract_city)
df["Job_Level"] = df["Job_Title"].apply(get_level)
df["Posted_On"] = pd.to_datetime(df["Posted_On"], errors="coerce")

# Remove blanks or invalids
df.dropna(subset=["Job_Title", "Company", "Location", "Posted_On"], inplace=True)
df = df[df["Description"].str.strip() != ""]
df.drop_duplicates(subset=["Job_Link"], inplace=True)

# Only keep relevant data roles
keep_keywords = ["data analyst", "data engineer", "business analyst", "data scientist", "bi analyst", "etl"]
df = df[df["Job_Title"].str.lower().str.contains('|'.join(keep_keywords))]

# Exclude non-data noise
exclude_keywords = ["marketing", "sales", "social media", "customer", "support", "recruiter", "driver", "retail", "manager"]
df = df[~df["Job_Title"].str.lower().str.contains('|'.join(exclude_keywords))]

# Filter out vague city values
exclude_cities = ["Canada", "USA", "United States", "United Kingdom", "India", "Remote", "Unknown"]
df = df[~df["City"].isin(exclude_cities)]

# Sort by newest
df.sort_values(by="Posted_On", ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)

# Save to CSV
df.to_csv("cleaned_jooble_jobs.csv", index=False)
print(f"✅ Cleaned dataset saved: {len(df)} rows with clear job titles, cities, and filters.")
