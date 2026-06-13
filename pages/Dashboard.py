import streamlit as st
import re


def load_css():
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

# ── Auth Guard ─────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.warning("⚠️ Please log in first.")
    if st.button("Go to Login"):
        st.switch_page("pages/Login.py")
    st.stop()


def load_skills():
    try:
        with open("skills.txt") as f:
            return [s.strip().lower() for s in f if s.strip()]
    except FileNotFoundError:
        return ["python", "java", "html", "css", "javascript", "sql",
                "machine learning", "data science", "communication", "teamwork"]


SKILLS = load_skills()


def extract_text(uploaded_file):
    try:
        import pdfplumber
        with pdfplumber.open(uploaded_file) as pdf:
            return " ".join(page.extract_text() or "" for page in pdf.pages)
    except ImportError:
        st.error("Run: pip install pdfplumber")
        return ""
    except Exception as e:
        st.error(f"Could not read PDF: {e}")
        return ""


def analyse(text):
    t = text.lower()
    found   = [s for s in SKILLS if s in t]
    missing = [s for s in SKILLS if s not in t]

    skill_score   = min(len(found) / max(len(SKILLS), 1) * 40, 40)
    length_score  = min(len(text.split()) / 300 * 20, 20)
    sections      = ["education", "experience", "skills", "projects", "summary", "objective"]
    section_score = sum(5 for k in sections if k in t)
    contact_score = 10 if re.search(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", t) else 0
    total         = min(int(skill_score + length_score + section_score + contact_score), 100)

    roles = {
        "Data Scientist":   ["python", "machine learning", "data science", "pandas", "tensorflow"],
        "Web Developer":    ["html", "css", "javascript", "react", "node"],
        "Java Developer":   ["java", "spring", "hibernate", "maven"],
        "DevOps Engineer":  ["docker", "kubernetes", "aws", "linux"],
        "Business Analyst": ["business analysis", "requirements", "sql"],
        "HR Professional":  ["recruitment", "hr", "human resources"],
    }
    role_scores = {r: sum(1 for kw in kws if kw in t) for r, kws in roles.items()}
    predicted   = max(role_scores, key=role_scores.get) if any(role_scores.values()) else "General Professional"

    return {
        "found": found, "missing": missing[:8],
        "score": total, "ats": total >= 50,
        "role": predicted, "words": len(text.split())
    }


# ── Job Platforms by Role ───────────────────────────────────
JOB_PLATFORMS = {
    "Data Scientist": [
        {"name": "LinkedIn",     "url": "https://www.linkedin.com/jobs/search/?keywords=Data+Scientist",     "icon": "💼"},
        {"name": "Naukri",       "url": "https://www.naukri.com/data-scientist-jobs",                        "icon": "🔍"},
        {"name": "Kaggle Jobs",  "url": "https://www.kaggle.com/jobs",                                       "icon": "📊"},
        {"name": "Indeed",       "url": "https://in.indeed.com/jobs?q=data+scientist",                       "icon": "🌐"},
        {"name": "Internshala",  "url": "https://internshala.com/jobs/data-science-jobs",                    "icon": "🎓"},
    ],
    "Web Developer": [
        {"name": "LinkedIn",     "url": "https://www.linkedin.com/jobs/search/?keywords=Web+Developer",      "icon": "💼"},
        {"name": "Naukri",       "url": "https://www.naukri.com/web-developer-jobs",                         "icon": "🔍"},
        {"name": "Internshala",  "url": "https://internshala.com/jobs/web-development-jobs",                 "icon": "🎓"},
        {"name": "Indeed",       "url": "https://in.indeed.com/jobs?q=web+developer",                        "icon": "🌐"},
        {"name": "Freelancer",   "url": "https://www.freelancer.in/jobs/website-design/",                    "icon": "💻"},
    ],
    "Java Developer": [
        {"name": "LinkedIn",     "url": "https://www.linkedin.com/jobs/search/?keywords=Java+Developer",     "icon": "💼"},
        {"name": "Naukri",       "url": "https://www.naukri.com/java-developer-jobs",                        "icon": "🔍"},
        {"name": "HackerEarth",  "url": "https://www.hackerearth.com/jobs/",                                 "icon": "⚡"},
        {"name": "Indeed",       "url": "https://in.indeed.com/jobs?q=java+developer",                       "icon": "🌐"},
        {"name": "Glassdoor",    "url": "https://www.glassdoor.co.in/Job/java-developer-jobs-SRCH_KO0,14.htm","icon": "🏢"},
    ],
    "DevOps Engineer": [
        {"name": "LinkedIn",     "url": "https://www.linkedin.com/jobs/search/?keywords=DevOps+Engineer",    "icon": "💼"},
        {"name": "Naukri",       "url": "https://www.naukri.com/devops-engineer-jobs",                       "icon": "🔍"},
        {"name": "Indeed",       "url": "https://in.indeed.com/jobs?q=devops+engineer",                      "icon": "🌐"},
        {"name": "Glassdoor",    "url": "https://www.glassdoor.co.in/Job/devops-jobs-SRCH_KO0,6.htm",        "icon": "🏢"},
        {"name": "AngelList",    "url": "https://wellfound.com/role/r/devops-engineer",                      "icon": "🚀"},
    ],
    "Business Analyst": [
        {"name": "LinkedIn",     "url": "https://www.linkedin.com/jobs/search/?keywords=Business+Analyst",   "icon": "💼"},
        {"name": "Naukri",       "url": "https://www.naukri.com/business-analyst-jobs",                      "icon": "🔍"},
        {"name": "Indeed",       "url": "https://in.indeed.com/jobs?q=business+analyst",                     "icon": "🌐"},
        {"name": "Glassdoor",    "url": "https://www.glassdoor.co.in/Job/business-analyst-jobs-SRCH_KO0,16.htm","icon": "🏢"},
        {"name": "iimjobs",      "url": "https://www.iimjobs.com/j/business-analyst",                        "icon": "🎯"},
    ],
    "HR Professional": [
        {"name": "LinkedIn",     "url": "https://www.linkedin.com/jobs/search/?keywords=HR",                 "icon": "💼"},
        {"name": "Naukri",       "url": "https://www.naukri.com/hr-jobs",                                    "icon": "🔍"},
        {"name": "Shine",        "url": "https://www.shine.com/job-search/hr-jobs",                          "icon": "✨"},
        {"name": "Indeed",       "url": "https://in.indeed.com/jobs?q=hr",                                   "icon": "🌐"},
        {"name": "iimjobs",      "url": "https://www.iimjobs.com/j/human-resources",                         "icon": "🎯"},
    ],
    "General Professional": [
        {"name": "LinkedIn",     "url": "https://www.linkedin.com/jobs/",                                    "icon": "💼"},
        {"name": "Naukri",       "url": "https://www.naukri.com/",                                           "icon": "🔍"},
        {"name": "Indeed",       "url": "https://in.indeed.com/",                                            "icon": "🌐"},
        {"name": "Internshala",  "url": "https://internshala.com/jobs/",                                     "icon": "🎓"},
        {"name": "Glassdoor",    "url": "https://www.glassdoor.co.in/Job/index.htm",                         "icon": "🏢"},
    ],
}


# ── PDF Report Generator ────────────────────────────────────
def clean_text(text):
    """Remove emojis and non-latin characters that reportlab can't render."""
    import re
    return re.sub(r'[^\x00-\x7F]+', '', text).strip()


def generate_pdf_report(name, r, tips):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.units import cm
        import io

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)

        story = []

        title_style = ParagraphStyle("Title", fontSize=22, fontName="Helvetica-Bold",
                                     textColor=colors.HexColor("#7C3AED"), spaceAfter=4)
        sub_style   = ParagraphStyle("Sub",   fontSize=11, fontName="Helvetica",
                                     textColor=colors.HexColor("#555555"), spaceAfter=20)
        h2_style    = ParagraphStyle("H2",    fontSize=13, fontName="Helvetica-Bold",
                                     textColor=colors.HexColor("#7C3AED"), spaceBefore=14, spaceAfter=6)
        body_style  = ParagraphStyle("Body",  fontSize=10, fontName="Helvetica",
                                     textColor=colors.HexColor("#333333"), spaceAfter=4)
        footer_style= ParagraphStyle("Footer",fontSize=8,  fontName="Helvetica",
                                     textColor=colors.grey)

        # Title
        story.append(Paragraph("Resume Analysis Report", title_style))
        story.append(Paragraph(f"Prepared for: <b>{clean_text(name)}</b>", sub_style))

        # Summary Table
        ats_text  = "Passes ATS" if r["ats"] else "Fails ATS"
        score_lbl = "Strong"     if r["score"] >= 70 else ("Moderate" if r["score"] >= 45 else "Needs Work")

        data = [
            ["Metric",            "Result"],
            ["Resume Score",      f"{r['score']}/100  ({score_lbl})"],
            ["ATS Compatibility", ats_text],
            ["Predicted Role",    r["role"]],
            ["Word Count",        f"{r['words']} words"],
        ]
        t = Table(data, colWidths=[6*cm, 10*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0),  colors.HexColor("#7C3AED")),
            ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
            ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, -1), 10),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1),  [colors.HexColor("#f0f0f0"), colors.white]),
            ("GRID",          (0, 0), (-1, -1),  0.5, colors.HexColor("#cccccc")),
            ("PADDING",       (0, 0), (-1, -1),  8),
        ]))
        story.append(t)

        # Skills Detected
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph("Skills Detected", h2_style))
        story.append(Paragraph(", ".join(r["found"]) if r["found"] else "None detected", body_style))

        # Missing Skills
        story.append(Paragraph("Missing Skills", h2_style))
        story.append(Paragraph(", ".join(r["missing"]) if r["missing"] else "All key skills present!", body_style))

        # Suggestions
        story.append(Paragraph("Suggestions", h2_style))
        for tip in tips:
            story.append(Paragraph(f"- {clean_text(tip)}", body_style))

        story.append(Spacer(1, 0.8*cm))
        story.append(Paragraph("Generated by AI Resume Analyzer", footer_style))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    except Exception as e:
        st.error(f"PDF Error: {e}")
        return None


