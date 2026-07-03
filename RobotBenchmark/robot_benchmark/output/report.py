import pandas as pd
import plotly.express as px
from typing import Any, Dict, List
from .metrics import MetricsCalculator

class BenchmarkReport:
    def __init__(self, results: List[Dict[str, Any]]):
        self.results = results
        self.metrics = MetricsCalculator.compute(results)

    def save_markdown(self, path: str) -> None:
        lines = ["# 具身智能基准测试报告", ""]
        lines.append("## 测试结果摘要")
        for k, v in self.metrics.items():
            lines.append(f"- **{k}**: {v:.4f}")
        lines.append("")
        lines.append("## 任务结果")
        df = pd.DataFrame(self.results)
        lines.append(df[["task_id", "name", "category", "success", "duration", "steps", "intervention_count"]].to_markdown(index=False))
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def save_plot(self, path: str) -> None:
        df = pd.DataFrame(self.results)
        fig = px.bar(df, x="name", y="duration", color="success", title="任务耗时对比")
        fig.write_html(path)