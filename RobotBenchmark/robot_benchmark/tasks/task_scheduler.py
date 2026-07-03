import asyncio
import random
from typing import List
from .task_db import TaskDatabase
from .task_models import TaskConfig, TaskSpec

class TaskScheduler:
    def __init__(self, task_db: TaskDatabase):
        self.task_db = task_db

    def sample_tasks(self, config: TaskConfig) -> List[TaskSpec]:
        tasks = []
        random.seed(config.random_seed)
        tasks.extend(self._sample_category("atomic", config.atomic_skills))
        tasks.extend(self._sample_category("basic", config.basic_tasks))
        tasks.extend(self._sample_category("long", config.long_running_tasks))
        return tasks

    def _sample_category(self, category: str, count: int) -> List[TaskSpec]:
        available = self.task_db.get_tasks(category=category)
        if not available:
            return []
        return random.sample(available, min(count, len(available)))

    async def execute_task(self, task_spec: TaskSpec, executor) -> dict:
        return await executor.execute(task_spec)

    async def run_all(self, task_specs: List[TaskSpec], executor) -> List[dict]:
        tasks = [self.execute_task(spec, executor) for spec in task_specs]
        return await asyncio.gather(*tasks)

    def run(self, task_specs: List[TaskSpec], executor) -> List[dict]:
        return asyncio.run(self.run_all(task_specs, executor))