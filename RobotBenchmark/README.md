# 具身智能基准测试框架原型

本项目基于 `YD/T 6770-2026` 框架设计，采用 Python 模块化三层结构实现快速原型验证。

## 结构

- `robot_benchmark/adapters/`：环境适配层
- `robot_benchmark/tasks/`：任务元数据与任务调度
- `robot_benchmark/execution/`：测试执行与模型推理
- `robot_benchmark/output/`：指标计算与报告生成

## 快速运行

```bash
pip install -r requirements.txt
python run_benchmark.py --config config/sample_task.yml --mode dynamic


说明与后续
这个原型已经覆盖你要求的三层架构、PyBullet 环境适配、SQLite 任务库、asyncio 调度、模型推理与指标输出。
ROS 适配已写占位模块，可继续扩展真实机器人集成。