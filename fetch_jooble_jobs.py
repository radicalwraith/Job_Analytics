
import requests
import json
import pandas as pd
import time
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("JOOBLE_API_KEY")
url = f"https://jooble.org/api/{API_KEY}"

# Updated keywords and countries
keywords = ["data analyst", "data engineer", "business analyst"]
countries = ["Canada", "USA", "India", "UK"]

all_jobs = []
headers = { "Content-Type": "application/json" }

for country in countries:
    for keyword in keywords:
        page = 1
        while True:
            print(f"📥 Fetching page {page} for '{keyword}' in {country}...")
            payload = {
                "keywords": keyword,
                "location": country,
                "page": page,
                "datePosted": 7
            }

            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code != 200:
                print(f"❌ Error: {response.status_code} for {keyword} in {country}")
                break

            jobs = response.json().get("jobs", [])
            if not jobs:
                break

            for job in jobs:
                job["Country"] = country  # Add the country for analysis later
                all_jobs.append(job)

            page += 1
            time.sleep(1)

# Save to CSV
df = pd.DataFrame(all_jobs)
df.to_csv("jooble_data_jobs_last7_days.csv", index=False)
print(f"✅ Total {len(df)} jobs saved including Canada, USA, India, and UK.")
