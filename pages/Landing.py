import streamlit as st


def load_css():
    with open("styles/style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

# ── Nav Bar ────────────────────────────────────────────────
col_logo, _, col_b1, col_b2, col_b3 = st.columns([3, 3, 1.2, 1.2, 1.2])

with col_logo:
    st.markdown('<div class="nav-logo">📄 ResumeAI</div>', unsafe_allow_html=True)
with col_b1:
    if st.button("🔑 Login", use_container_width=True):
        st.switch_page("pages/Login.py")
with col_b2:
    if st.button("📝 Register", use_container_width=True):
        st.switch_page("pages/Register.py")
with col_b3:
    if st.button("🛡️ Admin", use_container_width=True):
        st.switch_page("pages/Admin.py")

st.markdown("<hr style='border-color:#30363d;margin:0.5rem 0 2rem'>", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <p class="eyebrow">✦ AI-Powered Career Intelligence</p>
    <h1 class="hero-title">Is Your Resume<br><span>Good Enough?</span></h1>
    <p class="hero-sub">
        Upload your resume and get instant AI feedback — ATS score, skill gaps,
        job role predictions, and personalized improvement tips.
    </p>
</div>
""", unsafe_allow_html=True)

# ── CTA Buttons ────────────────────────────────────────────
_, c1, c2, _ = st.columns([4, 1.5, 1.5, 4])
with c1:
    if st.button("🚀 Register Now", use_container_width=True):
        st.switch_page("pages/Register.py")
with c2:
    if st.button("🔑 Login", use_container_width=True, key="hero_login"):
        st.switch_page("pages/Login.py")

st.markdown("<br>", unsafe_allow_html=True)

# ── Domain Notice ──────────────────────────────────────────
st.markdown("""
<div style="max-width:680px;margin:0 auto 1.5rem auto;
            background:#1c2a1c;border:1px solid #3fb950;
            border-radius:12px;padding:0.8rem 1.2rem;
            display:flex;align-items:center;gap:0.8rem;text-align:left;">
    <span style="font-size:1.4rem">&#128161;</span>
    <span style="color:#3fb950;font-size:0.88rem;line-height:1.5;">
        <b>Currently optimized for IT &amp; Computer Science resumes</b> —
        Developer, Data Scientist, DevOps, Business Analyst &amp; more.
        Results may vary for non-IT domains.
    </span>
</div>
""", unsafe_allow_html=True)

# ── Feature Cards ──────────────────────────────────────────
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">ATS Score</div>
        <div class="feature-desc">Check how well your resume passes automated screening systems</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <div class="feature-title">Job Role Prediction</div>
        <div class="feature-desc">AI predicts the best-fit job categories based on your resume</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🛠️</div>
        <div class="feature-title">Skill Gap Analysis</div>
        <div class="feature-desc">Discover missing skills and what to learn next for your target role</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Resume Score</div>
        <div class="feature-desc">Get a comprehensive score with detailed feedback to improve</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### How It Works")

s1, s2, s3, s4 = st.columns(4)
for col, icon, title, desc in zip(
    [s1, s2, s3, s4],
    ["1️⃣", "2️⃣", "3️⃣", "4️⃣"],
    ["Register & Login", "Upload Resume", "AI Analysis", "Get Feedback"],
    ["Create your account with your details",
     "Upload your resume as a PDF file",
     "AI extracts skills and scores your resume",
     "Get detailed insights and tips to improve"]
):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#8b949e;font-size:0.82rem'>© 2025 ResumeAI · Built by Aishwarya Poojari</p>",
    unsafe_allow_html=True
)