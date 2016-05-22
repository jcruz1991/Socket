 # *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************
import socket
import sys
import commands

#Throw flag if user does not send two arguments
if len(sys.argv) != 2:
	print "USAGE: python " + sys.argv[0] + " <Server Port>"
	exit()

#Listen port number
listenPort  = int(sys.argv[1])

#Connect to socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind to specidied port
connSock.bind(('', listenPort))

#Listen for connections
connSock.listen(1)

#Leave connection open
while True:
	print "Waiting for connections:"
	
	#Accept conection
	clientSock, addr = connSock.accept()
	
	#Print client address
	print "Accepted from client: ", addr
	print "\n"

	#Case for second connections
	while True:
		#Take in client's command and ephemeral port number
		cmd = clientSock.recv(1024)
		
		#If cmd is blank, jump out of loop		
		if (len(cmd) == 0):
			break
		
		#Parse string to list
		cmd = cmd.split()
		
		#Client specified "get"		
		if(cmd[0] == "get"):
			print "get"

		#Client specified "put"		
		if(cmd[0] == "put"):
			print "put"	
	
		#Client specified "ls"
		if(cmd[0] == "ls"):
			ephemeralPort = int(cmd[1])
			dataTransmitter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			dataTransmitter.connect(("localhost", ephemeralPort))	

			for line in commands.getstatusoutput('ls -l'):
				dataTransmitter.send(str(line))
				
			dataTransmitter.close()

		#Client specified "lls"
		if(cmd[0] == "lls"):
			print "lls"


def recvAll(sock, numBytes):
	recvBuff = ""
	
	tempBuff = ""

	while len(recvBuff) < numBytes:
		tempBuff = sock.recv(numBytes)

		if not tempBuff:
			break

		recvBuff += tempBuff
	return revBuff


