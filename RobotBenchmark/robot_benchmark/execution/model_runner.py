import time
from typing import Any, Dict

class ModelRunner:
    def __init__(self, framework: str = "pytorch", model_path: str = None):
        self.framework = framework
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self):
        if self.framework == "pytorch":
            try:
                import torch
                return torch.load(self.model_path) if self.model_path else None
            except ImportError:
                raise RuntimeError("PyTorch is not installed")
        elif self.framework == "tensorflow":
            try:
                import tensorflow as tf
                return tf.keras.models.load_model(self.model_path) if self.model_path else None
            except ImportError:
                raise RuntimeError("TensorFlow is not installed")
        return None

    def infer(self, input_data: Any) -> Dict[str, Any]:
        start = time.perf_counter()
        output = None
        if self.framework == "pytorch":
            import torch
            with torch.no_grad():
                output = self.model(input_data) if self.model else {}
        elif self.framework == "tensorflow":
            output = self.model.predict(input_data) if self.model else {}
        latency = time.perf_counter() - start
        return {"output": output, "latency": latency}