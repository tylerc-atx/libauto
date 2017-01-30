from car import STORE
from car.gpio import setup_pwm_on_pin, set_pin_pwm_value


STEERING_PIN         = STORE.get('STEERING_PIN',         24)
STEERING_ZERO_VALUE  = STORE.get('STEERING_ZERO_VALUE',  14.0)
STEERING_LEFT_VALUE  = STORE.get('STEERING_LEFT_VALUE',  19.0)
STEERING_RIGHT_VALUE = STORE.get('STEERING_RIGHT_VALUE',  9.0)


setup_pwm_on_pin(STEERING_PIN)


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def set_steering(angle):
    zero = STEERING_ZERO_VALUE
    left = STEERING_LEFT_VALUE
    right = STEERING_RIGHT_VALUE
    angle = clamp(angle, -45.0, 45.0)
    if angle < 0:
        angle = -angle
        other = right
    else:
        other = left
    a, b = zero, other
    set_pin_pwm_value(STEERING_PIN, (b - a) * (angle / 45.0) + a)


set_steering(0.0)


def _calibrate_steering(smin, smid, smax):
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
    forward()


def set_steering_pin():
    pin_index = int(input("enter the steering pin index: "))
    STORE.put('STEERING_PIN',  pin_index)
    print("process restart required")


def calibrate_steering():

    while True:

        smin = float(input("Steering min: "))
        smid = float(input("Steering mid: "))
        smax = float(input("Steering max: "))

        _calibrate_steering(smin, smid, smax)

        if input("Keep? [n/y] ") == 'y':
            break

