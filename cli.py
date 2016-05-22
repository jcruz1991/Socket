import socket
import os
import sys

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



while (cmd == "get" or cmd == "put" or cmd == "ls" or cmd == "lls"):
	
	cmdSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to port 0
	cmdSocket.bind(('',0))

	# Retreive the ephemeral port number
	ephemeralPort = cmdSocket.getsockname()[1]
	print "\n"
		
	#Concatenate user command with ephemeral port number	
	cmdData = cmd + " " + str(ephemeralPort)
		
	#Send that information to server through current connection
	connSock.send(cmdData)


	#if(cms == "get"):
	
	if(cmd == "ls"):
	
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
	print "\n"


connSock.close()
		
