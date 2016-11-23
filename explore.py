import brickpi
import time
import math

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

global usPort = 1
interface.sensorEnable(usPort, brickpi.SensorType.SENSOR_ULTRASONIC);

global speed = 4.0
global rot16 = 1.3
global usOffset = 11

global map[]

global start_pos = [0,0,0]
global cur_pos = [0,0,0]

def scan
	ds = []
	for i in range(0,16):
		usReading = interface.getSensorValue(usPort)
		ds.append(usReading[0]+usOffset)	
		interface.increaseMotorAngleReferences(motors,[rot16,-rot16])
		while not interface.motorAngleReferencesReached(motors) :
			time.sleep(0.01)
	return ds

def move(angle)
	interface.increaseMotorAngleReferences(motors,[angle,angle])
	while not interface.motorAngleReferencesReached(motors) :
		time.sleep(0.01)

	dir = cur_pos[2] * math.pi * 0.125
	dis = angle * 2.6

	n_pos = [0,0,0]
	n_pos[0] = cur_pos[0] + (dis * math.sin(dir))
	n_pos[1] = cur_pos[1] + (dis * math.cos(dir))
	n_pos[2] = cur_pos[2]
	cur_pos = n_pos
	

def rotate(times)
	anticlockwise = False
	if times > 7
		anticlockwise = True
		points = 16-times
	
	if anticlockwise
		for i in range(0,points):
			interface.increaseMotorAngleReferences(motors,[-rot16,rot16])
			while not interface.motorAngleReferencesReached(motors) :
				time.sleep(0.01)
			n_pos = cur_pos + [0,0,-points]
			cur_pos = n_pos
	else
		for i in range(0,times):
			interface.increaseMotorAngleReferences(motors,[rot16,-rot16])
			while not interface.motorAngleReferencesReached(motors) :
				time.sleep(0.01)
			n_pos = cur_pos + [0,0,times]

def computeSurfel(dist)
	angle = cur_pos[2] * math.pi * 0.125
	
	s_pos = [0,0,angle]
	s_pos[0] = cur_pos[0] + (dist * math.sin(angle))
	s_pos[1] = cur_pos[1] + (dist * math.cos(angle))
	return s_pos
	

def explore
	print 'My Current Position is:'
	print cur_pos

	print 'Scanning Environment'

	readings = scan

	for i in range(0,16)
		n_surf = computeSurfel(readings[i])
		map.append(n_surf)
	
	empt = max(readings)
	dir = list.index(empt)
	
	rotate(dir)
	print 'Displaying Map'
	print map

while True
	explore()