# ── Header ─────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns([6, 2, 2, 2])
with c1:
    st.markdown(f"👋 Welcome, {st.session_state.user_name}!")
    st.markdown("<p style='color:#6B7280'>Upload your resume for instant AI analysis</p>", unsafe_allow_html=True)
with c2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📄 Templates", use_container_width=True):
        st.switch_page("pages/Templates.py")
with c3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🛠️ Generator", use_container_width=True):
        st.switch_page("pages/Generator.py")
with c4:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("pages/Landing.py")

st.markdown("<hr style='border-color:rgba(139,92,246,0.14)'>", unsafe_allow_html=True)

# ── Upload ─────────────────────────────────────────────────
st.markdown("""
<div class="upload-card">
    <div style="font-size:3rem">📄</div>
    <h3 style="margin:0.5rem 0">Upload Your Resume</h3>
    <p style="color:#6B7280">PDF format only</p>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div style="background:#F0FFF4;border:1px solid rgba(22,163,74,0.35);border-radius:10px;
            padding:0.7rem 1rem;margin-bottom:1rem;display:flex;align-items:center;gap:0.6rem;">
    <span style="font-size:1.2rem">&#128161;</span>
    <span style="color:#16A34A;font-size:0.88rem;">
        <b>Note:</b> This analyzer is currently optimized for
        <b>IT &amp; Computer Science</b> domain resumes —
        including roles like Developer, Data Scientist, DevOps, and Business Analyst.
        Results may not be accurate for other domains.
    </span>
</div>""", unsafe_allow_html=True)

