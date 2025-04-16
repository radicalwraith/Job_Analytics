
# 📊 Job Market Analytics Dashboard

This is a fully functional data pipeline + interactive dashboard built to track **Data Analyst, Business Analyst, and Data Engineer** roles across Canada and the USA using **real-time job data from public APIs**.

---

## 🚀 Features

- ✅ Pulls jobs from **Jooble** and **Remotive APIs**
- 🧼 Cleans and normalizes job data across platforms
- 📍 Extracts country and city information
- 🧠 Classifies job levels (Entry, Mid, Senior)
- 📊 Displays job trends via a **Streamlit dashboard**
- 📁 Saves output as a clean, ready-to-use CSV
- ⚙️ Supports automation using **cron jobs**
- 🔄 Fully extensible with more job boards or cloud workflows

---

## 📁 Project Structure

```
job_analytics/
├── app.py                        # Streamlit dashboard
├── fetch_jooble_jobs.py         # Pulls jobs from Jooble API
├── clean_jooble_jobs.py         # Cleans and processes Jooble data
├── fetch_remotive_jobs.py       # Pulls jobs from Remotive API
├── clean_remotive_jobs.py       # Cleans and processes Remotive data
├── combine_all_sources.py       # Merges and deduplicates all job data
├── run_all_jobs_pipeline.py     # Master pipeline to run all steps
├── cleaned_jooble_jobs.csv
├── remotive_jobs_cleaned.csv
├── all_jobs_cleaned.csv         # Final cleaned merged dataset
├── requirements.txt
└── README.md
```

---

## 🌐 Data Sources

- [Jooble API](https://jooble.org/api/about)
- [Remotive API](https://remotive.io/api/remote-jobs)

Both APIs provide listings without requiring login or payment (Remotive is fully open, Jooble requires a free key).

---

## 📊 Dashboard

The dashboard (`app.py`) shows:

- **Top Job Titles** (pie chart)
- **Job Level Distribution** (donut chart)
- **Top Cities** (bar chart)
- **Top Hiring Companies** (horizontal bar chart)
- **Time Series Trend** of job postings
- Interactive job table with clickable “Apply” links

---

## ⚙️ How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the full pipeline
```bash
python run_all_jobs_pipeline.py
```

### 3. Launch the dashboard
```bash
streamlit run app.py
```

---

## ⏰ Automating with Cron (Optional)

To run the pipeline daily using `cron`, add this to your crontab:

```bash
0 8 * * * /path/to/venv/bin/python /your/project/run_all_jobs_pipeline.py >> /your/project/logs/job.log 2>&1
```

This runs the pipeline every day at 8:00 AM.

---

## 📦 Requirements

Python packages used:

- `pandas`
- `requests`
- `bs4`
- `streamlit`
- `matplotlib`

All included in `requirements.txt`.

---

## 📈 Use Cases

- Showcase your **Python + API integration** skills
- Build an **end-to-end data project** from real-world sources
- Present live analytics to hiring managers or recruiters
- Customize to monitor **other job roles or countries**

---

## 🙌 Credits

Built with ❤️ by **Adwaith Raj**  
Powered by Jooble & Remotive public APIs

---
