
import streamlit as st
import PyPDF2

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# -------------------------------
# CUSTOM CSS
# -------------------------------

st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
.title {
    text-align: center;
    color: #243b64;
    font-size: 38px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #555;
    font-size: 17px;
}
.result {
    background-color: #e8f5e9;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------

st.markdown(
    '<div class="title">AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Analyze your resume and match it with job requirements</div>',
    unsafe_allow_html=True
)

st.write("---")

# -------------------------------
# SKILLS DATABASE
# -------------------------------

skills = [
    "python",
    "java",
    "c++",
    "html",
    "css",
    "javascript",
    "sql",
    "mysql",
    "mongodb",
    "machine learning",
    "artificial intelligence",
    "deep learning",
    "data science",
    "flask",
    "django",
    "streamlit",
    "communication",
    "teamwork",
    "leadership",
    "problem solving"
]

# -------------------------------
# RESUME UPLOAD
# -------------------------------

st.subheader("Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose your PDF resume",
    type=["pdf"]
)

# -------------------------------
# JOB DESCRIPTION
# -------------------------------

st.subheader("Job Description")

job_description = st.text_area(
    "Enter the job requirements here:",
    placeholder="Example: We are looking for a Python developer with knowledge of SQL, Flask and Machine Learning.",
    height=150
)

# -------------------------------
# ANALYZE BUTTON
# -------------------------------

if st.button("Analyze Resume", type="primary"):

    if uploaded_file is None:
        st.error("Please upload your resume.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:

        try:
            # Extract PDF Text

            pdf_reader = PyPDF2.PdfReader(uploaded_file)

            resume_text = ""

            for page in pdf_reader.pages:
                resume_text += page.extract_text() or ""

            resume_text = resume_text.lower()
            job_text = job_description.lower()

            if not resume_text.strip():
                st.error(
                    "No readable text found. Please upload a text-based PDF."
                )
                st.stop()

            # Find required skills in job description

            required_skills = []

            for skill in skills:
                if skill in job_text:
                    required_skills.append(skill)

            # Match skills with resume

            matched_skills = []
            missing_skills = []

            for skill in required_skills:

                if skill in resume_text:
                    matched_skills.append(skill)

                else:
                    missing_skills.append(skill)

            # Calculate matching percentage

            total_skills = len(required_skills)

            if total_skills > 0:

                score = (
                    len(matched_skills) / total_skills
                ) * 100

            else:
                score = 0

            # -------------------------------
            # DISPLAY RESULTS
            # -------------------------------

            st.write("---")

            st.header("Resume Analysis Results")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Resume Match",
                    f"{score:.2f}%"
                )

            with col2:
                st.metric(
                    "Matched Skills",
                    len(matched_skills)
                )

            with col3:
                st.metric(
                    "Missing Skills",
                    len(missing_skills)
                )

            st.progress(int(score))

            # -------------------------------
            # MATCHED SKILLS
            # -------------------------------

            st.subheader("Matched Skills")

            if matched_skills:

                for skill in matched_skills:
                    st.success("✓ " + skill.title())

            else:
                st.warning("No matching skills found.")

            # -------------------------------
            # MISSING SKILLS
            # -------------------------------

            st.subheader("Missing Skills")

            if missing_skills:

                for skill in missing_skills:
                    st.error("✗ " + skill.title())

            else:
                st.success("No missing skills found!")

            # -------------------------------
            # RECOMMENDATIONS
            # -------------------------------

            st.subheader("AI Recommendations")

            if score >= 80:

                st.success(
                    "Your resume matches most of the required skills."
                )

            elif score >= 50:

                st.info(
                    "Your resume has a moderate match. "
                    "Improve your missing skills."
                )

            else:

                st.warning(
                    "Your resume needs improvement for this job."
                )

            if missing_skills:

                st.write("Recommended skills to learn:")

                for skill in missing_skills:
                    st.write("•", skill.title())

            # -------------------------------
            # DOWNLOAD REPORT
            # -------------------------------

            report = f"""
AI RESUME ANALYZER REPORT

Resume Match Score: {score:.2f}%

Matched Skills:
{', '.join(matched_skills)}

Missing Skills:
{', '.join(missing_skills)}

Total Required Skills: {total_skills}

Thank you for using AI Resume Analyzer.
"""

            st.download_button(
                label="Download Analysis Report",
                data=report,
                file_name="resume_analysis.txt",
                mime="text/plain"
            )

        except Exception as e:

            st.error(f"Error while analyzing resume: {e}")

# -------------------------------
# FOOTER
# -------------------------------

st.write("---")

st.markdown(
    "<center>AI Resume Analyzer | MCA Mini Project</center>",
    unsafe_allow_html=True
)
