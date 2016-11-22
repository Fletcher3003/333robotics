import brickpi
import time

interface=brickpi.Interface()
interface.initialize()

left_port = 3 # port which left touch sensor is plugged into
right_port = 2 # port which right touch sensor is plugged into

interface.sensorEnable(left_port, brickpi.SensorType.SENSOR_TOUCH);
interface.sensorEnable(right_port, brickpi.SensorType.SENSOR_TOUCH);

while True :
	lReading = interface.getSensorValue(left_port)
	rReading = interface.getSensorValue(right_port)

	if lReading :
		print 'Left '
		print lReading
	else:
		print "Failed Left Reading"

	if lReading :
		print 'Right '
		print rReading
	else:
		print "Failed Right Reading"

	time.sleep(0.05)

interface.terminate()
