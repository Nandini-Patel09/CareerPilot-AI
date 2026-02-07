import requests
import pandas as pd


def fetch_jobs():

    url = "https://remotive.com/api/remote-jobs"

    try:
        response = requests.get(url, timeout=15)
        data = response.json()
    except:
        return pd.DataFrame()

    priority_jobs = []   # AI / DATA
    secondary_jobs = []  # Adjacent tech

    # ------------------------------------------------
    # BLOCKLIST (NEVER SHOW)
    # ------------------------------------------------

    blocked_words = [
        "senior", "sr", "lead", "manager",
        "director", "principal", "staff",
        "architect", "head", "chief",

        "trainer", "rater", "annotator",
        "labeler", "evaluator",
        "transcription", "data entry",

        "writer", "marketing", "sales",
        "support", "customer", "assistant",

        "ios", "android", "mobile",
        "frontend", "react", "angular",
        "vue", "wordpress", "php"
    ]

    # ------------------------------------------------
    # PRIORITY KEYWORDS (AI / DATA)
    # ------------------------------------------------

    ai_data_keywords = [
        "data scientist",
        "machine learning",
        "ml engineer",
        "ai engineer",
        "data analyst",
        "artificial intelligence",
        "analytics",
        "nlp",
        "deep learning"
    ]

    # ------------------------------------------------
    # SECONDARY TECH KEYWORDS
    # ------------------------------------------------

    tech_keywords = [
        "python",
        "data engineer",
        "analytics engineer",
        "backend",
        "software engineer",
        "bi",
        "business intelligence"
    ]

    # =================================================
    # PASS — CLASSIFY JOBS
    # =================================================

    for job in data["jobs"]:

        title = job["title"].lower()

        # ❌ Global block
        if any(word in title for word in blocked_words):
            continue

        job_data = {
            "job_title": job["title"],
            "company": job["company_name"],
            "job_description": job["description"]
        }

        # 🟢 PRIORITY FIRST
        if any(word in title for word in ai_data_keywords):
            priority_jobs.append(job_data)

        # 🟡 SECONDARY
        elif any(word in title for word in tech_keywords):
            secondary_jobs.append(job_data)

        # Stop early if enough found
        if len(priority_jobs) >= 20:
            break

    # =================================================
    # FINAL RETURN LOGIC
    # =================================================

    if len(priority_jobs) >= 10:
        return pd.DataFrame(priority_jobs[:20])

    # Mix if priority is low
    combined = priority_jobs + secondary_jobs

    if combined:
        return pd.DataFrame(combined[:20])

    # FINAL SAFETY NET
    fallback = pd.read_csv("data/fallback_jobs.csv")
    return fallback

