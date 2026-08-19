import streamlit as st
import pandas as pd
from profiler import DataProfiler

st.set_page_config(
    page_title="DataLens — Profiler & Schema Assistant",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Force dark background everywhere ── */
    html, body,
    [class*="css"],
    .stApp,
    .stApp > div,
    section[data-testid="stAppViewContainer"],
    section[data-testid="stAppViewContainer"] > div,
    div[data-testid="stVerticalBlock"] {
        background-color: #ffffff !important;
        color: #16181d;
        font-family: 'Inter', sans-serif;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding-top: 0rem;
        padding-bottom: 4rem;
        max-width: 1080px;
    }

    /* ── Hero Wrapper ── */
    .hero-wrapper {
        position: relative;
        padding: 4rem 0 3rem 0;
        margin-bottom: 1.5rem;
        overflow: hidden;
        
    }

    /* Orb 1 — indigo, top left */
    .orb1 {
        position: absolute;
        top: -80px;
        left: -100px;
        width: 520px;
        height: 420px;
        background: radial-gradient(ellipse at center,
            rgba(99, 102, 241, 0.35) 0%,
            rgba(139, 92, 246, 0.18) 45%,
            transparent 70%);
        border-radius: 50%;
        animation: orbDrift1 8s ease-in-out infinite alternate;
        pointer-events: none;
    }

    /* Orb 2 — purple-blue, top right */
    .orb2 {
        position: absolute;
        top: -20px;
        right: -120px;
        width: 460px;
        height: 380px;
        background: radial-gradient(ellipse at center,
            rgba(168, 85, 247, 0.25) 0%,
            rgba(56, 189, 248, 0.12) 50%,
            transparent 70%);
        border-radius: 50%;
        animation: orbDrift2 10s ease-in-out infinite alternate;
        pointer-events: none;
    }

    /* Orb 3 — small accent bottom right */
    .orb3 {
        position: absolute;
        bottom: -40px;
        right: 200px;
        width: 260px;
        height: 200px;
        background: radial-gradient(ellipse at center,
            rgba(99, 102, 241, 0.18) 0%,
            transparent 70%);
        border-radius: 50%;
        animation: orbDrift1 12s ease-in-out infinite alternate-reverse;
        pointer-events: none;
    }

    @keyframes orbDrift1 {
        0%   { transform: translate(0px, 0px) scale(1); }
        100% { transform: translate(40px, 30px) scale(1.12); }
    }
    @keyframes orbDrift2 {
        0%   { transform: translate(0px, 0px) scale(1); }
        100% { transform: translate(-30px, 20px) scale(1.08); }
    }

    /* Hero text sits above orbs */
    .hero-content {
        position: relative;
        z-index: 2;
    }

    /* ── Eyebrow ── */
    .datalens-eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 500;
        letter-spacing: 0.14em;
        color: #818cf8;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .datalens-eyebrow .dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #6366f1;
        box-shadow: 0 0 8px #6366f1;
        animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; box-shadow: 0 0 8px #6366f1; }
        50%       { opacity: 0.4; box-shadow: 0 0 2px #6366f1; }
    }

    /* ── Title ── */
    .datalens-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #16181d;
        letter-spacing: -0.03em;
        line-height: 1.15;
        margin-bottom: 0.8rem;
        text-shadow: none;
    }

    .datalens-title .gradient-word {
        background: linear-gradient(110deg, #6366f1 0%, #a78bfa 50%, #38bdf8 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 4s linear infinite;
    }

    @keyframes shimmer {
        0%   { background-position: 0% center; }
        100% { background-position: 200% center; }
    }

    /* ── Subtitle ── */
    .datalens-sub {
        font-size: 0.96rem;
        color: #8b92a5;
        max-width: 520px;
        line-height: 1.65;
    }

    /* ── Section Labels ── */
    .section-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.70rem;
        font-weight: 500;
        letter-spacing: 0.12em;
        color: #6366f1;
        text-transform: uppercase;
        margin: 2.6rem 0 0.9rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, #2a2d3e, transparent);
    }

    /* ── Metric Cards ── */
    div[data-testid="stMetric"] {
        background: #1e2130 !important;
        border: 1px solid #2a2d3e;
        border-radius: 12px;
        padding: 1.2rem 1.4rem 1rem 1.4rem;
        position: relative;
        overflow: hidden;
    }
    div[data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #6366f1, #a78bfa);
    }
    div[data-testid="stMetricLabel"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 500;
        color: #6b7280 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #f0f1f5 !important;
    }

    /* ── File Uploader ── */
    div[data-testid="stFileUploaderDropzone"] {
        border-radius: 14px;
        border: 1.5px dashed #3b3f52 !important;
        background: #13151f !important;
        transition: border-color 0.2s ease, background 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    div[data-testid="stFileUploaderDropzone"]:hover {
        border-color: #6366f1 !important;
        background: #16192a !important;
    }
    div[data-testid="stFileUploaderDropzone"]::after {
        content: '';
        position: absolute;
        top: -5%; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, #6366f1, transparent);
        animation: scan 2.8s ease-in-out infinite;
    }
    @keyframes scan {
        0%   { top: -5%; opacity: 0; }
        20%  { opacity: 1; }
        80%  { opacity: 1; }
        100% { top: 105%; opacity: 0; }
    }

    /* ── DataFrames ── */
    div[data-testid="stDataFrame"] {
        border: 1px solid #2a2d3e;
        border-radius: 12px;
        overflow: hidden;
    }

    /* ── Code Block ── */
    div[data-testid="stCodeBlock"] pre {
        border-radius: 12px !important;
        border: 1px solid #2a2d3e !important;
        background: #13151f !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.82rem !important;
    }

    /* ── Text Input ── */
    div[data-testid="stTextInput"] input {
        border-radius: 10px;
        border: 1px solid #2a2d3e !important;
        background: #13151f !important;
        color: #e2e4eb !important;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
    }

    /* ── Alerts ── */
    div[data-testid="stAlert"] {
        border-radius: 10px;
        border: 1px solid #2a2d3e;
        background: #1e2130 !important;
    }

    /* ── Captions ── */
    .stCaption, div[data-testid="stCaptionContainer"] p {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #6b7280;
        letter-spacing: 0.04em;
    }

    hr { border-color: #2a2d3e; margin: 0.4rem 0 1.6rem 0; }

    .upload-hint {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.06em;
        color: #6366f1;
        background: rgba(99,102,241,0.1);
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 6px;
        padding: 0.2rem 0.55rem;
        margin-bottom: 0.7rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Hero ──
st.markdown("""
<div class="hero-wrapper">
    <div class="orb1"></div>
    <div class="orb2"></div>
    <div class="orb3"></div>
    <div class="hero-content">
        <div class="datalens-eyebrow">
            <span class="dot"></span> DataLens v1.0
        </div>
        <div class="datalens-title">
            Data Profiler &amp;<br>
            <span class="gradient-word">Schema Assistant</span>
        </div>
        <div class="datalens-sub">
            Upload a messy CSV — get instant data quality insights,
            outlier detection, and a production-ready SQL schema.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="upload-hint">CSV · up to 200MB</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    profiler = DataProfiler(df)
    summary = profiler.get_summary_stats()

    st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", f"{summary['total_rows']:,}")
    with col2:
        st.metric("Columns", summary['total_columns'])
    with col3:
        total_missing = sum(summary['missing_values'].values())
        st.metric("Missing Values", f"{total_missing:,}")

    st.markdown('<div class="section-label">Preview</div>', unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown('<div class="section-label">Data Quality</div>', unsafe_allow_html=True)
    col_left, col_right = st.columns(2)

    with col_left:
        st.caption("MISSING VALUES PER COLUMN")
        missing_df = pd.DataFrame(
            list(summary['missing_values'].items()),
            columns=["Column", "Missing"]
        )
        missing_df = missing_df[missing_df["Missing"] > 0]
        if not missing_df.empty:
            st.dataframe(missing_df, use_container_width=True, hide_index=True)
        else:
            st.success("✓ No missing values detected.")

    with col_right:
        st.caption("OUTLIERS — IQR METHOD")
        outliers = profiler.detect_outliers()
        outlier_df = pd.DataFrame(list(outliers.items()), columns=["Column", "Outliers"])
        st.dataframe(outlier_df, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-label">Generated SQL Schema</div>', unsafe_allow_html=True)
    table_name_input = st.text_input("Table name", value="imported_dataset")
    sql_script = profiler.generate_sql_ddl(table_name=table_name_input)
    st.code(sql_script, language="sql")

else:
    st.info("⬆ Drop a CSV file above to start profiling.")
