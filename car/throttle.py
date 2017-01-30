from car import STORE
from car.gpio import setup_pwm_on_pin, set_pin_pwm_value


THROTTLE_PIN                = STORE.get('THROTTLE_PIN',                23)
THROTTLE_ZERO_VALUE         = STORE.get('THROTTLE_ZERO_VALUE',         15.0)
THROTTLE_FULL_FORWARD_VALUE = STORE.get('THROTTLE_FULL_FORWARD_VALUE', 20.0)
THROTTLE_FULL_REVERSE_VALUE = STORE.get('THROTTLE_FULL_REVERSE_VALUE', 10.0)


setup_pwm_on_pin(THROTTLE_PIN)


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def set_throttle(throttle):
    zero = THROTTLE_ZERO_VALUE
    forward = THROTTLE_FULL_FORWARD_VALUE
    reverse = THROTTLE_FULL_REVERSE_VALUE
    throttle = clamp(throttle, -100.0, 100.0)
    if throttle < 0:
        throttle = -throttle
        other = reverse
    else:
        other = forward
    a, b = zero, other
    set_pin_pwm_value(THROTTLE_PIN, (b - a) * (throttle / 100.0) + a)


set_throttle(0.0)
