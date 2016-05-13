# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import socket
import os
import sys

# Command line checks
if len(sys.argv) < 2:
	print "USAGE python " + sys.argv[0] + " <FILE NAME>"

# Server address
serverAddr = sys.argv[1]

# Server port
serverPort = int(sys.argv[2])

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))

# The number of bytes sent
bytesSent = 0

#size of socket client will be recieving
socketSize = 1024

# Keep sending until all is sent
while True:

	# FTP raw input
	cmd = raw_input("ftp> ")

	# Make sure we did not hit EOF
	while len(cmd) > bytesSent:
		# Get the size of the data read
		# and convert it to string
		bytesSent += connSock.send(cmd[bytesSent:])
		print bytesSent
	bytesSent = 0
	# Accept connections
	#servSock, addr = welcomeSock.accept()

	#recieve content from server
	#data = revc(sockSize)

#print "Sent ", bytesSent, " bytes."

# Close the socket and the file
connSock.close()
#SfileObj.close()
