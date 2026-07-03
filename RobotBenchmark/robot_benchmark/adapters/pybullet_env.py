import pybullet as p
import pybullet_data
import random
import time
from typing import Any, Dict, Optional
from .base import EnvironmentAdapter

class PyBulletEnvironment(EnvironmentAdapter):
    def __init__(self, gui: bool = False, simulation_mode: str = "dynamic"):
        self.gui = gui
        self.simulation_mode = simulation_mode
        self.client_id: Optional[int] = None
        self.robot_id: Optional[int] = None
        self.plane_id: Optional[int] = None

    def setup(self) -> None:
        connection_mode = p.GUI if self.gui else p.DIRECT
        self.client_id = p.connect(connection_mode)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81, physicsClientId=self.client_id)
        self.plane_id = p.loadURDF("plane.urdf", physicsClientId=self.client_id)
        p.setTimeStep(1.0 / 240.0, physicsClientId=self.client_id)

    def teardown(self) -> None:
        if self.client_id is not None:
            p.disconnect(self.client_id)
            self.client_id = None

    def reset(self, task_spec: Dict[str, Any]) -> None:
        if self.client_id is None:
            raise RuntimeError("PyBullet client not initialized")
        if self.robot_id is not None:
            p.removeBody(self.robot_id, physicsClientId=self.client_id)
        self.robot_id = p.loadURDF(
            task_spec.get("robot_urdf", "humanoid_simple.urdf"),
            basePosition=task_spec.get("robot_start_pos", [0, 0, 0.5]),
            baseOrientation=p.getQuaternionFromEuler(task_spec.get("robot_start_ori", [0, 0, 0])),
            physicsClientId=self.client_id,
        )
        self.inject_disturbance()

    def step(self, action: Any) -> Dict[str, Any]:
        if self.client_id is None:
            raise RuntimeError("Simulation not initialized")
        if isinstance(action, dict):
            for joint_index, joint_target in action.items():
                p.setJointMotorControl2(
                    bodyIndex=self.robot_id,
                    jointIndex=joint_index,
                    controlMode=p.POSITION_CONTROL,
                    targetPosition=joint_target,
                    force=500,
                    physicsClientId=self.client_id,
                )
        p.stepSimulation(physicsClientId=self.client_id)
        time.sleep(1.0 / 240.0)
        return self.get_state()

    def inject_disturbance(self, level: float = 0.15) -> None:
        if self.client_id is None:
            return
        if self.simulation_mode in {"dynamic", "combined"}:
            light_x = random.uniform(-2.0, 2.0)
            light_y = random.uniform(-2.0, 2.0)
            p.resetDebugVisualizerCamera(
                cameraDistance=3,
                cameraYaw=random.uniform(0, 360),
                cameraPitch=random.uniform(-40, 40),
                cameraTargetPosition=[light_x, light_y, 0],
                physicsClientId=self.client_id,
            )
            num_obstacles = random.randint(1, 3)
            for _ in range(num_obstacles):
                pos = [random.uniform(-1, 1), random.uniform(-1, 1), 0.1]
                size = random.uniform(0.05, 0.2)
                col_box = p.createCollisionShape(p.GEOM_BOX, halfExtents=[size, size, size])
                p.createMultiBody(
                    baseMass=0,
                    baseCollisionShapeIndex=col_box,
                    basePosition=pos,
                    physicsClientId=self.client_id,
                )

    def get_state(self) -> Dict[str, Any]:
        if self.client_id is None or self.robot_id is None:
            return {}
        pos, orn = p.getBasePositionAndOrientation(self.robot_id, physicsClientId=self.client_id)
        return {
            "position": pos,
            "orientation": orn,
            "velocity": p.getBaseVelocity(self.robot_id, physicsClientId=self.client_id),
        }