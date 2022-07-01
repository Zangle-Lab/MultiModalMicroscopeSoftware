###########################################################################
# AcquireSnapshots.py
# Authors: Edward R. Polanco, Tarek E. Mustafa, Thomas A. Zangle
# This code is distributed under a creative commons attributable
# sharealike license. This license allows you to remix, adapt, and build 
# upon this work, as long as the authors are credited and the modified code
# is redistributed under the same license.
###########################################################################
from Microscope import Microscope
from StageXY import StageXY
import time
import numpy
import os
import smtplib
import ssl
from datetime import datetime



# choose directory to save your data
froot = '.\\data\\'
numFrames = 10
timeBetweenFrames = 10 # measured in seconds



startFrame = 0
# create microscope object
microscope = Microscope()
# establish serial connection with Arduino Metro
microscope.connectMetro()
# set current position as zero for the z-stage
microscope.homeStageZ()
time.sleep(2)
# create stageXY object
stageXY = StageXY()
# connect x-stage
stageXY.connectX()
# connect y-stage
stageXY.connectY()
# set stage max velocity
stageXY.setVelXY(50)
# set stage acceleration
stageXY.setAccXY(400)
# print velocity parameters
params = stageXY.getVelParametersX()
print(params)
time.sleep(.2)

# 0 is software trig and 1 is hardware trig
triggerType = 0
stageXY.createPositionListXY()
microscope.createPositionListZ()

# this still needs to be implemented
# microscope.createPositionListZDarkfield()

time.sleep(.2)
microscope.full()
time.sleep(.1)
microscope.off()
time.sleep(.1)

# 0 is software trig and 1 is hardware trig
# print('prepareTrigger: ' + str(microscope.prepareTrigger(0)))

time.sleep(.2)
microscope.full()
time.sleep(.2)
microscope.off()
time.sleep(.2)

# check for positionListXY.csv
if not os.path.exists(froot + 'positionListXY.csv'):
	# Let user know position list is not found
	print('positionListXY not found, please quit when prompted and create a position list and store in froot')
else: # position list found
	# retrieve position list from froot
	stageXY.positionListXY = numpy.genfromtxt(froot + 'positionListXY.csv', delimiter=',')
	numPos = len(stageXY.positionListXY)
	# print number of positions
	print(numPos)

# check for positionListZ.csv
if not os.path.exists(froot + 'positionListZ.csv'):
	# Let user know position list is not found
	print('positionListZ not found, please create a position list and store in froot')
else: # position list found
	# retrieve position list from froot
	microscope.positionListZ = numpy.genfromtxt(froot + 'positionListZ.csv', delimiter=',')
	numPosZ = len(microscope.positionListZ)
	# print number of positions
	print(numPosZ)

# check for positionListZDarkfield.csv
if not os.path.exists(froot + 'positionListZDarkfield.csv'):
	# Let user know position list is not found
	print('positionListZDarkfield not found, please create a position list and store in froot')
else: # position list found
	# retrieve position list from froot
	microscope.positionListZDarkfield = numpy.genfromtxt(froot + 'positionListZDarkfield.csv', delimiter=',')
	numPosZDarkfield = len(microscope.positionListZDarkfield)
	# print number of positions
	print(numPosZDarkfield)
# this control structure gives the user the opportunity to double check anything
# they think might be wrong before continuing with the program. This also gives
# the user the option to quit the program if a problem is identified.
chk = input('Please close camera GUI before continuing.  \n If you would like to continue \npress y, else if you would like to quit then press n. Then press enter...')
if (chk == 'N' or chk == 'n'):
	# need to prepare trigger to get a cam object in order to use closeMicroscope()
	microscope.prepareTrigger(0)
	microscope.off()
	microscope.closeMicroscope()
else:
	# create directory for each position in experiments
	# folders for frames are created dynamically
	for ii in range(stageXY.numPositions()):
		if not os.path.isdir(froot + 'pos' + str(ii+1)):
			os.mkdir(froot + 'pos' + str(ii + 1))
	microscope.prepareTrigger(triggerType)
	time.sleep(2) # give time for previous line to execute

	time.sleep(.1) # give time for previous line to execute

	microscope.homeStageZ() 
	for jj in range(startFrame,numFrames):
		start = time.time()
		for ii in range(numPos):
			stageXY.goToPositionXY(ii)
			print('Moved to Position ii')
			time.sleep(.1)
			microscope.goToPositionZ(int(ii))
			print('Moved to positionZ ii')
			time.sleep(.1)
			# acquire dpc image set at this location, save positions and frames
			# counting from 1 (therefore ii+1 or jj+1)
			microscope.acquireDPC(froot, ii + 1, jj + 1)

			print('Moved to positionZ for Darkfield ii')
			time.sleep(1)
			microscope.acquireDarkfield(froot, ii + 1, jj + 1)

			time.sleep(.01)

		time.sleep(.1)
	microscope.off()
	microscope.closeMicroscope()

