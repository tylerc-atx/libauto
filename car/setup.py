from car import throttle
from car import steering
from car import sonar


def set_pins():
    throttle._set_throttle_pin()
    steering._set_steering_pin()
    sonar._set_sonar_pins()


def calibrate():
    throttle._calibrate_esc()
    steering._calibrate_steering()

