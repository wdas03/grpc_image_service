import unittest
import os

import numpy as np
import grpc
from image_utils import *

from server import *
from client import *

import image_pb2

class TestClientServer(unittest.TestCase):
    def test_gray_img(self):
        self.assertFalse(img_is_color(get_img_from_file(os.path.join("images", "gray_dog.jpeg"))))

    def test_valid_img_data(self):
        for img_file in os.listdir("images"):
            self.assertTrue(is_valid_img_from_file(os.path.join("images", img_file)))

    def test_valid_byte_data(self):
        for img_file in os.listdir("images"):
            img = get_img_from_file(os.path.join("images", img_file))
            img_bytes = img_to_bytes(img, get_img_format_from_file(os.path.join("images", img_file)))

            self.assertTrue(is_valid_img_from_bytes(img_bytes))

    def test_invalid_byte_data(self):
        self.assertFalse(is_valid_img_from_bytes(np.random.bytes(10)))
        self.assertFalse(is_valid_img_from_bytes(np.random.bytes(100)))
        self.assertFalse(is_valid_img_from_bytes(np.random.bytes(1000)))
        self.assertFalse(is_valid_img_from_bytes(np.random.randint(low=0, high=255,size=(250,250), dtype=np.uint8).tobytes()))

    # Send random (invalid) byte data to server 
    # server should be running on localhost:8080
    # python server.py --port 8080 --host localhost
    def test_send_server_invalid_byte_data(self):
        channel_options = [('grpc.max_send_message_length', 512 * 1024 * 1024), ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        
        with grpc.insecure_channel(target="localhost:8080", options=channel_options) as channel:
            stub = image_pb2_grpc.NLImageServiceStub(channel)
            
            for i in range(0, 1001, 100):
                invalid_image_data = {
                    "color": True,
                    "data": np.random.bytes(i),
                    "width": 250,
                    "height": 250
                }

                resp = stub.MeanFilter(image_pb2.NLImage(**invalid_image_data))
                self.assertTrue(len(resp.data) == 0)

                req = image_pb2.NLImageRotateRequest(rotation=2, 
                                                    image=image_pb2.NLImage(**invalid_image_data))
                
                resp = stub.RotateImage(req)
                self.assertTrue(len(resp.data) == 0)
            
if __name__ == '__main__':
    unittest.main()