import streamlit as st
import pandas as pd
import plotly.express as px

from core.database import init_db, get_tasks
from core.scoring import analyze_task


st.set_page_config(
    page_title="Analysis · WorkLens",
    page_icon="◎",
    layout="wide",
)

init_db()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("Automation Analysis")

st.write(
    "Identify where time is being lost and which activities "
    "offer the strongest opportunities for automation."
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

tasks = get_tasks()

if not tasks:
    st.info(
        "No tasks recorded yet. Add some activities before running the analysis."
    )
    st.stop()


results = []

for task in tasks:

    analysis = analyze_task(task)

    results.append(
        {
            "ID": task["id"],
            "Task": task["task_name"],
            "Department": task["department"] or "Not specified",
            "Category": task["category"] or "Other",
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
# GLOBAL KPI
# --------------------------------------------------

total_hours = df["Monthly Hours"].sum()
potential_saved = df["Potential Hours Saved"].sum()

saving_percentage = (
    potential_saved / total_hours * 100
    if total_hours > 0
    else 0
)

high_priority = len(
    df[df["Priority"] == "HIGH"]
)

quick_wins = len(
    df[df["Opportunity"] == "QUICK WIN"]
)


st.markdown("### Overview")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Monthly workload",
    f"{total_hours:.1f} h",
)

c2.metric(
    "Potential saving",
    f"{potential_saved:.1f} h",
)

c3.metric(
    "Saving potential",
    f"{saving_percentage:.0f}%",
)

c4.metric(
    "High priority",
    high_priority,
)

c5.metric(
    "Quick wins",
    quick_wins,
)


st.divider()


# --------------------------------------------------
# OPPORTUNITY MATRIX
# --------------------------------------------------

st.subheader("Automation Opportunity Matrix")

st.caption(
    "High-impact activities with low implementation complexity "
    "are generally the strongest candidates for automation."
)


plot_df = df.copy()

# Plotly doesn't like bubbles with size 0.
plot_df["Bubble Size"] = (
    plot_df["Monthly Hours"]
    .clip(lower=0.5)
)


fig = px.scatter(
    plot_df,
    x="Complexity Score",
    y="Impact Score",
    size="Bubble Size",
    color="Automation Score",
    hover_name="Task",
    hover_data={
        "Department": True,
        "Category": True,
        "Monthly Hours": ":.1f",
        "Potential Hours Saved": ":.1f",
        "Priority Score": ":.0f",
        "Automation Score": ":.0f",
        "Complexity Score": ":.0f",
        "Impact Score": ":.0f",
        "Bubble Size": False,
    },
    size_max=45,
    color_continuous_scale="Viridis",
)


# Quadrant lines
fig.add_vline(
    x=50,
    line_width=1,
    line_dash="dash",
)

fig.add_hline(
    y=50,
    line_width=1,
    line_dash="dash",
)


# Quadrant labels
fig.add_annotation(
    x=25,
    y=96,
    text="QUICK WINS",
    showarrow=False,
    font=dict(size=13),
)

fig.add_annotation(
    x=75,
    y=96,
    text="STRATEGIC",
    showarrow=False,
    font=dict(size=13),
)

fig.add_annotation(
    x=25,
    y=4,
    text="LOW PRIORITY",
    showarrow=False,
    font=dict(size=13),
)

fig.add_annotation(
    x=75,
    y=4,
    text="REASSESS",
    showarrow=False,
    font=dict(size=13),
)


fig.update_xaxes(
    title="Implementation Complexity →",
    range=[0, 100],
)

fig.update_yaxes(
    title="Business Impact →",
    range=[0, 100],
)


fig.update_layout(
    height=600,
    margin=dict(
        l=20,
        r=20,
        t=30,
        b=20,
    ),
    coloraxis_colorbar=dict(
        title="Automation<br>Score"
    ),
)


st.plotly_chart(
    fig,
    use_container_width=True,
)


st.caption(
    "Bubble size represents estimated monthly workload. "
    "Color represents automation suitability."
)


# --------------------------------------------------
# PRIORITY RANKING
# --------------------------------------------------

st.divider()

st.subheader("Priority Ranking")

st.write(
    "Activities ranked by automation potential, business impact "
    "and estimated implementation complexity."
)


ranked = df.sort_values(
    "Priority Score",
    ascending=False,
).reset_index(drop=True)

ranked.insert(
    0,
    "Rank",
    range(1, len(ranked) + 1),
)


st.dataframe(
    ranked[
        [
            "Rank",
            "Task",
            "Department",
            "Monthly Hours",
            "Automation Score",
            "Impact Score",
            "Complexity Score",
            "Priority Score",
            "Potential Hours Saved",
            "Opportunity",
        ]
    ],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Monthly Hours": st.column_config.NumberColumn(
            format="%.1f h"
        ),
        "Potential Hours Saved": st.column_config.NumberColumn(
            format="%.1f h"
        ),
        "Automation Score": st.column_config.ProgressColumn(
            min_value=0,
            max_value=100,
            format="%.0f",
        ),
        "Impact Score": st.column_config.ProgressColumn(
            min_value=0,
            max_value=100,
            format="%.0f",
        ),
        "Priority Score": st.column_config.ProgressColumn(
            min_value=0,
            max_value=100,
            format="%.0f",
        ),
    },
)


