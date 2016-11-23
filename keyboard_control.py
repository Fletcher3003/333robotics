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

port = 1
interface.sensorEnable(port, brickpi.SensorType.SENSOR_ULTRASONIC);

#Commands:
#	w-Move Forward
#	a-Move Left
#	d-Move Right
#	s-Move Back
#	x-Stop

speed=1
incr=3.3


# Movement Commands
def fwd():
	interface.increaseMotorAngleReferences(motors,[speed, speed])

def left():
	interface.setMotorRotationSpeedReferences(motors,[0, 0])
	interface.increaseMotorAngleReferences(motors,[-incr,incr])
	
def right():
	interface.setMotorRotationSpeedReferences(motors,[0, 0])
	interface.increaseMotorAngleReferences(motors,[incr,-incr])

def back():
	interface.increaseMotorAngleReferences(motors,[-speed, -speed])

def stop():
	interface.setMotorRotationSpeedReferences(motors,[0, 0])

def acc(speed):
	nspeed = speed + 1.0
	return nspeed

def dec(speed):
	nspeed = speed - 1.0
	return nspeed

def sense():
	usReading = interface.getSensorValue(port)

	if usReading :
		print usReading
	else:
		print "Failed US reading"

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
	elif inp=='f':
		sense()
	elif inp=='q':
		speed = dec(speed)
		print speed
	elif inp=='e':
		speed = acc(speed)
		print speed
	time.sleep(.01)


