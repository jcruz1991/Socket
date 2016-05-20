# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import socket
import os
import sys
import subprocess 

def main():
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

	print("Commands: get <FILE NAME>, put <FILE NAME>, ls, lls, quit")
	# FTP raw inputs
	cmd = raw_input("ftp> ")	
	
	while cmd != "quit":

		dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		dataSock.bind(('',0))
		
		portNum_and_command = str(dataSock.getsockname()[serverAddr]) + data

		connSock.send(portNum_and_command)
		dataSock.listen(1)						
		
		dataConnection, address = dataSock.accept()			

		if(cmd == "get"):
			fileData = ""
			rcvBuff = ""
			fileSize = 0
			fSizeBuffer = (dataConnection, 10)
			fileSize = int(fSizeBuffer)

			print("The size of the received file is: ", fileSize)
			
			fileData = receiveFile(dataConnection, fileSize)
			print("The file name is: " + cmd[4:])

			file = open(data[4:], "w")
			file.write(fileData)			
			file.close()

		#elif(cmd == "put"):
			
		elif(cmd == "ls"):
			serverData = dataConnection.recv(9000)	
			print(serverData)

		#elif(cmd == "lls"):
			
		elif(cmd == "quit"):
			# Close the socket and the file
			connSock.close()

		else:
			dataSock.cloe()
			print(" ")
			print("Commands: get <FILE NAME>, put <FILE NAME>, ls, lls, quit")
			cmd = raw_input("ftp> ")
			
			

		# Make sure we did not hit EOF
		while len(cmd) > bytesSent:
			# Get the size of the data read
			# and convert it to string
			bytesSent += connSock.send(cmd[bytesSent:])
			print bytesSent
		bytesSent = 0
	
if __name__ == '__main__':
	main()
