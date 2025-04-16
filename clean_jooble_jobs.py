import pandas as pd
import re
import html
from bs4 import BeautifulSoup

# Load raw data
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

# Clean text fields
def clean_text(text):
    if pd.isna(text): return ""
    return re.sub(r'\s+', ' ', html.unescape(str(text))).strip()

def clean_description(text):
    if pd.isna(text): return ""
    soup = BeautifulSoup(text, "html.parser")
    cleaned = soup.get_text()
    cleaned = html.unescape(cleaned)
    return re.sub(r'\s+', ' ', cleaned).strip()

def extract_city(location):
    if pd.isna(location): return "Unknown"
    if ',' in location:
        return location.split(',')[0].strip()
    return location.strip()

def normalize_title(title):
    title = title.lower()

    # Remove trailing location or qualifiers after hyphen
    if "-" in title:
        title = title.split("-")[0].strip()

    # Replace short forms
    title = title.replace("sr.", "senior").replace("jr.", "junior")

    # Remove roman numerals and noise
    title = re.sub(r'\b(i{1,3}|[1-3])\b', '', title)
    title = re.sub(r'[^a-zA-Z\s]', '', title)
    title = re.sub(r'\s+', ' ', title).strip()

    # Smart keyword mappings
    if "data scientist" in title:
        return "Data Scientist"
    if "business data analyst" in title:
        return "Data Analyst"
    if "data analyst" in title:
        return "Data Analyst"
    if "data engineer" in title:
        return "Data Engineer"
    if "business analyst" in title:
        return "Business Analyst"
    if "bi analyst" in title:
        return "BI Analyst"

    if len(title.split()) > 5:
        if "data analyst" in title:
            return "Data Analyst"
        elif "data engineer" in title:
            return "Data Engineer"
        elif "business analyst" in title:
            return "Business Analyst"
        elif "data scientist" in title:
            return "Data Scientist"

    return title.title()

def detect_level(title):
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
df["Job_Title_Cleaned"] = df["Job_Title"].apply(normalize_title)
df["Job_Level"] = df["Job_Title"].apply(detect_level)
df["Posted_On"] = pd.to_datetime(df["Posted_On"], errors="coerce")

# Drop missing or broken records
df.dropna(subset=["Job_Title", "Company", "Location", "Posted_On"], inplace=True)
df = df[df["Description"].str.strip() != ""]
df = df[df["Job_Link"].str.startswith("http", na=False)]
df = df[df["Job_Title_Cleaned"] != ""]

# Drop duplicates
df.drop_duplicates(subset=["Job_Link"], inplace=True)

# Only valid data-related jobs
keep_keywords = ["data analyst", "data engineer", "business analyst", "data scientist", "bi analyst", "etl"]
df = df[df["Job_Title"].str.lower().str.contains('|'.join(keep_keywords))]

# Exclude noisy jobs
exclude_keywords = [
    "marketing", "sales", "social media", "customer", "support",
    "recruiter", "driver", "retail", "manager",
    "pivot", "transition", "consider", "launch", "career change", "thinking about"
]
df = df[~df["Job_Title"].str.lower().str.contains('|'.join(exclude_keywords))]

# Remove vague cities
exclude_cities = ["Canada", "USA", "United States", "United Kingdom", "India", "Remote", "Unknown"]
df = df[~df["City"].isin(exclude_cities)]

# Sort and reset
df.sort_values(by="Posted_On", ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)

# Save cleaned CSV
df.to_csv("cleaned_jooble_jobs.csv", index=False)
print(f"✅ Cleaned data saved with {len(df)} jobs in 'cleaned_jooble_jobs.csv'")
