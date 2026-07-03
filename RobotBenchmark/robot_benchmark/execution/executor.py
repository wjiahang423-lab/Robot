import asyncio
import time
from typing import Any, Dict, List
from ..adapters.base import EnvironmentAdapter
from ..tasks.task_models import TaskSpec
from .model_runner import ModelRunner

class BenchmarkExecutor:
    def __init__(self, env: EnvironmentAdapter):
        self.env = env
        self.model_runner = ModelRunner(framework="pytorch")
        self.intervention_count = 0

    async def execute(self, task_spec: TaskSpec) -> Dict[str, Any]:
        self.env.reset(task_spec.parameters)
        start_time = time.time()
        success = False
        result_details = {}
        timeout = task_spec.parameters.get("timeout", 30)
        for step_index in range(1, timeout + 1):
            action = self._generate_action(step_index, task_spec)
            state = self.env.step(action)
            inference = self.model_runner.infer(action)
            result_details[f"step_{step_index}"] = {
                "state": state,
                "output": inference["output"],
                "latency": inference["latency"],
            }
            if self._check_task_complete(state, task_spec):
                success = True
                break
            await asyncio.sleep(0)
        return {
            "task_id": task_spec.task_id,
            "name": task_spec.name,
            "category": task_spec.category,
            "success": success,
            "duration": time.time() - start_time,
            "intervention_count": self.intervention_count,
            "steps": len(result_details),
            "details": result_details,
        }

    def _generate_action(self, step_index: int, task_spec: TaskSpec) -> Dict[int, float]:
        return {0: 0.0}

    def _check_task_complete(self, state: Dict[str, Any], task_spec: TaskSpec) -> bool:
        if task_spec.category == "basic":
            goal = task_spec.parameters.get("goal")
            pos = state.get("position", [0, 0, 0])
            if goal is None:
                return False
            return sum((pos[i] - goal[i]) ** 2 for i in range(3)) < 0.05
        return False