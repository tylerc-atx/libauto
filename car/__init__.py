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


def capture(num_frames=1):
    """
    Capture `num_frames` frames from the car's camera and return
    them as a numpy ndarray.
    """
    import numpy as np

    if 'CAMERA' not in globals():
        global CAMERA
        from car.camera import CameraRGB
        CAMERA = CameraRGB()
        print("Instantiated a camera object!")

    if num_frames > 1:
        frames = []
        for i, frame in zip(range(num_frames), CAMERA.stream()):
            frames.append(frame)
        return np.array(frames)

    else:
        frame = CAMERA.capture()
        return np.array([frame])


def plot_frames(frames, **fig_kwargs):
    """
    Plot the given `frames` (a numpy ndarray) into a matplotlib figure,
    returning the figure object which can be shown. If you call this
    function from Jupyter, the figure object will be shown automatically!
    """
    import matplotlib.pyplot as plt
    from math import sqrt

    n = len(frames)
    height = int(round(sqrt(float(n))))
    width = n // height
    if (n % height) > 0:
        height += 1

    if 'figsize' not in fig_kwargs:
        fig_kwargs['figsize'] = (10, 10)
    fig, axes = plt.subplots(width, height, **fig_kwargs)
    try:
        axes = axes.reshape((-1,))
    except AttributeError:
        # This ^^ exception happens when width=height=1.
        axes = [axes]

    for ax, frame in zip(axes, frames):
        ax.imshow(frame)
        ax.axis('off')

    return fig

