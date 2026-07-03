import asyncio
from robot_benchmark.adapters.pybullet_env import PyBulletEnvironment
from robot_benchmark.execution.executor import BenchmarkExecutor
from robot_benchmark.tasks.task_db import TaskDatabase
from robot_benchmark.tasks.task_scheduler import TaskScheduler

async def run_test_pipeline():
    # 1. 配置路径
    db_path = "RobotBenchmark/robot_benchmark/tasks/test_tasks.db"
    
    # 2. 初始化数据库与调度器
    task_db = TaskDatabase(db_path)
    task_db.create_tables()
    scheduler = TaskScheduler(task_db)
    
    # 3. 获取测试 Case (例如获取所有 category='basic' 的任务)
    print("Fetching tasks from database...")
    tasks = scheduler.sample_tasks(category="basic") # 假设 scheduler 支持过滤
    if not tasks:
        # 如果没有过滤，就拿前两个
        tasks = scheduler.sample_tasks()[:2]
    
    print(f"Found {len(tasks)} tasks to run.")

    # 4. 初始化环境 (开启 GUI 以便观察)
    env = PyBulletEnvironment(gui=True, simulation_mode="dynamic")
    env.setup()
    
    # 5. 初始化执行器
    executor = BenchmarkExecutor(env)
    
    try:
        for task in tasks:
            print(f"\n>>> Starting Task: {task.name} (ID: {task.task_id})")
            # 使用 executor 异步执行任务
            result = await executor.execute(task)
            print(f"Task Finished. Success: {result['success']}, Duration: {result['duration']:.2f}s")
            
    finally:
        print("\nCleaning up environment...")
        env.teardown()

if __name__ == "__main__":
    asyncio.run(run_test_pipeline())
