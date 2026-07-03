import time
from robot_benchmark.adapters.pybullet_env import PyBulletEnvironment

def test_full_pipeline():
    print("=== Starting Smoke Test ===")
    
    # 1. 初始化环境 (开启 GUI 模式方便观察)
    # 这里我们开启 gui=True 看看机器人能不能出来
    env = PyBulletEnvironment(gui=True, simulation_mode="dynamic")
    
    try:
        print("[Step 1] Setting up PyBullet environment...")
        env.setup()
        
        # 2. 模拟从数据库获取到的任务参数
        # 我们手动模拟 JSON 里的第一个 case 里的参数
        mock_task_spec = {
            "robot_urdf": "humanoid_simple.urdf", # 使用我们刚才生成的模型
            "robot_start_pos": [0, 0, 0.5],
            "robot_start_ori": [0, 0, 0],
            "goal": [1.0, 0.0, 0.5],
            "timeout": 20
        }
        
        print(f"[Step 2] Resetting environment with spec: {mock_task_spec}")
        env.reset(mock_task_spec)
        
        # 3. 运行一个简单的循环（模拟模型输出动作）
        print("[Step 3] Running 100 simulation steps...")
        for i in range(100):
            # 模拟模型输出：给所有关节发送 0 度目标（让机器人保持不动或微动）
            # 这里的 joint_index 需要根据你的 URDF 调整，或者先发一个简单的
            mock_action = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0} 
            
            state = env.step(mock_action)
            
            if i % 20 == 0:
                print(f"  Step {i}: Position {state.get('position')}")
            
            # 控制运行速度，否则 GUI 窗口会飞速跳过
            time.sleep(1.0 / 240.0)
            
        print("=== Test Passed! ===")
        
    except Exception as e:
        print(f"!!! Test Failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("[Step 4] Tearing down environment...")
        env.teardown()

if __name__ == "__main__":
    test_full_pipeline()
