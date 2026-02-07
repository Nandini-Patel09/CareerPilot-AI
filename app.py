import streamlit as st
from utils import extract_text_from_pdf, clean_text, extract_skills
from job_api import fetch_jobs
from matcher import JobMatcher


# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Intelligent Career Recommendation System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("CareerPilot AI")
st.write("Upload your resume and get real-time AI-powered job recommendations.")


uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])


# ==================================================
# MAIN PIPELINE
# ==================================================

if uploaded_file:

    # ---------- Resume Analysis ----------
    with st.spinner("Analyzing resume..."):
        text = extract_text_from_pdf(uploaded_file)
        cleaned_resume = clean_text(text)
        skills = extract_skills(cleaned_resume)

    st.success("Resume analyzed successfully!")

    # ---------- Skills ----------
    st.subheader("✅ Extracted Skills")

    cols = st.columns(3)

    for i, skill in enumerate(skills):
        cols[i % 3].success(skill)

    # ---------- Fetch Jobs ----------
    with st.spinner("Fetching live entry-level jobs..."):
        jobs_df = fetch_jobs()

        if jobs_df.empty:
            st.warning("Live job data is currently limited. Try again in a moment.")
            st.stop()



        matcher = JobMatcher(jobs_df)

        recommendations = matcher.recommend(
            cleaned_resume,
            skills
        )

    st.divider()

    # ==================================================
    # JOB RECOMMENDATIONS
    # ==================================================

    st.subheader("🔥 Recommended Jobs For You")

    for _, job in recommendations.iterrows():

        clean_desc = clean_text(job["job_description"])

        match_percent = int(job["Match Score"] * 100)
        missing = job["Missing Skills"]

        with st.container():

            st.markdown(
                f"## 💼 {job['job_title']}  \n🏢 **{job['company']}**"
            )

            st.progress(match_percent / 100)

            st.write(f"### Match Score: {match_percent}%")

            # ---------- Smart Match Interpretation ----------
            if match_percent >= 75:
                st.success("🔥 Excellent Match!")

            elif match_percent >= 40:
                st.info("👍 Good Match — you meet many requirements.")

            else:
                st.warning("⚠ Low Match — consider improving relevant skills.")

            # ---------- Description ----------
            st.write(clean_desc[:450] + "...")

            # ---------- Missing Skills ----------
            if missing and match_percent < 75:
                st.error("Missing Skills: " + ", ".join(missing))

            elif match_percent >= 75:
                st.success("You already have most required skills!")

            st.divider()
