import car
import time

PIN = car.THROTTLE_PIN
MIN = car.THROTTLE_FULL_REVERSE_VALUE - 0.01
MID = car.THROTTLE_ZERO_VALUE
MAX = car.THROTTLE_FULL_FORWARD_VALUE + 0.01

car.set_pin_value(PIN, MID)

_ = input("In neutral, press enter to enter full throttle.")

car.set_pin_value(PIN, MAX)

_ = input("In full throttle, press enter to enter reverse throttle.")

car.set_pin_value(PIN, MIN)

_ = input("In reverse throttle, press enter to return to neutral.")

car.set_pin_value(PIN, MID)

_ = input("In neutral, press enter to exit.")

