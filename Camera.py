###############################################################################
# Camera.py
# Author: Eddie Polanco, Tarek E. Moustafa, Thomas A. Zangle
# This is the first class that is written to function as a superclass for the
# Microscope class. Specifically, this is a superclass of the Microscope_v7 class.
# Changes from previous version: The interaction with the Time class and the LED
# has been removed. This is to make this class independent of other hardware on the
# microscope, so that it can be used with another PtGrey camera with few if any
# modifications to the code. Furthermore, it can continue to be used if we decide
# to change the light source in any way. Currently it works with an Adafruit
# LED array, but this code is now light source independent.
#
# This code is distributed under a creative commons attributable
# sharealike license. This license allows you to remix, adapt, and build 
# upon this work, as long as the authors are credited and the modified code
# is redistributed under the same license.
###############################################################################

import PySpin
import time
from PIL import Image
import cv2
import numpy

class Camera():

	def __init__(self):
		"""
		The camera is opened and initialized in this function and then deinitialized and closed at
		the end. The camera cannot be left open after the constructor, but can be left open after subsequent 
		function calls. This the purpose of the prepareTrigger() function is included, because after the  
		constructor sets up the camera, those settings persist when the camera is opened again. Therefore, 
		after the object has been created, the next function that should be called is prepareTrigger() in 
		order to reopen and reinitialize the camera in order for it to be triggered using the triggerCamera() 
		function. This class is most effective using the software trigger, unless a hardware trigger is well 
		timed with the illumination source. This class cannot be used to trigger the camera
		off the LED array which is why a class called microscope that inherits this camera function, will
		be used to interface the LED array with the camera in order to have the correct timing.

		The constructor power cycles the camera, causing the camera to reset to default settings
		every time an instance of the Camera class is created. The constructor then turns off the
		automatic settings (such as auto exposure time, frame rate, and gain) and then changes
		the settings to new default settings. The trigger is not turned on in the constructor, which is 
		why the prepareTrigger() function is necessary before taking an image.
		"""

		# result is true by default, and changes to false when an error is reached
		result = True
		self.SOFTWARE = 0
		self.HARDWARE = 1

		# Retrieve node (Enumeration node in this case)

		# Sets up system variable, must be released by constructor
		system = PySpin.System.GetInstance()

		# Get current version of pyspin
		version = system.GetLibraryVersion()
		print('Library version: %d.%d.%d.%d' % (version.major, version.minor, version.type, version.build))

		# Retrieve list of cameras from the system
		cam_list = system.GetCameras()

		num_cameras = cam_list.GetSize()

		print('Number of cameras detected: %d' % num_cameras)

		# Finish if there are no cameras

		if num_cameras == 0: # if no cameras, we should release everything that
		# needs to be released by the constructor

			# Clear camera list before releasing system
			cam_list.Clear()

			# Release system instance
			system.ReleaseInstance()

			print('Not enough cameras!')
			input('Done! Press Enter to exit...')
			return False

		for i, cam in enumerate(cam_list):

			# Retrieve TL device nodemap and print device information
			nodemap_tldevice = cam.GetTLDeviceNodeMap()

			result &= self.print_device_info(nodemap_tldevice)

			# Initialize camera
			cam.Init()

			# Retrieve GenICam nodemap
			nodemap = cam.GetNodeMap()

			# Restore Default settings

			node_usersetselector_mode = PySpin.CEnumerationPtr(nodemap.GetNode("UserSetSelector"))

			node_usersetselector_mode_default = node_usersetselector_mode.GetEntryByName("Default")

			node_usersetselector_mode.SetIntValue(node_usersetselector_mode_default.GetValue())

			# Retrieve node (command)
			node_iusersetload_cmd = PySpin.CCommandPtr(nodemap.GetNode("UserSetLoad"))

			# Execute command
			node_iusersetload_cmd.Execute()

			############################# Turn off auto gain ##############################

			node_gainauto_mode = PySpin.CEnumerationPtr(nodemap.GetNode("GainAuto"))

			# EnumEntry node (always associated with an Enumeration node)
			node_gainauto_mode_off = node_gainauto_mode.GetEntryByName("Off")

			# Turn off Auto Gain
			node_gainauto_mode.SetIntValue(node_gainauto_mode_off.GetValue())

			############################# Turn off auto framerate ##############################

			node_framerateauto_mode = PySpin.CEnumerationPtr(nodemap.GetNode("AcquisitionFrameRateAuto"))

			# # EnumEntry node (always associated with an Enumeration node)
			node_framerateauto_mode_off = node_framerateauto_mode.GetEntryByName("Off")

			# # Turn off Auto FrameRate
			node_framerateauto_mode.SetIntValue(node_framerateauto_mode_off.GetValue())

			############################# Turn off auto exposure ##############################

			node_exposureauto_mode = PySpin.CEnumerationPtr(nodemap.GetNode("pgrExposureCompensationAuto"))

			node_exposureauto_mode_off = node_exposureauto_mode.GetEntryByName("Off")

			node_exposureauto_mode.SetIntValue(node_exposureauto_mode_off.GetValue())

			# End of Default Settings "power-cycle"

			if cam.ExposureAuto.GetAccessMode() != PySpin.RW:
				print('Unable to disable automatic exposure. Aborting...')
				return False

			cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)
			print('Automatic exposure disabled...')

			node_framerate_float = PySpin.CFloatPtr(nodemap.GetNode("AcquisitionFrameRate"))

			# Set FrameRate to 17 Hz
			node_framerate_float.SetValue(17)

			# Set gain
			node_iGain_float = PySpin.CFloatPtr(nodemap.GetNode("Gain"))

			# Set gain to 15 dB
			node_iGain_float.SetValue(15)

			node_pixel_format = PySpin.CEnumerationPtr(nodemap.GetNode('PixelFormat'))
			if PySpin.IsAvailable(node_pixel_format) and PySpin.IsWritable(node_pixel_format):

				# Retrieve the desired entry node from the enumeration node
				node_pixel_format_mono16 = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName('Mono16'))
				if PySpin.IsAvailable(node_pixel_format_mono16) and PySpin.IsReadable(node_pixel_format_mono16):

					# Retrieve the integer value from the entry node
					pixel_format_mono16 = node_pixel_format_mono16.GetValue()

					# Set integer as new value for enumeration node
					node_pixel_format.SetIntValue(pixel_format_mono16)

					print('Pixel format set to %s...' % node_pixel_format.GetCurrentEntry().GetSymbolic())

				else:
					print('Pixel format mono 16 not available...')

			else:
				print('Pixel format not available...')

			# *** NOTES ***
			# Notice that the node is checked for availability and writability
			# prior to the setting of the node. In QuickSpin, availability and
			# writability are ensured by checking the access mode.
			#
			# Further, it is ensured that the desired exposure time does not exceed
			# the maximum. Exposure time is counted in microseconds - this can be
			# found out either by retrieving the unit with the GetUnit() method or
			# by checking SpinView.

			if cam.ExposureTime.GetAccessMode() != PySpin.RW:
				print('Unable to set exposure time. Aborting...')
				return False

			# Ensure desired exposure time does not exceed the maximum
			exposure_time_to_set = 50000.0
			# exposure_time_to_set = min(cam.ExposureTime.GetMax(), exposure_time_to_set)
			cam.ExposureTime.SetValue(exposure_time_to_set)

			# Configure custom image settings
			# self.configure_custom_image_settings(nodemap)
			try:
				# Set acquisition mode to continuous
				# In order to access the node entries, they have to be casted to a pointer type (CEnumerationPtr here)
				node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
				if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
					print('Unable to set acquisition mode to continuous (enum retrieval). Aborting...')
					return False

				# Retrieve entry node from enumeration node
				node_acquisition_mode_singleFrame = node_acquisition_mode.GetEntryByName('Continuous')
				if not PySpin.IsAvailable(node_acquisition_mode_singleFrame) or not PySpin.IsReadable(
						node_acquisition_mode_singleFrame):
						print('Unable to set acquisition mode to continuous (entry retrieval). Aborting...')
						return False

				# Retrieve integer value from entry node
				acquisition_mode_singleFrame = node_acquisition_mode_singleFrame.GetValue()

				# Set integer value from entry node as new value of enumeration node
				node_acquisition_mode.SetIntValue(acquisition_mode_singleFrame)

				device_serial_number = ''
				node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
				if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(node_device_serial_number):
					device_serial_number = node_device_serial_number.GetValue()
					print('Device serial number retrieved as %s...' % device_serial_number)

			except PySpin.SpinnakerException as ex:
				# if exception is thrown, catch by releasing system
				self.cam.EndAcquisition()
				self.cam.DeInit()
				del self.cam
				self.cam_list.Clear()
				self.system.ReleaseInstance()
				return False

		cam.DeInit()

		del cam

		cam_list.Clear()

		# Release system instance, instance must be released each time it is opened.
		system.ReleaseInstance()

	def prepareTrigger(self, triggerType):
		"""
		Prepares camera to receive a trigger to acquire a single image. This
		function must be run prior to running the triggerCam() function.
		Arguments:
			triggertype = 0: prepares camera to receive a software trigger
			triggertype = 1; prepares camera to receive a hardware trigger

		Note: The camera is not currently configured to receive a hardware trigger.

		Ex:
		prepareTrigger(0) # sets up camera to receive software trigger

		"""
		result = True
		if triggerType != 0 and triggerType != 1:
			triggerType = 0

		# triggerType is 0 for software triggers, and 1 for hardware triggers
		self.triggerType = triggerType
		self.system = PySpin.System.GetInstance()
		self.cam_list = self.system.GetCameras()
		num_cameras = self.cam_list.GetSize()
		for i, self.cam in enumerate(self.cam_list):
			# Initialize camera
			self.cam.Init()
			# Retrieve GenICam nodemap
			self.nodemap = self.cam.GetNodeMap()
			# configure trigger settings
			self.configure_trigger(self.cam)

			# # changes analog to digital conversion to a 12 bit image
			# self.cam.AdcBitDepth.SetValue(PySpin.AdcBitDepth_Bit12)
			# # changes pixel format to be 12 bits on the camera
			# self.cam.PixelFormat.SetValue(PySpin.PixelFormat_Mono12p)

			#  Begin acquiring images this should go here when using continuous
			#  acquisition mode.
			self.cam.BeginAcquisition()

		return True


	def changeExposureTime(self,exposure_time_to_set):
		self.cam.ExposureTime.SetValue(exposure_time_to_set)


	def setDarkfieldCameraSettings(self):
	
		# Ensure desired exposure time does not exceed the maximum
		exposure_time_to_set = 220000.0
		self.changeExposureTime(exposure_time_to_set)

	def setBrightfieldCameraSettings(self):
		# Ensure desired exposure time does not exceed the maximum
		exposure_time_to_set = 50000.0
		self.changeExposureTime(exposure_time_to_set)
	

	def triggerCam(self, filename):
		"""
		This is the trigger function for the camera. The camera is continuously streaming
		images, and when the trigger is received the camera will readout the image captured
		on the next exposure and then read it out and transfer the data to the computer. For a
		software trigger, the function just sends a command to the camera to activate the trigger.
		For a hardware trigger, the function instructs the camera to wait for a trigger, and then
		the function sends a TTL signal to the camera via the arduino that controls the LED array.
		We found that the software trigger is fast and reliable, so we have primarily been using the
		software trigger instead of the hardware trigger.
		"""
		try:


			result = True

			result &= self.grab_next_image_by_trigger(self.cam, self.nodemap)

			#  Retrieve next received image
			image_result = self.cam.GetNextImage()

			#  Ensure image completion
			if image_result.IsIncomplete():
				print('Image incomplete with image status %d ...' % image_result.GetImageStatus())

			else:

				image_converted = image_result.Convert(PySpin.PixelFormat_Mono16)
				imageDataArray = image_result.GetNDArray()
				mean = numpy.mean(numpy.mean(imageDataArray, axis = 0), axis = 0)

				filename = filename  + '.tiff'
				cv2.imwrite(filename,imageDataArray)
				image = Image.open(filename)
				image.save(filename,"TIFF",compression=None)
				print('Image saved at %s\n' % filename)
				#  Release image
				#
				#  *** NOTES ***
				#  Images retrieved directly from the camera (i.e. non-converted
				#  images) need to be released in order to keep from filling the
				#  buffer.
				image_result.Release()


		except PySpin.SpinnakerException as ex:
			self.cam.EndAcquisition()
			self.cam.DeInit()
			del self.cam
			self.cam_list.Clear()
			self.system.ReleaseInstance()
			return False

	def grab_next_image_by_trigger(self, cam, nodemap):

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
			# The software trigger only feigns being executed by the Enter key;
			# what might not be immediately apparent is that there is not a
			# continuous stream of images being captured; in other examples that
			# acquire images, the camera captures a continuous stream of images.
			# When an image is retrieved, it is plucked from the stream.

			if self.triggerType == self.SOFTWARE:
				# Execute software trigger
				node_softwaretrigger_cmd = PySpin.CCommandPtr(nodemap.GetNode('TriggerSoftware'))
				if not PySpin.IsAvailable(node_softwaretrigger_cmd) or not PySpin.IsWritable(node_softwaretrigger_cmd):
					print('Unable to execute trigger. Aborting...')
					return False

				node_softwaretrigger_cmd.Execute()

			elif self.triggerType == self.HARDWARE:
				print('Use the hardware to trigger image acquisition.')

		except PySpin.SpinnakerException as ex:
			print('Error: %s' % ex)
			return False

		return result

	def configure_trigger(self, cam):
		"""
		This function configures the camera to use a trigger. First, trigger mode is
		set to off in order to select the trigger source. Once the trigger source
		has been selected, trigger mode is then enabled, which has the camera
		capture only a single image upon the execution of the chosen trigger.

		 :param cam: Camera to configure trigger for.
		 :type cam: CameraPtr
		 :return: True if successful, False otherwise.
		 :rtype: bool
		"""

		result = True

		print('*** CONFIGURING TRIGGER ***\n')

		if self.triggerType == self.SOFTWARE:
			print('Software trigger chosen ...')
		elif self.triggerType == self.HARDWARE:
			print('Hardware trigger chosen ...')


		try:
			# Ensure trigger mode off
			# The trigger must be disabled in order to configure whether the source
			# is software or hardware.
			nodemap = cam.GetNodeMap()
			node_trigger_mode = PySpin.CEnumerationPtr(nodemap.GetNode('TriggerMode'))
			if not PySpin.IsAvailable(node_trigger_mode) or not PySpin.IsReadable(node_trigger_mode):
				print('Unable to disable trigger mode (node retrieval). Aborting...')
				return False

			node_trigger_mode_off = node_trigger_mode.GetEntryByName('Off')
			if not PySpin.IsAvailable(node_trigger_mode_off) or not PySpin.IsReadable(node_trigger_mode_off):
				print('Unable to disable trigger mode (enum entry retrieval). Aborting...')
				return False

			node_trigger_mode.SetIntValue(node_trigger_mode_off.GetValue())

			print('Trigger mode disabled...')

			# Select trigger source
			# The trigger source must be set to hardware or software while trigger
			# mode is off.
			node_trigger_source = PySpin.CEnumerationPtr(nodemap.GetNode('TriggerSource'))
			if not PySpin.IsAvailable(node_trigger_source) or not PySpin.IsWritable(node_trigger_source):
				print('Unable to get trigger source (node retrieval). Aborting...')
				return False

			if self.triggerType == self.SOFTWARE:
				node_trigger_source_software = node_trigger_source.GetEntryByName('Software')
				if not PySpin.IsAvailable(node_trigger_source_software) or not PySpin.IsReadable(
						node_trigger_source_software):
					print('Unable to set trigger source (enum entry retrieval). Aborting...')
					return False
				node_trigger_source.SetIntValue(node_trigger_source_software.GetValue())

			elif self.triggerType == self.HARDWARE:
				node_trigger_source_hardware = node_trigger_source.GetEntryByName('Line0')
				if not PySpin.IsAvailable(node_trigger_source_hardware) or not PySpin.IsReadable(
						node_trigger_source_hardware):
					print('Unable to set trigger source (enum entry retrieval). Aborting...')
					return False
				node_trigger_source.SetIntValue(node_trigger_source_hardware.GetValue())

			# Turn trigger mode on
			# Once the appropriate trigger source has been set, turn trigger mode
			# on in order to retrieve images using the trigger.
			node_trigger_mode_on = node_trigger_mode.GetEntryByName('On')
			if not PySpin.IsAvailable(node_trigger_mode_on) or not PySpin.IsReadable(node_trigger_mode_on):
				print('Unable to enable trigger mode (enum entry retrieval). Aborting...')
				return False

			node_trigger_mode.SetIntValue(node_trigger_mode_on.GetValue())
			print('Trigger mode turned back on...')

		except PySpin.SpinnakerException as ex:
			print('Error: %s' % ex)
			return False

		return result




	def configure_custom_image_settings(self, nodemap):
		"""
		Configures a number of settings on the camera including offsets  X and Y, width,
		height, and pixel format. These settings must be applied before BeginAcquisition()
		is called; otherwise, they will be read only. Also, it is important to note that
		settings are applied immediately. This means if you plan to reduce the width and
		move the x offset accordingly, you need to apply such changes in the appropriate order.

		:param nodemap: GenICam nodemap.
		:type nodemap: INodeMap
		:return: True if successful, False otherwise.
		:rtype: bool
		"""
		print('\n*** CONFIGURING CUSTOM IMAGE SETTINGS *** \n')

		try:
			result = True

			# Apply mono 8 pixel format
			#
			# *** NOTES ***
			# Enumeration nodes are slightly more complicated to set than other
			# nodes. This is because setting an enumeration node requires working
			# with two nodes instead of the usual one.
			#
			# As such, there are a number of steps to setting an enumeration node:
			# retrieve the enumeration node from the nodemap, retrieve the desired
			# entry node from the enumeration node, retrieve the integer value from
			# the entry node, and set the new value of the enumeration node with
			# the integer value from the entry node.
			#
			# Retrieve the enumeration node from the nodemap
			node_pixel_format = PySpin.CEnumerationPtr(nodemap.GetNode('PixelFormat'))
			if PySpin.IsAvailable(node_pixel_format) and PySpin.IsWritable(node_pixel_format):

				# Retrieve the desired entry node from the enumeration node
				node_pixel_format_mono8 = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName('Mono8'))
				if PySpin.IsAvailable(node_pixel_format_mono8) and PySpin.IsReadable(node_pixel_format_mono8):

					# Retrieve the integer value from the entry node
					pixel_format_mono8 = node_pixel_format_mono8.GetValue()

					# Set integer as new value for enumeration node
					node_pixel_format.SetIntValue(pixel_format_mono8)

					print('Pixel format set to %s...' % node_pixel_format.GetCurrentEntry().GetSymbolic())

				else:
					print('Pixel format mono 8 not available...')

			else:
				print('Pixel format not available...')

			# Apply minimum to offset X
			#
			# *** NOTES ***
			# Numeric nodes have both a minimum and maximum. A minimum is retrieved
			# with the method GetMin(). Sometimes it can be important to check
			# minimums to ensure that your desired value is within range.
			node_offset_x = PySpin.CIntegerPtr(nodemap.GetNode('OffsetX'))
			if PySpin.IsAvailable(node_offset_x) and PySpin.IsWritable(node_offset_x):

				node_offset_x.SetValue(node_offset_x.GetMin())
				print('Offset X set to %i...' % node_offset_x.GetMin())

			else:
				print('Offset X not available...')

			# Apply minimum to offset Y
			#
			# *** NOTES ***
			# It is often desirable to check the increment as well. The increment
			# is a number of which a desired value must be a multiple of. Certain
			# nodes, such as those corresponding to offsets X and Y, have an
			# increment of 1, which basically means that any value within range
			# is appropriate. The increment is retrieved with the method GetInc().
			node_offset_y = PySpin.CIntegerPtr(nodemap.GetNode('OffsetY'))
			if PySpin.IsAvailable(node_offset_y) and PySpin.IsWritable(node_offset_y):

				node_offset_y.SetValue(node_offset_y.GetMin())
				print('Offset Y set to %i...' % node_offset_y.GetMin())

			else:
				print('Offset Y not available...')

			# Set maximum width
			#
			# *** NOTES ***
			# Other nodes, such as those corresponding to image width and height,
			# might have an increment other than 1. In these cases, it can be
			# important to check that the desired value is a multiple of the
			# increment. However, as these values are being set to the maximum,
			# there is no reason to check against the increment.
			node_width = PySpin.CIntegerPtr(nodemap.GetNode('Width'))
			if PySpin.IsAvailable(node_width) and PySpin.IsWritable(node_width):

				width_to_set = node_width.GetMax()
				node_width.SetValue(width_to_set)
				print('Width set to %i...' % node_width.GetValue())

			else:
				print('Width not available...')

			# Set maximum height
			#
			# *** NOTES ***
			# A maximum is retrieved with the method GetMax(). A node's minimum and
			# maximum should always be a multiple of its increment.
			node_height = PySpin.CIntegerPtr(nodemap.GetNode('Height'))
			if PySpin.IsAvailable(node_height) and PySpin.IsWritable(node_height):

				height_to_set = node_height.GetMax()
				node_height.SetValue(height_to_set)
				print('Height set to %i...' % node_height.GetValue())

			else:
				print('Height not available...')

		except PySpin.SpinnakerException as ex:
			print('Error: %s' % ex)
			return False

		return result


	def print_device_info(self, nodemap):
		"""
		This function prints the device information of the camera from the transport
		layer; please see NodeMapInfo example for more in-depth comments on printing
		device information from the nodemap.

		:param nodemap: Transport layer device nodemap.
		:type nodemap: INodeMap
		:returns: True if successful, False otherwise.
		:rtype: bool
		"""

		print('*** DEVICE INFORMATION ***\n')

		try:
			result = True
			node_device_information = PySpin.CCategoryPtr(nodemap.GetNode('DeviceInformation'))

			if PySpin.IsAvailable(node_device_information) and PySpin.IsReadable(node_device_information):
				features = node_device_information.GetFeatures()
				for feature in features:
					node_feature = PySpin.CValuePtr(feature)
					print('%s: %s' % (node_feature.GetName(),
									  node_feature.ToString() if PySpin.IsReadable(node_feature) else 'Node not readable'))

			else:
				print('Device control information not available.')

		except PySpin.SpinnakerException as ex:
			print('Error: %s' % ex)
			return False

		return result

	def closeCamera(self):
		"""
		The camera runs in continuous acquisition mode in order to obtain the fastest
		framerate possible. Therefore, it is necessary to close the camera when finished
		with it, because the camera is continuously streaming images and then when a trigger
		is sent the camera reads out the next image acquired and transfers the data to
		the computer. Therefore, when you are finished with the Camera, it must be closed
		prior to disconnecting it.

		"""
		nodemap = self.cam.GetNodeMap()
		node_trigger_mode = PySpin.CEnumerationPtr(nodemap.GetNode('TriggerMode'))
		if not PySpin.IsAvailable(node_trigger_mode) or not PySpin.IsReadable(node_trigger_mode):
			print('Unable to disable trigger mode (node retrieval). Aborting...')
			return False

		node_trigger_mode_off = node_trigger_mode.GetEntryByName('Off')
		if not PySpin.IsAvailable(node_trigger_mode_off) or not PySpin.IsReadable(node_trigger_mode_off):
			print('Unable to disable trigger mode (enum entry retrieval). Aborting...')
			return False

		node_trigger_mode.SetIntValue(node_trigger_mode_off.GetValue())

		print('Trigger mode disabled...')

		self.cam.EndAcquisition()
		self.cam.DeInit()
		del self.cam
		self.cam_list.Clear()
		self.system.ReleaseInstance()
