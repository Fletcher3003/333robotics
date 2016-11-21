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
motorParams.pidParameters.minOutput = params.pidParameters.minOutput
motorParams.pidParameters.maxOutput = params.pidParameters.maxOutput
motorParams.pidParameters.k_p = params.pidParameters.k_p
motorParams.pidParameters.k_i = params.pidParameters.k_i
motorParams.pidParameters.k_d = params.pidParameters.k_d

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
	interface.setMotorRotationSpeedReferences(motors,[speed, -speed])
	
def right():
	interface.setMotorRotationSpeedReferences(motors,[-speed, speed])

def back():
	interface.setMotorRotationSpeedReferences(motors,[-speed, -speed])

def stop():
	interface.setMotorRotationSpeedReferences(motors,[0, 0])

speed=200
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
	time.sleep(.01)


