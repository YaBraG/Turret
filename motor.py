import time
from AX12 import Ax12
from Inertial import InertialSensor

# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
Ax12.DEVICENAME = '/dev/ttyUSB0'

Ax12.BAUDRATE = 1_000_000

# sets baudrate and opens com port
Ax12.connect()
sensor = InertialSensor()

time.sleep(1)  # delay necessary to allow mpu9250 to settle

# create AX12 instance with ID 10
motor1 = Ax12(1)
motor1.set_max_voltage_limit(130)
motor1.enable_torque()
motor1.set_torque_limit(1023)


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


def main2():
    gyro, accel, mag, time, cycle, inertial = sensor.comp_filter()
    input_pos = int(input("Goal Possition: "))
    power = True
    forward = True

    while (True):
        print(mag)

    # while( power ):
    #     if(mag[0] - 1 > forward ):
    #         return
    #     if(mag[0] + 1 < forward):
    #         return


try:
    main()

except KeyboardInterrupt:
    time.sleep(0.05)
    motor1.set_moving_speed(0)
    motor1.disable_torque()
