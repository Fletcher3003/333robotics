import brickpi
import time

import brickpi
import time

interface=brickpi.Interface()
interface.initialize()

port = 1 # port which ultrasonic sensor is plugged in to

interface.sensorEnable(port, brickpi.SensorType.SENSOR_ULTRASONIC);

motors = [0,1]

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParams = interface.MotorAngleControllerParameters()
motorParams.maxRotationAcceleration = 6.0
motorParams.maxRotationSpeed = 12.0
motorParams.feedForwardGain = 255/20.0
motorParams.minPWM = 18.0
motorParams.pidParameters.minOutput = -255
motorParams.pidParameters.maxOutput = 255
motorParams.pidParameters.k_p = 400
motorParams.pidParameters.k_i = 0
motorParams.pidParameters.k_d = 600

interface.setMotorAngleControllerParameters(motors[0],motorParams)
interface.setMotorAngleControllerParameters(motors[1],motorParams)


desiredDistance = 100;
gain = 0.1;

while True:
	usReading = interface.getSensorValue(port)
		
	if (!usReading) :
		print "US Sensor not Detected"
		interface.terminate()
	else:
		dis = usReading - desiredDistance

		speed = gain*dis
		interface.setMotorRotationSpeedReferences(motors,[speed,speed])

	time.sleep(0.05)

interface.terminate
