import yaml
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class TaskConfig:
    atomic_skills: int
    basic_tasks: int
    long_running_tasks: int
    environment: str
    mode: str
    random_seed: int = 42
    task_constraints: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load_from_yaml(cls, path: str) -> "TaskConfig":
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return cls(
            atomic_skills=config["task_structure"]["atomic_skills"],
            basic_tasks=config["task_structure"]["basic_tasks"],
            long_running_tasks=config["task_structure"]["long_running_tasks"],
            environment=config["environment"]["type"],
            mode=config["environment"]["mode"],
            random_seed=config["task_structure"].get("random_seed", 42),
            task_constraints=config.get("task_constraints", {}),
        )

@dataclass
class TaskSpec:
    task_id: int
    name: str
    category: str
    description: str
    parameters: Dict[str, Any]