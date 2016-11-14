import brickpi # brickpi module
import time # time module
import os # os module

# INITIALISATION #
#----------------#

# initialise interface
interface=brickpi.Interface()
interface.initialize()

# set motor input ports
motors = [0,1]

# enable motors from specified ports
interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParams = interface.MotorAngleControllerParameters()
motorParams.maxRotationAcceleration = 6.0
motorParams.maxRotationSpeed = 12.0
motorParams.feedForwardGain = 255/20.0
motorParams.minPWM = 18.0
motorParams.pidParameters.minOutput = -255
motorParams.pidParameters.maxOutput = 255
motorParams.pidParameters.k_p = 100.0
motorParams.pidParameters.k_i = 0.0
motorParams.pidParameters.k_d = 0.0

interface.setMotorAngleControllerParameters(motors[0],motorParams)
interface.setMotorAngleControllerParameters(motors[1],motorParams)

while True:
	angle = float(input("Enter a angle to rotate (in radians): "))

	interface.startLogging("LogFile.txt")
	interface.increaseMotorAngleReferences(motors,[angle,angle])

	while not interface.motorAngleReferencesReached(motors) :
		motorAngles = interface.getMotorAngles(motors)
		if motorAngles :
			print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
		time.sleep(0.1)

	interface.stopLogging()

	os.system("scp LogFile.txt djl11@129.31.228.215:/home/djl11/Documents/BrickBot_Repo/BrickBot/Practical_1/LogFile.txt")

	print "Destination reached!"


interface.terminate()
