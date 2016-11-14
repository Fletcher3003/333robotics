import os

# read local nb default file #
with open('default_inputs.txt') as f:
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
nb_repo = os.popen('git rev-parse --show-toplevel').read()
nb_usr = os.popen('whoami').read()
nb_nw_if = raw_input('Please enter your PC wireless network interface name: (found from ifconfig command) [Enter for default]') or default_inputs[6]
nb_ip = ni.ifaddresses(nb_nw_if)[2][0]['addr']
nb_port = pi_repo = ('Please enter your desired PC port for TCP communication: [Enter for default]') or default_inputs[8]

pi_repo = ('Please enter your full pi git repo directory: [Enter for default]') or default_inputs[0]
pi_usr = 'pi'
pi_ip = ('Please enter your pi ip address: (found at https://www.doc.ic.ac.uk/~jrj07/robotics/index.cgi via known MAC address) [Enter for default]')  or default_inputs[2]
pi_port = ('Please enter your desired pi port for TCP communication: [Enter for default]') or default_inputs[3]

default_inputs[0] = pi_repo
default_inputs[1] = pi_usr
default_inputs[2] = pi_ip
default_inputs[3] = pi_port

default_inputs[4] = nb_repo
default_inputs[5] = nb_usr
default_inputs[6] = nb_nw_if
default_inputs[7] = nb_ip
default_inputs[8] = nb_port

f.write(default_inputs)

# scp updates over to pi default file
os.system('scp default_inputs.txt ' +  pi_usr + '@' + pi_ip + ':' + pi_repo + cwd.replace(nb_repo,"") + 'default_inputs.txt')
print("start pi PID application now")
print("updating default data on pi...")
packet = 'scp performed'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((pi_ip, pi_port))
sock.sendall(packet)
received = sock.recv(1024)
sock.close()
print("update complete")


# send commands for robot to move
while true:
    packet = raw_input('Press enter to send another motor command: ') or ''

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server and send data
    sock.connect((pi_ip, pi_port))
    sock.sendall(packet)

    # Receive data from the server and shut down
    received = sock.recv(1024)

    sock.close()
    print "performing motor command"