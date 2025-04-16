import requests
import json
import pandas as pd
import time

API_KEY = "cae46c3a-26ce-4a1f-b13a-9f8b1e46fe0e"
url = f"https://jooble.org/api/{API_KEY}"

# Keywords to search
keywords = ["data analyst", "data analytics", "data engineer", "data engineering"]
all_jobs = []

headers = {
    "Content-Type": "application/json"
}

for keyword in keywords:
    page = 1
    while True:
        print(f"Fetching page {page} for keyword: '{keyword}'...")
        payload = {
            "keywords": keyword,
            "location": "Canada",
            "page": page,
            "datePosted": "3"  # Last 3 days
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code != 200:
            print(f"❌ Failed on page {page} for '{keyword}' — Status code: {response.status_code}")
            break

        data = response.json()
        jobs = data.get("jobs", [])

        if not jobs:
            print(f"✅ No more jobs for '{keyword}' on page {page}")
            break

        all_jobs.extend(jobs)
        page += 1
        time.sleep(1)  # Respect API limits

# Remove duplicates by job link (optional but useful)
df = pd.DataFrame(all_jobs)
df.drop_duplicates(subset="link", inplace=True)

# Save to CSV
df.to_csv("jooble_data_jobs_last_3_days.csv", index=False)
print(f"✅ Total {len(df)} jobs saved to 'jooble_data_jobs_last_3_days.csv'")
