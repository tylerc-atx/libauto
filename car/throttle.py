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
This module handles the throttle of the car. It allows for setting
the throttle of the car in the range [-100, 100], and it allows for
calibrating the throttle as well (which should be a one-time thing).
"""

__all__ = ['set_throttle']


from car import STORE
from car.gpio import setup_pwm_on_pin, set_pin_pwm_value, delay_micros


THROTTLE_PIN                = STORE.get('THROTTLE_PIN',                16)
THROTTLE_ZERO_VALUE         = STORE.get('THROTTLE_ZERO_VALUE',         15.0)
THROTTLE_FULL_FORWARD_VALUE = STORE.get('THROTTLE_FULL_FORWARD_VALUE', 20.0)
THROTTLE_FULL_REVERSE_VALUE = STORE.get('THROTTLE_FULL_REVERSE_VALUE', 10.0)
THROTTLE_SAFE_FORWARD_VALUE = STORE.get('THROTTLE_SAFE_FORWARD_VALUE', 55)
THROTTLE_SAFE_REVERSE_VALUE = STORE.get('THROTTLE_SAFE_REVERSE_VALUE', -55)


setup_pwm_on_pin(THROTTLE_PIN)


def _clamp(n, smallest, largest):
    """Clamp `n` into the range [`smallest`, `largest`], and return it."""
    return max(smallest, min(n, largest))


def _pwm_to_throttle(pwm_value):
    zero = THROTTLE_ZERO_VALUE
    forward = THROTTLE_FULL_FORWARD_VALUE
    reverse = THROTTLE_FULL_REVERSE_VALUE
    pwm_value = _clamp(pwm_value, min(forward, reverse), max(forward, reverse))
    if pwm_value < zero:
        pwm_value = (zero - pwm_value) / (zero - reverse)
        other = -100.0
    else:
        pwm_value = (pwm_value - zero) / (forward - zero)
        other = 100.0
    a, b = 0.0, other
    return (b - a) * pwm_value + a


def _throttle_to_pwm(throttle):
    zero = THROTTLE_ZERO_VALUE
    forward = THROTTLE_FULL_FORWARD_VALUE
    reverse = THROTTLE_FULL_REVERSE_VALUE
    throttle = _clamp(throttle, -100.0, 100.0)
    if throttle < 0:
        throttle = -throttle
        other = reverse
    else:
        other = forward
    a, b = zero, other
    return (b - a) * (throttle / 100.0) + a


def set_throttle(throttle):
    """
    Set the vehicle's throttle in the range [-100, 100], where -100 means
    full-reverse and 100 means full-forward.
    """
    pwm_value = _throttle_to_pwm(throttle)
    set_pin_pwm_value(THROTTLE_PIN, pwm_value)


set_throttle(0.0)
delay_micros(500000)  # 0.5 seconds


def _set_throttle_pin():
    """
    Ask the user to input the throttle pin index, and then
    store it in the database. To use the throttle, the
    process should be restarted after a call to this function.
    """
    pin_index = int(input("enter the throttle pin index: "))
    STORE.put('THROTTLE_PIN',  pin_index)
    print("process restart required")


def _calibrate_esc():
    """
    Ask the user to input the throttle PWM range parameters, and then
    store them in the database.
    """

    global THROTTLE_FULL_REVERSE_VALUE, THROTTLE_ZERO_VALUE, THROTTLE_FULL_FORWARD_VALUE

    THROTTLE_FULL_REVERSE_VALUE = float(input("enter throttle full-reverse value: "))
    THROTTLE_ZERO_VALUE         = float(input("enter throttle neutral value: "))
    THROTTLE_FULL_FORWARD_VALUE = float(input("enter throttle full-forward value: "))

    STORE.put('THROTTLE_FULL_REVERSE_VALUE', THROTTLE_FULL_REVERSE_VALUE)
    STORE.put('THROTTLE_ZERO_VALUE', THROTTLE_ZERO_VALUE)
    STORE.put('THROTTLE_FULL_FORWARD_VALUE', THROTTLE_FULL_FORWARD_VALUE)

    PIN = THROTTLE_PIN
    MIN = THROTTLE_FULL_REVERSE_VALUE - 0.01
    MID = THROTTLE_ZERO_VALUE
    MAX = THROTTLE_FULL_FORWARD_VALUE + 0.01

    set_pin_pwm_value(PIN, MID)

    _ = input("In neutral, press enter to enter full throttle.")

    set_pin_pwm_value(PIN, MAX)

    _ = input("In full throttle, press enter to enter reverse throttle.")

    set_pin_pwm_value(PIN, MIN)

    _ = input("In reverse throttle, press enter to return to neutral.")

    set_pin_pwm_value(PIN, MID)

    _ = input("In neutral, press enter to exit.")


def _calibrate_safe_speed():
    """
    Ask the user repeatedly to enter a throttle value in [0, 100] until the
    car drives at a safe speed for kids.
    """

    global THROTTLE_SAFE_FORWARD_VALUE, THROTTLE_SAFE_REVERSE_VALUE
    from car import forward, left, right

    while True:

        THROTTLE_SAFE_FORWARD_VALUE = int(input("Throttle safe forward value [0, 100]: "))
        THROTTLE_SAFE_REVERSE_VALUE = int(input("Throttle safe reverse value [0, -100]: "))

        STORE.put('THROTTLE_SAFE_FORWARD_VALUE', THROTTLE_SAFE_FORWARD_VALUE)
        STORE.put('THROTTLE_SAFE_REVERSE_VALUE', THROTTLE_SAFE_REVERSE_VALUE)

        left()
        right()
        forward()

        if input("Keep? [n/y] ") == 'y':
            break

