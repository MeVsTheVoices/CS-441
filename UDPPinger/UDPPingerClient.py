import socket
import time

serverAddress = ['localhost', 12000]

pingSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pingSocket.settimeout(1)

try:
    for i in range(10):
        initialTimestamp = time.time()
        message = "Ping " + str(i + 1) + " " + time.strftime("%H:%M:%S")
        pingSocket.sendto(message.encode(), tuple(serverAddress))
        try:
            data, server = pingSocket.recvfrom(1024)
            finalTimestamp = time.time()
            elapsed = finalTimestamp - initialTimestamp
            print ("Elapsed (", elapsed, " seconds), data(", data.decode(), ")")
        except socket.timeout:
            print ("Request timed out.")
        except KeyboardInterrupt:
            print ("KeyboardInterrupt")
            break
finally:
    pingSocket.close()