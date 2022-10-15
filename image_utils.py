import numpy as np 
import cv2
import filetype

import image_pb2

import os

# Image utils

# Checks if image is valid
def is_valid_img_from_bytes(img_bytes):
    return filetype.is_image(img_bytes)

def is_valid_img_from_file(filename):
    return filetype.is_image(filename)

# Read image from file
def get_img_from_file(filename, cv2_flag=cv2.IMREAD_COLOR):
    return np.array(cv2.imread(filename, cv2_flag), dtype=np.uint8)

# Format image array as NLImage dict object
def NLImage_from_arr(img_arr, img_format, img_is_color):
    image_data = {
        "color": img_is_color,
        "data": img_to_bytes(img_arr, img_format),
        "width": img_arr.shape[1],
        "height": img_arr.shape[0]
    }

    return image_pb2.NLImage(**image_data) 

# Return image format given byte array of image as (".jpeg", ".png", etc...)
# If invalid/data image type can't be determined, return None
def get_img_format_from_bytes(img_bytes):
    if not is_valid_img_from_bytes(img_bytes):
        return None

    img_format = filetype.guess_extension(img_bytes)
    return ".{}".format(img_format)

# Return image format from image file (".jpeg", ".png", etc...)
# If invalid/data image type can't be determined, return None
def get_img_format_from_file(filename):
    if not is_valid_img_from_bytes(filename):
        return None

    img_format = filetype.guess_extension(filename)
    return ".{}".format(img_format)

# Encode image in specified format given image array and format
def img_to_bytes(img_arr, img_format):
    bytes_encoded, img_buffer = cv2.imencode(img_format, img_arr)
    if not bytes_encoded:
        return None
    
    return img_buffer.tobytes()

# Decode image from byte array
def bytes_to_img(img_bytes, cv2_flag=cv2.IMREAD_COLOR):
    return cv2.imdecode(np.frombuffer(img_bytes, dtype=np.uint8), cv2_flag)

# Check if image is color given image array
def img_is_color(img_arr):
    if len(img_arr) < 3: 
        return False
    
    if img_arr.shape[2] == 1:
        return False
    
    # Check if 3 channels are equal
    return not (np.all(img_arr[:, :, 0] == img_arr[:, :, 1]) and np.all(img_arr[:, :, 0] == img_arr[:, :, 2]))