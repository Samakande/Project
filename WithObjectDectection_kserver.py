import io
import socket
import struct
import matplotlib.pyplot as pl
import cv2
import numpy as np
from skimage.color import rgb2gray
from skimage import data
#from PIL import Image
import time
import csv

server_socket = socket.socket()
server_socket.bind(('137.158.123.241', 8015))  # ADD IP HERE
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')

try:
    img = None
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)

        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes,0)
        #img = cv2.imread("image.jpg")
        stop_data = cv2.CascadeClassifier('stop_data.xml')

        found = stop_data.detectMultiScale(img, minSize =(20, 20))

	# Don't do anything if there's 
	# no sign
        amount_found = len(found)
        print(amount_found)
        if amount_found != 0:
            # sent items found to the back to the raspberrypi
            # 
            # There may be more than one
            # sign in the image
            for (x, y, width, height) in found:

                cv2.rectangle(img, (x, y), (x + height, y + width), (0, 255, 0), 5)

        cv2.imshow('res2',img)
        cv2.waitKey(1)

finally:
    connection.close()
    server_socket.close()
