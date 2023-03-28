from socket import *
import sys

if (len(sys.argv) <= 1):
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server'
    sys.exit(2)


def main():
    # Create a server socket, bind it to a port and start listening
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Prepare a sever socket
    serverPort = 6789
    serverSocket.bind(('localhost', serverPort))
    serverSocket.listen(1)

    try:
        connectionSocket, addr = serverSocket.accept()
    except timeout:
        print('Request timed out')
        sys.exit()

    while True:
        # Establish the connection
        print('Ready to serve...')

        clientSocket, addr = serverSocket.accept()

        print('Received a connection from: ', addr)
        message = clientSocket.recv(1024).decode()
        print(message)
        filename = message.split()[1].partition("/")[2]
        print(filename)
        fileExist = "false"
        filetouse = "/" + filename
        print(filetouse)
        try:
            # Check wether the file exist in the cache
            f = open(filetouse[1:], "r")
            outputdata = f.readlines()
            fileExist = "true"

            # ProxyServer finds a cache hit and generates a response message
            clientSocket.send("HTTP/1.0 200 OK\r\n")
            clientSocket.send("Content-Type:text/html\r\n")
            clientSocket.send(read(f))
            print('Read from cache')

        # Error handling for file not found in cache
        except IOError:
            if fileExist == "false":
                # Create a socket on the proxyserver   
                c = socket(AF_INET, SOCK_STREAM)


if __name__ == "__main__":
    main()