# Scan at 16 points around the robot and return sonar readings
import brickpi
import time

interface=brickpi.Interface()
interface.initialize()

motors = [0,1]

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

#Bad Practice
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

# Define a 22.5 degree rotation angle
rot_angle=1.65

for i in range(0,16):
	usReading = interface.getSensorValue(port)
	ds[i]= usReading[0]
	
	interface.increaseMotorAngleReferences(motors,[rot_angle,-rot_angle])

print ds
	
