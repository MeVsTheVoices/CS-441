#import socket module 
from socket import * 
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket 
port = 6789
serverSocket.bind(("", port))
serverSocket.listen()

while True: 
    #Establish the connection 
    print('Ready to serve...') 
    connectionSocket, addr = serverSocket.accept()
    try:
        bufferSize = 4096
        message = connectionSocket.recv(bufferSize)
        filename = message.split()[1]
        print('getting file ', filename)

        f = open(filename[1:])                         
        outputdata = f.read()
        #Send one HTTP header line into socket 
        connectionSocket.send(b"HTTP/1.1 200 OK")
        #Send the content of the requested file to the client 
        #for i in range(0, len(outputdata)):            
        connectionSocket.send(outputdata.encode()) 
        connectionSocket.send("\r\n".encode()) 

        connectionSocket.close() 
    except IOError: 
    #Send response message for file not found 
        connectionSocket.send(b"HTTP/1.1 404 Not Found")
        connectionSocket.send(filename + ' was not in the folder the server is running in')
    #Close client socket 
    #Fill in start 
        connectionSocket.close()
    #Fill in end             
        serverSocket.close() 
        sys.exit()#Terminate the program after sending the corresponding data                                     