import streamlit as st
from database import init_db

init_db()

landing   = st.Page("pages/Landing.py",   title="Home",      icon="🏠", default=True)
login     = st.Page("pages/Login.py",     title="Login",     icon="🔑")
register  = st.Page("pages/Register.py",  title="Register",  icon="📝")
admin     = st.Page("pages/Admin.py",     title="Admin",     icon="🛡️")
dashboard = st.Page("pages/Dashboard.py", title="Dashboard", icon="📊")
templates = st.Page("pages/Templates.py", title="Templates", icon="📄")
generator = st.Page("pages/Generator.py", title="Generator", icon="🛠️")

pg = st.navigation(
    pages=[landing, login, register, admin, dashboard, templates, generator],
    position="hidden"
)

pg.run()