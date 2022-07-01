######################################################################################
# ZStage.py
# Author: Eddie Polanco, Tarek E. Moustafa, Thomas A. Zangle
# Date: October 14, 2019
# Last Edited May 24, 2022
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
import numpy as np
import time

class Zstage():

	def __init__():
		pass

	def moveZ(self, um):
		# Note: This code sends a string with only z axis motion information followed by
		# a terminator return "\n" 

		self.step = int(um/.03)
		self.z += um
		# check to make sure stage doesn't move out of range
		if um < 1000 or um > -1000:
			self.conn.write(('M'+str(self.step)+'\n').encode())
		else:
			return 'warning: units in microns'

		# print('sent moveZ')
		a = time.time()
		for ii in range(500):
			time.sleep(.05)
			# check if stage is moving
			if self.conn.inWaiting():
				# wait for stage to finish moving
				while(self.conn.inWaiting()):
					b = time.time()
					test = self.conn.read()
					# print('value returned: ' + str(test))
					# print('time to return: ' + str(b-a))
					# print('number of zMove iterations: ' + str(ii))
				break
			else:
				continue

		# print('received moveZ')
		
		c = time.time()
		# print('time to return and process: ' + str(c-a) + '\n')
		self.timeToZStageResponse[self.zz] = c-a
		self.zz += 1

	def moveRelZ(self, um):
		# move z-stage relative to current position
		self.currentPos = self.currentPos + um
		self.moveZ(um)

	def homeStageZ(self):
		# set current z-position to zero
		self.currentPos = 0
		self.home = 0
		self.pos = 0

		self.timeToZStageResponse = np.zeros(1000000)
		self.zz = 0

	def returnToHome(self):
		# return to z-position = 0
		self.moveAbsZ(self.home)

	def moveAbsZ(self, myZ):
		# move z-stage relative to 0 position
		if int(myZ) < 100 and int(myZ) > -100:
			oldPos = self.currentPos
			self.currentPos = myZ
			self.moveZ(self.currentPos-oldPos)
		elif myZ > 100:
			myZ = 100
			oldPos = self.currentPos
			self.currentPos = myZ
			self.moveZ(self.currentPos-oldPos)
		elif myZ < -100:
			myZ = -100
			oldPos = self.currentPos
			self.currentPos = myZ
			self.moveZ(self.currentPos-oldPos)
			

	def focusHere(self, myPos):
		# focus on current position using z-position list
		self.goToPositionZ(int(myPos))
		print("focusing well: " + str(myPos))

	def createPositionListZ(self):
		# create empty z-position list
		self.positionListZ = np.zeros((1,1))

	def goToPositionZ(self, pos):
		# go to z-position logged in row pos
		self.pos = pos
		if self.pos >= np.size(self.positionListZ, 0) - 1:
			self.pos = np.size(self.positionListZ, 0) - 1
			self.moveAbsZ(self.positionListZ[pos])
		else:
			self.moveAbsZ(self.positionListZ[pos])

	def printPositionListZ(self):
		# print the z-position list
		print(self.positionListZ)

	def savePositionListZ(self):
		# save z-position list to csv file
		np.savetxt(".\\data\\positionListZ.csv", self.positionListZ, delimiter=",")


	def numPositions(self):
		# find number of positions in position list
		rows = len(self.positionListZ)
		return rows

	def savePositionZ(self):
		# append current z-position to the end of z-position list
		posZ = self.getPosZ()
		posListRows = np.size(self.positionListZ)
		print('posListRows: ' + str(posListRows))
		if self.pos >= posListRows:
			print('making z-position list longer')
			self.positionListZ = np.resize(self.positionListZ, (posListRows + 1, 1))
			self.pos = posListRows
		self.positionListZ[self.pos]= posZ

		self.pos+=1
		print('saved z-positions = ' + str(self.pos))


	def setPosNumZ(self,pos):
		self.pos = int(pos)
		print(str(self.pos))

	def incrementPosZ(self):
		self.pos = self.pos + 1
		if self.pos == np.size(self.positionListZ):
			self.pos = 0
		else:
			self.pos += 1

	def decrementPosZ(self):
		self.pos = self.pos - 1
		if self.pos < 0:
			self.pos = np.size(self.positionListZ,0) - 1
		else:
			self.pos += 1

	def getPosZ(self):
		# get current z-position
		return self.currentPos

