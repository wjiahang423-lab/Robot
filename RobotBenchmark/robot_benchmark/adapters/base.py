from abc import ABC, abstractmethod
from typing import Any, Dict

class EnvironmentAdapter(ABC):
    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def teardown(self) -> None:
        pass

    @abstractmethod
    def reset(self, task_spec: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def step(self, action: Any) -> Dict[str, Any]:
        pass

    @abstractmethod
    def inject_disturbance(self, level: float = 0.1) -> None:
        pass

    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        pass