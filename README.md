# WorkLens

### Find the work worth automating.

WorkLens is an open-source, local-first task diary designed to help individuals and organizations identify repetitive work and discover high-impact automation opportunities.

Instead of asking *"What should we automate?"*, WorkLens starts with a simpler question:

> **Where is your time actually going?**

Employees record repetitive, manual, or time-consuming activities during their workday. WorkLens analyzes those activities to identify where automation could generate the greatest impact.

---

## Why WorkLens?

Organizations often know that employees spend time on repetitive work — but they rarely have structured data showing:

- which activities consume the most time;
- how frequently they are performed;
- which tasks are highly repetitive;
- where manual errors occur;
- which processes could realistically be automated.

WorkLens turns a simple task diary into an **automation opportunity map**.

---

## How it works

### 1. Capture

Employees record activities they regularly perform, including:

- frequency;
- execution time;
- repetitiveness;
- manual effort;
- standardization;
- human judgement required;
- tools used;
- inputs and outputs.

### 2. Analyze

WorkLens evaluates the recorded activities and estimates their automation potential.

### 3. Prioritize

Tasks are compared using factors such as:

- time impact;
- automation potential;
- implementation complexity;
- potential time savings.

The goal is to identify **high-impact, low-complexity automation opportunities**.

### 4. Automate

WorkLens suggests which processes should be investigated first and which technologies may be suitable.

---

## Automation Opportunity Score

WorkLens is being designed around an explainable scoring model.

Each activity will receive an:

- **Automation Score**
- **Impact Score**
- **Complexity Score**
- **Priority Score**

The scoring methodology considers characteristics such as:

```text
Frequency
Execution time
Repetitiveness
Standardization
Manual effort
Human judgement
Digital inputs
Error probability
```

The objective is not to replace process analysis, but to help teams quickly identify where deeper investigation is worthwhile.

---

## Example

An employee records:

> Every morning I download several Excel files from an ERP system,
> copy the data into another workbook, refresh a pivot table,
> and email the report.

WorkLens could identify the activity as:

```text
Automation Score     93 / 100
Monthly workload     17.3 hours
Potential saving     13.8 hours
Priority             HIGH
Opportunity          QUICK WIN
```

Possible automation approach:

```text
Scheduled extraction
        ↓
Automated data transformation
        ↓
Report refresh
        ↓
Automatic distribution
```

---

## Local-first

WorkLens is designed to work locally.

Task diary information is stored in a local SQLite database and is excluded from the Git repository.

```text
Employee
   ↓
WorkLens
   ↓
Local SQLite database
   ↓
Automation analysis
```

This makes it possible to experiment with process discovery without requiring a cloud database or external service.

---

## Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- OpenPyXL

---

## Project Structure

```text
worklens/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── core/
│   ├── __init__.py
│   └── database.py
│
├── pages/
│   ├── 1_Log_Task.py
│   └── 2_My_Diary.py
│
└── data/
    └── worklens.db
```

The local database is excluded from Git.

---

## Run locally

Clone the repository:

```bash
git clone https://github.com/FabioCarando/worklens.git
cd worklens
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run WorkLens:

```bash
streamlit run app.py
```

---

## Roadmap

WorkLens is currently in early development.

Planned features:

- [x] Local task diary
- [x] SQLite persistence
- [x] Task management
- [ ] Automation Opportunity Score
- [ ] Impact Score
- [ ] Complexity Score
- [ ] Estimated time savings
- [ ] Impact × Effort matrix
- [ ] Automation recommendations
- [ ] Analytics dashboard
- [ ] CSV / Excel export
- [ ] Multi-user aggregated analysis
- [ ] Optional AI-assisted process analysis

---

## Philosophy

WorkLens is based on a simple idea:

> **Before automating work, understand the work.**

---

## Contributing

WorkLens is an experimental open-source project.

Ideas, issues, feedback and contributions are welcome.

---

## License

A license will be added as the project matures.