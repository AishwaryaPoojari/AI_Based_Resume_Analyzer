import streamlit as st
from database import login_user


def load_css():
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

if st.button("← Back to Home"):
    st.switch_page("pages/Landing.py")

col1, col2, col3 = st.columns([1, 1.5, 1])

with col2:

    st.markdown("""
    <div class="auth-card">
        <div class="auth-title">Welcome Back 👋</div>
        <div class="auth-sub">Log in to access your resume analyzer dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input(
            "📧 Email Address",
            placeholder="you@example.com"
        )

        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Your password"
        )

        submitted = st.form_submit_button(
            "Login →",
            use_container_width=True
        )

    if submitted:
        if not email or not password:
            st.error("Please fill in all fields.")
        else:
            user = login_user(email.strip().lower(), password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_id = user["id"]
                st.session_state.user_name = user["name"]
                st.session_state.user_email = user["email"]
                st.session_state.user_occupation = user["occupation"]
                st.session_state.user_department = user["department"]
                st.session_state.user_experience = user["experience"]

                st.success(f"Welcome back, {user['name']}! Redirecting...")
                st.switch_page("pages/Dashboard.py")
            else:
                st.error("Invalid email or password. Please try again.")

st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown("<p style='color:#6B7280;font-size:0.88rem'>Don't have an account?</p>", unsafe_allow_html=True)
with col2:
    if st.button("📝 Register here", use_container_width=True):
        st.switch_page("pages/Register.py")