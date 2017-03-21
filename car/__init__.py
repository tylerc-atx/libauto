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
This module provides easy helper functions which abstract the behavior of
the car to a very high level. These functions are intended to be used by
beginners. All of the functionality in these helper functions can be
recreated using lower-level abstractions exposed by the other modules of
this library.

These helper functions, when invoked, each print info about what they are
doing. Normally a library should _not_ print anything, but we make an
exception for these functions because they are intended to be used by
beginners who are new to programming, and the printouts are helpful for
the beginners to see what is happening. The other modules of this library
do not print.
"""

__all__ = ['forward', 'reverse', 'left', 'right', 'pause',
           'capture', 'plot', 'classify_color',
           'detect_faces', 'detect_stop_signs', 'detect_pedestrians',
           'object_location', 'object_size']


from car import db
import numpy as np
import time
import cv2
import os


CURR_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILE_PATH = os.path.join(CURR_DIR, 'settings.db')
STORE = db.KeyValueStore(DB_FILE_PATH)


def forward(duration=1.0):
    """
    Drive the car forward for `duration` seconds.
    """
    from car.steering import set_steering
    from car.throttle import set_throttle, THROTTLE_SAFE_FORWARD_VALUE
    if duration > 5.0:
        print("Error: The duration exceeds 5 seconds; will reset to 5 seconds.")
        duration = 5.0
    print("Driving forward for {} seconds.".format(duration))
    set_steering(0.0)
    time.sleep(0.05)
    set_throttle(THROTTLE_SAFE_FORWARD_VALUE)
    time.sleep(duration)
    set_throttle(0)


def reverse(duration=1.0):
    """
    Drive the car in reverse for `duration` seconds.
    """
    from car.steering import set_steering
    from car.throttle import set_throttle, THROTTLE_SAFE_REVERSE_VALUE
    if duration > 5.0:
        print("Error: The duration exceeds 5 seconds; will reset to 5 seconds.")
        duration = 5.0
    print("Driving in reverse for {} seconds.".format(duration))
    set_steering(0.0)
    set_throttle(THROTTLE_SAFE_REVERSE_VALUE)
    time.sleep(0.1)
    set_throttle(0)
    time.sleep(0.1)
    set_throttle(THROTTLE_SAFE_REVERSE_VALUE)
    time.sleep(duration)
    set_throttle(0)


def left(duration=1.0):
    """
    Drive the car forward and left for `duration` seconds.
    """
    from car.steering import set_steering
    from car.throttle import set_throttle, THROTTLE_SAFE_FORWARD_VALUE
    if duration > 5.0:
        print("Error: The duration exceeds 5 seconds; will reset to 5 seconds.")
        duration = 5.0
    print("Driving left for {} seconds.".format(duration))
    set_steering(45.0)
    time.sleep(0.05)
    set_throttle(THROTTLE_SAFE_FORWARD_VALUE)
    time.sleep(duration)
    set_throttle(0)


def right(duration=1.0):
    """
    Drive the car forward and right for `duration` seconds.
    """
    from car.steering import set_steering
    from car.throttle import set_throttle, THROTTLE_SAFE_FORWARD_VALUE
    if duration > 5.0:
        print("Error: The duration exceeds 5 seconds; will reset to 5 seconds.")
        duration = 5.0
    print("Driving right for {} seconds.".format(duration))
    set_steering(-45.0)
    time.sleep(0.05)
    set_throttle(THROTTLE_SAFE_FORWARD_VALUE)
    time.sleep(duration)
    set_throttle(0)


def pause(duration=1.0):
    """
    Pause the car's code for `duration` seconds.
    """
    print("Pausing for {} seconds.".format(duration))
    time.sleep(duration)


def capture(num_frames=1):
    """
    Capture `num_frames` frames from the car's camera and return
    them as a numpy ndarray.
    """
    if 'CAMERA' not in globals():
        global CAMERA
        from car.camera import CameraRGB
        CAMERA = CameraRGB()
        print("Instantiated a camera object!")

    if num_frames > 1:
        frames = []
        for i, frame in zip(range(num_frames), CAMERA.stream()):
            frames.append(frame)
        frames = np.array(frames)
        print("Captured {} frames.".format(num_frames))
        return frames

    else:
        frame = CAMERA.capture()
        print("Captured 1 frame.")
        return frame


def plot(frames, **fig_kwargs):
    """
    Plot the given `frames` (a numpy ndarray) into a matplotlib figure,
    returning the figure object which can be shown. If you call this
    function from Jupyter, the figure object will be shown automatically!

    The `frames` parameter must be a numpy ndarray with one of the
    following shapes:
        - (n, h, w, 3)   meaning `n` 3-channel RGB images of size `w`x`h`
        - (n, h, w, 1)   meaning `n` 1-channel gray images of size `w`x`h`
        -    (h, w, 3)   meaning a single 3-channel RGB image of size `w`x`h`
        -    (h, w, 1)   meaning a single 1-channel gray image of size `w`x`h`
        -    (h, w)      meaning a single 1-channel gray image of size `w`x`h`
    """
    import matplotlib.pyplot as plt
    from math import sqrt

    # Ensure the proper shape of `frames`.
    if frames.ndim == 4:
        pass
    elif frames.ndim == 3:
        frames = np.expand_dims(frames, axis=0)
    elif frames.ndim == 2:
        frames = np.expand_dims(frames, axis=2)
        frames = np.expand_dims(frames, axis=0)
    else:
        raise Exception("invalid frames ndarray shape")
    if frames.shape[3] != 3 and frames.shape[3] != 1:
        raise Exception("invalid number of channels")

    # Compute the figure grid size (this will be (height x width) subplots).
    n = frames.shape[0]
    width = int(round(sqrt(float(n))))
    height = n // width
    if (n % width) > 0:
        height += 1
    print("Plotting {} frame{}...".format(n, 's' if n != 1 else ''))

    # Create the figure grid.
    if 'figsize' not in fig_kwargs:
        fig_kwargs['figsize'] = (5, 5) if n == 1 else (10, 10)
    fig, axes = plt.subplots(width, height, **fig_kwargs)

    # Ensure `axes` is a 1d iterable.
    try:
        axes = axes.flatten()
    except AttributeError:
        # This ^^ exception happens when width=height=1.
        axes = [axes]

    # Plot each frame into the grid.
    from itertools import zip_longest
    for ax, frame in zip_longest(axes, frames):
        if frame is not None:
            if frame.shape[2] == 1:
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
            ax.imshow(frame)
        ax.axis('off')

    return fig


def classify_color(frame, annotate=True):
    """
    Classify the center region of `frame` as having either primarily "red",
    "yellow", or "green, or none of those ("background").

    The `frame` parameter must be a numpy array containing an RGB image.

    Returns a string representing the color found in the center of the
    image, one of "red", "yellow", "green", or "background".
    """
    if 'COLORCLASSIFIER' not in globals():
        global COLORCLASSIFIER
        from car.models import ColorClassifier
        COLORCLASSIFIER = ColorClassifier()
        print("Instantiated a ColorClassifier object!")

    p1, p2, classific = COLORCLASSIFIER.classify(frame, annotate=annotate)
    print("Classified color as '{}'.".format(classific))
    return classific


def detect_faces(frame, annotate=True):
    """
    Detect faces inside of `frame`, and annotate each face.

    The `frame` parameter must be an image as a numpy array either containing
    3-channel RGB values _or_ 1-channel gray values.

    Returns a list of faces, where each face is a 4-tuple of:
        (x, y, width, height)
    """
    if 'FACEDETECTOR' not in globals():
        global FACEDETECTOR
        from car.models import FaceDetector
        FACEDETECTOR = FaceDetector()
        print("Instantiated a FaceDetector object!")

    faces = FACEDETECTOR.detect(frame, annotate=annotate)
    n = len(faces)
    print("Found {} face{}.".format(n, 's' if n != 1 else ''))
    return faces


def detect_stop_signs(frame, annotate=True):
    """
    Detect stop signs inside of `frame`, and annotate each stop sign.

    The `frame` parameter must be an image as a numpy array either containing
    3-channel RGB values _or_ 1-channel gray values.

    Returns a list of rectangles, where each rectangle is a 4-tuple of:
        (x, y, width, height)
    """
    if 'STOPSIGNDETECTOR' not in globals():
        global STOPSIGNDETECTOR
        from car.models import StopSignDetector
        STOPSIGNDETECTOR = StopSignDetector()
        print("Instantiated a StopSignDetector object!")

    rects = STOPSIGNDETECTOR.detect(frame, annotate=annotate)
    n = len(rects)
    print("Found {} stop sign{}.".format(n, 's' if n != 1 else ''))
    return rects


def detect_pedestrians(frame, annotate=True):
    """
    Detect pedestrians inside of `frame`, and annotate each pedestrian.

    The `frame` parameter must be an image as a numpy array either containing
    3-channel RGB values _or_ 1-channel gray values.

    Returns a list of rectangles, where each rectangle is a 4-tuple of:
        (x, y, width, height)
    """
    if 'PEDESTRIANDETECTOR' not in globals():
        global PEDESTRIANDETECTOR
        from car.models import PedestrianDetector
        PEDESTRIANDETECTOR = PedestrianDetector()
        print("Instantiated a PedestrianDetector object!")

    rects = PEDESTRIANDETECTOR.detect(frame, annotate=annotate)
    n = len(rects)
    print("Found {} pedestrian{}.".format(n, 's' if n != 1 else ''))
    return rects


def object_location(object_list, frame_shape):
    """
    Calculate the location of the largest object in `object_list`.

    Returns one of: 'frame_left', 'frame_right', 'frame_center', None
    """
    if not object_list:
        print("Object location is None.")
        return None
    areas = [w*h for x, y, w, h in object_list]
    i = np.argmax(areas)
    nearest = object_list[i]
    x, y, w, h = nearest
    x_center = x + w/2.
    if x_center < frame_shape[1]/3.:
        location = 'frame_left'
    elif x_center < 2*frame_shape[1]/3.:
        location = 'frame_center'
    else:
        location = 'frame_right'
    print("Object location is '{}'.".format(location))
    return location


def object_size(object_list, frame_shape):
    """
    Calculate the ratio of the nearest object's area to the frame's area.
    """
    if not object_list:
        print("Object area is 0.")
        return 0.0
    areas = [w*h for x, y, w, h in object_list]
    ratio = max(areas) / (frame_shape[0] * frame_shape[1])
    print("Object area is {}.".format(ratio))
    return ratio

