import streamlit as st
import pandas as pd

from core.database import (
    init_db,
    get_tasks,
    delete_task,
)


st.set_page_config(
    page_title="My Diary · WorkLens",
    page_icon="◫",
    layout="wide",
)

init_db()


st.title("My Diary")

st.write(
    "Review the activities you have recorded."
)


tasks = get_tasks()


if not tasks:

    st.info(
        "No tasks recorded yet. Go to **Log Task** to add your first activity."
    )

    st.stop()


df = pd.DataFrame(tasks)


display_columns = [
    "id",
    "task_name",
    "department",
    "category",
    "frequency",
    "executions_per_period",
    "minutes_per_execution",
    "repetitiveness",
    "manual_effort",
]


st.dataframe(
    df[display_columns],
    use_container_width=True,
    hide_index=True,
)


st.subheader("Delete task")

task_options = {
    f"{row['id']} · {row['task_name']}": row["id"]
    for _, row in df.iterrows()
}


selected = st.selectbox(
    "Select task",
    list(task_options.keys()),
)


if st.button(
    "Delete selected task",
    type="secondary",
):

    delete_task(
        task_options[selected]
    )

    st.success(
        "Task deleted."
    )

    st.rerun()