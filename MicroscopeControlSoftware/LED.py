######################################################################################
# LED.py
# Authors: Eddie Polanco, Tarek E. Moustafa, Thomas A. Zangle
# Date: May 15, 2022
#
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
import time

class LED():

	def __init__(self):
		pass

	def send(self, phrase):

		""" General phrase to send a serial command to the LED Arduino. General format
		is self.conn.write((' [ string of direction to move ]\n'.encode() )
		Commands for the LED are: Left half: 'L\n'. Right half: 'R\n'. Top Half: 'T\n'.
		Bottom half: 'B\n'. Full: 'F\n'. and Off: 'O\n'.
		"""

		self.conn.write(phrase)
		for ii in range(500):
			time.sleep(.05)
			if self.conn.inWaiting():
				while(self.conn.inWaiting()):
					test = self.conn.read()
					# next two lines can be uncommented for troubleshooting
					# print('value returned: ' + str(test))
					# print('iter: ' + str(ii))
				break
			else:
				continue

	def left_half(self):

		""" Light the left-half of the LED array
		"""
		self.conn.write(('IL\n').encode())
		print('sent left')
		for ii in range(10000):
			time.sleep(.001)
			if self.conn.inWaiting():
				while(self.conn.inWaiting()):
					test = self.conn.read()
					# next two lines can be uncommented for troubleshooting
					# print('value returned: ' + str(test))
					# print('iter: ' + str(ii))
				break
			else:
				continue
		print('received left')

	def right_half(self):

		""" Light the Right-Half of the LED array
		"""

		self.conn.write(('IR\n').encode())
		print('sent right')
		for ii in range(10000):
			time.sleep(.001)
			if self.conn.inWaiting():
				while(self.conn.inWaiting()):
					test = self.conn.read()
					# next two lines can be uncommented for troubleshooting
					# print('value returned: ' + str(test))
					# print('iter: ' + str(ii))
				break
			else:
				continue
		print('received right')

	def top_half(self):

		""" Light the Top-Half of the LED array
		"""
		self.conn.write(('IT\n').encode())
		
		print('sent top')
		for ii in range(10000):
			time.sleep(.001)
			if self.conn.inWaiting():
				while(self.conn.inWaiting()):
					test = self.conn.read()
					# next two lines can be uncommented for troubleshooting
					# print('value returned: ' + str(test))
					# print('iter: ' + str(ii))
				break
			else:
				continue
		
		print('received top')

	def bottom_half(self):

		""" Light the Bottom-Half of the LED array
		"""
		self.conn.write(('IB\n').encode())
		print('sent bot')
		for ii in range(10000):
			time.sleep(.001)
			if self.conn.inWaiting():
				while(self.conn.inWaiting()):
					test = self.conn.read()
					# next two lines can be uncommented for troubleshooting
					# print('value returned: ' + str(test))
					# print('iter: ' + str(ii))
				break
			else:
				continue
		print('receieved bot')

	def edges(self):
		""" Light outer edges of the LED array
		"""
		self.conn.write(('IE\n').encode())
		for ii in range(10000):
			time.sleep(.001)
			if self.conn.inWaiting():
				while(self.conn.inWaiting()):
					test = self.conn.read()
					# next two lines can be uncommented for troubleshooting
					# print('value returned: ' + str(test))
					# print('iter: ' + str(ii))
				break
			else:
				continue

	def full(self):

		""" Light the Full circle configuration of the LED array
		"""
		self.conn.write(('IF\n').encode())
		for ii in range(10000):
			time.sleep(.001)
			if self.conn.inWaiting():
				while(self.conn.inWaiting()):
					test = self.conn.read()
					# next two lines can be uncommented for troubleshooting
					# print('value returned: ' + str(test))
					# print('iter: ' + str(ii))
				break
			else:
				continue

	def small(self):

		""" Light the Full circle configuration of the LED array
		"""
		self.conn.write(('IS\n').encode())
		for ii in range(10000):
			time.sleep(.001)
			if self.conn.inWaiting():
				while(self.conn.inWaiting()):
					test = self.conn.read()
					# next two lines can be uncommented for troubleshooting
					# print('value returned: ' + str(test))
					# print('iter: ' + str(ii))
				break
			else:
				continue

	def off(self):

		""" Turn off the LED array
		"""
		self.conn.write(('IO\n').encode())
		for ii in range(10000):
			time.sleep(.001)
			if self.conn.inWaiting():
				while(self.conn.inWaiting()):
					test = self.conn.read()
					# next two lines can be uncommented for troubleshooting
					# print('value returned: ' + str(test))
					# print('iter: ' + str(ii))
				break
			else:
				continue
				
