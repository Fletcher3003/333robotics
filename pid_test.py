import brickpi
import time

interface=brickpi.Interface()
interface.initialize()

motors = [0,1]
speed = 6.0

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

# Bad Practice
import params

# Map imported Parameters
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

interface.startLogging('pidtest.dat')
while True :
	angle = float(input("Enter an angle to rotate (in radians): "))
	
	interface.increaseMotorAngleReferences(motors,[angle,angle])
	
	while not interface.motorAngleReferencesReached(motors) :
		motorAngles = interface.getMotorAngles(motors)
		if motorAngles :
			print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
		time.sleep(0.1)
	
	print "Destination reached!"

interface.stopLogging()
interface.terminate()
