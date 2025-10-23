from controller import Robot, DistanceSensor, Motor

TIME_STEP = 64
MAX_SPEED = 6.28

class MyRobotController:
    def __init__(self, max_speed=6.28):
        self.MAX_SPEED = max_speed

    def detect_obstacles(self, psValues):
        right_obstacle = psValues[0] < 80.0 or psValues[1] < 80.0 or psValues[2] < 80.0
        left_obstacle  = psValues[5] < 80.0 or psValues[6] < 80.0 or psValues[7] < 80.0
        return left_obstacle, right_obstacle

    def set_speeds(self, left_obstacle, right_obstacle):
        leftSpeed  = 0.5 * self.MAX_SPEED
        rightSpeed = 0.5 * self.MAX_SPEED
        return leftSpeed, rightSpeed

def manual_tests():
    controller = MyRobotController()
    test_cases = [
        ([0]*8, False, False, "No obstacles"),
        ([0,0,0,0,0,90,90,90], True, False, "Left obstacle"),
        ([90,90,90,0,0,0,0,0], False, True, "Right obstacle"),
        ([90,0,0,0,0,90,0,90], True, True, "Both sides obstacles"),
        ([80.0]*8, False, False, "All sensors at threshold"),
    ]
    for i, (psVals, expect_left, expect_right, desc) in enumerate(test_cases):
        left, right = controller.detect_obstacles(psVals)
        leftSpeed, rightSpeed = controller.set_speeds(left, right)
        print(f"TEST {i+1}: {desc}")
        print(f"  psValues: {psVals}")
        print(f"  Detected left: {left} (expected: {expect_left})")
        print(f"  Detected right: {right} (expected: {expect_right})")
        print(f"  leftSpeed: {leftSpeed}, rightSpeed: {rightSpeed}")
        print("-"*30)

# Run manual tests first
manual_tests()

# --- Webots simulation code (REMOVE the if __name__ == "__main__": block!) ---

# create the Robot instance
robot = Robot()
controller = MyRobotController(MAX_SPEED)

# initialize devices
ps = []
psNames = [
    'ps0', 'ps1', 'ps2', 'ps3',
    'ps4', 'ps5', 'ps6', 'ps7'
]

for i in range(8):
    ps.append(robot.getDevice(psNames[i]))
    ps[i].enable(TIME_STEP)

leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

# feedback loop: step simulation until receiving an exit event
while robot.step(TIME_STEP) != -1:
    # read sensors outputs
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())

    # detect obstacles using class method
    left_obstacle, right_obstacle = controller.detect_obstacles(psValues)

    # calculate target speeds using class method
    leftSpeed, rightSpeed = controller.set_speeds(left_obstacle, right_obstacle)

    # set wheel speeds
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)
