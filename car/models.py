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
This module provides many pre-trained and/or pre-configured models which
enable to car to exhibit more advanced behaviors. These models each provide
easier interfaces which abstract the underlying algorithms and only expose
the resulting desired behaviors.
"""

__all__ = ['ColorClassifier']


import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class ColorClassifier:
    """
    This class processes images and classifies the color which appears in the
    center region of each image. It classifies the center region as containing
    one of:
      - "red"         <-- the center of the image appears RED
      - "yellow"      <-- the center of the image appears YELLOW
      - "green"       <-- the center of the image appears GREEN
      - "background"  <-- the center of the image appears to be a mix of colors
    """

    def __init__(self, center_region_width=0.25, center_region_height=0.25):
        """
        Build a color classifier object which looks at the center region of
        an image and determines if it contains primarily either "red", "yellow",
        or "green", or none of those ("background"). The size of the center
        region is given by the parameters `center_region_width` and
        `center_region_height`.
        """
        self.center_region_width  = center_region_width
        self.center_region_height = center_region_height

        # Colors as canonical vectors [R,G,B]:
        self.colors = np.array([[  255,   0, 0],
                                [  255, 255, 0],
                                [    0, 255, 0]])
        self.color_names = ['red', 'yellow', 'green']

        # Threshold for std deviation cutoff:
        self.std_thresh = np.array([20, 20, 20])

    def classify(self, img, annotate=False):
        """
        Classify one image's center region as having either primarily "red",
        "yellow", or "green, or none of those ("background").

        The `img` parameter must be a numpy array containing an RGB image.

        Returns a tuple of the form (`p1`, `p2`, `classific`, `center_img`).
        """

        # Check `img` for correct shape. It should be an 3-channel, 2d image.
        if len(img.shape) != 3 or img.shape[2] != 3:
            raise Exception("incorrect img shape: Please input an RGB image.")

        # Define the center region of `img`.
        height, width = img.shape[0], img.shape[1]
        y_center      = height/2
        x_center      = width/2
        p1 = int(x_center - (width  * self.center_region_width)/2), \
             int(y_center - (height * self.center_region_height)/2)
        p2 = int(x_center + (width  * self.center_region_width)/2), \
             int(y_center + (height * self.center_region_height)/2)

        # Crop the center region.
        center_img = img[ p1[1]:p2[1], p1[0]:p2[0] ]

        # Get mean and std dev values of the pixels in `center_img`.
        h, w, p = center_img.shape
        center_reshaped = center_img.reshape((h*w, p))
        center_mean = np.average(center_reshaped, axis=0).reshape(1, -1)
        center_std = np.std(center_reshaped, axis=0)

        # Assume the image is just background when all channels have "too big" of
        # standard deviation.
        if (center_std > self.std_thresh).all():
            classific = 'background'

        # Otherwise, find which canonical color is most similar to the center
        # region's mean color.
        else:
            cosine_sims = cosine_similarity(center_mean, self.colors)[0]
            classific = self.color_names[np.argmax(cosine_sims)]

        if annotate:
            self.annotate(p1, p2, classific, img)

        return p1, p2, classific

    def annotate(self, p1, p2, classific, img):
        """
        Annotate the image by adding a box around the center region and
        writing the classification on the image to show the result of
        the color classification.
        """
        box_color = None
        text = None
        text_color = None

        if   classific == 'green':
            box_color = (0, 255, 0)
            text = 'GREEN'
            text_color = (0, 255, 0)

        elif classific == 'yellow':
            box_color = (255, 255, 0)
            text = 'YELLOW'
            text_color = (0, 0, 0)

        elif classific == 'red':
            box_color = (255, 0, 0)
            text = 'RED'
            text_color = (255, 0, 0)

        elif classific == 'background':
            box_color = (0, 0, 0)
            text = 'background'
            text_color = (0, 0, 0)

        else:
            box_color = (204, 204, 204)

        if box_color:
            cv2.rectangle(img, p1, p2, box_color, 3)
        if text and text_color:
            cv2.putText(img, text, p1, cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

