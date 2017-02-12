from car import throttle
from car import steering
from car import sonar


def set_pins():
    """
    Set all the GPIO pins for all the components on the vehicle.
    """
    throttle._set_throttle_pin()
    steering._set_steering_pin()
    sonar._set_sonar_pins()


def calibrate():
    """
    Calibrate all the necessary components on the vehicle.
    """
    throttle._calibrate_esc()
    steering._calibrate_steering()

