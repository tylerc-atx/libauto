"""
Copyright (c) 2017 AutoAuto, LLC
ALL RIGHTS RESERVED

Use of this library, in source or binary form, is prohibited without written
approval from AutoAuto, LLC.
"""

import cv2
import weakref
import numpy as np
from threading import Thread, Condition


class CameraRGB:
    """
    This class represents a camera which captures in raw RGB.
    """

    def __init__(self, width=320, height=240, fps=16):
        """
        Initialize a camera object which captures frames of size `width`x`height`
        at `fps` frames-per-second.
        """
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, width)
        self.camera.set(4, height)
        self.fsize = (width, height)
        self.stop = False
        self.error = False
        self.frame = None
        self.cond = Condition()
        self.thread = Thread(target=self._thread_main)
        self.thread.start()

    def _thread_main(self):
        while not self.stop:
            ret, img = self.camera.read()
            if not ret:
                self.error = True
                break
            img = cv2.resize(img, self.fsize)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.cond.acquire()
            self.frame = img
            self.cond.notifyAll()
            self.cond.release()
        self.camera.release()

    def capture(self):
        """
        Capture and return one frame from the camera as a numpy ndarray,
        or None if an error occurred.
        """
        self.cond.acquire()
        self.cond.wait(1.0)
        while self.frame is None and not self.stop and not self.error:
            self.cond.wait(1.0)
        if self.stop or self.error:
            frame = None
        else:
            frame = np.copy(self.frame)
        self.cond.release()
        return frame

    def stream(self):
        """
        Yield frames one-at-a-time from the camera as numpy ndarrays.
        """
        while True:
            frame = self.capture()
            if not frame:
                break
            yield frame

    def close(self):
        """
        Release the resources held by this camera object.
        """
        self.stop = True
        self.thread.join()

    def __del__(self):
        """
        Python destructor which calls `close()` on this object.
        """
        self.close()

