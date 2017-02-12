from car import STORE
from car.gpio import setup_pwm_on_pin, set_pin_pwm_value, delay_micros


THROTTLE_PIN                = STORE.get('THROTTLE_PIN',                24)
THROTTLE_ZERO_VALUE         = STORE.get('THROTTLE_ZERO_VALUE',         15.0)
THROTTLE_FULL_FORWARD_VALUE = STORE.get('THROTTLE_FULL_FORWARD_VALUE', 20.0)
THROTTLE_FULL_REVERSE_VALUE = STORE.get('THROTTLE_FULL_REVERSE_VALUE', 10.0)


setup_pwm_on_pin(THROTTLE_PIN)


def _clamp(n, smallest, largest):
    """Clamp `n` into the range [`smallest`, `largest`], and return it."""
    return max(smallest, min(n, largest))


def set_throttle(throttle):
    """
    Set the vehicle's throttle in the range [-100, 100], where -100 means
    full-reverse and 100 means full-forward.
    """
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
    set_pin_pwm_value(THROTTLE_PIN, (b - a) * (throttle / 100.0) + a)


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

