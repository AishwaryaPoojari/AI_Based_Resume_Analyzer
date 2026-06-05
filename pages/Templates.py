import streamlit as st
import os


def load_css():
    with open("styles/style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

# ── Auth Guard ─────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.warning("⚠️ Please log in first.")
    if st.button("Go to Login"):
        st.switch_page("pages/Login.py")
    st.stop()

# ── Header ─────────────────────────────────────────────────
c1, c2 = st.columns([8, 2])
with c1:
    st.markdown("## 📄 Resume Templates")
    st.markdown("<p style='color:#8b949e'>Download a professional ATS-friendly template and fill it with your details.</p>",
                unsafe_allow_html=True)
with c2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("pages/Landing.py")

st.markdown("<hr style='border-color:#30363d'>", unsafe_allow_html=True)

# ── Tips banner ────────────────────────────────────────────
st.markdown("""
<div style="background:#1c2a1c;border:1px solid #3fb950;border-radius:10px;
            padding:0.8rem 1.2rem;margin-bottom:1.5rem;">
    <b style="color:#3fb950;">&#128161; Tips for using these templates:</b>
    <ul style="color:#8b949e;margin:0.4rem 0 0 1rem;font-size:0.87rem;">
        <li>Replace all placeholder text with your actual details.</li>
        <li>Keep font and formatting consistent — do not change colors or sizes.</li>
        <li>Save as PDF before submitting to job portals for best ATS results.</li>
        <li>Keep resume to 1 page (Fresher) or max 2 pages (Experienced).</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ── Template Cards ─────────────────────────────────────────
TEMPLATES = [
    {
        "title":    "Fresher / Student",
        "icon":     "🎓",
        "color":    "#2E75B6",
        "desc":     "Perfect for final-year students and fresh graduates. Includes Objective, Education, Projects, Internship, and Certifications sections.",
        "best_for": "B.Tech / BCA / MCA Students, First Job",
        "file":     "templates/template_fresher.docx",
        "sections": ["Career Objective", "Education", "Technical Skills", "Projects", "Internships", "Certifications"],
    },
    {
        "title":    "Software Developer",
        "icon":     "💻",
        "color":    "#1a1a2e",
        "desc":     "Clean and professional template for developers with work experience. Highlights tech stack, projects, and measurable achievements.",
        "best_for": "Junior / Mid-level Developers, Full Stack, Backend",
        "file":     "templates/template_developer.docx",
        "sections": ["Summary", "Work Experience", "Technical Skills", "Projects", "Education", "Certifications"],
    },
    {
        "title":    "Data Scientist",
        "icon":     "📊",
        "color":    "#00695c",
        "desc":     "Specialized template for data science and ML roles. Showcases tools, models built, and business impact of your work.",
        "best_for": "Data Analyst, ML Engineer, AI Researcher",
        "file":     "templates/template_datascience.docx",
        "sections": ["Profile Summary", "Technical Skills", "Work Experience", "Projects", "Education", "Certifications"],
    },
    {
        "title":    "General / ATS Friendly",
        "icon":     "📋",
        "color":    "#333333",
        "desc":     "Simple, clean, ATS-optimized template for any role or domain. Best for anyone who wants maximum compatibility with job portals.",
        "best_for": "Any role, Any domain, Safe choice",
        "file":     "templates/template_general.docx",
        "sections": ["Summary", "Work Experience", "Education", "Skills", "Certifications", "Projects"],
    },
]

cols = st.columns(2)

for i, t in enumerate(TEMPLATES):
    with cols[i % 2]:
        # Read file bytes
        file_path = t["file"]
        file_exists = os.path.exists(file_path)

        sections_html = "".join(
            f'<span style="background:#21262d;color:#8b949e;padding:0.2rem 0.5rem;'
            f'border-radius:20px;font-size:0.75rem;margin:0.15rem;display:inline-block;">'
            f'{s}</span>'
            for s in t["sections"]
        )

        st.markdown(f"""
        <div style="background:#161b22;border:2px solid {t['color']};border-radius:14px;
                    padding:1.2rem 1.2rem 0.8rem;margin-bottom:1.2rem;">
            <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.5rem;">
                <span style="font-size:2rem">{t['icon']}</span>
                <div>
                    <div style="color:#e6edf3;font-weight:700;font-size:1.05rem;">{t['title']}</div>
                    <div style="color:{t['color']};font-size:0.78rem;font-weight:600;">Best for: {t['best_for']}</div>
                </div>
            </div>
            <p style="color:#8b949e;font-size:0.87rem;margin:0.5rem 0 0.8rem;">{t['desc']}</p>
            <div style="margin-bottom:0.8rem;"><b style="color:#e6edf3;font-size:0.82rem;">Sections included:</b><br>{sections_html}</div>
        </div>
        """, unsafe_allow_html=True)

        if file_exists:
            with open(file_path, "rb") as f:
                st.download_button(
                    label=f"⬇️ Download {t['title']} Template",
                    data=f.read(),
                    file_name=f"resume_template_{t['title'].lower().replace(' ','_').replace('/','_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                    key=f"dl_{i}"
                )
        else:
            st.warning(f"Template file not found: {file_path}")

        st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#30363d'>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align:center;color:#8b949e;font-size:0.82rem;'>
    All templates are in <b>.docx</b> format — open with Microsoft Word or Google Docs.
    After filling, export as PDF before uploading to job portals.
</p>
""", unsafe_allow_html=True)