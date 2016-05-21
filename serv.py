 # *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************
import socket
import sys


# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""
	# The temporary buffer
	tmpBuff = ""
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		# The other side has closed the socket
		if not tmpBuff:
			break
		# Add the received bytes to the buffer
		recvBuff += tmpBuff

	return recvBuff

def sendFile(data, socket):
	#Server Address
	serverAddr = "localhost"

	fileName = data[9:]
	fileObj = open(fileName, "r")

	ephemeralSocket = int(data[:5])

	#Create the Socket
	dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dataSock.connect((serverAddr, ephemeralSocket))

	#Number of bytes sent
	numSent = 0

	fileData = None

	while True:
		#Read from fileObj
		fileData = fileObj.read(65536)
		if fileData:
			#Find length of fileData
			dataSizeStr = str(len(fileData))
			#Adds "0" to dataSizeStr if less than 10
			while len(dataSizeStr) < 10:
				dataSizeStr = "0" + dataSizeStr
			fileData = dataSizeStr + fileData
			numSent = 0
			#Keep sending until all is sent
			while len(fileData)> numSent:
				numSent += dataSock.send(fileData[numSent:])
		else:
			break

	dataSock.close()

def main():

	#Error checks is correct number of
	#arguments are passed
	if len(sys.argv) != 2:
		print("USAGE: python" + sys.argv[0] + "<Server Port>")
		exit()

	# The port on which to listen
	listenPort = int(sys.argv[1])

	# Create a welcome socket.
	welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Bind the socket to the port
	welcomeSock.bind(('', listenPort))
	# Start listening on the socket
	welcomeSock.listen(1)

	# Accept connections forever
	while True:
		print "Waiting for connections..."
		# Accept connections
		clientSock, addr = welcomeSock.accept()
		print "Accepted connection from client: ", addr
		print "\n"
		while True:
			data = clientSock.recv(1024)
			if data[0:2] == "ls":
				#CREATING A NEW DATA CONNECTION FOR DATA TRANSFER
				ephemeralSocket = int(data[3:])
				# Create a socket
				dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				# Bind the socket to port 0
				#dataSocket.bind(('',0))
				#Connection
				dataSocket.connect(("localhost", ephemeralSocket))
				#Gets output for ls
				data = subprocess.check_output(["ls"])
				#Sends back to client
				dataSocket.send(info)
				#Close socket
				dataSocket.close()
			#Checks if command is get
			elif data[5:8] == "get":
				sendFile(data,clientSock)

			#Checks if command is put
			elif data[5:8] == "put":
				#Create empermal socket
				ephemeralSocket = int(data[:5])
				dataSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				dataSocket = connect(("localhost", ephemeralSocket))
				# The buffer to all data received from the
				# the client.
				fileData = ""
				# The temporary buffer to store the received
				# data.
				recvBuff = ""
				# The size of the incoming file
				fileSize = 0
				# The buffer containing the file size
				ileSizeBuff = ""
				# Receive the first 10 bytes indicating the
				# size of the file
				fileSizeBuff = recvAll(clientSock, 10)
				# Get the file size
				fileSize = int(fileSizeBuff)
				print "The file size is ", fileSize
				#Get the file data
				fileData = recvAll(dataSock, fileSize)
				#Print fileData
				print fileData
				#Open file with write option
				file = open(data[9:], "w")
				#Write to file
				file.write(fileData)
				#Close the file
				file.close()

				#If input is quit
			elif data[0:4] == "quit":
				print("Connection closed...")
				break

		# Close our side
		clientSock.close()

#Open main file first
if __name__ == '__main__':
	main()
