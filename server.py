import sys
import socket
import numpy as np
import picamera
from picamera import PiCamera
import time
import _pickle as cPickle
import struct
def main():
	server, client, port = '196.47.238.244', '137.158.123.241',3357
	#client_address = (client, port)
	server_address = (server, port)

	# capture image
	with picamera.PiCamera() as camera:
		camera.resolution = (320, 240)
		camera.framerate = 24
		time.sleep(2)
		output = np.empty((240*320*3), dtype=np.uint8)
		camera.capture(output, 'bgr')
		print(sys.getsizeof(output))
		frame = output.reshape((240, 320,3))
		print(len(frame))

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # establishing a tcp connection
	sock.bind(server_address)
	sock.listen(5)

	while True:
		(client_socket, client_address) = sock.accept() # wait for client/pc
		print('connection established with ' +str(client_address))

		while True:
			frame = cPickle.dumps(frame)
			size = len(frame)
			p = struct.pack('I', size)
			frame = p + frame
			client_socket.sendall(output)
			break
		break

	# create a datagram socket and bind to address and ip
	#server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	#server_socket.sendto(image, client_address)
	#print("sent")

if __name__ == '__main__':
	main()
