#!/usr/bin/env python

# The Keyboard Controller Node for the tutorial "Up and flying with the AR.Drone and ROS | Getting Started"
# https://github.com/mikehamer/ardrone_tutorials

# This controller extends the base DroneVideoDisplay class, adding a keypress handler to enable keyboard control of the drone

# Import the ROS libraries, and load the manifest file which through <depend package=... /> will give us access to the project dependencies
import roslib; roslib.load_manifest('ardrone_tutorials')
import rospy

# Load the DroneController class, which handles interactions with the drone, and the DroneVideoDisplay class, which handles video display
from drone_controller import BasicDroneController
from drone_video_display import DroneVideoDisplay
from ardrone_autonomy.msg import Navdata # for receiving navdata feedback
from geometry_msgs.msg import Pose #publish quadrotor state (velocity for every pose)

# Finally the GUI libraries
from PySide import QtCore, QtGui


# Here we define the keyboard map for our controller (note that python has no enums, so we use a class)
class KeyMapping(object):
	PitchForward     = QtCore.Qt.Key.Key_E
	PitchBackward    = QtCore.Qt.Key.Key_D
	RollLeft         = QtCore.Qt.Key.Key_S
	RollRight        = QtCore.Qt.Key.Key_F
	YawLeft          = QtCore.Qt.Key.Key_W
	YawRight         = QtCore.Qt.Key.Key_R
	IncreaseAltitude = QtCore.Qt.Key.Key_Q
	DecreaseAltitude = QtCore.Qt.Key.Key_A
	Takeoff          = QtCore.Qt.Key.Key_Y
	Land             = QtCore.Qt.Key.Key_H
	Emergency        = QtCore.Qt.Key.Key_Space


# Our controller definition, note that we extend the DroneVideoDisplay class
class KeyboardController(DroneVideoDisplay):
	def __init__(self):
		super(KeyboardController,self).__init__()
		
		self.rotX = 0
		self.rotY = 0
		self.rotZ = 0
		
		self.pitch = 0
		self.roll = 0
		self.yaw_velocity = 0 
		self.z_velocity = 0
		self.vel_max = 0.25
		self.subNavdata = rospy.Subscriber('/ardrone/navdata',Navdata,self.ReceiveNavdata) 
		self.pub = rospy.Publisher('/motion_model_data',Pose)
		
	def ReceiveNavdata(self,navdata):
	# Although there is a lot of data in this packet, we're only interested in the state at the moment	
		self.status = navdata.state
		self.rotX = navdata.rotX
		self.rotY = navdata.rotY
		self.rotZ = navdata.rotZ

# We add a keyboard handler to the DroneVideoDisplay to react to keypresses
	def keyPressEvent(self, event):
		key = event.key()

		# If we have constructed the drone controller and the key is not generated from an auto-repeating key
		if controller is not None and not event.isAutoRepeat():
			# Handle the important cases first!
			if key == KeyMapping.Emergency:
				controller.SendEmergency()
			elif key == KeyMapping.Takeoff:
				controller.SendTakeoff()
			elif key == KeyMapping.Land:
				controller.SendLand()
			else:
				# Now we handle moving, notice that this section is the opposite (+=) of the keyrelease section
				if key == KeyMapping.YawLeft:
					self.yaw_velocity += self.vel_max
				elif key == KeyMapping.YawRight:
					self.yaw_velocity += -self.vel_max

				elif key == KeyMapping.PitchForward:
					self.pitch += self.vel_max
				elif key == KeyMapping.PitchBackward:
					self.pitch += -self.vel_max

				elif key == KeyMapping.RollLeft:
					self.roll += self.vel_max
				elif key == KeyMapping.RollRight:
					self.roll += -self.vel_max

				elif key == KeyMapping.IncreaseAltitude:
					self.z_velocity += self.vel_max
				elif key == KeyMapping.DecreaseAltitude:
					self.z_velocity += -self.vel_max

			# finally we set the command to be sent. The controller handles sending this at regular intervals
			controller.SetCommand(self.roll, self.pitch, self.yaw_velocity, self.z_velocity)
			
			#Publish vx, vy, vz and actual angle - roll, pitch, yaw w.r.t world
			x = Pose()
			x.position.x = self.pitch
			x.position.y = self.roll
			x.position.z = self.z_velocity
			
			x.orientation.x = self.rotX
			x.orientation.y = self.rotY
			x.orientation.z = self.rotZ
			x.orientation.w = 0.0
			
			self.pub.publish(x)

	def keyReleaseEvent(self,event):
		key = event.key()

		# If we have constructed the drone controller and the key is not generated from an auto-repeating key
		if controller is not None and not event.isAutoRepeat():
			# Note that we don't handle the release of emergency/takeoff/landing keys here, there is no need.
			# Now we handle moving, notice that this section is the opposite (-=) of the keypress section
			if key == KeyMapping.YawLeft:
				self.yaw_velocity -= self.vel_max
			elif key == KeyMapping.YawRight:
				self.yaw_velocity -= -self.vel_max

			elif key == KeyMapping.PitchForward:
				self.pitch -= self.vel_max
			elif key == KeyMapping.PitchBackward:
				self.pitch -= -self.vel_max

			elif key == KeyMapping.RollLeft:
				self.roll -= self.vel_max
			elif key == KeyMapping.RollRight:
				self.roll -= -self.vel_max

			elif key == KeyMapping.IncreaseAltitude:
				self.z_velocity -= self.vel_max
			elif key == KeyMapping.DecreaseAltitude:
				self.z_velocity -= -self.vel_max

			# finally we set the command to be sent. The controller handles sending this at regular intervals
			controller.SetCommand(self.roll, self.pitch, self.yaw_velocity, self.z_velocity)



# Setup the application
if __name__=='__main__':
	import sys
	# Firstly we setup a ros node, so that we can communicate with the other packages
	rospy.init_node('ardrone_keyboard_controller')

	# Now we construct our Qt Application and associated controllers and windows
	app = QtGui.QApplication(sys.argv)
	controller = BasicDroneController()
	display = KeyboardController()

	display.show()

	# executes the QT application
	status = app.exec_()

	# and only progresses to here once the application has been shutdown
	rospy.signal_shutdown('Great Flying!')
	sys.exit(status)
