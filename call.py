import time
import socketio
from Inertial import InertialSensor

EMITTER_PI = 'EMITTER_PI'

EMIT_DISCRETE = 'EMIT_DISCRETE'
EMIT_INTEGRATED = 'EMIT_INTEGRATED'

DISCRETE = False
INTEGRATED = False

sio = socketio.Client()
sensor = InertialSensor()

time.sleep(1)  # delay necessary to allow mpu9250 to settle


@sio.event
def emit_discrete(val):
    DISCRETE = val

# make global variable to activate stuff


@sio.event
def emit_integrated(val):
    INTEGRATED = val


@sio.event
def connect():
    print('connection established')
    sio.emit("ID", EMITTER_PI)

    initLoop()


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    print('disconnected from server')


def initLoop():
    print("EMITING")
    while sio.handle_sigint:

        data = sensor.comp_filter()

        gyro, accel, mag, time, cycle, inertial = sensor.comp_filter()

        if (INTEGRATED):
            print("INT")
            sio.emit('pi-inertial', inertial)

        if (DISCRETE):
            print("DIS")
            sio.emit('pi-discrete', data)


sio.connect('http://192.168.2.13:3000')
sio.wait()
