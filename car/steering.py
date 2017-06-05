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
This module handles the steering of the car. It allows for setting
the steering of the car in the range [-45, 45], and it allows for
calibrating the steering as well (which should be a one-time thing).
"""

__all__ = ['set_steering']


from car import STORE
from car.gpio import setup_pwm_on_pin, set_pin_pwm_value


STEERING_PIN         = STORE.get('STEERING_PIN',         26)
STEERING_ZERO_VALUE  = STORE.get('STEERING_ZERO_VALUE',  14.0)
STEERING_LEFT_VALUE  = STORE.get('STEERING_LEFT_VALUE',  19.0)
STEERING_RIGHT_VALUE = STORE.get('STEERING_RIGHT_VALUE',  9.0)


setup_pwm_on_pin(STEERING_PIN)


def _clamp(n, smallest, largest):
    """Clamp `n` into the range [`smallest`, `largest`], and return it."""
    return max(smallest, min(n, largest))


def set_steering(angle):
    """
    Set the vehicle's steering in the range [-45, 45], where -45 means
    full-right and 45 means full-left.
    """
    zero = STEERING_ZERO_VALUE
    left = STEERING_LEFT_VALUE
    right = STEERING_RIGHT_VALUE
    angle = _clamp(angle, -45.0, 45.0)
    if angle < 0:
        angle = -angle
        other = right
    else:
        other = left
    a, b = zero, other
    set_pin_pwm_value(STEERING_PIN, (b - a) * (angle / 45.0) + a)


set_steering(0.0)


def _calibrate_steering_helper(smin, smid, smax):
    global STEERING_ZERO_VALUE, STEERING_LEFT_VALUE, STEERING_RIGHT_VALUE
    STEERING_ZERO_VALUE  = smid
    STEERING_LEFT_VALUE  = smax
    STEERING_RIGHT_VALUE = smin
    STORE.put('STEERING_ZERO_VALUE',  STEERING_ZERO_VALUE)
    STORE.put('STEERING_LEFT_VALUE',  STEERING_LEFT_VALUE)
    STORE.put('STEERING_RIGHT_VALUE', STEERING_RIGHT_VALUE)
    from car import forward, left, right
    forward()
    left()
    right()


def _calibrate_steering():
    """
    Ask the user to input the steering PWM range parameters, and then
    store them in the database.
    """

    while True:

        smin = float(input("Steering min: "))
        smid = float(input("Steering mid: "))
        smax = float(input("Steering max: "))

        _calibrate_steering_helper(smin, smid, smax)

        if input("Keep? [n/y] ") == 'y':
            break


def _set_steering_pin():
    """
    Ask the user to input the steering pin index, and then
    store it in the database. To use the steering, the
    process should be restarted after a call to this function.
    """
    pin_index = int(input("enter the steering pin index: "))
    STORE.put('STEERING_PIN',  pin_index)
    print("process restart required")

