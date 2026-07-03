from typing import List, Dict

class MetricsCalculator:
    @staticmethod
    def compute(results: List[Dict]) -> Dict[str, float]:
        total = len(results)
        success_count = sum(1 for r in results if r["success"])
        avg_duration = sum(r["duration"] for r in results) / total if total else 0.0
        avg_steps = sum(r["steps"] for r in results) / total if total else 0.0
        intervention_total = sum(r["intervention_count"] for r in results)
        robustness = 1.0 - (intervention_total / (total * 10)) if total else 0.0
        return {
            "success_rate": success_count / total if total else 0.0,
            "average_duration": avg_duration,
            "average_steps": avg_steps,
            "intervention_rate": intervention_total / total if total else 0.0,
            "robustness": max(0.0, min(1.0, robustness)),
        }