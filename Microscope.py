#####################################################################################
# Microscope.py
# Author: Edward R. Polanco, Tarek E. Moustafa, Thomas A. Zangle
# Date: December 26, 2019
# Last edited: May 24, 2022
#
# Example of how to import and instantiate class object:
# import Microscope_v12
# microscope = Microscope_v12.Microscope()
#
# Example of how to use members of Microscope class to connect to LED array, then
# to turn on the LED array, and finally to close the connection:
# microscope.connectLED()
# microscope.full()
# time.sleep(.1)
# microscope.full()
# time.sleep(.1)
# microscope.left_half()
# microscope.closeLED()
#
# Note: For some reason when lighting the LED array, it is necessary to use the
# function: microscope.full() twice as shown above. This only occurs the first time
# that you try to light the LED array, and every time the pattern on the LED array
# is changed, it should change with a single command (again as shown above). The
# time.sleep(.1) command is necessary when sending multiple commands to the LED array
# with no other commands in between because otherwise the LED array will not be able
# to keep up with all the commands being sent to it in rapid succession.
#
# Example of how to use members of Microscope class to setup hardware trigger, trigger
# camera, and how to close the connection to the camera:
# trigger:
# microscope.prepareTrigger(2)
# microscope.hardwareTrigger("filename")
# microscope.closeCamera()
#
# If a connection exists to both the LED array and the camera, the
# connection to both can be closed simultaneously using the closeMicroscope() function.
#
# This code is distributed under a creative commons attributable
# sharealike license. This license allows you to remix, adapt, and build 
# upon this work, as long as the authors are credited and the modified code
# is redistributed under the same license.
#####################################################################################

import PySpin
# The syntax on the next two lines is important because you must import the LED class
# from the LED file if you try to do it as follows
# import LED
# this will not work. You will get an error.
from Metro import Metro
from Camera import Camera
import threading
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from tifffile import imsave
from mpl_toolkits.axes_grid1 import make_axes_locatable
import time
from PIL import Image
import os
import matlab.engine
from scipy import optimize
import math




