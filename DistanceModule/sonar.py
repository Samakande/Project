import RPi.GPIO as GPIO
import time
from concurrent.futures import ThreadPoolExecutor
#GPIO.cleanup()

GPIO.setmode(GPIO.BCM)

TRIG1 = 23

ECHO1 = 24

GPIO.setup(TRIG1,GPIO.OUT)

GPIO.setup(ECHO1,GPIO.IN)

TRIG2 = 17

ECHO2 = 27

GPIO.setup(TRIG2,GPIO.OUT)

GPIO.setup(ECHO2,GPIO.IN)


def dist(TRIG,ECHO):
	while True:
		GPIO.output(TRIG, False)
		time.sleep(0.00001)
		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)
		while GPIO.input(ECHO)==0:
			pulse_start = time.time()
		while GPIO.input(ECHO)==1:
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration* 17150
		distance = round(distance, 2)
		print (TRIG," Distance:",distance,"cm")


		#GPIO.cleanup()

def run_parallel(*functions):
	'''
	Run functions in parallel
	'''
	from multiprocessing import Process
	processes = []
	for function in functions:
		proc = Process(target=function)
		proc.start()
#		processes.append(proc)
#	for proc in processes:
#		proc.join()

if __name__ == '__main__':

	run_parallel(dist(TRIG1, ECHO1),dist(TRIG2,ECHO2))
#	GPIO.cleanup()
