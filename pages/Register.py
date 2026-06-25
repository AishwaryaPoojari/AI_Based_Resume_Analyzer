import streamlit as st
from database import register_user


def load_css():
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

if st.button("← Back to Home"):
    st.switch_page("pages/Landing.py")

st.markdown("""
<div class="auth-card">
    <div class="auth-title">Create Account ✨</div>
    <div class="auth-sub">Join ResumeAI and start improving your career profile today</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    with st.form("register_form"):
        st.markdown("**👤 Personal Details**")
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name *", placeholder="e.g. Aishwarya Poojari")
        with c2:
            age = st.number_input("Age *", min_value=16, max_value=80, value=21, step=1)

        email = st.text_input("📧 Email Address *", placeholder="you@example.com")
        c3, c4 = st.columns(2)
        with c3:
            password = st.text_input("🔒 Password *", type="password", placeholder="Min. 6 characters")
        with c4:
            confirm = st.text_input("🔒 Confirm Password *", type="password", placeholder="Repeat password")

        st.markdown("<br>**💼 Professional Details**", unsafe_allow_html=True)
        c5, c6 = st.columns(2)
        with c5:
            department = st.selectbox("Department *", [
                "Select Department", "Computer Science", "Information Technology",
                "Electronics & Communication", "Mechanical Engineering", "Civil Engineering",
                "Electrical Engineering", "Business Administration", "Commerce",
                "Arts & Humanities", "Other"
            ])
        with c6:
            experience = st.selectbox("Experience Level *", [
                "Select Experience", "Fresher (0 years)", "0–1 years",
                "1–2 years", "2–5 years", "5–10 years", "10+ years"
            ])

        occupation = st.selectbox("Current Occupation *", [
            "Select Occupation", "Student", "Recent Graduate", "Software Developer",
            "Data Analyst", "Data Scientist", "Web Developer", "DevOps Engineer",
            "Business Analyst", "HR Professional", "Project Manager", "Other"
        ])

        submitted = st.form_submit_button("Create Account →", use_container_width=True)

if submitted:
    errors = []
    if not name.strip():           errors.append("Name is required.")
    if not email.strip():          errors.append("Email is required.")
    if department == "Select Department": errors.append("Please select a department.")
    if experience == "Select Experience": errors.append("Please select experience level.")
    if occupation == "Select Occupation": errors.append("Please select an occupation.")
    if len(password) < 6:          errors.append("Password must be at least 6 characters.")
    if password != confirm:        errors.append("Passwords do not match.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        success, msg = register_user(
            name.strip(), email.strip().lower(), password,
            int(age), department, experience, occupation
        )
        if success:
            st.success("🎉 Account created! Please log in.")
            st.balloons()
            st.info(f"Your login email: **{email.strip().lower()}**")
            if st.button("Go to Login →"):
                st.switch_page("pages/Login.py")
        else:
            st.error(msg)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<style>
[data-testid="stPageLink"] {
    background: rgba(139,92,246,0.10) !important;
    border: 1px solid rgba(139,92,246,0.35) !important;
    border-radius: 8px !important;
}
[data-testid="stPageLink"] p {
    color: #8B5CF6 !important;
    font-weight: 600 !important;
}
[data-testid="stPageLink"]:hover {
    background: rgba(139,92,246,0.18) !important;
    border-color: #8B5CF6 !important;
}
</style>
""", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    t1, t2 = st.columns([2.2, 1])
    with t1:
        st.markdown(
            "<p style='color:#6B7280;font-size:0.9rem;padding-top:0.4rem'>Already have an account?</p>",
            unsafe_allow_html=True
        )
    with t2:
        st.page_link("pages/Login.py", label="**Login here**")