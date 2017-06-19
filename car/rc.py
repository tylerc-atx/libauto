###############################################################################
#
# Copyright (c) 2017 AutoAuto, LLC
# ALL RIGHTS RESERVED
#
# Use of this library, in source or binary form, is prohibited without written
# approval from AutoAuto, LLC.
#
###############################################################################

"""
This module allows for "radio controlled" (RC) AutoAuto cars!
"""

__all__ = ['query_receiver', 'manual_control']


import time
import car
from car import STORE
from car import steering, throttle
from car.gpio import setup_input_on_pin, read_pin_pwm_value


RC_STEERING_PIN = STORE.get('RC_STEERING_PIN', 5)
RC_THROTTLE_PIN = STORE.get('RC_THROTTLE_PIN', 6)


setup_input_on_pin(RC_STEERING_PIN)
setup_input_on_pin(RC_THROTTLE_PIN)


def query_receiver():
    """
    Query the receiver to obtain the steering and throttle values.
    Returns a tuple `(steering_angle, throttle_value)` where
    the `steering_angle` is in [-45, 45] and the `throttle_value`
    is in [-100, 100].
    """
    steering_pwm_value = read_pin_pwm_value(RC_STEERING_PIN)
    throttle_pwm_value = read_pin_pwm_value(RC_THROTTLE_PIN)
    steering_angle = steering._pwm_to_angle(steering_pwm_value)
    throttle_value = throttle._pwm_to_throttle(throttle_pwm_value)
    return steering_angle, throttle_value


def manual_control():
    """
    Go into an infinite loop querying the receiver then setting
    the car's throttle and steering according to the receiver's
    output. I.e. Make this car a normal RC car again!
    """
    i = 0
    while True:
        steering_angle, throttle_value = query_receiver()
        steering.set_steering(steering_angle)
        throttle.set_throttle(throttle_value)
        if (i % 50) == 0:
            car.print("Steering {:.1f}, Throttle {:.1f}".format(steering_angle, throttle_value))
        time.sleep(0.01)
        i += 1

