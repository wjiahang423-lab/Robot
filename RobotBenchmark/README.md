# 具身智能基准测试框架 (Embodied Intelligence Benchmark)

本项目基于 `YD/T 6770-2026` 框架设计，采用 Python 模块化三层结构实现机器人任务的快速原型验证与基准测试。

## 🚀 快速开始

### 1. 环境准备
安装必要的依赖：
```bash
pip install -r requirements.txt
```
*注意：如果安装 `pybullet` 失败，请确保系统中已安装 **Microsoft C++ Build Tools**。*

### 2. 数据初始化
本项目使用 SQLite 数据库管理测试 Case。首先初始化数据库并导入测试数据：

```bash
# 使用导入脚本加载 test_cases.json
python import_test_cases.py
```

### 3. 运行基准测试
使用主入口运行完整的测试流程：
```bash
python run_benchmark.py --config config/sample_task.yml --mode dynamic
```

## 🏗 架构设计

项目采用解耦的四层架构：

### 1. 环境适配层 (`adapters/`)
负责与物理引擎或真实机器人硬件的交互。
- **`PyBulletEnvironment`**: 支持 PyBullet 仿真。包含环境初始化 (`setup`)、重置 (`reset`)、步进 (`step`) 和状态获取 (`get_state`)。
- **`EnvironmentAdapter`**: 基类，定义了所有适配器必须遵循的标准接口。

### 2. 任务元数据与调度层 (`tasks/`)
负责测试 Case 的定义、存储与分发。
- **`TaskDatabase`**: 基于 SQLite 的持久化存储。
    - `add_task(spec)`: 将新的测试 Case 写入数据库。
    - `get_tasks(category)`: 按类别检索任务。
- **`TaskScheduler`**: 负责从数据库中获取并安排测试顺序。
- **`TaskSpec`**: 定义任务的参数结构（包含模型路径、目标位置、超时时间等）。

### 3. 测试执行与模型推理层 (`execution/`)
负责驱动模型在环境中运行。
- **`BenchmarkExecutor`**: 核心循环引擎。它接收任务，调用适配器获取状态，并将模型输出的动作发送给环境。
- **`ModelRunner`**:（待扩展）负责具体模型的加载与推理逻辑。

### 4. 指标计算与报告层 (`output/`)
负责评估测试表现。
- **`Metrics`**: 定义成功率、路径长度、耗时等核心评价指标。
- **`BenchmarkReport`**: 生成 Markdown 报告和可视化图表（HTML）。

## 🛠 核心 API 说明

### TaskDatabase
| 函数 | 说明 |
| :--- | :--- |
| `create_tables()` | 初始化 SQLite 数据库表结构 |
| `add_task(spec)` | 将 `TaskSpec` 转换为 JSON 字符串存入数据库 |
| `get_tasks(category)` | 从数据库加载任务列表，并解析 JSON 参数 |

### PyBulletEnvironment
| 函数 | 说明 |
| :--- | :--- |
| `setup()` | 连接 PyBullet 引擎，设置重力与基础平面 |
| `reset(task_spec)` | 加载 URDF 模型，设置初始位置，注入随机干扰 |
| `step(action)` | 执行关节电机控制 (`POSITION_CONTROL`) 并步进仿真 |
| `get_state()` | 返回当前的机器人位置、朝向和速度 |

## 扩展指南

### 如何添加新的测试 Case
1. 在 `test_cases.json` 中添加新的 JSON 对象。
2. 运行 `python import_test_cases.py` 刷新数据库。

### 如何添加新的环境适配器
1. 在 `adapters/` 下创建一个新类继承 `EnvironmentAdapter`。
2. 实现 `setup`, `reset`, `step`, `get_state` 方法。
3. 在 `run_benchmark.py` 中根据配置选择对应的适配器类。

---
*本项目旨在为具身智能提供标准化的评测基准。*