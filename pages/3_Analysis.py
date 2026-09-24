import streamlit as st
import pandas as pd

from core.database import init_db, get_tasks
from core.scoring import analyze_task


st.set_page_config(
    page_title="Analysis · WorkLens",
    page_icon="◎",
    layout="wide",
)

init_db()


st.title("Automation Analysis")

st.write(
    "Discover which activities are consuming the most time "
    "and where automation could generate the greatest impact."
)


# --------------------------------------------------
# LOAD TASKS
# --------------------------------------------------

tasks = get_tasks()

if not tasks:
    st.info(
        "No tasks recorded yet. Add some activities before running the analysis."
    )
    st.stop()


# --------------------------------------------------
# ANALYZE
# --------------------------------------------------

results = []

for task in tasks:

    analysis = analyze_task(task)

    results.append(
        {
            "ID": task["id"],
            "Task": task["task_name"],
            "Department": task["department"],
            "Category": task["category"],
            "Monthly Hours": analysis["monthly_hours"],
            "Automation Score": analysis["automation_score"],
            "Impact Score": analysis["impact_score"],
            "Complexity Score": analysis["complexity_score"],
            "Priority Score": analysis["priority_score"],
            "Potential Hours Saved": analysis["potential_hours_saved"],
            "Priority": analysis["priority"],
            "Opportunity": analysis["opportunity"],
        }
    )


df = pd.DataFrame(results)


# --------------------------------------------------
# KPI
# --------------------------------------------------

total_hours = df["Monthly Hours"].sum()

potential_saved = df[
    "Potential Hours Saved"
].sum()

high_priority = len(
    df[df["Priority"] == "HIGH"]
)

quick_wins = len(
    df[df["Opportunity"] == "QUICK WIN"]
)


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Monthly workload",
    f"{total_hours:.1f} h",
)

c2.metric(
    "Potential time saved",
    f"{potential_saved:.1f} h",
)

c3.metric(
    "High priority",
    high_priority,
)

c4.metric(
    "Quick wins",
    quick_wins,
)


st.divider()


# --------------------------------------------------
# TOP OPPORTUNITIES
# --------------------------------------------------

st.subheader("Top automation opportunities")

ranked = df.sort_values(
    "Priority Score",
    ascending=False,
)


st.dataframe(
    ranked[
        [
            "Task",
            "Monthly Hours",
            "Automation Score",
            "Impact Score",
            "Complexity Score",
            "Potential Hours Saved",
            "Priority",
            "Opportunity",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)


# --------------------------------------------------
# INDIVIDUAL ANALYSIS
# --------------------------------------------------

st.divider()

st.subheader("Explore a task")


selected_task_name = st.selectbox(
    "Select activity",
    ranked["Task"].tolist(),
)


selected_row = ranked[
    ranked["Task"] == selected_task_name
].iloc[0]


st.markdown(
    f"## {selected_row['Task']}"
)


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Automation",
    f"{selected_row['Automation Score']:.0f}/100",
)

c2.metric(
    "Impact",
    f"{selected_row['Impact Score']:.0f}/100",
)

c3.metric(
    "Complexity",
    f"{selected_row['Complexity Score']:.0f}/100",
)

c4.metric(
    "Priority",
    f"{selected_row['Priority Score']:.0f}/100",
)


st.markdown("### Opportunity")

st.success(
    selected_row["Opportunity"]
)


col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Current workload",
        f"{selected_row['Monthly Hours']:.1f} h/month",
    )

with col2:

    st.metric(
        "Potential saving",
        f"{selected_row['Potential Hours Saved']:.1f} h/month",
    )