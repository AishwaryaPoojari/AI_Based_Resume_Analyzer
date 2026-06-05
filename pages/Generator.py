import streamlit as st
import subprocess
import tempfile
import os
import json


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
c1, c2, c3 = st.columns([7, 2, 2])
with c1:
    st.markdown("## 🛠️ Resume Generator")
    st.markdown("<p style='color:#8b949e'>Fill in the details below and download your generated resume as a DOCX file.</p>",
                unsafe_allow_html=True)
with c2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
with c3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("pages/Landing.py")

st.markdown("<hr style='border-color:#30363d'>", unsafe_allow_html=True)

# ── Info banner ────────────────────────────────────────────
st.markdown("""
<div style="background:#1c2438;border:1px solid #1f6feb;border-radius:10px;
            padding:0.8rem 1.2rem;margin-bottom:1.5rem;">
    <b style="color:#58a6ff;">&#128161; How it works:</b>
    <span style="color:#8b949e;font-size:0.87rem;">
        Your basic info is pre-filled from your account. Just add your skills,
        projects, and education — then click Generate to download your resume!
    </span>
</div>
""", unsafe_allow_html=True)

# ── Resume Color Theme ─────────────────────────────────────
st.markdown("### 🎨 Choose Resume Color Theme")
theme_col1, theme_col2, theme_col3, theme_col4 = st.columns(4)
with theme_col1:
    if st.button("🔵 Blue (Default)", use_container_width=True):
        st.session_state.resume_color = "2E75B6"
with theme_col2:
    if st.button("🟢 Green", use_container_width=True):
        st.session_state.resume_color = "00695c"
with theme_col3:
    if st.button("⚫ Dark", use_container_width=True):
        st.session_state.resume_color = "1a1a2e"
with theme_col4:
    if st.button("🔴 Maroon", use_container_width=True):
        st.session_state.resume_color = "7b0000"

chosen_color = st.session_state.get("resume_color", "2E75B6")
color_names  = {"2E75B6": "Blue", "00695c": "Green", "1a1a2e": "Dark", "7b0000": "Maroon"}
st.markdown(
    "<p style='color:#8b949e;font-size:0.82rem;margin-top:0.3rem;'>Selected theme: <b style='color:#e6edf3;'>"
    + color_names.get(chosen_color, "Blue") + "</b></p>",
    unsafe_allow_html=True
)

st.markdown("<hr style='border-color:#30363d'>", unsafe_allow_html=True)

# ── Section 1: Personal Info (pre-filled) ─────────────────
st.markdown("### 👤 Personal Details")
st.markdown("<p style='color:#8b949e;font-size:0.85rem;'>Basic info is pre-filled from your account. Edit if needed.</p>",
            unsafe_allow_html=True)

p1, p2 = st.columns(2)
with p1:
    name  = st.text_input("Full Name *", value=st.session_state.get("user_name", ""))
    email = st.text_input("Email *",     value=st.session_state.get("user_email", ""))
with p2:
    phone    = st.text_input("Phone Number", placeholder="+91 9000000000")
    linkedin = st.text_input("LinkedIn URL", placeholder="linkedin.com/in/yourname")

github = st.text_input("GitHub URL (optional)", placeholder="github.com/yourname")

st.markdown("<hr style='border-color:#30363d'>", unsafe_allow_html=True)

# ── Section 2: Professional Info (pre-filled) ─────────────
st.markdown("### 💼 Professional Details")

pr1, pr2 = st.columns(2)
with pr1:
    occupation = st.text_input("Current Occupation *",
                               value=st.session_state.get("user_occupation", ""))
    experience = st.text_input("Experience Level *",
                               value=st.session_state.get("user_experience", ""))
with pr2:
    department = st.text_input("Department / Field *",
                               value=st.session_state.get("user_department", ""))

summary = st.text_area("Professional Summary *",
                        placeholder="Write 2-3 sentences about yourself, your skills, and your career goal.",
                        height=100)

st.markdown("<hr style='border-color:#30363d'>", unsafe_allow_html=True)

# ── Section 3: Education ───────────────────────────────────
st.markdown("### 🎓 Education")
st.markdown("<p style='color:#8b949e;font-size:0.85rem;'>Add up to 2 education entries.</p>",
            unsafe_allow_html=True)

