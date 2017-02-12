"""
Copyright (c) 2017 AutoAuto, LLC
ALL RIGHTS RESERVED

Use of this library, in source or binary form, is prohibited without written
approval from AutoAuto, LLC.
"""

from car import db
import os


CURR_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILE_PATH = os.path.join(CURR_DIR, 'settings.db')
STORE = db.KeyValueStore(DB_FILE_PATH)


def forward(t=0.65):
    """
    Drive the car forward for `t` seconds.
    """
    import time
    from car.steering import set_steering
    from car.throttle import set_throttle
    print("Driving forward for {} seconds.".format(t))
    set_steering(0.0)
    time.sleep(0.05)
    set_throttle(90)
    time.sleep(t)
    set_throttle(0)


def reverse(t=0.65):
    """
    Drive the car in reverse for `t` seconds.
    """
    import time
    from car.steering import set_steering
    from car.throttle import set_throttle
    print("Driving in reverse for {} seconds.".format(t))
    set_steering(0.0)
    set_throttle(-45)
    time.sleep(0.1)
    set_throttle(0)
    time.sleep(0.05)
    set_throttle(-90)
    time.sleep(t)
    set_throttle(0)


def left(t=0.65):
    """
    Drive the car forward and left for `t` seconds.
    """
    import time
    from car.steering import set_steering
    from car.throttle import set_throttle
    print("Driving left for {} seconds.".format(t))
    set_steering(45.0)
    time.sleep(0.05)
    set_throttle(90)
    time.sleep(t)
    set_throttle(0)


def right(t=0.65):
    """
    Drive the car forward and right for `t` seconds.
    """
    import time
    from car.steering import set_steering
    from car.throttle import set_throttle
    print("Driving right for {} seconds.".format(t))
    set_steering(-45.0)
    time.sleep(0.05)
    set_throttle(90)
    time.sleep(t)
    set_throttle(0)