uploaded = st.file_uploader("Resume PDF", type=["pdf"], label_visibility="collapsed")

if uploaded:
    with st.spinner("🤖 Analysing your resume..."):
        text = extract_text(uploaded)

    if not text.strip():
        st.error("Could not extract text. Please check the PDF.")
        st.stop()

    r = analyse(text)

    st.markdown("📊 Analysis Results", unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    s   = r["score"]
    cls = "score-high" if s >= 70 else ("score-mid" if s >= 45 else "score-low")
    lbl = "Strong ✅"  if s >= 70 else ("Moderate ⚠️" if s >= 45 else "Needs Work ❌")

    with m1:
        st.markdown(f"""<div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Resume Score</div>
            <span class="score-badge {cls}">{s}/100 · {lbl}</span>
        </div>""", unsafe_allow_html=True)
    with m2:
        ats_txt = "✅ Passes ATS" if r["ats"] else "❌ Fails ATS"
        clr     = "#3fb950"       if r["ats"] else "#f85149"
        st.markdown(f"""<div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">ATS Compatibility</div>
            <span style="color:{clr};font-weight:700">{ats_txt}</span>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="feature-card">
            <div class="feature-icon">💼</div>
            <div class="feature-title">Predicted Role</div>
            <span style="color:#7C3AED;font-weight:600">{r['role']}</span>
        </div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""<div class="feature-card">
            <div class="feature-icon">📝</div>
            <div class="feature-title">Word Count</div>
            <span style="color:#1E1245;font-weight:600">{r['words']} words</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cf, cm = st.columns(2)
    with cf:
        st.markdown("✅ Skills Detected")
        if r["found"]:
            st.markdown(" ".join(f'<span class="skill-tag">{s}</span>' for s in r["found"]), unsafe_allow_html=True)
        else:
            st.info("No matching skills found.")
    with cm:
        st.markdown("❌ Missing Skills")
        if r["missing"]:
            st.markdown(" ".join(f'<span class="skill-tag missing">{s}</span>' for s in r["missing"]), unsafe_allow_html=True)
        else:
            st.success("All key skills present! 🎉")

    # ── NEW: Learn Missing Skills ───────────────────────────
    if r["missing"]:
        st.markdown("<hr style='border-color:rgba(139,92,246,0.14)'>", unsafe_allow_html=True)
        st.markdown("### 📚 Learn Your Missing Skills")
        st.markdown("<p style='color:#6B7280'>Free & paid resources to learn each missing skill — click any platform to start learning:</p>",
                    unsafe_allow_html=True)

        SKILL_COURSES = {
            "python": [
                {"platform": "YouTube",        "url": "https://www.youtube.com/results?search_query=python+tutorial+for+beginners", "color": "#E95858"},
                {"platform": "W3Schools",       "url": "https://www.w3schools.com/python/",                                         "color": "#55C39A"},
                {"platform": "Coursera",        "url": "https://www.coursera.org/learn/python",                                     "color": "#669AE2"},
                {"platform": "Udemy",           "url": "https://www.udemy.com/topic/python/",                                       "color": "#C792EA"},
                {"platform": "GeeksforGeeks",   "url": "https://www.geeksforgeeks.org/python-programming-language/",                "color": "#67B079"},
            ],
            "java": [
                {"platform": "YouTube",        "url": "https://www.youtube.com/results?search_query=java+tutorial+for+beginners",  "color": "#E95858"},
                {"platform": "W3Schools",       "url": "https://www.w3schools.com/java/",                                          "color": "#55C39A"},
                {"platform": "Coursera",        "url": "https://www.coursera.org/learn/java-programming",                          "color": "#669AE2"},
                {"platform": "Udemy",           "url": "https://www.udemy.com/topic/java/",                                        "color": "#C792EA"},
                {"platform": "GeeksforGeeks",   "url": "https://www.geeksforgeeks.org/java/",                                      "color": "#67B079"},
            ],
            "c": [
                {"platform": "YouTube",        "url": "https://www.youtube.com/results?search_query=c+programming+tutorial",       "color": "#E95858"},
                {"platform": "W3Schools",       "url": "https://www.w3schools.com/c/",                                             "color": "#55C39A"},
                {"platform": "GeeksforGeeks",   "url": "https://www.geeksforgeeks.org/c-programming-language/",                    "color": "#67B079"},
                {"platform": "Udemy",           "url": "https://www.udemy.com/topic/c-programming/",                               "color": "#C792EA"},
            ],
            "c++": [
                {"platform": "YouTube",        "url": "https://www.youtube.com/results?search_query=c%2B%2B+tutorial+for+beginners","color": "#E95858"},
                {"platform": "W3Schools",       "url": "https://www.w3schools.com/cpp/",                                           "color": "#55C39A"},
                {"platform": "GeeksforGeeks",   "url": "https://www.geeksforgeeks.org/c-plus-plus/",                               "color": "#67B079"},
                {"platform": "Udemy",           "url": "https://www.udemy.com/topic/c-plus-plus/",                                 "color": "#C792EA"},
            ],
            "html": [
                {"platform": "YouTube",        "url": "https://www.youtube.com/results?search_query=html+tutorial+for+beginners",  "color": "#E66363"},
                {"platform": "W3Schools",       "url": "https://www.w3schools.com/html/",                                          "color": "#55C39A"},
                {"platform": "MDN Docs",        "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML",                      "color": "#FF6900"},
                {"platform": "freeCodeCamp",    "url": "https://www.freecodecamp.org/learn/responsive-web-design/",                "color": "#006400"},
            ],
            "css": [
                {"platform": "YouTube",        "url": "https://www.youtube.com/results?search_query=css+tutorial+for+beginners",   "color": "#E66363"},
                {"platform": "W3Schools",       "url": "https://www.w3schools.com/css/",                                           "color": "#55C39A"},
                {"platform": "MDN Docs",        "url": "https://developer.mozilla.org/en-US/docs/Learn/CSS",                       "color": "#D47A39"},
                {"platform": "freeCodeCamp",    "url": "https://www.freecodecamp.org/learn/responsive-web-design/",                "color": "#709D70"},
            ],
            "javascript": [
                {"platform": "YouTube",        "url": "https://www.youtube.com/results?search_query=javascript+tutorial+beginners","color": "#E95858"},
                {"platform": "W3Schools",       "url": "https://www.w3schools.com/js/",                                            "color": "#55C39A"},
                {"platform": "Coursera",        "url": "https://www.coursera.org/learn/javascript-basics",                         "color": "#669AE2"},
                {"platform": "freeCodeCamp",    "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/","color": "#5F6F5F"},
                {"platform": "Udemy",           "url": "https://www.udemy.com/topic/javascript/",                                  "color": "#C792EA"},
            ],
            "sql": [
                {"platform": "YouTube",        "url": "https://www.youtube.com/results?search_query=sql+tutorial+for+beginners",   "color": "#E95858"},
                {"platform": "W3Schools",       "url": "https://www.w3schools.com/sql/",                                           "color": "#55C39A"},
                {"platform": "Coursera",        "url": "https://www.coursera.org/learn/sql-for-data-science",                      "color": "#669AE2"},
                {"platform": "GeeksforGeeks",   "url": "https://www.geeksforgeeks.org/sql-tutorial/",                              "color": "#67B079"},
            ],
            "machine learning": [
                {"platform": "YouTube",        "url": "https://www.youtube.com/results?search_query=machine+learning+tutorial",    "color": "#E95858"},
                {"platform": "Coursera",        "url": "https://www.coursera.org/learn/machine-learning",                          "color": "#669AE2"},
                {"platform": "Udemy",           "url": "https://www.udemy.com/topic/machine-learning/",                            "color": "#C792EA"},
                {"platform": "GeeksforGeeks",   "url": "https://www.geeksforgeeks.org/machine-learning/",                          "color": "#67B079"},
                {"platform": "fast.ai",         "url": "https://www.fast.ai/",                                                     "color": "#b47e7e"},
            ],
            "data science": [
                {"platform": "YouTube",        "url": "https://www.youtube.com/results?search_query=data+science+tutorial",        "color": "#E95858"},
                {"platform": "Coursera",        "url": "https://www.coursera.org/specializations/jhu-data-science",                "color": "#669AE2"},
                {"platform": "Kaggle",          "url": "https://www.kaggle.com/learn",                                             "color": "#20BEFF"},
                {"platform": "Udemy",           "url": "https://www.udemy.com/topic/data-science/",                                "color": "#C792EA"},
                {"platform": "GeeksforGeeks",   "url": "https://www.geeksforgeeks.org/data-science-tutorial/",                     "color": "#67B079"},
            ],
            "communication": [
                {"platform": "YouTube",        "url": "https://www.youtube.com/results?search_query=communication+skills+training","color": "#E95858"},
                {"platform": "Coursera",        "url": "https://www.coursera.org/learn/communication-skills",                      "color": "#669AE2"},
                {"platform": "Udemy",           "url": "https://www.udemy.com/topic/communication-skills/",                        "color": "#C792EA"},
            ],
            "teamwork": [
                {"platform": "YouTube",        "url": "https://www.youtube.com/results?search_query=teamwork+skills",              "color": "#E95858"},
                {"platform": "Coursera",        "url": "https://www.coursera.org/learn/teamwork-skills",                           "color": "#669AE2"},
                {"platform": "Udemy",           "url": "https://www.udemy.com/topic/teamwork/",                                    "color": "#C792EA"},
            ],
            "problem solving": [
                {"platform": "YouTube",        "url": "https://www.youtube.com/results?search_query=problem+solving+skills",       "color": "#E95858"},
                {"platform": "Coursera",        "url": "https://www.coursera.org/learn/creative-problem-solving",                  "color": "#669AE2"},
                {"platform": "GeeksforGeeks",   "url": "https://www.geeksforgeeks.org/problem-solving/",                           "color": "#67B079"},
            ],
        }

        for skill in r["missing"]:
            courses = SKILL_COURSES.get(skill.lower(), [
                {"platform": "YouTube",       "url": "https://www.youtube.com/results?search_query=" + skill.replace(' ', '+') + "+tutorial", "color": "#E95858"},
                {"platform": "Udemy",         "url": "https://www.udemy.com/courses/search/?q="      + skill.replace(' ', '+'),               "color": "#C792EA"},
                {"platform": "Coursera",      "url": "https://www.coursera.org/search?query="        + skill.replace(' ', '+'),               "color": "#669AE2"},
                {"platform": "GeeksforGeeks", "url": "https://www.geeksforgeeks.org/search/?q="      + skill.replace(' ', '+'),               "color": "#67B079"},
            ])

            # Build button HTML separately to avoid nested quote issues
            buttons_html = ""
            for c in courses:
                buttons_html += (
                    '<a href="' + c["url"] + '" target="_blank" style="text-decoration:none;">'
                    '<span style="background:' + c["color"] + ';color:#fff;padding:0.25rem 0.7rem;'
                    'border-radius:20px;font-size:0.75rem;font-weight:600;white-space:nowrap;">'
                    + c["platform"] +
                    '</span></a>'
                )

            row_html = (
                '<div style="background:#FAF8FF;border:1px solid rgba(139,92,246,0.14);border-radius:10px;'
                'padding:0.8rem 1rem;margin-bottom:0.6rem;display:flex;'
                'align-items:center;flex-wrap:wrap;gap:0.5rem;">'
                '<span style="color:#1E1245;font-weight:700;font-size:0.95rem;min-width:140px;">'
                '&#10060; ' + skill.title() + '</span>'
                '<span style="color:#6B7280;font-size:0.8rem;margin-right:0.5rem;">Learn on:</span>'
                + buttons_html +
                '</div>'
            )
            st.markdown(row_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("💡 Suggestions")
    tips = []
    if r["words"] < 200:  tips.append("📌 Resume too short — add more project/experience details.")
    if r["words"] > 700:  tips.append("✂️ Resume too long — try to keep under 700 words.")
    if not r["ats"]:      tips.append("🤖 Add more job-relevant keywords to pass ATS.")
    if len(r["found"]) < 5: tips.append("🛠️ Add more technical skills to your resume.")
    if "education"  not in text.lower(): tips.append("🎓 Add an Education section.")
    if "project"    not in text.lower(): tips.append("🚀 Add a Projects section.")
    if not re.search(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", text.lower()):
        tips.append("Make sure your email is visible.")
    if not tips: tips.append(" Great resume! Keep it updated.")
    for tip in tips:
        st.markdown(f"- {tip}")

    if r["found"]:
        st.markdown("📈 Skill Coverage")
        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(4, 4))
            fig.patch.set_facecolor("#FAF8FF")
            ax.set_facecolor("#F0EEFF")
            ax.pie(
                [len(r["found"]), len(r["missing"])],
                labels=["Found", "Missing"],
                colors=["#8B5CF6", "#C4B5FD"],
                autopct="%1.0f%%",
                textprops={"color": "#1E1245"},
                startangle=90
            )
            ax.set_title("Skill Coverage", color="#1E1245", fontweight="bold")
            st.pyplot(fig)
        except ImportError:
            st.info("pip install matplotlib for the chart")

    # ── Resume Templates ────────────────────────────────────
    st.markdown("<hr style='border-color:rgba(139,92,246,0.14)'>", unsafe_allow_html=True)
    st.markdown("### 📄 Resume Templates")
    st.markdown("<p style='color:#6B7280'>Not happy with your resume format? Download a professional ATS-friendly template and rebuild it.</p>",
                unsafe_allow_html=True)

    TEMPLATES = [
        {"title": "Fresher / Student",   "icon": "🎓", "color": "#2E75B6", "file": "templates/template_fresher.docx",     "best_for": "Students, First Job"},
        {"title": "Software Developer",  "icon": "💻", "color": "#8B5CF6", "file": "templates/template_developer.docx",   "best_for": "Junior / Mid Developers"},
        {"title": "Data Scientist",      "icon": "📊", "color": "#00695c", "file": "templates/template_datascience.docx", "best_for": "ML / AI / Data Roles"},
        {"title": "General / ATS Safe",  "icon": "📋", "color": "#6B7280", "file": "templates/template_general.docx",     "best_for": "Any Role / Any Domain"},
    ]

    import os
    tcols = st.columns(4)
    for i, t in enumerate(TEMPLATES):
        with tcols[i]:
            st.markdown(
                '<div style="background:#FAF8FF;border:2px solid ' + t["color"] + ';border-radius:12px;'
                'padding:1rem 0.8rem;text-align:center;margin-bottom:0.5rem;">'
                '<div style="font-size:2rem">' + t["icon"] + '</div>'
                '<div style="color:#1E1245;font-weight:700;font-size:0.88rem;margin:0.4rem 0;">' + t["title"] + '</div>'
                '<div style="color:' + t["color"] + ';font-size:0.74rem;margin-bottom:0.6rem;">Best for: ' + t["best_for"] + '</div>'
                '</div>',
                unsafe_allow_html=True
            )
            if os.path.exists(t["file"]):
                with open(t["file"], "rb") as f:
                    st.download_button(
                        label="⬇️ Download",
                        data=f.read(),
                        file_name="resume_" + t["title"].lower().replace(" ","_").replace("/","_") + ".docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                        key="tmpl_" + str(i)
                    )
            else:
                st.caption("File not found")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── NEW: Download Report as PDF ─────────────────────────
    st.markdown("<hr style='border-color:rgba(139,92,246,0.14)'>", unsafe_allow_html=True)
    st.markdown("### 📥 Download Your Report")

    pdf_bytes = generate_pdf_report(st.session_state.user_name, r, tips)

    if pdf_bytes:
        st.download_button(
            label="⬇️ Download Resume Analysis Report (PDF)",
            data=pdf_bytes,
            file_name=f"resume_report_{st.session_state.user_name.replace(' ','_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.warning("⚠️ To enable PDF download, run: `pip install reportlab`")

    # ── NEW: Job Platform Recommendations ──────────────────
    st.markdown("<hr style='border-color:rgba(139,92,246,0.14)'>", unsafe_allow_html=True)
    st.markdown(f"### 🚀 Apply for Jobs — Recommended Platforms for **{r['role']}**")
    st.markdown("<p style='color:#6B7280'>Based on your predicted role, here are the best platforms to find jobs:</p>",
                unsafe_allow_html=True)

    platforms = JOB_PLATFORMS.get(r["role"], JOB_PLATFORMS["General Professional"])

    cols = st.columns(len(platforms))
    for i, p in enumerate(platforms):
        with cols[i]:
            st.markdown(f"""
            <a href="{p['url']}" target="_blank" style="text-decoration:none;">
                <div style="
                    background:#FAF8FF;
                    border:1px solid rgba(139,92,246,0.14);
                    border-radius:12px;
                    padding:1rem 0.5rem;
                    text-align:center;
                    cursor:pointer;
                    transition:border-color 0.2s;
                " onmouseover="this.style.borderColor='#8B5CF6'"
                   onmouseout="this.style.borderColor='rgba(139,92,246,0.14)'">
                    <div style="font-size:1.8rem">{p['icon']}</div>
                    <div style="color:#1E1245;font-weight:600;font-size:0.85rem;margin-top:0.4rem">{p['name']}</div>
                    <div style="color:#7C3AED;font-size:0.75rem;margin-top:0.2rem">Apply Now →</div>
                </div>
            </a>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 Tip: Keep your LinkedIn profile updated — most recruiters check it first!")

    # ── Interview Questions Generator ───────────────────────
    st.markdown("<hr style='border-color:rgba(139,92,246,0.14)'>", unsafe_allow_html=True)
    st.markdown(f"### 🎯 Interview Questions for **{r['role']}**")
    st.markdown("<p style='color:#6B7280'>Prepare for your next interview with these commonly asked questions for your predicted role.</p>",
                unsafe_allow_html=True)

    INTERVIEW_QUESTIONS = {
        "Data Scientist": {
            "technical": [
                "What is the difference between supervised and unsupervised learning?",
                "Explain overfitting and how you would prevent it.",
                "What is the difference between L1 and L2 regularization?",
                "How does a Random Forest algorithm work?",
                "What is the purpose of cross-validation?",
                "Explain the bias-variance tradeoff.",
                "What is TF-IDF and where is it used?",
                "How would you handle missing data in a dataset?",
                "What is the difference between Precision and Recall?",
                "Explain the working of a Neural Network.",
            ],
            "hr": [
                "Tell me about yourself and your experience in data science.",
                "Describe a data science project you are most proud of.",
                "How do you explain complex data findings to non-technical stakeholders?",
                "How do you stay updated with the latest trends in AI and ML?",
                "Describe a situation where your analysis led to a business decision.",
            ]
        },
        "Web Developer": {
            "technical": [
                "What is the difference between HTML, CSS, and JavaScript?",
                "Explain the CSS Box Model.",
                "What is the difference between GET and POST requests?",
                "What are React hooks and why are they used?",
                "Explain the concept of RESTful APIs.",
                "What is the difference between localStorage and sessionStorage?",
                "How does the DOM work in a browser?",
                "What is CORS and how do you handle it?",
                "Explain the difference between == and === in JavaScript.",
                "What is responsive design and how do you achieve it?",
            ],
            "hr": [
                "Tell me about yourself and your web development experience.",
                "Describe a challenging web project you built and how you solved problems.",
                "How do you keep up with new web technologies and frameworks?",
                "How do you handle feedback during code reviews?",
                "Describe your experience working in an Agile team.",
            ]
        },
        "Java Developer": {
            "technical": [
                "What is the difference between JDK, JRE, and JVM?",
                "Explain the four pillars of Object-Oriented Programming.",
                "What is the difference between an Abstract class and an Interface?",
                "How does garbage collection work in Java?",
                "What is multithreading and how is it implemented in Java?",
                "Explain the difference between ArrayList and LinkedList.",
                "What is the purpose of the final keyword in Java?",
                "How does Exception Handling work in Java?",
                "What is Spring Boot and why is it used?",
                "Explain the concept of Design Patterns with an example.",
            ],
            "hr": [
                "Tell me about yourself and your Java development experience.",
                "Describe the most complex Java application you have built.",
                "How do you approach debugging a production issue?",
                "How do you handle tight deadlines in a project?",
                "Describe your experience working with a team on a large codebase.",
            ]
        },
        "DevOps Engineer": {
            "technical": [
                "What is the difference between Continuous Integration and Continuous Deployment?",
                "Explain how Docker containers work.",
                "What is Kubernetes and why is it used?",
                "How does a CI/CD pipeline work?",
                "What is Infrastructure as Code (IaC)?",
                "Explain the difference between Docker and a Virtual Machine.",
                "What is the purpose of load balancing?",
                "How do you monitor application performance in production?",
                "What is the difference between Git merge and Git rebase?",
                "How does AWS EC2 differ from AWS Lambda?",
            ],
            "hr": [
                "Tell me about yourself and your DevOps experience.",
                "Describe a major production incident you resolved.",
                "How do you handle communication between development and operations teams?",
                "How do you prioritize tasks when multiple systems are down?",
                "Describe your experience with cloud platforms.",
            ]
        },
        "Business Analyst": {
            "technical": [
                "What is the difference between functional and non-functional requirements?",
                "Explain the Software Development Life Cycle (SDLC).",
                "What is a Use Case diagram and when is it used?",
                "How do you gather requirements from stakeholders?",
                "What is the difference between a BRD and an FRD?",
                "How do you prioritize requirements when resources are limited?",
                "What is Agile methodology and how does it differ from Waterfall?",
                "How do you handle conflicting requirements from different stakeholders?",
                "What tools do you use for requirement management?",
                "How do you validate that a delivered solution meets business requirements?",
            ],
            "hr": [
                "Tell me about yourself and your experience as a Business Analyst.",
                "Describe a project where you successfully gathered and managed requirements.",
                "How do you handle stakeholders who frequently change requirements?",
                "Describe a time when you identified a process improvement opportunity.",
                "How do you communicate technical concepts to non-technical teams?",
            ]
        },
        "HR Professional": {
            "technical": [
                "What is the end-to-end recruitment process?",
                "How do you source candidates for difficult-to-fill positions?",
                "What is the difference between training and development?",
                "How do you handle employee performance management?",
                "What are the key components of an effective onboarding program?",
                "How do you calculate employee attrition rate?",
                "What is competency-based interviewing?",
                "How do you ensure compliance with labor laws and regulations?",
                "What HR metrics do you track and why?",
                "How do you handle workplace conflict resolution?",
            ],
            "hr": [
                "Tell me about yourself and your HR experience.",
                "Describe a challenging recruitment situation you successfully handled.",
                "How do you maintain confidentiality in sensitive HR matters?",
                "How do you stay updated with changing labor laws and HR trends?",
                "Describe a time when you improved an HR process in your organization.",
            ]
        },
        "General Professional": {
            "technical": [
                "What technical skills are most relevant to this role?",
                "How do you approach learning a new tool or technology?",
                "Describe your experience with project management tools.",
                "How do you ensure quality in your work deliverables?",
                "What is your experience with data analysis or reporting?",
                "How do you handle working with cross-functional teams?",
                "Describe your experience with documentation and reporting.",
                "What productivity tools do you use regularly?",
                "How do you manage deadlines when handling multiple tasks?",
                "Describe a technical challenge you faced and how you solved it.",
            ],
            "hr": [
                "Tell me about yourself and your professional background.",
                "What are your greatest strengths and areas for improvement?",
                "Where do you see yourself in 5 years?",
                "How do you handle working under pressure?",
                "Describe a time when you went above and beyond at work.",
            ]
        },
    }

    questions = INTERVIEW_QUESTIONS.get(r["role"], INTERVIEW_QUESTIONS["General Professional"])

    tab1, tab2 = st.tabs(["💻 Technical Questions", "🤝 HR / Behavioral Questions"])

    with tab1:
        for i, q in enumerate(questions["technical"], 1):
            st.markdown(
                '<div style="background:#FAF8FF;border-left:4px solid #2E75B6;'
                'border-radius:0 8px 8px 0;padding:0.7rem 1rem;margin-bottom:0.5rem;">'
                '<span style="color:#7C3AED;font-weight:700;margin-right:0.5rem;">Q' + str(i) + '.</span>'
                '<span style="color:#1E1245;font-size:0.92rem;">' + q + '</span>'
                '</div>',
                unsafe_allow_html=True
            )

    with tab2:
        for i, q in enumerate(questions["hr"], 1):
            st.markdown(
                '<div style="background:#FAF8FF;border-left:4px solid #8B5CF6;'
                'border-radius:0 8px 8px 0;padding:0.7rem 1rem;margin-bottom:0.5rem;">'
                '<span style="color:#7C3AED;font-weight:700;margin-right:0.5rem;">Q' + str(i) + '.</span>'
                '<span style="color:#1E1245;font-size:0.92rem;">' + q + '</span>'
                '</div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 Tip: Practice answering these questions out loud — confidence matters as much as the answer!")

else:
    st.markdown("""
    <div style="text-align:center;padding:3rem;color:#6B7280">
        <div style="font-size:4rem">⬆️</div>
        <p>Upload a PDF resume above to begin</p>
    </div>""", unsafe_allow_html=True)