#!/usr/bin/env python

# The Keyboard Controller Node for the tutorial "Up and flying with the AR.Drone and ROS | Getting Started"
# https://github.com/mikehamer/ardrone_tutorials

# This controller extends the base DroneVideoDisplay class, adding a keypress handler to enable keyboard control of the drone

# Import the ROS libraries, and load the manifest file which through <depend package=... /> will give us access to the project dependencies
import roslib; roslib.load_manifest('ardrone_tutorials')
import rospy
import time

# Load the DroneController class, which handles interactions with the drone, and the DroneVideoDisplay class, which handles video display
from drone_controller import BasicDroneController
from drone_video_display import DroneVideoDisplay

# Finally the GUI libraries
from PySide import QtCore, QtGui
roll = 0
pitch = 0
yaw_velocity = 0
z_velocity = 0

def helloWorld():
	time.sleep(2)
	controller.SendEmergency()
	time.sleep(2)
	controller.SendTakeoff()
	start = time.time()
	errorX = 0.5
	errorY = 0.5
	while(errorX >= 0.05):
		roll = 0
		pitch = errorX*0.5
		yaw_velocity = errorY*0.05
		z_velocity = 0
		controller.SetCommand(roll, pitch, yaw_velocity, z_velocity)
		t = time.time()
		errorX = errorX - errorX*(start-t)*1.3
		errorY = errorY - errorY*(start-t)*1.3
		start = t
		
	time.sleep(5)
	controller.SendLand()
	time.sleep(5)

# Setup the application
if __name__=='__main__':
	import sys
	# Firstly we setup a ros node, so that we can communicate with the other packages
	rospy.init_node('helloWorld')
	
	# Now we construct our Qt Application and associated controllers and windows
	#app = QtGui.QApplication(sys.argv)
	controller = BasicDroneController()
	
	helloWorld()

	# and only progresses to here once the application has been shutdown
	rospy.signal_shutdown('Great Flying!')
	#sys.exit(status)
