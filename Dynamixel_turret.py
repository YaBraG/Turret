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


motor1 = Ax12(1)  # Yaw
motor1.set_max_voltage_limit(160)
motor1.enable_torque()
motor1.set_torque_limit(1023)
motor2 = Ax12(2)  # Pitch
motor2.set_max_voltage_limit(160)
motor2.enable_torque()
motor2.set_torque_limit(1023)
# Motor 2 limit needs to be set at 150


try:
    @sio.event
    def connect():
        print('connection established')
        sio.emit("ID", 'python-servo-client')

    @sio.event
    def my_message(data):
        print('message received with ', data)
        sio.emit('my response', {'response': 'my response'})

    @sio.event
    def disconnect():
        print('disconnected from server')
        time.sleep(0.5)
        motor1.set_moving_speed(0)
        motor2.set_moving_speed(0)
        motor1.disable_torque()
        motor2.disable_torque()

    @sio.on('inertial-order')
    def on_message(yaw, pitch):
        m1Yaw = remap(yaw, -180, 180, 0, 1023)
        m2Pitch = remap(pitch, -180, 180, 150, 1023)
        motor1.set_goal_position(m1Yaw)
        motor2.set_goal_position(m2Pitch)
        print("Motor 1 position: %d " %
              (motor1.get_present_position()))

    sio.connect('http://192.168.2.13:3000')
    sio.wait()

except KeyboardInterrupt:
    time.sleep(0.5)
    motor1.set_moving_speed(0)
    motor2.set_moving_speed(0)
    motor1.disable_torque()
    motor2.disable_torque()