education = []
for idx in range(2):
    label = "Primary" if idx == 0 else "Secondary (optional)"
    with st.expander(f"📚 {label} Education", expanded=(idx == 0)):
        e1, e2 = st.columns(2)
        with e1:
            degree  = st.text_input("Degree / Course",   placeholder="B.Tech Computer Science", key=f"deg_{idx}")
            college = st.text_input("College / University", placeholder="Your University Name",  key=f"col_{idx}")
        with e2:
            year  = st.text_input("Year",  placeholder="2021 – 2025", key=f"yr_{idx}")
            grade = st.text_input("Grade / CGPA", placeholder="8.5 / 10", key=f"gr_{idx}")
        education.append({"degree": degree, "college": college, "year": year, "grade": grade})

st.markdown("<hr style='border-color:#30363d'>", unsafe_allow_html=True)

# ── Section 4: Skills ──────────────────────────────────────
st.markdown("### 🛠️ Skills")

sk1, sk2 = st.columns(2)
with sk1:
    skills = st.text_input("Technical Skills *",
                            placeholder="Python, Java, HTML, CSS, JavaScript, SQL")
with sk2:
    softskills = st.text_input("Soft Skills",
                               placeholder="Communication, Teamwork, Problem Solving")

st.markdown("<hr style='border-color:#30363d'>", unsafe_allow_html=True)

# ── Section 5: Projects ────────────────────────────────────
st.markdown("### 🚀 Projects")
st.markdown("<p style='color:#8b949e;font-size:0.85rem;'>Add up to 3 projects. Put each point on a new line.</p>",
            unsafe_allow_html=True)

projects = []
for idx in range(3):
    label = f"Project {idx+1}" + (" *" if idx == 0 else " (optional)")
    with st.expander(f"💡 {label}", expanded=(idx == 0)):
        proj_name = st.text_input("Project Name", placeholder="AI Resume Analyzer", key=f"pname_{idx}")
        proj_desc = st.text_area("Description (one point per line)",
                                 placeholder="Built a web app using Python and Streamlit\nImplemented ML model for job role prediction",
                                 height=80, key=f"pdesc_{idx}")
        proj_tech = st.text_input("Tech Stack", placeholder="Python, Streamlit, Scikit-learn", key=f"ptech_{idx}")
        projects.append({"name": proj_name, "description": proj_desc, "tech": proj_tech})

st.markdown("<hr style='border-color:#30363d'>", unsafe_allow_html=True)

# ── Section 6: Certifications ──────────────────────────────
st.markdown("### 🏆 Certifications & Achievements (optional)")
certifications = st.text_area("One per line",
                               placeholder="Python for Everybody — Coursera (2024)\nMachine Learning — Andrew Ng (2024)",
                               height=80)

st.markdown("<hr style='border-color:#30363d'>", unsafe_allow_html=True)

# ── Generate Button ────────────────────────────────────────
st.markdown("### ⚡ Generate Resume")

