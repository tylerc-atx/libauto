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

__all__ = ['manual_control']


import time
from car import STORE
from car import steering, throttle
from car.gpio import setup_input_on_pin, read_pin_pwm_value


RC_STEERING_PIN = STORE.get('RC_STEERING_PIN', 5)
RC_THROTTLE_PIN = STORE.get('RC_THROTTLE_PIN', 6)


setup_input_on_pin(RC_STEERING_PIN)
setup_input_on_pin(RC_THROTTLE_PIN)


def manual_control():
    while True:
        cur_steering = read_pin_pwm_value(RC_STEERING_PIN)
        cur_throttle = read_pin_pwm_value(RC_THROTTLE_PIN)
        steering.set_pin_pwm_value(steering.STEERING_PIN, cur_steering)
        throttle.set_pin_pwm_value(throttle.THROTTLE_PIN, cur_throttle)
        time.sleep(0.01)

