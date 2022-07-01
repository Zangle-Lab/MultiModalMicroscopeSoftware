######################################################################################
# Metro.py
# Author: Eddie Polanco, Tarek E. Moustafa, Thomas A. Zangle
# Date: May 15, 2022
#
#Example of how to import class, instantiate class object, and connect to LED array:
# import LED
# led = LED.LED()
# led.connectLED()
#
# This code is distributed under a creative commons attributable
# sharealike license. This license allows you to remix, adapt, and build 
# upon this work, as long as the authors are credited and the modified code
# is redistributed under the same license.
#####################################################################################

import serial
from LED import LED
from Zstage import Zstage # for GUI version of code

class Metro(LED,Zstage):

	def __init__(self, serial_port='COM5', baud_rate = 57600, read_timeout = 10, verbose = False):
		""" Open serial communication with the LED. Note how the COM is different, and
		baud_rate is recommended to be at 57600 for the LED. Paramters for this experiment
		were baud_rate = 57600, read_timeout = 1000, verbose = False, parity = None,
		eight serial bits, 1 stopbit

		Make sure to check the COM# in the Arudino software (Tools -> port), it probably is not COM5.
		"""
		print('Connecting to Metro M4 controller ... ')
		self.conn = serial.Serial(port = serial_port, baudrate = baud_rate, timeout = read_timeout, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE, parity = serial.PARITY_NONE, write_timeout = read_timeout)
		self.conn.timeout = read_timeout

		self.step = 0
		self.z = 0
		print('Connected to Metro m4')

	def connectMetro(self, serial_port='COM5', baud_rate = 57600, read_timeout = 10, verbose = False):
		print('Connecting to Metro M4 ... ')
		self.conn = serial.Serial(port = serial_port, baudrate = baud_rate, timeout = read_timeout, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE, parity = serial.PARITY_NONE, write_timeout = read_timeout)
		self.conn.timeout = read_timeout
		self.step = 0
		self.z = 0

		print('Connected to Metro M4')

	def closeMetro(self):

		"""Important to close serial communication with the LED after each
		run. Must turn off LED prior to disconnecting otherwise it will remain on.
		"""
		self.off()
		self.conn.close()
		print('Connection to Metro m4 closed')
