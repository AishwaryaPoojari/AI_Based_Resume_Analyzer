"""
theme.py — import this at the top of every page to apply the global ResumeAI theme.

Usage:
    from theme import apply_theme
    apply_theme()
"""

import streamlit as st


_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
/* ── Base reset ─────────────────────────────────── */
* { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"], .main, .block-container {
    background: #0A0F1E !important;
    color: #E8EDF5 !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] { display: none !important; }
[data-testid="stToolbar"]  { display: none !important; }
header { visibility: hidden !important; }
.block-container { padding: 2rem 3rem !important; max-width: 900px !important; }

/* ── Color tokens ───────────────────────────────── */
:root {
    --teal:       #00D4AA;
    --teal-dim:   rgba(0,212,170,0.12);
    --teal-border:rgba(0,212,170,0.25);
    --blue:       #0066FF;
    --surface:    #111827;
    --surface-2:  #0D1323;
    --text:       #E8EDF5;
    --muted:      #8A95AA;
    --border:     rgba(255,255,255,0.06);
}

/* ── Keyframes ──────────────────────────────────── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(0,212,170,0.4); }
    50%       { box-shadow: 0 0 0 9px rgba(0,212,170,0); }
}

/* ── Streamlit widget overrides ─────────────────── */

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] > div > div {
    background: #111827 !important;
    border: 1px solid rgba(0,212,170,0.2) !important;
    border-radius: 8px !important;
    color: #E8EDF5 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #00D4AA !important;
    box-shadow: 0 0 0 3px rgba(0,212,170,0.12) !important;
    outline: none !important;
}

/* Labels */
label, .stTextInput label, .stTextArea label, .stSelectbox label {
    color: #C8D0DC !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* Primary button */
[data-testid="stButton"] button[kind="primary"],
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #00D4AA, #00A882) !important;
    color: #0A0F1E !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
}
[data-testid="stButton"] button[kind="primary"]:hover,
[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(0,212,170,0.35) !important;
}

/* Secondary / default button */
[data-testid="stButton"] button[kind="secondary"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #E8EDF5 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s ease !important;
}
[data-testid="stButton"] button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.09) !important;
    border-color: rgba(0,212,170,0.4) !important;
    color: #00D4AA !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #111827 !important;
    border: 1.5px dashed rgba(0,212,170,0.3) !important;
    border-radius: 12px !important;
    color: #E8EDF5 !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #00D4AA !important;
}

/* Progress bar */
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #00D4AA, #0066FF) !important;
    border-radius: 100px !important;
}

/* Metric */
[data-testid="stMetric"] {
    background: #111827 !important;
    border: 1px solid rgba(0,212,170,0.15) !important;
    border-radius: 12px !important;
    padding: 16px 18px !important;
}
[data-testid="stMetricValue"] {
    color: #00D4AA !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] {
    color: #8A95AA !important;
    font-size: 0.8rem !important;
}

/* Info / success / warning / error boxes */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
}

/* Tabs */
[data-testid="stTabs"] [role="tab"] {
    color: #8A95AA !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #00D4AA !important;
    border-bottom-color: #00D4AA !important;
}

/* Dividers */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* Headings */
h1, h2, h3, h4 { color: #E8EDF5 !important; font-family: 'Inter', sans-serif !important; }

/* Matplotlib / chart bg */
[data-testid="stPlotlyChart"], [data-testid="stImage"] {
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Dataframe / table */
[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden !important;
    border: 1px solid rgba(0,212,170,0.1) !important;
}

/* ── Reusable helper classes ─────────────────────── */

/* Card */
.ra-card {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 24px;
    animation: fadeUp 0.5s ease both;
}
.ra-card:hover {
    border-color: rgba(0,212,170,0.25);
    transition: border-color 0.2s ease;
}

/* Section eyebrow */
.ra-eyebrow {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #00D4AA;
    margin-bottom: 8px;
}

/* Tag / pill */
.ra-tag {
    display: inline-block;
    padding: 4px 11px;
    border-radius: 100px;
    font-size: 0.76rem;
    font-weight: 500;
    background: rgba(0,212,170,0.1);
    border: 1px solid rgba(0,212,170,0.25);
    color: #00D4AA;
    margin: 3px;
}

/* Score badge */
.ra-score {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0,212,170,0.08);
    border: 1px solid rgba(0,212,170,0.25);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 0.9rem;
    font-weight: 600;
    color: #00D4AA;
    animation: pulse 2.5s ease-in-out infinite;
}

/* Page title */
.ra-page-title {
    font-size: 1.8rem;
    font-weight: 800;
    color: #E8EDF5;
    margin-bottom: 6px;
    animation: fadeUp 0.5s ease both;
}
.ra-page-sub {
    font-size: 0.92rem;
    color: #8A95AA;
    margin-bottom: 28px;
    animation: fadeUp 0.5s 0.08s ease both;
}

/* Teal gradient text */
.ra-gradient-text {
    background: linear-gradient(135deg, #00D4AA, #0066FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
</style>
"""


def apply_theme():
    """Inject the global ResumeAI theme CSS into the current Streamlit page."""
    st.markdown(_CSS, unsafe_allow_html=True)