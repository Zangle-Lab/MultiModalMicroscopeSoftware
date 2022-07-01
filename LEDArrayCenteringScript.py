######################################################################################
# LEDArrayCenteringScript.py
# Authors: Eddie Polanco, Tarek E. Moustafa, Thomas A. Zangle
# Date: May 15, 2022
# This code is distributed under a creative commons attributable
# sharealike license. This license allows you to remix, adapt, and build 
# upon this work, as long as the authors are credited and the modified code
# is redistributed under the same license.
######################################################################################
from Microscope import Microscope
# from StageXY import StageXY
import time
import numpy

microscope = Microscope()
microscope.connectMetro()
time.sleep(.2)
microscope.full()
time.sleep(.1)
microscope.off()
microscope.prepareTrigger(0)
time.sleep(5)

pos = 1
start = time.time()
for ii in range(100):
	microscope.acquireDPC('.\\data\\', pos, ii+1)


stop = time.time()
print(stop-start)

microscope.off()
microscope.closeMetro()
microscope.closeCamera()
