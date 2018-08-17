from socket import *
import time

servername='127.0.0.1'
serverport= 12000
clientSocket=socket(AF_INET,SOCK_DGRAM)
clientSocket.settimeout(1)

for i in range(1,11):
    t0=time.time()
    clientSocket.sendto(('Ping %d %s' % (i,t0)).encode(), (servername,serverport))
    try:
        modifiedMessage,serveraddress=clientSocket.recvfrom(1024)
        total_time=time.time()-t0
        print('%d: response by %s   RTT=%.3f'%(i,servername,total_time))

    except Exception as e:
        print('%d: time out!' %i)
clientSocket.close()

