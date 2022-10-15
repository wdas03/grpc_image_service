import argparse
import logging
import pathlib

import grpc
import image_pb2
import image_pb2_grpc

import numpy as np
import cv2
import imghdr
import os

from image_utils import *
from config import ROTATION_ENUM

class ImageServiceRequest:
    def __init__(self):
        pass
    
    # args: dict
    # port, host, input, output, rotate, mean
    # Run client given command line arguments
    def run_client(self, args):
        server_addr = "{}:{}".format(args.host, args.port)
        
        # Get image info
        if not os.path.exists(args.input):
            logging.warning("File {} doesn't exist.".format(args.input))
            return

        if not is_valid_img_from_file(args.input):
            logging.warning("Image file {} is not valid.".format(args.input))
            return

        img = get_img_from_file(args.input)
        img_height, img_width, img_num_channels = img.shape[0], img.shape[1], img.shape[2]
        
        # Encode/compress image for network transfer
        img_bytes = img_to_bytes(img, get_img_format_from_file(args.input))
        
        channel_options = [('grpc.max_send_message_length', 512 * 1024 * 1024), ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        
        logging.info("Connecting to {}...".format(server_addr))
        with grpc.insecure_channel(target=server_addr, options=channel_options) as channel:
            logging.info("Connected to grpc server @ {}...".format(server_addr))
            
            stub = image_pb2_grpc.NLImageServiceStub(channel)
            output_img = img
            
            # Use mean filter
            if args.mean:
                resp = stub.MeanFilter(NLImage_from_arr(output_img, get_img_format_from_file(args.input), 
                                                        img_is_color(output_img)))
                
                # Invalid image given, corrupted data
                if len(resp.data) == 0:
                    logging.warning("Could not apply mean filter")
                    return
                
                # Decode output image
                output_img = bytes_to_img(resp.data)
                
                if output_img is not None:
                    logging.info("Applied mean filter to image.")
                else:
                    logging.info("Could not apply mean filter/invalid image.")
                
            # Rotate image
            if ROTATION_ENUM[args.rotate] > 0:
                req = image_pb2.NLImageRotateRequest(rotation=ROTATION_ENUM[args.rotate], 
                                                    image=NLImage_from_arr(output_img, 
                                                                            get_img_format_from_file(args.input), 
                                                                            img_is_color(output_img)))
                
                resp = stub.RotateImage(req)

                # Invalid image given, corrupted data
                if len(resp.data) == 0:
                    logging.warning("Could not apply rotation.")
                    return
            
                # Decode output image
                output_img = bytes_to_img(resp.data)
                
                if output_img is not None:
                    logging.info("Applied rotation {} to image.".format(args.rotate))
                else:
                    logging.info("Could not rotation {} to image.".format(args.rotate)) 
            
            # Write image to output file
            if cv2.imwrite(args.output, output_img):
                logging.info("Wrote image to file: {}".format(args.output))


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--port", help="Port")
    parser.add_argument("--host", help="Hostname")
    parser.add_argument("--input", help="Input image file")
    parser.add_argument("--output", help="Output image file")
    
    parser.add_argument("--rotate", help="Rotation value")
    parser.add_argument("--mean", help="Use mean filter", action='store_true')

    args = parser.parse_args()
    
    return args

    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Parse command line arguments
    args = parse_args()

    req = ImageServiceRequest()
    req.run_client(args)
    
    
  