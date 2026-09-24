import streamlit as st
import pandas as pd

from core.database import init_db, get_tasks


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="WorkLens",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()


# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown(
    """
<style>
.block-container {
    padding-top: 3rem;
    padding-bottom: 4rem;
    max-width: 1250px;
}

.hero {
    padding: 40px 0 50px 0;
}

.hero-title {
    font-size: 64px;
    font-weight: 750;
    letter-spacing: -3px;
    line-height: 1;
    margin-bottom: 20px;
}

.hero-subtitle {
    font-size: 22px;
    color: #888;
    max-width: 750px;
    line-height: 1.5;
}

.section-title {
    font-size: 28px;
    font-weight: 650;
    margin-top: 50px;
    margin-bottom: 25px;
}

.feature-card {
    border: 1px solid rgba(128,128,128,0.25);
    border-radius: 18px;
    padding: 28px;
    min-height: 180px;
}

.feature-number {
    font-size: 13px;
    opacity: 0.5;
    margin-bottom: 18px;
}

.feature-title {
    font-size: 21px;
    font-weight: 650;
    margin-bottom: 10px;
}

.feature-description {
    opacity: 0.7;
    line-height: 1.6;
    font-size: 15px;
}

.tag {
    display: inline-block;
    border: 1px solid rgba(128,128,128,0.3);
    border-radius: 30px;
    padding: 6px 12px;
    font-size: 12px;
    margin-bottom: 22px;
    opacity: 0.75;
}
</style>
""",
    unsafe_allow_html=True,
)


# --------------------------------------------------
# HERO
# --------------------------------------------------

hero_html = """
<div class="hero">
<div class="tag">AUTOMATION DISCOVERY</div>
<div class="hero-title">WorkLens.</div>
<div class="hero-subtitle">
Find the work worth automating.<br>
Track repetitive activities, understand where time is being lost
and identify the best opportunities for automation.
</div>
</div>
"""

st.markdown(
    hero_html,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# DATA
# --------------------------------------------------

tasks = get_tasks()

if tasks:

    df = pd.DataFrame(tasks)

    total_tasks = len(df)

    total_minutes = (
        df["minutes_per_execution"].fillna(0)
        * df["executions_per_period"].fillna(0)
    ).sum()

    total_hours = total_minutes / 60

else:

    total_tasks = 0
    total_hours = 0


# --------------------------------------------------
# KPI
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Tasks recorded",
        total_tasks,
    )

with col2:
    st.metric(
        "Recorded workload",
        f"{total_hours:.1f} h",
    )

with col3:
    st.metric(
        "Automation opportunities",
        "—",
    )

with col4:
    st.metric(
        "Potential time saved",
        "—",
    )


# --------------------------------------------------
# HOW IT WORKS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">How WorkLens works</div>',
    unsafe_allow_html=True,
)


c1, c2, c3 = st.columns(3)


with c1:

    card_1 = """
<div class="feature-card">
<div class="feature-number">01</div>
<div class="feature-title">Capture</div>
<div class="feature-description">
Record repetitive tasks and describe how your time
is currently being spent.
</div>
</div>
"""

    st.markdown(
        card_1,
        unsafe_allow_html=True,
    )


with c2:

    card_2 = """
<div class="feature-card">
<div class="feature-number">02</div>
<div class="feature-title">Analyze</div>
<div class="feature-description">
WorkLens evaluates frequency, repetitiveness,
manual effort and automation potential.
</div>
</div>
"""

    st.markdown(
        card_2,
        unsafe_allow_html=True,
    )


with c3:

    card_3 = """
<div class="feature-card">
<div class="feature-number">03</div>
<div class="feature-title">Automate</div>
<div class="feature-description">
Discover high-impact opportunities and understand
which processes should be automated first.
</div>
</div>
"""

    st.markdown(
        card_3,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# CTA
# --------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

st.divider()

st.markdown("### Start discovering automation opportunities")

st.write(
    "Record the repetitive activities you perform during your workday. "
    "WorkLens will analyze them and identify where automation could have "
    "the greatest impact."
)

st.page_link(
    "pages/1_Log_Task.py",
    label="＋ Log your first task",
    icon=None,
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("<br><br>", unsafe_allow_html=True)

st.caption(
    "WorkLens · Local-first automation discovery"
)