from car import throttle
from car import steering
from car import sonar


def set_pins():
    throttle.set_throttle_pin()
    steering.set_steering_pin()
    sonar.set_sonar_pins()


def calibrate():
    throttle.calibrate_esc()
    steering.calibrate_steering()

