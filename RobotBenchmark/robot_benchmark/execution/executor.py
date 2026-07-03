import asyncio
import time
from typing import Any, Dict, List
from ..adapters.base import EnvironmentAdapter
from ..tasks.task_models import TaskSpec
from .model_runner import ModelRunner

# ... 保持前面的 import 不变 ...

class BenchmarkExecutor:
    def __init__(self, env: EnvironmentAdapter):
        self.env = env
        self.model_runner = ModelRunner(framework="pytorch")
        self.intervention_count = 0
        # 新增：关节映射表
        # 实际应用中，这个表可以从 URDF 解析出来，或者在 TaskSpec 里定义
        self.joint_map = {
            "left_hip": 0,
            "left_knee": 1,
            "right_hip": 2,
            "right_knee": 3,
            "left_shoulder": 4,
            "left_elbow": 5,
            "right_shoulder": 6,
            "right_elbow": 7
        }

    async def execute(self, task_spec: TaskSpec) -> Dict[str, Any]:
        # 这里保持原样，但在 _generate_action 中使用新的映射逻辑
        self.env.reset(task_spec.parameters)
        start_time = time.time()
        success = False
        result_details = {}
        timeout = task_spec.parameters.get("timeout", 30)
        
        for step_index in range(1, timeout + 1):
            # 修改点：这里现在能处理稍微复杂的动作了
            action = self._generate_action(step_index, task_spec)
            state = self.env.step(action)
            
            # 注意：这里 model_runner.infer 目前可能还没写好，
            # 如果报错，可以暂时 mock 掉它。
            try:
                inference = self.model_runner.infer(action)
            except Exception:
                inference = {"output": None, "latency": 0.0}

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
        """
        生成动作的占位逻辑。
        在模型跑通前，我们可以模拟一个简单的摆动动作。
        """
        # 模拟机器人由于重力稍微弯曲膝盖的动作
        # 这里我们将 joint_map 中的 key 映射到真实的关节 ID
        return {
            self.joint_map["left_knee"]: 0.2, 
            self.joint_map["right_knee"]: 0.2
        }

    def _check_task_complete(self, state: Dict[str, Any], task_spec: TaskSpec) -> bool:
        if task_spec.category == "basic":
            goal = task_spec.parameters.get("goal")
            pos = state.get("position", [0, 0, 0])
            if goal is None:
                return False
            # 计算欧氏距离
            distance = sum((pos[i] - goal[i]) ** 2 for i in range(3))
            return distance < 0.05
        return False

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