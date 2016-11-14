import os
import netifaces
import socket
import paramiko
from paramiko import SSHClient
from scp import SCPClient
import getpass
import pexpect
import matplotlib.pyplot
import numpy


# read local nb default file #
with open('default_inputs.txt', 'r') as f:
    default_inputs = [x.strip('\n') for x in f.readlines()]

# 0. pi repo
# 1. pi usr
# 2. pi pass
# 3. pi ip
# 4. pi_port

# 5. nb repo
# 6. nb usr
# 7. nb pass
# 8. nb nw_if
# 9. nb ip
# 10. nb_port

# determine and write updated pi and nb properties to file
cwd = os.getcwd()

pi_repo = raw_input('Please enter your full pi git repo directory: [Enter for default]') or default_inputs[0]
pi_usr = 'pi'
pi_pass = getpass.getpass('Please enter your pi password: [Enter for default]') or default_inputs[2]
pi_ip = raw_input('Please enter your pi ip address: (found at https://www.doc.ic.ac.uk/~jrj07/robotics/index.cgi via known MAC address) [Enter for default]')  or default_inputs[3]
pi_port = raw_input('Please enter your desired pi port for TCP communication: [Enter for default]') or default_inputs[4]

nb_repo = os.popen('git rev-parse --show-toplevel').read().replace('\n','')
nb_usr = os.popen('whoami').read().replace('\n','')
nb_pass = getpass.getpass('Please enter your pi password: [Enter for default]') or default_inputs[7]
nb_nw_if = raw_input('Please enter your PC wireless network interface name: (found from ifconfig command) [Enter for default]') or default_inputs[8]
nb_ip = netifaces.ifaddresses(nb_nw_if)[2][0]['addr']
nb_port = raw_input('Please enter your desired PC port for TCP communication: [Enter for default]') or default_inputs[10]

default_inputs[0] = pi_repo + '\n'
default_inputs[1] = pi_usr  + '\n'
default_inputs[2] = pi_pass  + '\n'
default_inputs[3] = pi_ip  + '\n'
default_inputs[4] = pi_port  + '\n'

default_inputs[5] = nb_repo  + '\n'
default_inputs[6] = nb_usr  + '\n'
default_inputs[7] = nb_pass  + '\n'
default_inputs[8] = nb_nw_if  + '\n'
default_inputs[9] = nb_ip  + '\n'
default_inputs[10] = nb_port  + '\n'

f.close()

with open('default_inputs.txt', 'w') as file:
    file.writelines(default_inputs)
f.close()

# scp updates over to pi default file
print("updating default parameters on the pi...")
scp = pexpect.spawn('scp default_inputs.txt ' +  pi_usr + '@' + pi_ip + ':' + pi_repo + cwd.replace(nb_repo,"") + '/default_inputs.txt')
scp.expect (pi_usr + '@' + pi_ip + "'s password: ")
scp.sendline (pi_pass)
print("update complete")
dummy = raw_input("start pi PID application now, then AFTER it has started, press enter")

# send commands for robot to move
while True:

    # send motor command signal #
    packet = raw_input('Press enter to send another motor command: ') or 'motor_command'
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to server and send data
    sock.connect((pi_ip, int(pi_port)))
    sock.sendall(packet)
    print "sending motor command"
    # Receive data from the server and shut down
    received = sock.recv(1024)
    print "motor command received"
    sock.close()

    # wait for LogFile-Complete signal #
    print "waiting for Logfile"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((nb_ip, int(nb_port)))
    sock.listen(1)
    conn, addr = sock.accept()
    while 1:
        data = conn.recv(1024)
        if not data: break
        conn.send(data)  # echo
    print "LogFile received!"
    conn.close()
    # LogFile has arrived!

    Data = numpy.loadtxt("LogFile.txt")
    matplotlib.pyplot.clf()
    matplotlib.pyplot.plot(Data[:, 0], Data[:, 1], 'r')
    matplotlib.pyplot.plot(Data[:, 0], Data[:, 2], 'b')
    matplotlib.pyplot.show()
