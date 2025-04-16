import pandas as pd
import re
import html
from bs4 import BeautifulSoup

# Load the raw data
df = pd.read_csv("jooble_data_jobs_last_3_days.csv")

# Step 1: Keep only relevant columns
columns_to_keep = [
    "title", "location", "company", "salary", "type", "updated", "snippet", "link"
]
df = df[columns_to_keep]

# Step 2: Rename columns for consistency
df.rename(columns={
    "title": "Job_Title",
    "location": "Location",
    "company": "Company",
    "salary": "Salary",
    "type": "Job_Type",
    "updated": "Posted_On",
    "snippet": "Description",
    "link": "Job_Link"
}, inplace=True)

# Step 3: Clean Description field
def clean_description(text):
    if pd.isna(text):
        return ""
    # Remove HTML tags and unescape HTML characters
    text = BeautifulSoup(text, "html.parser").get_text()
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df["Description"] = df["Description"].apply(clean_description)

# Optional: Clean Salary and Job_Type fields (remove extra spaces, HTML leftovers)
df["Salary"] = df["Salary"].astype(str).apply(lambda x: re.sub(r'\s+', ' ', html.unescape(x.strip())))
df["Job_Type"] = df["Job_Type"].astype(str).apply(lambda x: x.strip().capitalize())

# Step 4: Drop rows with missing key info
df.dropna(subset=["Job_Title", "Company", "Location"], inplace=True)

# Step 5: Clean and format Posted_On
df["Posted_On"] = pd.to_datetime(df["Posted_On"], errors="coerce")
df = df[df["Posted_On"].notna()]

# Step 6: Save the cleaned data
df.to_csv("cleaned_jooble_jobs.csv", index=False)
print(f"✅ Cleaned data saved as 'cleaned_jooble_jobs.csv' with {len(df)} records.")
