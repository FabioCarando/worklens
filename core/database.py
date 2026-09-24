import sqlite3
from pathlib import Path
from datetime import datetime

DB_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DB_DIR / "worklens.db"


def get_connection():
    DB_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            task_name TEXT NOT NULL,
            description TEXT,
            department TEXT,
            category TEXT,
            frequency TEXT,
            executions_per_period REAL,
            minutes_per_execution REAL,
            repetitiveness INTEGER,
            standardization INTEGER,
            manual_effort INTEGER,
            judgement_required INTEGER,
            error_probability INTEGER,
            digital_input INTEGER,
            tools_used TEXT,
            task_input TEXT,
            task_output TEXT,
            automation_wish TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def add_task(task):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (
            created_at,
            task_name,
            description,
            department,
            category,
            frequency,
            executions_per_period,
            minutes_per_execution,
            repetitiveness,
            standardization,
            manual_effort,
            judgement_required,
            error_probability,
            digital_input,
            tools_used,
            task_input,
            task_output,
            automation_wish
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().isoformat(),
            task["task_name"],
            task["description"],
            task["department"],
            task["category"],
            task["frequency"],
            task["executions_per_period"],
            task["minutes_per_execution"],
            task["repetitiveness"],
            task["standardization"],
            task["manual_effort"],
            task["judgement_required"],
            task["error_probability"],
            task["digital_input"],
            task["tools_used"],
            task["task_input"],
            task["task_output"],
            task["automation_wish"],
        ),
    )

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM tasks
        ORDER BY created_at DESC
        """
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def delete_task(task_id):
    conn = get_connection()

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()