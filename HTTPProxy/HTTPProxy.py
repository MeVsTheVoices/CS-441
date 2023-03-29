from socket import *
import sys

if (len(sys.argv) <= 1):
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)


def main():
    # Create a server socket, bind it to a port and start listening
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Prepare a sever socket
    serverPort = 6789
    serverSocket.bind(('localhost', serverPort))
    serverSocket.listen(2)

    try:
        connectionSocket, addr = serverSocket.accept()
    except timeout:
        print('Request timed out')
        sys.exit()

    while True:
        # Establish the connection
        print('Ready to serve...')


        print('Received a connection from: ', addr)
        message = connectionSocket.recv(1024)
        print(message)
        filename = message.split()[1].partition("/".encode())[2]
        fileExist = "false"
        filetouse = "/" + filename.decode()
        print(filetouse)
        try:
            # Check wether the file exist in the cache
            f = open(filetouse[1:], "rb")
            outputdata = f.readlines()
            fileExist = "true"

            print(b"\r\n".join(outputdata))

            # ProxyServer finds a cache hit and generates a response message
            connectionSocket.send(b"HTTP/1.0 200 OK\r\n")
            connectionSocket.send(b"Content-Type:text/html\r\n")
            connectionSocket.send(b"\r\n".join(outputdata))
            print('Read from cache')

        # Error handling for file not found in cache
        except IOError:
            if fileExist == "false":
                # Create a socket on the proxyserver   
                c = socket(AF_INET, SOCK_STREAM)
                hostn = filename.replace("www.".encode(), "".encode(), 1)
                print(hostn)
                try:
                    c.connect((hostn, 80))
                    fileobj = c.makefile('rwb', 0)
                    fileobj.write(b"GET " + b"http://" + filename + b" HTTP/1.0\n\n")
                    # Read the response into buffer
                    buff = fileobj.readlines()
                    # Create a new file in the cache for the requested file.
                    # Also send the response in the buffer to client socket and the corresponding file in the cache
                    tmpFile = open("./" + filename.decode(), "wb")
                    for i in range(0, len(buff)):
                        tmpFile.write(buff[i])
                        connectionSocket.send(buff[i])
                    tmpFile.flush()
                    tmpFile.close()
                except Exception as e:
                    print("Illegal request ", e)
            else:
                # HTTP response message for file not found
                connectionSocket.send("HTTP/1.0 404 Not Found\r\n")
                connectionSocket.send("Content-Type:text/html\r\n")
                connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
    serverSocket.close()


if __name__ == "__main__":
    main()