import streamlit as st
import pandas as pd
from profiler import DataProfiler

# ────────────────────────────────────────────────────────────────────────────
# Page Configuration
# ────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataLens — Profiler & Schema Assistant",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ────────────────────────────────────────────────────────────────────────────
# Design System CSS
# ────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Reset & Base ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0f1117;
        color: #e2e4eb;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding-top: 3rem;
        padding-bottom: 4rem;
        max-width: 1080px;
    }

    /* ── Header ── */
    .datalens-eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 500;
        letter-spacing: 0.14em;
        color: #6366f1;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .datalens-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.4rem;
        font-weight: 700;
        color: #f0f1f5;
        letter-spacing: -0.03em;
        line-height: 1.15;
        margin-bottom: 0.6rem;
    }
    .datalens-title span {
        background: linear-gradient(90deg, #6366f1, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .datalens-sub {
        font-size: 0.95rem;
        color: #8b92a5;
        max-width: 560px;
        line-height: 1.6;
        margin-bottom: 2.8rem;
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
        background: #1e2130;
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
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #f0f1f5;
    }

    /* ── File Uploader ── */
    div[data-testid="stFileUploaderDropzone"] {
        border-radius: 14px;
        border: 1.5px dashed #3b3f52;
        background: #13151f;
        transition: border-color 0.2s ease, background 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    div[data-testid="stFileUploaderDropzone"]:hover {
        border-color: #6366f1;
        background: #16192a;
    }
    div[data-testid="stFileUploaderDropzone"]::after {
        content: '';
        position: absolute;
        top: -100%; left: 0; right: 0;
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
        background: #1e2130;
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
        border: 1px solid #2a2d3e;
        background: #13151f;
        color: #e2e4eb;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.15);
    }

    /* ── Alerts ── */
    div[data-testid="stAlert"] {
        border-radius: 10px;
        border: 1px solid #2a2d3e;
        background: #1e2130;
    }

    /* ── Captions ── */
    .stCaption, div[data-testid="stCaptionContainer"] p {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #6b7280;
        letter-spacing: 0.04em;
    }

    /* ── Horizontal Rule ── */
    hr {
        border-color: #2a2d3e;
        margin: 0.4rem 0 1.6rem 0;
    }

    /* ── Upload hint badge ── */
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

# ────────────────────────────────────────────────────────────────────────────
# Header
# ────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="datalens-eyebrow">⬡ DataLens v1.0</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="datalens-title">Data Profiler &<br><span>Schema Assistant</span></div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="datalens-sub">Upload a messy CSV — get instant data quality insights, '
    'outlier detection, and a production-ready SQL schema.</div>',
    unsafe_allow_html=True
)

# Upload
st.markdown('<div class="upload-hint">CSV · up to 200MB</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

# ────────────────────────────────────────────────────────────────────────────
# Main Content
# ────────────────────────────────────────────────────────────────────────────
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    profiler = DataProfiler(df)
    summary = profiler.get_summary_stats()

    # Overview
    st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", f"{summary['total_rows']:,}")
    with col2:
        st.metric("Columns", summary['total_columns'])
    with col3:
        total_missing = sum(summary['missing_values'].values())
        st.metric("Missing Values", f"{total_missing:,}")

    # Preview
    st.markdown('<div class="section-label">Preview</div>', unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True)

    # Data Quality
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

    # SQL Schema
    st.markdown('<div class="section-label">Generated SQL Schema</div>', unsafe_allow_html=True)
    table_name_input = st.text_input("Table name", value="imported_dataset")
    sql_script = profiler.generate_sql_ddl(table_name=table_name_input)
    st.code(sql_script, language="sql")

else:
    st.info("⬆ Drop a CSV file above to start profiling.")