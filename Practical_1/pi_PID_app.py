import brickpi # brickpi module
import time # time module
import socket
import os
import pexpect

# INITIALISATION #
#----------------#

# read recently scp'ed default file #
with open('default_inputs.txt') as f:
    default_inputs = [x.strip('\n') for x in f.readlines()]

cwd = os.getcwd()

pi_repo = default_inputs[0]
pi_usr = default_inputs[1]
pi_pass = default_inputs[2]
pi_ip = default_inputs[3]
pi_port = default_inputs[4]

nb_repo = default_inputs[5]
nb_usr = default_inputs[6]
nb_pass = default_inputs[7]
nb_nw_if = default_inputs[8]
nb_ip = default_inputs[9]
nb_port = default_inputs[10]

# tcp connection
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

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
    # wait until motor command arrives
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((pi_ip, int(pi_port)))
    sock.listen(1)

    conn, addr = sock.accept()
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        conn.send(data)  # echo
    conn.close()
    # command has arrived!

    interface.startLogging("LogFile.txt")
    interface.increaseMotorAngleReferences(motors,[10,10])

    while not interface.motorAngleReferencesReached(motors) :
	motorAngles = interface.getMotorAngles(motors)
	if motorAngles :
		print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
	time.sleep(0.1)

    interface.stopLogging()

    scp = pexpect.spawn('scp LogFile.txt ' + nb_usr + '@' + nb_ip + ':' + nb_repo + cwd.replace(pi_repo,'') + '/LogFile.txt')
    scp.expect(nb_usr + '@' + nb_ip + "'s password: ")
    scp.sendline(nb_pass)

    # send LogFile Complete signal #
    packet = 1
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to server and send data
    sock.connect((pi_ip, int(pi_port)))
    sock.sendall(packet)
    print "sending LogFile"
    # Receive data from the server and shut down
    received = sock.recv(1024)
    print "LogFile Sent!"
    sock.close()

interface.terminate()
