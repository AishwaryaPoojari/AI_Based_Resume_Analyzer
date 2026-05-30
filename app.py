import matplotlib.pyplot as plt
import streamlit as st
import pdfplumber
import pickle

# --------------------------------
# Page Config
# --------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# Sidebar
st.sidebar.title("AI Resume Analyzer")

st.sidebar.write("Upload your resume for AI analysis.")

st.sidebar.info(
    """
    Features:
    • Resume Score
    • Skill Detection
    • Job Prediction
    • ATS Analysis
    """
)

# --------------------------------
# Load CSS
# --------------------------------
def load_css():
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
# Load ML model
model = pickle.load(open("models/model.pkl", "rb"))

vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))

# --------------------------------
# Extract text from PDF
# --------------------------------
def extract_text_from_pdf(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text.lower()

# --------------------------------
# Load skills
# --------------------------------
def load_skills():
    with open("skills.txt", "r") as file:
        skills = file.read().splitlines()

    return [skill.lower() for skill in skills]

# --------------------------------
# Find matching skills
# --------------------------------
def find_skills(resume_text, skills_list):

    found_skills = []

    for skill in skills_list:
        if skill in resume_text:
            found_skills.append(skill)

    return found_skills

# --------------------------------
# Main UI
# --------------------------------
st.title("📄 AI-Based Resume Analyzer")

st.write("Upload your resume and get AI-based analysis.")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("Resume Uploaded Successfully!")

    # Extract resume text
    resume_text = extract_text_from_pdf(uploaded_file)
    # Convert text into vector
    resume_vector = vectorizer.transform([resume_text])
    # Predict role
    prediction = model.predict(resume_vector)
    # Load skills
    skills = load_skills()

    # Match skills
    matched_skills = find_skills(resume_text, skills)

    # Calculate score
    score = len(matched_skills) * 10

    if score > 100:
        score = 100

    # --------------------------------
    # Display Results
    # --------------------------------
    st.subheader("📊 Resume Score")

    st.progress(score / 100)

    st.write(f"### {score}/100")
    # ATS Compatibility
        # ATS Compatibility
    st.subheader("📌 ATS Compatibility")

    if score >= 80:
        st.success("ATS Friendly Resume")

    elif score >= 50:
        st.warning("Moderately ATS Friendly")

    else:
        st.error("Low ATS Compatibility")

    # --------------------------------
    # Missing Skills
    # --------------------------------
    missing_skills = list(set(skills) - set(matched_skills))

    # --------------------------------
    # Skills Found
    # --------------------------------
    st.subheader("✅ Skills Found")

    for skill in matched_skills:
        st.write(f"✔ {skill}")

    # --------------------------------
    # Pie Chart
    # --------------------------------
    fig, ax = plt.subplots()

    skills_count = len(matched_skills)
    missing_count = len(missing_skills)

    labels = ['Matched Skills', 'Missing Skills']
    values = [skills_count, missing_count]

    ax.pie(values, labels=labels, autopct='%1.1f%%')

    st.pyplot(fig)

    # --------------------------------
    # Missing Skills
    # --------------------------------
    st.subheader("❌ Missing Skills")

    for skill in missing_skills[:5]:
        st.write(f"➜ {skill}")

    # --------------------------------
    # Resume Feedback
    # --------------------------------
    st.subheader("📌 Resume Feedback")

    if score >= 80:
        st.success("Excellent Resume!")

    elif score >= 50:
        st.warning("Good Resume but can be improved.")

    else:
        st.error("Resume needs improvement.")

    # --------------------------------
    # AI Job Prediction
    # --------------------------------
    st.subheader("💼 Predicted Job Role")

    st.success(prediction[0])