import cv2

# Rotation value constants

"""
Rotation enum:

NONE = 0;
NINETY_DEG = 1;
ONE_EIGHTY_DEG = 2;
TWO_SEVENTY_DEG = 3;
"""

ROTATION_ENUM = {
    "NONE": 0,
    "NINETY_DEG": 1,
    "ONE_EIGHTY_DEG": 2,
    "TWO_SEVENTY_DEG": 3
}

ROTATION_CV_CONSTANTS = {
    1: cv2.ROTATE_90_CLOCKWISE,
    2: cv2.ROTATE_180,
    3: cv2.ROTATE_90_COUNTERCLOCKWISE
}