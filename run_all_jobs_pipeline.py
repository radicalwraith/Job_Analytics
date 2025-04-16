import subprocess

print("🚀 Starting job data pipeline...\n")

scripts = [
    "fetch_jooble_jobs.py",
    "fetch_remotive_jobs.py",
    "clean_jooble_jobs.py",
    "clean_remotive_jobs.py",
    "combine_all_sources.py"
]

for script in scripts:
    print(f"▶️ Running {script}...")
    result = subprocess.run(["python", script])
    if result.returncode != 0:
        print(f"❌ Error running {script}, exiting.")
        exit(1)
    print(f"✅ Completed {script}\n")

print("🎉 All jobs fetched, cleaned, and combined successfully!")
