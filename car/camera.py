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

__all__ = ['CameraRGB']


try:
    from car.camera_pi import CameraRGB
except ImportError:
    from car.camera_cv2 import CameraRGB

