#####################################################################################
# StageXY.py
# Author: Edward R. Polanco, Tarek E. Moustafa, Thomas A. Zangle
# Date: December 26, 2019
# Last edited: May 24, 2022
#
# This code is distributed under a creative commons attributable
# sharealike license. This license allows you to remix, adapt, and build 
# upon this work, as long as the authors are credited and the modified code
# is redistributed under the same license.
#####################################################################################

from PyAPT import APTMotor
import numpy as np



class StageXY():

	def _init_():
		pass

	def connectX(self, SerialNum = 94950671, HWTYPE = 44):
		# change serial num to the serial number on the x output of BBD202
		self.motorX = APTMotor(SerialNum, HWTYPE)

	def connectY(self, 	SerialNum = 94950672, HWTYPE = 44):
		# change serial num to the serial number on the y output of BBD202
		self.motorY = APTMotor(SerialNum, HWTYPE)

	def createPositionListXY(self):
		# create empty XY position list
		self.positionListXY = np.zeros((1,2))
		self.pos = 0
		self.posNum = 0

	def connectStageXY(self):
		# connect to stage
		self.connectX()
		self.connectY()

	def getVelX(self):
		# get current max velocity in x-direction
		self.motorX.getVel()

	def getVelY(self):
		# get current max velocity in y-direction
		self.motorY.getVel()

	def getVel(self):
		pass

	def setVelX(self, maxVel):
		# sets max velocity for each move, the move speed
		# is not constant, therefore this is max speed
		self.motorX.setVel(maxVel)

	def setVelY(self, maxVel):
		# sets max velocity for each move, the move speed
		# is not constant, therefore this is max speed
		self.motorY.setVel(maxVel)

	def setVelXY(self, maxVel):
		# sets max velocity for each move, the move speed
		# is not constant, therefore this is max speed
		self.setVelX(maxVel)
		self.setVelY(maxVel)

	def getVelParametersX(self):
		params = self.motorX.getVelocityParameters()
		return params

	def getVelParametersY(self):
		params = self.motorY.getVelocityParameters()
		return params

	def setAccX(self, acc):
	#     # set parameters such as acceleration
		minVel, temp, maxVel = self.motorX.getVelocityParameters()
		self.motorX.setVelocityParameters(minVel, acc, maxVel)

	def setAccY(self, acc):
	#     # set parameters such as acceleration
		minVel, temp, maxVel = self.motorY.getVelocityParameters()
		self.motorY.setVelocityParameters(minVel, acc, maxVel)

	def setAccXY(self, acc):
	#     # set parameters such as acceleration
		self.setAccX( acc)
		self.setAccY( acc)

	def homeX(self):
		self.motorX.go_home()

	def homeY(self):
		self.motorY.go_home()

	def getPosX(self):
		# get current x-position
		return self.motorX.getPos()

	def getPosY(self):
		# get current y-position
		return self.motorY.getPos()

	def moveAbsX(self, um):
		# move to absolute x-position
		self.motorX.mAbs(um)

	def moveAbsY(self, um):
		# move to absolute y-position
		self.motorY.mAbs(um)

	def moveRelX(self, um):
		# move in x-direction relative to current position
		self.motorX.mRel(um)

	def moveRelY(self, um):
		# move in y-direction relative to current position
		self.motorY.mRel(um)

	def closeStageX(self):
		# disconnect from x-stage
		self.motorX.cleanUpAPT()

	def closeStageY(self):
		# disconnect from y-stage
		self.motorY.cleanUpAPT()

	def closeStageXY(self):
		# disconnect from both x and y stages
		self.closeStageX()
		self.closeStageY()

	def savePositionXY(self):
		# save current xy-position to position list
		posX = self.getPosX()
		posY = self.getPosY()
		posListRows = np.size(self.positionListXY,0)
		if self.pos >= posListRows:
			print('making xy-position list longer')
			self.positionListXY = np.resize(self.positionListXY, (posListRows + 1, 2))
			self.pos = posListRows
		self.positionListXY[self.pos,0] = posX
		self.positionListXY[self.pos,1] = posY

		self.pos += 1
		print('saved xy-positions = ' + str(self.pos))

	def goToPositionXY(self, pos):
		# go to a specific xy position saved in the position list
		self.pos = pos
		if self.pos >= np.size(self.positionListXY, 0) - 1:
			self.pos = np.size(self.positionListXY, 0) - 1
			self.moveAbsX(self.positionListXY[self.pos,0])
			self.moveAbsY(self.positionListXY[self.pos,1])
		else:
			self.moveAbsX(self.positionListXY[self.pos,0])
			self.moveAbsY(self.positionListXY[self.pos,1])

	
	def goToNextPos(self):
		# go to next position in position list
		self.pos = self.pos + 1
		# if currently at last position, go to first position
		if self.pos == np.size(self.positionListXY, 0):
			self.pos = 0
			self.moveAbsX(self.positionListXY[self.pos,0])
			self.moveAbsY(self.positionListXY[self.pos,1])
		else:
			self.moveAbsX(self.positionListXY[self.pos,0])
			self.moveAbsY(self.positionListXY[self.pos,1])
	
	def goToPrevPos(self):
		# go to previous position in position list
		self.pos = self.pos - 1
		# if currently at first position, go to last position
		if self.pos < 0:
			self.pos = np.size(self.positionListXY,0) - 1
			self.moveAbsX(self.positionListXY[self.pos,0])
			self.moveAbsY(self.positionListXY[self.pos,1])
		else:
			self.moveAbsX(self.positionListXY[self.pos,0])
			self.moveAbsY(self.positionListXY[self.pos,1])


	def goToCurrentPosition(self):
		self.moveAbsX(self.positionListXY[self.pos,0])
		self.moveAbsY(self.positionListXY[self.pos,1])

	def printPositionList(self):
		# print the saved position list
		print(self.positionListXY)

	def printNumPositions(self):
		# print number of saved positions
		print(len(self.positionListXY))

	def removeZeros(self):
		self.positionListXY = self.positionListXY[~np.all(self.positionListXY==0, axis = 1)]

	def numPositions(self):
		# get number of positions saved in position list
		rows = len(self.positionListXY)
		return rows

	def setFocusLoc(self):
		# set a position for a focus target
		posX = self.getPosX()
		posY = self.getPosY()
		self.focusLoc[0,0] = posX
		self.focusLoc[0,1] = posY

	def setFirstWellCenterX(self):
		# set x position for a reference location
		self.firstWellCenter[0,0] = self.getPosX()

	def setFirstWellCenterY(self):
		# set y position for a reference location
		self.firstWellCenter[0,1] = self.getPosY()

	def goToFirstWellCenter(self):
		# go to reference location
		self.moveAbsX(self.firstWellCenter[0,0])
		self.moveAbsY(self.firstWellCenter[0,1])

	def goToFocusLoc(self):
		# go to focus target
		self.moveAbsX(self.focusLoc[0,0])
		self.moveAbsY(self.focusLoc[0,1])
	
	def savePositionListXY(self):
		# save position list to a file
		np.savetxt(".\\data\\positionListXY.csv", self.positionListXY, delimiter=",")
	
	def setPosNumXY(self, posNum):
		self.pos = int(posNum)
		print(str(self.pos))