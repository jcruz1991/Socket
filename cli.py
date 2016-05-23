import socket
import os
import sys

#Receives file from server
def recvAll(sock, numBytes):
	#Buffer for what has been received
	recvBuff = ""
	
	#Used to check if no data was received
	tempBuff = ""

	#get all data
	while len(recvBuff) < numBytes:		
		tempBuff = sock.recv(numBytes)
		
		#no data was received
		if not tempBuff:
			break
		
		#add to buffer size
		recvBuff += tempBuff

	return recvBuff

#Throw flag if user did not supply enough arguments
if (len(sys.argv) < 2):
	print "Usage python " + sys.argv[0] + "<FILE NAME>"

#Server addres
serverAddr = sys.argv[1]

#Server port
serverPort = sys.argv[2]

#Create a TCP Socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect to the server
connSock.connect((serverAddr, int(serverPort)))


print "Use commands: ls, get <FILE NAME>, put <FILE NAME>, or quit" 
print "\n"
cmd = raw_input("<ftp> ")

#separate input by spaces
cmd = cmd.split()

while (cmd[0] == "get" or cmd[0] == "put" or cmd[0] == "ls" or cmd[0] == "lls"):

	#open temporary data transfer connection
	cmdSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to port 0
	cmdSocket.bind(('',0))

	# Retreive the ephemeral port number
	ephemeralPort = cmdSocket.getsockname()[1]
	print "\n"


	if(cmd[0] == "get"):
		#Concatenate user command with ephemeral port number	
		cmdData = cmd[0] + " " + cmd[1] + " " + str(ephemeralPort)
		
		#Send that information to server through current connection
		connSock.send(cmdData)

		#listen for server's response		
		cmdSocket.listen(1)
			
		#accept the connection
		serverSocket, addr = cmdSocket.accept()
		print "Data transfer channel connection established. \n"

		#used to get content inside of the file
		fileData = ""
		
		#get and print size of the file		
		fileSize = 0
		fileSize = int(recvAll(serverSocket, 10))
		print "The size of the received file is: ", fileSize

		#get contents of the file
		fileData = recvAll(serverSocket, fileSize)
		
		#print name of the file
		print "The name of the received file is: " + cmd[1]
		
		#open and write the file data
		file = open(cmd[1], "w")
		file.write(fileData)
		
		#close the file
		file.close()

		#close data temporary transfer connection
		serverSocket.close()

		
	elif(cmd[0] == "ls"):
		#Concatenate user command with ephemeral port number	
		cmdData = cmd[0] + " " + str(ephemeralPort)
		
		#Send that information to server through current connection
		connSock.send(cmdData)	
	
		#Listen for server's response
		cmdSocket.listen(1)
		
		#Accept connection from server
		serverSocket, addr = cmdSocket.accept()
		print "Data transfer channel connection established. \n"
		
		#Server's response
		cmdResponse = serverSocket.recv(9000)
		print(cmdResponse)

		#Close temporary data connection
		serverSocket.close()
				
	cmd = raw_input("<ftp> ")
	cmd = cmd.split()
	print "\n"


connSock.close()
		