# defines Microscope as a derived class of both the LED and Camera classes
class Microscope(Camera, Metro):

	# defines constructor to accept a triggerType argument. This is necessary because
	# Camera class needs a trigger type argument to know whether or not to set itself up
	# to work with a hardware or software trigger, triggerType is an integer such that
	# a software trigger should be 1 and a hardware trigger should be 2.
	def _init_(self):
		pass

	def closeMicroscope(self):
		# execute close functions in the parent classes of Microscope
		self.closeMetro()
		self.closeCamera()

	def acquireDPC(self, froot, pos, frame):

		try:


			result = True

			# uint8 in the next line should probably be changed to a floating point number
			dpc_images = np.zeros([4,1200,1920], 'uint16')
			savedir = froot + 'pos' + str(pos) + '\\frame' + str(frame)
			if not os.path.isdir(savedir):
				os.mkdir(savedir)
			savedir = savedir + '\\'

			for ii in range(4):
				#  Retrieve the next image from the trigger

				if ii == 0:
					result = self.grab_left_image_by_trigger(self.cam, self.nodemap)
					filename = savedir + 'Image_' + str(frame) + 'L'
				elif ii == 1:
					result = self.grab_bottom_image_by_trigger(self.cam, self.nodemap)
					filename = savedir + 'Image_' + str(frame) + 'B'
				elif ii == 2:
					result = self.grab_right_image_by_trigger(self.cam, self.nodemap)
					filename = savedir + 'Image_' + str(frame) + 'R'
				elif ii == 3:
					result = self.grab_top_image_by_trigger(self.cam, self.nodemap)
					filename = savedir + 'Image_' + str(frame) + 'T'

				#  Retrieve next received image
				image_result = self.cam.GetNextImage()

				#  Ensure image completion
				if image_result.IsIncomplete():
					print('Image incomplete with image status %d ...' % image_result.GetImageStatus())

				else:
					self.saveFunc(image_result,filename)
					image_converted = image_result.Convert(PySpin.PixelFormat_Mono16)

			print('DPC image set saved at: ' + savedir)

		except PySpin.SpinnakerException as ex:
			# each of these steps must be done to properly close the camera,
			# and they must be executed in this order
			# stop streaming from the camera
			self.cam.EndAcquisition()
			# deinitialize the camera
			self.cam.DeInit()
			# delete cam object
			del self.cam
			# clear camera list
			self.cam_list.Clear()
			# release camera instance
			self.system.ReleaseInstance()
			return False

	def acquireDarkfield(self, froot, pos, frame):

		try:
			

			result = True
			self.setDarkfieldCameraSettings()
			# uint8 in the next line should probably be changed to a floating point number
			
			darkfield_images = np.zeros([1200,1920], 'uint16')
			savedir = froot + 'pos' + str(pos) + '\\darkfield'
			if not os.path.isdir(savedir):
				os.mkdir(savedir)
			savedir = savedir + '\\'

			time.sleep(0.1)
			result = self.grab_darkfield_image_by_trigger(self.cam,self.nodemap)
			filename = savedir + 'DarkfieldImage_' + str(frame)


			#  Retrieve next received image
			image_result = self.cam.GetNextImage()

			#  Ensure image completion
			if image_result.IsIncomplete():
				print('Image incomplete with image status %d ...' % image_result.GetImageStatus())

			else:
				self.saveFunc(image_result,filename)
				image_converted = image_result.Convert(PySpin.PixelFormat_Mono16)

			print('Darkfield image saved at: ' + savedir)

		except PySpin.SpinnakerException as ex:
			# each of these steps must be done to properly close the camera,
			# and they must be executed in this order
			# stop streaming from the camera
			self.cam.EndAcquisition()
			# deinitialize the camera
			self.cam.DeInit()
			# delete cam object
			del self.cam
			# clear camera list
			self.cam_list.Clear()
			# release camera instance
			self.system.ReleaseInstance()
			return False

	def grab_right_image_by_trigger(self, cam, nodemap):
		self.grab_image_by_trigger(cam, nodemap, "right")

	def grab_left_image_by_trigger(self, cam, nodemap):
		self.grab_image_by_trigger(cam, nodemap, "left")

	def grab_top_image_by_trigger(self, cam, nodemap):
		self.grab_image_by_trigger(cam, nodemap, "top")

	def grab_bottom_image_by_trigger(self, cam, nodemap):
		self.grab_image_by_trigger(cam, nodemap, "bottom")

	def grab_image_by_trigger(self, cam, nodemap, side):
		"""
		This function acquires an image by executing the trigger node.

		:param cam: Camera to acquire images from.
		:param nodemap: Device nodemap.
		:type cam: CameraPtr
		:type nodemap: INodeMap
		:return: True if successful, False otherwise.
		:rtype: bool
		"""
		try:
			result = True
			# Use trigger to capture image
			# the camera captures a continuous stream of images.
			# When an image is retrieved, it is plucked from the stream.

			if self.triggerType == self.SOFTWARE:
				# Execute software trigger
				if side == "left":
					self.left_half()
				elif side == "right":
					self.right_half()
				elif side == "top":
					self.top_half()
				elif side == "bottom":
					self.bottom_half()

				node_softwaretrigger_cmd = PySpin.CCommandPtr(nodemap.GetNode('TriggerSoftware'))
				if not PySpin.IsAvailable(node_softwaretrigger_cmd) or not PySpin.IsWritable(node_softwaretrigger_cmd):
					print('Unable to execute trigger. Aborting...')
					return False

				node_softwaretrigger_cmd.Execute()


			elif self.triggerType == self.HARDWARE:
				print('Use the hardware to trigger image acquisition.')
				if side == "left":
					self.left_half()
				elif side == "right":
					self.right_half()
				elif side == "top":
					self.top_half()
				elif side == "bottom":
					self.bottom_half()

		except PySpin.SpinnakerException as ex:
			print('Error: %s' % ex)
			return False

		return result

	def grab_darkfield_image_by_trigger(self, cam, nodemap):
		"""
		This function acquires an image by executing the trigger node.

		:param cam: Camera to acquire images from.
		:param nodemap: Device nodemap.
		:type cam: CameraPtr
		:type nodemap: INodeMap
		:return: True if successful, False otherwise.
		:rtype: bool
		"""
		try:
			result = True
			# Use trigger to capture image
			# the camera captures a continuous stream of images.
			# When an image is retrieved, it is plucked from the stream.

			if self.triggerType == self.SOFTWARE:
				# Execute software trigger
				self.edges()
				node_softwaretrigger_cmd = PySpin.CCommandPtr(nodemap.GetNode('TriggerSoftware'))
				if not PySpin.IsAvailable(node_softwaretrigger_cmd) or not PySpin.IsWritable(node_softwaretrigger_cmd):
					print('Unable to execute trigger. Aborting...')
					return False

				node_softwaretrigger_cmd.Execute()

				# TODO: Blackfly and Flea3 GEV cameras need 2 second delay after software trigger

			elif self.triggerType == self.HARDWARE:
				print('Use the hardware to trigger image acquisition.')
				self.edges()

		except PySpin.SpinnakerException as ex:
			print('Error: %s' % ex)
			return False

		return result
	
	def saveFunc(self, image_result, filename):
		image_converted = image_result.Convert(PySpin.PixelFormat_Mono16)
		imageDataArray = image_converted.GetNDArray()
		filename = filename+'.tiff'

		# Save image
		cv2.imwrite(filename,imageDataArray)
		image = Image.open(filename)
		image.save(filename,"TIFF",compression=None)

		#  Release image
		image_result.Release()
