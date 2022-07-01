###########################################################################
# DPCQPIMicroscopeInterface.py
# Authors: Edward R. Polanco, Tarek E. Mustafa, Thomas A. Zangle
# This code is distributed under a creative commons attributable
# sharealike license. This license allows you to remix, adapt, and build 
# upon this work, as long as the authors are credited and the modified code
# is redistributed under the same license.
###########################################################################

import tkinter as tk
from tkinter import ttk
from Metro import Metro
from StageXY import StageXY
import numpy
import time


class findLocsWindow(tk.Toplevel):
	def __init__(self, parent, metro, stage):
		super().__init__(parent)

		self.geometry('350x500')
		self.title('Find Locations')
		# make label prompting user to center focusing target
		self.frame = tk.Frame(self)
		ledControlsLabel = ttk.Label(self,text="LED array controls:")

		# define buttons: all buttons have self as an argument
		# the command=lambda *args: funtionName(param1, param2, ...)
		# seems to work.
		
		ledOnButton = ttk.Button(self,
			text="brightfield",
			command=lambda *args: metro.small()
			)

		ledLeftButton = ttk.Button(self,
			text="left half",
			command=lambda *args: metro.left_half()
			)

		ledTopButton = ttk.Button(self,
			text="top half",
			command=lambda *args: metro.top_half()
			)

		darkfieldButton = ttk.Button(self,
			text="darkfield",
			command=lambda *args: metro.edges()
			)

		ledRightButton = ttk.Button(self,
			text="right half",
			command=lambda *args: metro.right_half()
			)

		ledBottomButton = ttk.Button(self,
			text="bottom half",
			command=lambda *args: metro.bottom_half()
			)

		ledOffButton = ttk.Button(self,
			text="LED off",
			command=lambda *args: metro.off()
			)
			
		zStageControlsLabel = ttk.Label(self,text="z-stage controls:")

		moveZStageUp2Button = ttk.Button(self,
			text="+2",
			command=lambda *args: metro.moveRelZ(2)
			)

		moveZStageDown2Button = ttk.Button(self,
			text="-2",
			command=lambda *args: metro.moveRelZ(-2)
			)

		moveZStageUp3Button = ttk.Button(self,
			text="+3",
			command=lambda *args: metro.moveRelZ(3)
			)

		moveZStageDown3Button = ttk.Button(self,
			text="-3",
			command=lambda *args: metro.moveRelZ(-3)
			)

		moveZStageUp5Button = ttk.Button(self,
			text="+5",
			command=lambda *args: metro.moveRelZ(5)
			)

		moveZStageDown5Button = ttk.Button(self,
			text="-5",
			command=lambda *args: metro.moveRelZ(-5)
			)

		moveZStageUp7Button = ttk.Button(self,
			text="+7",
			command=lambda *args: metro.moveRelZ(7)
			)

		moveZStageDown7Button = ttk.Button(self,
			text="-7",
			command=lambda *args: metro.moveRelZ(-7)
			)
			
		xyStageControlsLabel = ttk.Label(self,text="xyz-stage controls:")

		firstPosButton = ttk.Button(self,
			text="first pos",
			command=lambda *args: self.goToFirstPosition(metro, stage)
			)

		prevPosButton = ttk.Button(self,
			text="prev pos",
			command=lambda *args: self.prevPos(metro, stage)
			)

		nextPosButton = ttk.Button(self,
			text="next pos",
			command=lambda *args: self.nextPos(metro, stage)
			)

		focusHereButton = ttk.Button(self,
			text="focus",
			command=lambda *args: metro.focusHere(metro.pos)
			)

		self.posNumEntry = ttk.Entry(self, width=3)

		setPosNumButton = ttk.Button(self,
			text="set pos num",
			command=lambda *args: self.setPosNum(metro,stage)
			)

		goToCurrentPosButton = ttk.Button(self,
			text="current pos",
			command=lambda *args: stage.goTo(metro,stage)
			)

		homeZStageButton = ttk.Button(self,
			text="save first z-pos",
			command=lambda *args: self.saveFirstZPosition(metro)
			)

		savePosButtonXY = ttk.Button(self,
			text="save xy-pos",
			command=lambda *args: stage.savePositionXY()
			)

		savePosButtonZ = ttk.Button(self,
			text="save z-pos",
			command=lambda *args: metro.savePositionZ()
			)

		savePosListXYButton = ttk.Button(self,
			text="save xy-pos list",
			command=lambda *args: stage.savePositionListXY()
			)

		savePositionListZButton = ttk.Button(self,
			text="save z-pos list",
			command=lambda *args: metro.savePositionListZ()
			)

		goToHomeButton = ttk.Button(self,
			text="go to home",
			command=lambda *args: metro.moveAbsZ(0)
			)

		closeButton = ttk.Button(self,
				text='Close',
				command=self.destroy)

		ledControlsLabel.grid(row=0,column=0)
		ledTopButton.grid(row=1, column=1)
		darkfieldButton.grid(row=1, column =3)
		ledLeftButton.grid(row=2, column=0)
		ledRightButton.grid(row=2, column=2)
		ledBottomButton.grid(row=3, column=1)
		ledOnButton.grid(row=2, column=1)
		ledOffButton.grid(row=4, column=3)
		zStageControlsLabel.grid(row=5,column=0)
		moveZStageUp2Button.grid(row=6,column=0)
		moveZStageDown2Button.grid(row=7,column=0)
		moveZStageUp3Button.grid(row=6,column=1)
		moveZStageDown3Button.grid(row=7,column=1)
		moveZStageUp5Button.grid(row=6,column=2)
		moveZStageDown5Button.grid(row=7,column=2)
		moveZStageUp7Button.grid(row=6,column=3)
		moveZStageDown7Button.grid(row=7,column=3)
		moveZStageUp5Button.grid(row=6,column=2)
		moveZStageDown5Button.grid(row=7,column=2)
		xyStageControlsLabel.grid(row=8, column=0)
		firstPosButton.grid(row=9,column=0)
		prevPosButton.grid(row=9,column=1)
		nextPosButton.grid(row=9,column=2)
		focusHereButton.grid(row=9,column=3)
		self.posNumEntry.grid(row=10,column=0)
		setPosNumButton.grid(row=10,column=1)
		goToCurrentPosButton.grid(row=10,column=2)
		homeZStageButton.grid(row=10,column=3)
		savePosButtonXY.grid(row=11,column=0)
		savePosButtonZ.grid(row=11,column=1)
		savePosListXYButton.grid(row=11,column=2)
		savePositionListZButton.grid(row=11,column=3)
		goToHomeButton.grid(row=12,column=0)
		closeButton.grid(row=13,column=0)

	def setPosNum(self,metro,stage):
		posNum = self.posNumEntry.get()
		stage.setPosNumXY(posNum)
		metro.setPosNumZ(posNum)

	def nextPos(self, metro, stage):
		stage.goToNextPos()
		metro.incrementPosZ()

	def prevPos(self, metro, stage):
		stage.goToPrevPos()
		metro.decrementPosZ()

	def goToFirstPosition(self, metro, stage):
		stage.goToPositionXY(0)
		metro.goToPositionZ(0)

	def saveFirstZPosition(self, metro):
		metro.homeStageZ()
		metro.savePositionZ()

class App(tk.Tk):
	def __init__(self):
		super().__init__()

		self.geometry('300x200')
		self.title('Main Window')
		self.stage = StageXY()
		self.metro = Metro()
		self.metro.homeStageZ()
		self.metro.createPositionListZ()
		self.stage.connectStageXY()
		self.stage.createPositionListXY()

		findLocsButton = ttk.Button(self,
			text='find locations',
			command=self.openFindLocsButton
			)

		closeMetroButton = ttk.Button(self,
			text = 'close arduino',
			command=lambda:self.metro.closeMetro()
			)

		closeStageButton = ttk.Button(self,
			text = 'close stage',
			command=lambda:self.stage.closeStageXY()
			)

		closeButton = ttk.Button(self,
			text='close program',
			command=self.destroy
			)

		# place and position GUI elements
		findLocsButton.grid(row = 0, column = 1)
		closeStageButton.grid(row = 6, column = 1)
		closeMetroButton.grid(row = 7, column = 1)
		closeButton.grid(row = 8, column = 1)

	def openFindLocsButton(self):
		window = findLocsWindow(self, self.metro, self.stage)
		window.grab_set()