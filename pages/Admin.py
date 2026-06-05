import streamlit as st
import csv
import io
from database import login_admin, get_all_users


def load_css():
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


def show_login():
    if st.button("← Back to Home"):
        st.switch_page("pages/Landing.py")

    st.markdown("""
    <div class="auth-card">
        <div class="auth-title">Admin Panel 🛡️</div>
        <div class="auth-sub">Enter admin credentials to access the control panel</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("admin_login"):
        email    = st.text_input("📧 Admin Email", placeholder="example@google.com")
        password = st.text_input("🔒 Password", type="password")
        submitted = st.form_submit_button("Access Admin Panel →", use_container_width=True)

    if submitted:
        admin = login_admin(email.strip().lower(), password)
        if admin:
            st.session_state.admin_logged_in = True
            st.session_state.admin_email     = email.strip().lower()
            st.rerun()
        else:
            st.error("Invalid admin credentials.")


def export_users_csv(users):
    """Convert users list to CSV bytes for download."""
    output = io.StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow(["#", "Name", "Email", "Age", "Department", "Experience", "Occupation", "Registered At"])

    # Data rows
    for u in users:
        writer.writerow([
            u["id"],
            u["name"],
            u["email"],
            u["age"]        or "—",
            u["department"] or "—",
            u["experience"] or "—",
            u["occupation"] or "—",
            str(u["created_at"])[:16]
        ])

    return output.getvalue().encode("utf-8")


def show_dashboard():
    col_title, col_logout = st.columns([8, 2])
    with col_title:
        st.markdown("## 🛡️ Admin Dashboard")
        st.markdown(f"<p style='color:#8b949e'>Logged in as <b>{st.session_state.admin_email}</b></p>",
                    unsafe_allow_html=True)
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()

    st.markdown("<hr style='border-color:#30363d'>", unsafe_allow_html=True)

    users = get_all_users()

    # ── Metrics ────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Total Users", len(users))
    with m2: st.metric("Students",    sum(1 for u in users if u["occupation"] == "Student"))
    with m3: st.metric("Freshers",    sum(1 for u in users if u["experience"] and "Fresher" in u["experience"]))
    with m4: st.metric("Latest",      users[0]["created_at"][:10] if users else "—")

    # ── Header row: title + export button ──────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    h1, h2 = st.columns([7, 3])
    with h1:
        st.markdown("### 👥 Registered Users")
    with h2:
        if users:
            csv_bytes = export_users_csv(users)
            st.download_button(
                label="⬇️ Export as CSV",
                data=csv_bytes,
                file_name="registered_users.csv",
                mime="text/csv",
                use_container_width=True
            )

    if not users:
        st.info("No users registered yet.")
        return

    # ── Users Table ────────────────────────────────────────
    rows = "".join(f"""
    <tr>
        <td>{u['id']}</td><td>{u['name']}</td><td>{u['email']}</td>
        <td>{u['age'] or '—'}</td><td>{u['department'] or '—'}</td>
        <td>{u['experience'] or '—'}</td><td>{u['occupation'] or '—'}</td>
        <td>{str(u['created_at'])[:16]}</td>
    </tr>""" for u in users)

    st.markdown(f"""
    <div style="overflow-x:auto">
    <table class="user-table">
        <thead><tr>
            <th>#</th><th>Name</th><th>Email</th><th>Age</th>
            <th>Department</th><th>Experience</th><th>Occupation</th><th>Registered</th>
        </tr></thead>
        <tbody>{rows}</tbody>
    </table></div>""", unsafe_allow_html=True)

    st.markdown(f"<p style='color:#8b949e;font-size:0.8rem;margin-top:0.5rem'>Showing {len(users)} registered user(s)</p>",
                unsafe_allow_html=True)


if st.session_state.get("admin_logged_in"):
    show_dashboard()
else:
    show_login()