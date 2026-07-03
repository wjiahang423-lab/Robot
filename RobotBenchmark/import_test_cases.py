import json
import os
from robot_benchmark.tasks.task_db import TaskDatabase
from robot_benchmark.tasks.task_models import TaskSpec

def batch_import_cases(json_file_path: str, db_path: str):
    # 1. 初始化数据库
    db = TaskDatabase(db_path)
    db.create_tables()
    print(f"Connected to database at: {db_path}")

    # 2. 读取 JSON 文件
    if not os.path.exists(json_file_path):
        print(f"Error: File {json_file_path} not found.")
        return

    with open(json_file_path, 'r', encoding='utf-8') as f:
        cases = json.load(f)

    # 3. 批量写入
    count = 0
    for case_data in cases:
        # 将 JSON 字典转换为 TaskSpec 对象
        spec = TaskSpec(
            task_id=case_data['task_id'],
            name=case_data['name'],
            category=case_data['category'],
            description=case_data['description'],
            parameters=case_data['parameters']
        )
        db.add_task(spec)
        count += 1
        print(f"Imported: [{spec.task_id}] {spec.name}")

    print(f"\nSuccessfully imported {count} test cases.")

if __name__ == "__main__":
    # 配置路径（根据你的实际环境微调）
    JSON_PATH = "RobotBenchmark/test_cases.json"
    # 假设数据库文件在 RobotBenchmark 目录下
    DB_PATH = "RobotBenchmark/robot_benchmark/tasks/test_tasks.db" 
    
    batch_import_cases(JSON_PATH, DB_PATH)