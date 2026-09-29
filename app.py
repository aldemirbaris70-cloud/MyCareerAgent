"""Streamlit dashboard for MyCareerAgent."""

from html import escape

import streamlit as st

from career_agent.core.application import CareerAgent
from career_agent.core.errors import CareerAgentError
from career_agent.reports.markdown import MarkdownReportWriter


st.set_page_config(
    page_title="MyCareerAgent",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded",
)

dark_mode = st.sidebar.toggle("Dark mode", value=True)
palette = (
    "--background:#10161b;--surface:#172127;--surface-raised:#1e2b32;--border:#2b3b43;--ink:#f4f7f8;--muted:#9caeb5;--accent:#ff765c;--positive:#70d6a2;--positive-soft:#17352b;"
    if dark_mode
    else "--background:#f4f6f5;--surface:#ffffff;--surface-raised:#f8faf9;--border:#dfe6e3;--ink:#18242b;--muted:#68777d;--accent:#d75c45;--positive:#17885b;--positive-soft:#e7f6ee;"
)

st.markdown(
    f"""
    <style>
    :root {{ {palette} }}
    .stApp {{ background: var(--background); color: var(--ink); }}
    [data-testid="stHeader"] {{ background: transparent; }}
    [data-testid="stSidebar"] {{ background: #172127; border-right: 1px solid #2b3b43; }}
    [data-testid="stSidebar"] * {{ color: #edf3f4; }}
    [data-testid="stSidebar"] .stCaption {{ color: #9caeb5; }}
    [data-testid="stFileUploader"] {{ border: 1px dashed #61747c; border-radius: 10px; padding: .2rem; }}
    [data-testid="stFileUploaderDropzone"] {{ background: #1e2b32; }}
    .block-container {{ max-width: 1440px; padding: 2rem 3.5rem 4rem; }}
    h1, h2, h3, p, label, .stMarkdown {{ color: var(--ink); }}
    h1, h2, h3 {{ letter-spacing: -0.025em; }}
    .hero {{ align-items: flex-start; display: flex; justify-content: space-between; padding: .8rem 0 2rem; border-bottom: 1px solid var(--border); margin-bottom: 1.5rem; }}
    .hero h1 {{ font-size: clamp(2rem, 4vw, 3.5rem); letter-spacing: -0.055em; margin: 0; color: var(--ink); }}
    .hero p {{ color: var(--muted); font-size: 1.02rem; margin-top: .65rem; max-width: 620px; }}
    .eyebrow {{ color: var(--accent); font-size: .72rem; font-weight: 800; letter-spacing: .16em; text-transform: uppercase; margin-bottom: .55rem; }}
    .status {{ background: var(--positive-soft); border: 1px solid var(--positive); border-radius: 999px; color: var(--positive); font-size: .78rem; font-weight: 700; padding: .5rem .8rem; white-space: nowrap; }}
    .kpi {{ background: var(--surface); border: 1px solid var(--border); border-radius: 14px; min-height: 130px; padding: 1.1rem 1.25rem; box-shadow: 0 8px 25px rgba(10,27,34,.05); }}
    .kpi-accent {{ border-top: 4px solid var(--accent); }}
    .kpi-positive {{ border-top: 4px solid var(--positive); }}
    .kpi-label {{ color: var(--muted); font-size: .73rem; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; }}
    .kpi-value {{ color: var(--ink); font-size: 2.25rem; font-weight: 800; line-height: 1.15; margin: .7rem 0 .4rem; }}
    .kpi-detail {{ color: var(--muted); font-size: .82rem; }}
    .panel {{ background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 1.2rem 1.3rem; }}
    .panel-title {{ color: var(--ink); font-size: 1rem; font-weight: 800; margin-bottom: 1rem; }}
    .skill-row {{ margin-bottom: .8rem; }}
    .skill-meta {{ display: flex; justify-content: space-between; margin-bottom: .3rem; }}
    .skill-name {{ color: var(--ink); font-size: .87rem; font-weight: 650; }}
    .skill-count {{ color: var(--muted); font-size: .76rem; }}
    .bar-track {{ background: var(--border); border-radius: 999px; height: 8px; overflow: hidden; }}
    .bar-fill {{ background: var(--accent); border-radius: inherit; height: 100%; }}
    .bar-fill-positive {{ background: var(--positive); }}
    .recommendation {{ border-left: 3px solid var(--accent); color: var(--ink); font-size: .9rem; line-height: 1.45; margin: .7rem 0; padding-left: .8rem; }}
    .question {{ border-bottom: 1px solid var(--border); color: var(--ink); font-size: .9rem; line-height: 1.45; padding: .6rem 0; }}
    .stButton > button, .stDownloadButton > button {{ border-radius: 9px; font-weight: 750; min-height: 2.6rem; }}
    .stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] {{ background: var(--accent); border-color: var(--accent); color: #fff; }}
    .stTabs [data-baseweb="tab"] {{ font-weight: 700; }}
    div[data-testid="stProgressBar"] > div > div {{ background: var(--accent); }}
    @media (max-width: 800px) {{ .block-container {{ padding: 1.25rem 1rem 3rem; }} .hero {{ flex-direction: column; gap: 1rem; }} }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero"><div><div class="eyebrow">Career intelligence workspace</div><h1>Make your next move count.</h1><p>Compare your experience to a target role, find the gaps that matter, and leave with an application you can stand behind.</p></div><div class="status">● Ready to analyze</div></div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## MyCareerAgent")
    st.caption("Career intelligence for your next application.")
    st.divider()
    st.markdown("### Application inputs")
    cv_file = st.file_uploader("Upload CV", type=["pdf", "docx", "txt"], key="cv")
    job_file = st.file_uploader("Upload job description", type=["pdf", "docx", "txt"], key="job")
    st.caption("PDF, DOCX, and TXT files are supported.")
    candidate_name = st.text_input("Candidate name", placeholder="Jordan Lee")
    company = st.text_input("Company", placeholder="Example Co")
    analyze = st.button("Analyze application", type="primary", use_container_width=True)

if analyze:
    if not cv_file or not job_file:
        st.warning("Upload both a CV and a job description to begin.")
    else:
        try:
            with st.spinner("Reading documents and preparing your application plan..."):
                report = CareerAgent().analyze_uploaded(
                    cv_file.name,
                    cv_file.getvalue(),
                    job_file.name,
                    job_file.getvalue(),
                    candidate_name=candidate_name,
                    company=company,
                )
            st.session_state["report"] = report
        except CareerAgentError as error:
            st.error(str(error))

report = st.session_state.get("report")
if report:
    score = report.score
    kpi_one, kpi_two, kpi_three, kpi_four = st.columns(4)
    with kpi_one:
        st.markdown(
            f'<div class="kpi kpi-accent"><div class="kpi-label">ATS compatibility</div><div class="kpi-value">{score.overall:.1f}%</div><div class="kpi-detail">Overall role fit</div></div>',
            unsafe_allow_html=True,
        )
    with kpi_two:
        st.markdown(
            f'<div class="kpi kpi-positive"><div class="kpi-label">Matched skills</div><div class="kpi-value">{len(score.matched_skills)}</div><div class="kpi-detail">Keywords already evidenced</div></div>',
            unsafe_allow_html=True,
        )
    with kpi_three:
        st.markdown(
            f'<div class="kpi"><div class="kpi-label">Priority gaps</div><div class="kpi-value">{len(score.missing_skills)}</div><div class="kpi-detail">Keywords to address</div></div>',
            unsafe_allow_html=True,
        )
    with kpi_four:
        st.markdown(
            f'<div class="kpi"><div class="kpi-label">CV structure</div><div class="kpi-value">{score.section_coverage:.1f}%</div><div class="kpi-detail">Core sections detected</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("## Skill alignment")
    st.caption("Detected job keywords compared with your CV evidence.")
    matching, missing = st.columns(2)
    with matching:
        with st.container(border=True):
            st.markdown('<div class="panel-title">Matching skills</div>', unsafe_allow_html=True)
            if score.matched_skills:
                for index, skill in enumerate(score.matched_skills):
                    width = max(28, 100 - index * max(8, 58 // len(score.matched_skills)))
                    st.markdown(
                        f'<div class="skill-row"><div class="skill-meta"><span class="skill-name">{escape(skill)}</span><span class="skill-count">Matched</span></div><div class="bar-track"><div class="bar-fill bar-fill-positive" style="width:{width}%"></div></div></div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No matching skills detected.")
    with missing:
        with st.container(border=True):
            st.markdown('<div class="panel-title">Missing skills</div>', unsafe_allow_html=True)
            if score.missing_skills:
                for index, skill in enumerate(score.missing_skills):
                    width = max(28, 100 - index * max(8, 58 // len(score.missing_skills)))
                    st.markdown(
                        f'<div class="skill-row"><div class="skill-meta"><span class="skill-name">{escape(skill)}</span><span class="skill-count">Priority gap</span></div><div class="bar-track"><div class="bar-fill" style="width:{width}%"></div></div></div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No missing skills detected.")

    st.markdown("## Action plan")
    st.caption("Turn the score into concrete preparation.")
    recommendations, interview = st.columns(2)
    with recommendations:
        with st.container(border=True):
            st.markdown('<div class="panel-title">Recommendations</div>', unsafe_allow_html=True)
            for recommendation in report.recommendations:
                st.markdown(f'<div class="recommendation">{escape(recommendation)}</div>', unsafe_allow_html=True)
    with interview:
        with st.container(border=True):
            st.markdown('<div class="panel-title">Likely interview questions</div>', unsafe_allow_html=True)
            for question in report.interview_questions:
                st.markdown(f'<div class="question">{escape(question)}</div>', unsafe_allow_html=True)

    st.markdown("## Application materials")
    st.caption("Review, edit, and download your tailored drafts.")
    cover, resume = st.tabs(["Cover letter", "Optimized CV"])
    with cover:
        st.text_area("Tailored cover letter", report.cover_letter, height=300, label_visibility="collapsed")
        st.download_button("Download cover letter", data=report.cover_letter, file_name="mycareeragent_cover_letter.txt", mime="text/plain", key="download-cover-letter")
    with resume:
        st.text_area("ATS-optimized CV draft", report.optimized_cv, height=300, label_visibility="collapsed")
        st.download_button("Download optimized CV", data=report.optimized_cv, file_name="mycareeragent_optimized_cv.md", mime="text/markdown", key="download-optimized-cv")

    markdown = MarkdownReportWriter().render(report)
    st.download_button(
        "Download complete Markdown report",
        data=markdown,
        file_name="mycareeragent_job_match.md",
        mime="text/markdown",
        type="primary",
        use_container_width=True,
        key="download-full-report",
    )
else:
    st.markdown('<div class="panel"><div class="panel-title">Your workspace is ready</div><div style="color:var(--muted)">Upload your CV and target job description in the sidebar, then select Analyze application to generate your career brief.</div></div>', unsafe_allow_html=True)