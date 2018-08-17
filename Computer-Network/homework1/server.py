#import socket module
from socket import *
serversocket=socket(AF_INET, SOCK_STREAM)


#prepare a server socket

serversocket.bind(('',6789))
serversocket.listen(1)
while True:
    print('Ready to serve...')
    connectionSocket,addr=serversocket.accept()
    try:
        message=connectionSocket.recv(1024)
        filename=message.split()[1]
        f=open(filename[1:])
        outputdata=f.read()
        header = ' HTTP/1.1 200 OK\nConnection: close\nContent-Type: text/html\nContent-Length: %d\n\n' % (len(outputdata))
        connectionSocket.send(header.encode())
        for i in range(len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()
    except IOError:
        connectionSocket.send("HTTP/1.1 404 Found".encode())
        connectionSocket.close()
serversocket.close()
