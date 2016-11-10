import socket
import sys

HOST, PORT = "129.31.227.59", 9999
data = " ".join(sys.argv[1:])


while True :

	# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    	# Connect to server and send data
    	sock.connect((HOST, PORT))
    	sock.sendall(data + "\n")

    	# Receive data from the server and shut down
    	received = sock.recv(1024)

	print "Sent:     {}".format(data)
	print "Received: {}".format(received)

	sock.close()
