from concurrent import futures
import logging

import argparse

import grpc

import image_pb2
import image_pb2_grpc

import numpy as np
import cv2
import imghdr

from image_utils import *
from config import ROTATION_ENUM, ROTATION_CV_CONSTANTS

class NLImageService(image_pb2_grpc.NLImageServiceServicer):
    
    # Rotate image
    def RotateImage(self, request, context):
        #logging.info("color: {}, width: {}, height: {}".format(request.image.color, request.image.width, request.image.height))

        # Get image format
        img_format = get_img_format_from_bytes(request.image.data)

        # Check if img is valid or not:
        if img_format is None:
            logging.warning("Image byte data is invalid.")
            return image_pb2.NLImage(** {"color": request.image.color, 
                                        "data": None, 
                                        "width": request.image.width, 
                                        "height": request.image.height})

        # Decode byte array image
        img = bytes_to_img(request.image.data)
        output_img = img
        
        if request.rotation > 0:
            output_img = cv2.rotate(output_img, ROTATION_CV_CONSTANTS[request.rotation])
        
        return NLImage_from_arr(output_img, img_format, request.image.color)
        
    # Apply mean filter   
    def MeanFilter(self, request, context):
        # Get image format
        img_format = get_img_format_from_bytes(request.data)

        # Check if img is valid or not:
        if img_format is None:
            logging.warning("Image byte data is invalid.")
            return image_pb2.NLImage(** {"color": request.color, 
                                        "data": None, 
                                        "width": request.width, 
                                        "height": request.height})


        # Decode byte array image
        # kernel size by default: 3x3
        img = bytes_to_img(request.data)
        output_img = cv2.blur(img, (3,3))
        
        return NLImage_from_arr(output_img, img_format, request.color)

class ImageServiceServer:
    def __init__(self):
        pass
    
    # Run server
    # args: dict
    # port, host
    def run_server(self, args):
        server_addr = "{}:{}".format(args.host, args.port)
    
        server = grpc.server(futures.ThreadPoolExecutor(), options = [
            ('grpc.max_send_message_length', 512 * 1024 * 1024),
            ('grpc.max_receive_message_length', 512 * 1024 * 1024)
        ])
        image_pb2_grpc.add_NLImageServiceServicer_to_server(NLImageService(), server)
        
        #server.add_insecure_port("{}".format(server_addr))
        server.add_insecure_port("[::]:{}".format(args.port))

        logging.info("Starting grpc server @ {}...".format(server_addr))
        server.start()
        logging.info("Server started.".format(server_addr))
        
        server.wait_for_termination()

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--port", help="Port")
    parser.add_argument("--host", help="Host")

    args = parser.parse_args()
    
    return args 
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    args = parse_args()

    server = ImageServiceServer()
    server.run_server(args)
    
    
    
    
    