# --------------------------------------------------
# TOP OPPORTUNITY
# --------------------------------------------------

st.divider()

st.subheader("Top Opportunity")


top = ranked.iloc[0]


st.markdown(
    f"## {top['Task']}"
)

st.write(
    f"**{top['Opportunity']}** · "
    f"{top['Department']} · "
    f"{top['Category']}"
)


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Automation",
    f"{top['Automation Score']:.0f}/100",
)

c2.metric(
    "Impact",
    f"{top['Impact Score']:.0f}/100",
)

c3.metric(
    "Complexity",
    f"{top['Complexity Score']:.0f}/100",
)

c4.metric(
    "Priority",
    f"{top['Priority Score']:.0f}/100",
)


c1, c2 = st.columns(2)

with c1:

    st.metric(
        "Current workload",
        f"{top['Monthly Hours']:.1f} h/month",
    )

with c2:

    st.metric(
        "Potential saving",
        f"{top['Potential Hours Saved']:.1f} h/month",
    )


# --------------------------------------------------
# EXPLORE TASK
# --------------------------------------------------

st.divider()

st.subheader("Explore an activity")


task_options = {
    f"{row['Task']} · #{row['ID']}": row["ID"]
    for _, row in ranked.iterrows()
}


selected_label = st.selectbox(
    "Activity",
    list(task_options.keys()),
)


selected_id = task_options[selected_label]

selected = ranked[
    ranked["ID"] == selected_id
].iloc[0]


st.markdown(
    f"### {selected['Task']}"
)


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Automation",
    f"{selected['Automation Score']:.0f}/100",
)

c2.metric(
    "Impact",
    f"{selected['Impact Score']:.0f}/100",
)

c3.metric(
    "Complexity",
    f"{selected['Complexity Score']:.0f}/100",
)

c4.metric(
    "Priority",
    f"{selected['Priority Score']:.0f}/100",
)


st.markdown("#### Assessment")

if selected["Opportunity"] == "QUICK WIN":

    st.success(
        "QUICK WIN — High-value opportunity with relatively low "
        "implementation complexity."
    )

elif selected["Opportunity"] == "STRATEGIC AUTOMATION":

    st.warning(
        "STRATEGIC AUTOMATION — Strong automation opportunity, "
        "but implementation may require more effort."
    )

elif selected["Opportunity"] == "GOOD CANDIDATE":

    st.info(
        "GOOD CANDIDATE — Worth investigating as part of the "
        "automation roadmap."
    )

else:

    st.info(
        selected["Opportunity"]
    )


c1, c2 = st.columns(2)

c1.metric(
    "Current workload",
    f"{selected['Monthly Hours']:.1f} h/month",
)

c2.metric(
    "Potential saving",
    f"{selected['Potential Hours Saved']:.1f} h/month",
)