if st.button("🛠️ Generate My Resume", use_container_width=True, type="primary"):

    # Validation
    errors = []
    if not name.strip():       errors.append("Full Name is required.")
    if not email.strip():      errors.append("Email is required.")
    if not occupation.strip(): errors.append("Occupation is required.")
    if not department.strip(): errors.append("Department is required.")
    if not summary.strip():    errors.append("Professional Summary is required.")
    if not skills.strip():     errors.append("At least Technical Skills are required.")
    if not projects[0]["name"].strip(): errors.append("At least 1 Project is required.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        with st.spinner("⚙️ Building your resume..."):

            # Build data payload
            data = {
                "name":           name.strip(),
                "email":          email.strip(),
                "phone":          phone.strip(),
                "linkedin":       linkedin.strip(),
                "github":         github.strip(),
                "occupation":     occupation.strip(),
                "department":     department.strip(),
                "experience":     experience.strip(),
                "summary":        summary.strip(),
                "education":      [e for e in education if e["degree"].strip()],
                "skills":         skills.strip(),
                "softskills":     softskills.strip(),
                "projects":       [p for p in projects if p["name"].strip()],
                "certifications": certifications.strip(),
                "color":          chosen_color,
            }

            # Write JS generator script
            js_script = r"""
const {
  Document, Packer, Paragraph, TextRun,
  AlignmentType, BorderStyle, LevelFormat
} = require('docx');
const fs = require('fs');

const dataPath   = process.argv[2];
const outputPath = process.argv[3];
const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

const BULLETS = {
  numbering: { config: [{ reference: "bullets", levels: [{
    level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 360, hanging: 360 } } }
  }]}]}
};

function hr(color) {
  return new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: color || "2E75B6", space: 1 } },
    spacing: { after: 100 }
  });
}
function section(text, color) {
  return new Paragraph({
    children: [new TextRun({ text: text.toUpperCase(), bold: true, size: 22, color: color || "2E75B6", font: "Arial" })],
    spacing: { before: 200, after: 80 }
  });
}
function body(text) {
  return new Paragraph({
    children: [new TextRun({ text, size: 20, font: "Arial" })],
    spacing: { after: 60 }
  });
}
function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    children: [new TextRun({ text, size: 20, font: "Arial" })],
    spacing: { after: 50 }
  });
}
function boldVal(label, val) {
  return new Paragraph({
    children: [
      new TextRun({ text: label + ": ", bold: true, size: 20, font: "Arial" }),
      new TextRun({ text: val, size: 20, font: "Arial" })
    ],
    spacing: { after: 60 }
  });
}

const color = data.color || "2E75B6";
const children = [];

// Name
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 50 },
  children: [new TextRun({ text: data.name.toUpperCase(), bold: true, size: 44, font: "Arial", color })]
}));

// Contact
const contact = [data.email, data.phone, data.linkedin, data.github].filter(Boolean).join("  |  ");
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 40 },
  children: [new TextRun({ text: contact, size: 18, font: "Arial", color: "555555" })]
}));

// Role line
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: data.occupation + "  |  " + data.department, size: 20, font: "Arial", color: "777777", italics: true })]
}));

children.push(hr(color));

// Summary
if (data.summary) {
  children.push(section("Professional Summary", color));
  children.push(body(data.summary));
  children.push(hr(color));
}

// Education
if (data.education && data.education.length > 0) {
  children.push(section("Education", color));
  for (const e of data.education) {
    if (e.degree) {
      children.push(new Paragraph({
        children: [new TextRun({ text: e.degree, bold: true, size: 22, font: "Arial" })],
        spacing: { after: 40 }
      }));
      const line = [e.college, e.year, e.grade].filter(Boolean).join("  |  ");
      if (line) children.push(body(line));
    }
  }
  children.push(hr(color));
}

// Skills
if (data.skills) {
  children.push(section("Technical Skills", color));
  children.push(boldVal("Technical", data.skills));
  if (data.softskills) children.push(boldVal("Soft Skills", data.softskills));
  children.push(hr(color));
}

// Experience
if (data.experience) {
  children.push(section("Experience", color));
  children.push(body(data.experience));
  children.push(hr(color));
}

// Projects
if (data.projects && data.projects.length > 0) {
  children.push(section("Projects", color));
  for (const p of data.projects) {
    if (p.name) {
      children.push(new Paragraph({
        children: [new TextRun({ text: p.name, bold: true, size: 22, font: "Arial" })],
        spacing: { after: 40 }
      }));
      if (p.description) {
        const lines = p.description.split('\n').filter(l => l.trim());
        for (const l of lines) children.push(bullet(l.trim()));
      }
      if (p.tech) children.push(boldVal("Tech Stack", p.tech));
      children.push(new Paragraph({ spacing: { after: 100 } }));
    }
  }
  children.push(hr(color));
}

// Certifications
if (data.certifications) {
  children.push(section("Certifications & Achievements", color));
  const certs = data.certifications.split('\n').filter(l => l.trim());
  for (const c of certs) children.push(bullet(c.trim()));
  children.push(hr(color));
}

// Footer
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "Generated by AI Resume Analyzer", size: 16, font: "Arial", color: "aaaaaa", italics: true })]
}));

const doc = new Document({
  ...BULLETS,
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 } } },
    children
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outputPath, buf);
  console.log("done");
});
"""
            # Use system temp directory (works on Windows + Linux)
            import tempfile
            tmp_dir     = tempfile.gettempdir()
            js_path     = os.path.join(tmp_dir, "resume_gen.js")
            data_path   = os.path.join(tmp_dir, "resume_data.json")
            output_path = os.path.join(tmp_dir, "generated_resume.docx")

            # Write JS script and data
            with open(js_path, "w") as f:
                f.write(js_script)

            with open(data_path, "w") as f:
                json.dump(data, f)

            # Run node with paths as arguments
            result = subprocess.run(
                ["node", js_path, data_path, output_path],
                capture_output=True, text=True, timeout=30
            )

            if result.returncode == 0 and os.path.exists(output_path):
                with open(output_path, "rb") as f:
                    docx_bytes = f.read()

                st.success("✅ Resume generated successfully!")
                st.download_button(
                    label="⬇️ Download Your Resume (.docx)",
                    data=docx_bytes,
                    file_name=f"resume_{name.strip().replace(' ','_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
                st.info("💡 Open in Microsoft Word or Google Docs. Export as PDF before uploading to job portals.")
            else:
                st.error("❌ Generation failed. Error: " + result.stderr[:300])