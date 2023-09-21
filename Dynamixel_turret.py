import time
from AX12 import Ax12
import socketio

sio = socketio.Client()
Ax12.DEVICENAME = '/dev/ttyUSB0'
Ax12.BAUDRATE = 1000000
Ax12.connect()


def remap(x, oMin, oMax, nMin, nMax):

    # range check
    if oMin == oMax:
        print("Warning: Zero input range")
        return None

    if nMin == nMax:
        print("Warning: Zero output range")
        return None

    # check reversed input range
    reverseInput = False
    oldMin = min(oMin, oMax)
    oldMax = max(oMin, oMax)
    if not oldMin == oMin:
        reverseInput = True

    # check reversed output range
    reverseOutput = False
    newMin = min(nMin, nMax)
    newMax = max(nMin, nMax)
    if not newMin == nMin:
        reverseOutput = True

    portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
    if reverseInput:
        portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)

    result = portion + newMin
    if reverseOutput:
        result = newMax - portion

    return result


motor1 = Ax12(1)
motor1.set_max_voltage_limit(160)
motor1.enable_torque()
motor1.set_torque_limit(1023)
motor2 = Ax12(2)
motor2.set_max_voltage_limit(160)
motor2.enable_torque()
motor2.set_torque_limit(1023)


def user_input():
    """Check to see if user wants to continue"""
    ans = input('Continue? : y/n ')
    if ans == 'n':
        return False
    else:
        return True


def main():
    """ sets goal position based on user input """
    bool_test = True
    speed = int(input("Motor Speed: "))
    motor1.set_moving_speed(speed)
    while bool_test:

        print("\nPosition of dxl ID: %d is %d " %
              (motor1.id, motor1.get_present_position()))
        # desired angle input
        input_pos = int(input("Goal Possition: "))
        motor1.set_goal_position(input_pos)
        print("Position of dxl ID: %d is now: %d " %
              (motor1.id, motor1.get_present_position()))
        bool_test = user_input()


try:
    main()

except KeyboardInterrupt:
    time.sleep(0.05)
    motor1.set_moving_speed(0)
    motor2.set_moving_speed(0)
    motor1.disable_torque()
    motor2.disable_torque()
