from car import db
import os


CURR_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILE_PATH = os.path.join(CURR_DIR, 'settings.db')
STORE = db.KeyValueStore(DB_FILE_PATH)


def forward(t=0.65):
    import time
    from car.steering import set_steering
    from car.throttle import set_throttle
    print("Driving forward to {} second.".format(t))
    set_steering(0.0)
    set_throttle(30)
    time.sleep(0.1)
    set_throttle(90)
    time.sleep(t)
    set_throttle(0)
    time.sleep(0.2)


def reverse(t=0.65):
    import time
    from car.steering import set_steering
    from car.throttle import set_throttle
    print("Driving in reverse to {} second.".format(t))
    set_steering(0.0)
    set_throttle(-30)
    time.sleep(0.1)
    set_throttle(-90)
    time.sleep(t)
    set_throttle(0)
    time.sleep(0.2)


def left(t=0.65):
    import time
    from car.steering import set_steering
    from car.throttle import set_throttle
    print("Driving left to {} second.".format(t))
    set_steering(45.0)
    set_throttle(30)
    time.sleep(0.1)
    set_throttle(90)
    time.sleep(t)
    set_throttle(0)
    time.sleep(0.2)


def right(t=0.65):
    import time
    from car.steering import set_steering
    from car.throttle import set_throttle
    print("Driving right to {} second.".format(t))
    set_steering(-45.0)
    set_throttle(30)
    time.sleep(0.1)
    set_throttle(90)
    time.sleep(t)
    set_throttle(0)
    time.sleep(0.2)

