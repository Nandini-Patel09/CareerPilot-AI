from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import clean_text
from skills import SKILLS


class JobMatcher:

    def __init__(self, jobs_df):
        if "job_description" not in jobs_df.columns:
            raise ValueError("Jobs dataframe is empty or malformed.")

        # Clean job descriptions
        jobs_df["clean_desc"] = jobs_df["job_description"].apply(clean_text)

        self.jobs = jobs_df

        # Strong vectorizer
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)   # captures phrases like "machine learning"
        )

        self.job_vectors = self.vectorizer.fit_transform(
            self.jobs["clean_desc"]
        )

    # ----------------------------------------------------

    def recommend(self, resume_text, resume_skills, top_n=5):

        resume_clean = clean_text(resume_text)

        resume_vector = self.vectorizer.transform([resume_clean])

        scores = cosine_similarity(
            resume_vector,
            self.job_vectors
        )[0]

        self.jobs["Match Score"] = scores

        top_jobs = self.jobs.sort_values(
            by="Match Score",
            ascending=False
        ).head(top_n)

        # ---------- SKILL GAP ENGINE ----------
        skill_gaps = []

        for _, job in top_jobs.iterrows():

            job_text = job["clean_desc"]

            # Skills required by job
            required_skills = [
                skill for skill in SKILLS
                if skill in job_text
            ]

            # Missing from resume
            missing = [
                skill for skill in required_skills
                if skill not in resume_skills
            ]

            # Limit for UI cleanliness
            skill_gaps.append(missing[:6])

        top_jobs["Missing Skills"] = skill_gaps

        return top_jobs
