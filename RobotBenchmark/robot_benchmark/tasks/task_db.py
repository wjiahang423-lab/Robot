import sqlite3
import json
from typing import List
from .task_models import TaskSpec

CREATE_TASK_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    parameters TEXT NOT NULL
);
"""

class TaskDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_tables(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(CREATE_TASK_TABLE)
            conn.commit()

    def add_task(self, spec: TaskSpec) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO tasks (task_id, name, category, description, parameters) VALUES (?, ?, ?, ?, ?)",
                (spec.task_id, spec.name, spec.category, spec.description, json.dumps(spec.parameters)),
            )
            conn.commit()

    def get_tasks(self, category: str = None) -> List[TaskSpec]:
        query = "SELECT task_id, name, category, description, parameters FROM tasks"
        params = []
        if category:
            query += " WHERE category = ?"
            params.append(category)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
        return [
            TaskSpec(
                task_id=row[0],
                name=row[1],
                category=row[2],
                description=row[3],
                parameters=json.loads(row[4]),
            )
            for row in rows
        ]

    def ensure_sample_tasks(self) -> None:
        existing_tasks = self.get_tasks()
        if existing_tasks:
            return
        sample_tasks = [
            TaskSpec(
                task_id=1,
                name="navigate_to_point",
                category="basic",
                description="Navigate to a target location while avoiding obstacles",
                parameters={"robot_urdf": "r2d2.urdf", "goal": [1.0, 0.0, 0.5], "timeout": 20},
            ),
            TaskSpec(
                task_id=2,
                name="pick_and_place",
                category="atomic",
                description="Pick an object and place it at target position",
                parameters={"robot_urdf": "kuka_iiwa/model.urdf", "object_pos": [0.5, 0, 0.1]},
            ),
            TaskSpec(
                task_id=3,
                name="long_inspection",
                category="long",
                description="Execute a long-running inspection trajectory",
                parameters={"robot_urdf": "r2d2.urdf", "duration": 60},
            ),
        ]
        for task in sample_tasks:
            self.add_task(task)