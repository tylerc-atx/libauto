"""
Copyright (c) 2017 AutoAuto, LLC
ALL RIGHTS RESERVED

Use of this library, in source or binary form, is prohibited without written
approval from AutoAuto, LLC.
"""

"""
This module is an adapter for the specific camera you use on your SBC.

If you're using a Raspberry Pi, this module will internally use the `picamera` library.
"""

from picamera import PiCamera
from picamera.array import PiRGBArray


class CameraRGB:
    """
    This class represents a camera which captures in raw RGB.
    """

    def __init__(self, width=320, height=240, fps=16):
        """
        Initialize a camera object which captures frames of size `width`x`height`
        at `fps` frames-per-second.
        """
        self.camera = PiCamera(resolution=(width, height), framerate=fps)
        self.array = PiRGBArray(self.camera, size=(width, height))

    def capture(self):
        """
        Capture and return one frame from the camera as a numpy ndarray.
        """
        self.camera.capture(self.array, format='rgb', use_video_port=True)
        frame = self.array.array
        self.array.truncate(0)
        return frame

    def stream(self):
        """
        Yield frames one-at-a-time from the camera as numpy ndarrays.
        """
        for _ in self.camera.capture_continuous(self.array,
                                                format='rgb',
                                                use_video_port=True):
            frame = self.array.array
            self.array.truncate(0)
            yield frame

