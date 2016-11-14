import os
import netifaces
import socket

# read local nb default file #
with open('default_inputs.txt', 'r') as f:
    default_inputs = [x.strip('\n') for x in f.readlines()]

# 0. pi repo
# 1. pi usr
# 2. pi ip
# 3. pi_port

# 4. nb repo
# 5. nb usr
# 6. nb nw_if
# 7. nb ip
# 8. nb_port

# determine and write updated pi and nb properties to file
cwd = os.getcwd()

pi_repo = raw_input('Please enter your full pi git repo directory: [Enter for default]') or default_inputs[0]
pi_usr = 'pi'
pi_ip = raw_input('Please enter your pi ip address: (found at https://www.doc.ic.ac.uk/~jrj07/robotics/index.cgi via known MAC address) [Enter for default]')  or default_inputs[2]
pi_port = raw_input('Please enter your desired pi port for TCP communication: [Enter for default]') or default_inputs[3]

nb_repo = os.popen('git rev-parse --show-toplevel').read().replace('\n','')
nb_usr = os.popen('whoami').read().replace('\n','')
nb_nw_if = raw_input('Please enter your PC wireless network interface name: (found from ifconfig command) [Enter for default]') or default_inputs[6]
nb_ip = netifaces.ifaddresses(nb_nw_if)[2][0]['addr']
nb_port = raw_input('Please enter your desired PC port for TCP communication: [Enter for default]') or default_inputs[8]

default_inputs[0] = pi_repo + '\n'
default_inputs[1] = pi_usr  + '\n'
default_inputs[2] = pi_ip  + '\n'
default_inputs[3] = pi_port  + '\n'

default_inputs[4] = nb_repo  + '\n'
default_inputs[5] = nb_usr  + '\n'
default_inputs[6] = nb_nw_if  + '\n'
default_inputs[7] = nb_ip  + '\n'
default_inputs[8] = nb_port  + '\n'

f.close()

with open('default_inputs.txt', 'w') as file:
    file.writelines(default_inputs)
f.close()

print('scp default_inputs.txt ' +  pi_usr + '@' + pi_ip + ':' + pi_repo + cwd.replace(nb_repo,"") + '/default_inputs.txt')

# scp updates over to pi default file
print("updating default parameters on the pi...")
os.system('scp default_inputs.txt ' +  pi_usr + '@' + pi_ip + ':' + pi_repo + cwd.replace(nb_repo,"") + '/default_inputs.txt')
print("update complete")
dummy = raw_input("start pi PID application now, then AFTER it has started, press enter")

# send commands for robot to move
while True:
    packet = raw_input('Press enter to send another motor command: ') or 'motor_command'

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server and send data
    sock.connect((pi_ip, int(pi_port)))
    sock.sendall(packet)

    # Receive data from the server and shut down
    received = sock.recv(1024)

    sock.close()
    print "performing motor command"