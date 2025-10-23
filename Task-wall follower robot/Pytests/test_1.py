import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print("SYSPATH DEBUG:", sys.path)

from controller.my_robot_controller import MyRobotController

def test_no_obstacle():
    controller = MyRobotController()
    psValues = [0]*8
    left_obstacle, right_obstacle = controller.detect_obstacles(psValues)
    leftSpeed, rightSpeed = controller.set_speeds(left_obstacle, right_obstacle)
    assert not left_obstacle
    assert not right_obstacle
    assert leftSpeed == 0.5 * controller.MAX_SPEED
    assert rightSpeed == 0.5 * controller.MAX_SPEED
