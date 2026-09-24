import streamlit as st

from core.database import init_db, add_task


st.set_page_config(
    page_title="Log Task · WorkLens",
    page_icon="✚",
    layout="wide",
)

init_db()


st.title("Log a task")

st.write(
    "Describe an activity you regularly perform. "
    "Focus especially on repetitive, manual or time-consuming work."
)


with st.form("task_form"):

    st.subheader("Task")

    task_name = st.text_input(
        "Task name *",
        placeholder="e.g. Prepare weekly sales report"
    )

    description = st.text_area(
        "What do you do?",
        placeholder=(
            "I download an Excel file, copy the data into another workbook, "
            "update formulas and send the final report by email..."
        ),
        height=120,
    )

    col1, col2 = st.columns(2)

    with col1:
        department = st.text_input(
            "Department",
            placeholder="e.g. Finance"
        )

    with col2:
        category = st.selectbox(
            "Category",
            [
                "Data entry",
                "Reporting",
                "Document processing",
                "Email",
                "Data validation",
                "Administration",
                "Analysis",
                "Communication",
                "Other",
            ],
        )


    st.subheader("Frequency")

    col1, col2, col3 = st.columns(3)

    with col1:
        frequency = st.selectbox(
            "Frequency",
            [
                "Daily",
                "Weekly",
                "Monthly",
                "Quarterly",
                "Yearly",
                "Ad hoc",
            ],
        )

    with col2:
        executions = st.number_input(
            "Executions per period",
            min_value=0.0,
            value=1.0,
            step=1.0,
        )

    with col3:
        minutes = st.number_input(
            "Minutes per execution",
            min_value=0.0,
            value=15.0,
            step=5.0,
        )


    st.subheader("How is the task performed?")

    col1, col2 = st.columns(2)

    with col1:
        repetitiveness = st.slider(
            "Repetitiveness",
            1,
            5,
            3,
            help="1 = always different, 5 = almost identical every time",
        )

        standardization = st.slider(
            "Standardization",
            1,
            5,
            3,
            help="1 = no fixed procedure, 5 = clear and repeatable procedure",
        )

        manual_effort = st.slider(
            "Manual effort",
            1,
            5,
            3,
        )

    with col2:
        judgement = st.slider(
            "Human judgement required",
            1,
            5,
            3,
            help="1 = rule based, 5 = requires significant judgement",
        )

        error_probability = st.slider(
            "Risk of manual errors",
            1,
            5,
            3,
        )

        digital_input = st.checkbox(
            "Inputs are primarily digital",
            value=True,
        )


    st.subheader("Process")

    tools = st.text_input(
        "Tools used",
        placeholder="Excel, Outlook, SAP..."
    )

    col1, col2 = st.columns(2)

    with col1:
        task_input = st.text_area(
            "Input",
            placeholder="Excel export from ERP"
        )

    with col2:
        task_output = st.text_area(
            "Output",
            placeholder="Weekly management report"
        )


    st.subheader("Automation")

    automation_wish = st.text_area(
        "If you could automate something about this task, what would it be?",
        placeholder=(
            "I would like the report to be generated automatically "
            "without copying data manually."
        ),
        height=100,
    )


    submitted = st.form_submit_button(
        "Save task",
        use_container_width=True,
        type="primary",
    )


if submitted:

    if not task_name.strip():

        st.error(
            "Please enter a task name."
        )

    else:

        task = {
            "task_name": task_name,
            "description": description,
            "department": department,
            "category": category,
            "frequency": frequency,
            "executions_per_period": executions,
            "minutes_per_execution": minutes,
            "repetitiveness": repetitiveness,
            "standardization": standardization,
            "manual_effort": manual_effort,
            "judgement_required": judgement,
            "error_probability": error_probability,
            "digital_input": int(digital_input),
            "tools_used": tools,
            "task_input": task_input,
            "task_output": task_output,
            "automation_wish": automation_wish,
        }

        add_task(task)

        st.success(
            "Task saved successfully."
        )

        st.balloons()