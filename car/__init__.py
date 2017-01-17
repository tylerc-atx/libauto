from car import db
import os
import time

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILE_PATH = os.path.join(CURR_DIR, 'gpio_settings.db')
STORE = db.KeyValueStore(DB_FILE_PATH)


STEERING_PIN = STORE.get('STEERING_PIN', 24)
THROTTLE_PIN = STORE.get('THROTTLE_PIN', 23)

STEERING_ZERO_VALUE  = STORE.get('STEERING_ZERO_VALUE',  14.0)
STEERING_LEFT_VALUE  = STORE.get('STEERING_LEFT_VALUE',  19.0)
STEERING_RIGHT_VALUE = STORE.get('STEERING_RIGHT_VALUE',  9.0)

THROTTLE_ZERO_VALUE         = STORE.get('THROTTLE_ZERO_VALUE',         15.0)
THROTTLE_FULL_FORWARD_VALUE = STORE.get('THROTTLE_FULL_FORWARD_VALUE', 20.0)
THROTTLE_FULL_REVERSE_VALUE = STORE.get('THROTTLE_FULL_REVERSE_VALUE', 10.0)


# The following tells wiringpi to open /dev/gpiomem instead of /dev/mem.
os.environ['WIRINGPI_GPIOMEM'] = "1"

import wiringpi as wpi

# The following init method doesn't need root, but it
# is a very limited interface.
#wpi.wiringPiSetupSys()

# The following init method either needs root,
#   -- OR --
# it needs you to be in the `gpio` group and have set
# the WIRINGPI_GPIOMEM environment variable above.
wpi.wiringPiSetupGpio()

# The PWM range is related to the frequency.
# See the comments in:
#   https://projects.drogon.net/raspberry-pi/wiringpi/software-pwm-library/
PWM_RANGE = 100


wpi.pinMode(STEERING_PIN, 1)  # 0=input, 1=output 2=PWM
wpi.softPwmCreate(STEERING_PIN, 0, PWM_RANGE)

wpi.pinMode(THROTTLE_PIN, 1)  # 0=input, 1=output 2=PWM
wpi.softPwmCreate(THROTTLE_PIN, 0, PWM_RANGE)


def set_pin_value(pin_index, value):
    value = int(value / 100.0 * PWM_RANGE)
    wpi.softPwmWrite(pin_index, value)


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
    set_pin_value(STEERING_PIN, (b - a) * (angle / 45.0) + a)


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
    set_pin_value(THROTTLE_PIN, (b - a) * (throttle / 100.0) + a)


set_steering(0.0)
set_throttle(0.0)


def forward(t=0.5):
    print("Driving forward to {} second.".format(t))
    set_steering(0.0)
    set_throttle(30)
    time.sleep(0.1)
    set_throttle(90)
    time.sleep(t)
    set_throttle(0)
    time.sleep(0.2)


def reverse(t=0.5):
    print("Driving in reverse to {} second.".format(t))
    set_steering(0.0)
    set_throttle(-30)
    time.sleep(0.1)
    set_throttle(-90)
    time.sleep(t)
    set_throttle(0)
    time.sleep(0.2)


def left(t=0.5):
    print("Driving left to {} second.".format(t))
    set_steering(45.0)
    set_throttle(30)
    time.sleep(0.1)
    set_throttle(90)
    time.sleep(t)
    set_throttle(0)
    time.sleep(0.2)


def right(t=0.5):
    print("Driving right to {} second.".format(t))
    set_steering(-45.0)
    set_throttle(30)
    time.sleep(0.1)
    set_throttle(90)
    time.sleep(t)
    set_throttle(0)
    time.sleep(0.2)


def calibrate_steering(smin, smid, smax):
    global STEERING_ZERO_VALUE, STEERING_LEFT_VALUE, STEERING_RIGHT_VALUE
    STEERING_ZERO_VALUE  = smid
    STEERING_LEFT_VALUE  = smax
    STEERING_RIGHT_VALUE = smin
    STORE.put('STEERING_ZERO_VALUE',  STEERING_ZERO_VALUE)
    STORE.put('STEERING_LEFT_VALUE',  STEERING_LEFT_VALUE)
    STORE.put('STEERING_RIGHT_VALUE', STEERING_RIGHT_VALUE)
    forward()
    left()
    right()
    forward()

