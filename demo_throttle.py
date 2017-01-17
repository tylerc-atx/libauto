import car
import numpy as np
import time

PIN = car.THROTTLE_PIN
MIN = car.THROTTLE_FULL_REVERSE_VALUE
MID = car.THROTTLE_ZERO_VALUE
MAX = car.THROTTLE_FULL_FORWARD_VALUE

car.set_pin_value(PIN, MID)

while True:

    time.sleep(1)

    for val in np.linspace(MID, MAX, 50):
        print(val)
        car.set_pin_value(PIN, val)
        time.sleep(.05)

    for val in np.linspace(MAX, MID, 50):
        print(val)
        car.set_pin_value(PIN, val)
        time.sleep(.05)

    time.sleep(1)

    for val in np.linspace(MID, MIN, 50):
        print(val)
        car.set_pin_value(PIN, val)
        time.sleep(.05)

    for val in np.linspace(MIN, MID, 50):
        print(val)
        car.set_pin_value(PIN, val)
        time.sleep(.05)

