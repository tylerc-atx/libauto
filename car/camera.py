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
This module is an adapter for the specific camera you are using.

If you're using a Raspberry Pi, this module will internally use the `picamera`
library.

Else, it will use OpenCV for capturing frames.
"""

__all__ = ['CameraRGB', 'wrap_frame_index_decorator']


import cv2


try:
    from car.camera_pi import CameraRGB
except ImportError:
    from car.camera_cv2 import CameraRGB


def wrap_frame_index_decorator(camera):
    """
    Wrap `camera` in a decorator which draws the frame index onto
    each from once captured from the camera.
    Returns a camera-like object.
    """
    class CameraRGBFrameIndexDecorator:
        def __init__(self,
                     decorated,
                     text_scale=0.75,
                     text_color=[255, 255, 255],
                     text_line_width=2):
            self.decorated = decorated
            self.frame_index = 0
            self.text_scale = text_scale
            self.text_color = text_color
            self.text_line_width = text_line_width

        def _draw_frame_index(self, frame):
            text = "frame {}".format(self.frame_index)
            self.frame_index += 1
            x = 5
            y = frame.shape[0] - 5
            cv2.putText(frame,
                        text,
                        (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        self.text_scale,
                        self.text_color,
                        self.text_line_width)

        def capture(self):
            frame = self.decorated.capture()
            self._draw_frame_index(frame)
            return frame

        def stream(self):
            for frame in self.decorated.stream():
                self._draw_frame_index(frame)
                yield frame

    return CameraRGBFrameIndexDecorator(camera)

