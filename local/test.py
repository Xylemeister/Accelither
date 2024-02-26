import accelerometer_input as acc
from math import pi

while True:
    print(acc.Input.getJoystick(pi / 6)[1:])