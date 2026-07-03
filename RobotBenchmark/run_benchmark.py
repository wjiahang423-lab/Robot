
import argparse
from robot_benchmark.adapters.pybullet_env import PyBulletEnvironment
from robot_benchmark.execution.executor import BenchmarkExecutor
from robot_benchmark.output.report import BenchmarkReport
from robot_benchmark.tasks.task_db import TaskDatabase
from robot_benchmark.tasks.task_scheduler import TaskScheduler
from robot_benchmark.tasks.task_models import TaskConfig

def main():
    parser = argparse.ArgumentParser(description="Embodied Intelligence Benchmark Runner")
    parser.add_argument("--config", default="config/sample_task.yml", help="YAML task config file")
    parser.add_argument("--mode", choices=["static", "dynamic", "combined"], default="dynamic")
    parser.add_argument("--db", default="benchmark_tasks.db", help="SQLite task database")
    args = parser.parse_args()

    task_db = TaskDatabase(args.db)
    task_db.create_tables()
    task_db.ensure_sample_tasks()

    config = TaskConfig.load_from_yaml(args.config)
    scheduler = TaskScheduler(task_db)
    tasks = scheduler.sample_tasks(config)

    env = PyBulletEnvironment(gui=False, simulation_mode=args.mode)
    env.setup()
    executor = BenchmarkExecutor(env)
    results = executor.run(tasks, executor)

    report = BenchmarkReport(results)
    report.save_markdown("benchmark_report.md")
    report.save_plot("benchmark_plot.html")

    env.teardown()
    print("Benchmark complete. Report saved to benchmark_report.md")

if __name__ == "__main__":
    main()