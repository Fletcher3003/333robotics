import brickpi
import time

interface=brickpi.Interface()
interface.initialize()

motors = [0,1]

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

# Bad Practice
import params

motorParams=interface.MotorAngleControllerParameters()
motorParams.maxRotationAcceleration = params.maxRotationAcceleration
motorParams.maxRotationSpeed = params.maxRotationSpeed
motorParams.feedForwardGain = params.feedForwardGain
motorParams.minPWM = params.minPWM
motorParams.pidParameters.minOutput = params.minOutput
motorParams.pidParameters.maxOutput = params.maxOutput
motorParams.pidParameters.k_p = params.k_p
motorParams.pidParameters.k_i = params.k_i
motorParams.pidParameters.k_d = params.k_d

interface.setMotorAngleControllerParameters(motors[0],motorParams)
interface.setMotorAngleControllerParameters(motors[1],motorParams)

#Commands:
#	w-Move Forward
#	a-Move Left
#	d-Move Right
#	s-Move Back
#	x-Stop

# Movement Commands
def fwd():
	interface.setMotorRotationSpeedReferences(motors,[speed, speed])

def left():
	interface.setMotorRotationSpeedReferences(motors,[speed/2, -speed/2])
	
def right():
	interface.setMotorRotationSpeedReferences(motors,[-speed/2, speed/2])

def back():
	interface.setMotorRotationSpeedReferences(motors,[-speed, -speed])

def stop():
	interface.setMotorRotationSpeedReferences(motors,[0, 0])

def acc():
	speed = speed + 25

def dec():
	speed = speed - 25

speed=100
while True:
	inp=str(raw_input())
	#Move Robot
	if inp=='w':
		fwd()
	elif inp=='a':
		left()
	elif inp=='d':
		right()
	elif inp=='s':
		back()
	elif inp=='x':
		stop()
	elif inp=='q':
		dec()
	elif inp=='e':
		acc()
	time.sleep(.01)


