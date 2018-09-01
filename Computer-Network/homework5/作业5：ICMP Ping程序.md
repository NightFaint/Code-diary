# 套接字编程作业5：ICMP Ping程序

## 作业描述

  在这个作业中，您将更好地理解因特网控制报文协议（ICMP）。您会学习使用ICMP请求和响应消息实现Ping程序。 Ping是一个网络应用程序，用于测试某个主机在IP网络中是否可访问。它也用于测试计算机的网卡或测试网络延迟。它通过向目标主机发送ICMP“回显”包并监听ICMP“回显”应答来工作。“回显”有时称为"pong"。ping程序测量往返时间，记录数据包丢失，并输出接收到的回显包的统计摘要（往返时间的最小值、最大值和平均值，以及在某些版本中的平均值的标准差）。 您的任务是用python开发自己的Ping程序。您的程序将使用ICMP，但为了保持简单，将不完全遵循RFC 1739中的正式规范。请注意，您只需要编写程序的客户端，因为服务器端所需的功能几乎内置于所有操作系统中。 您的Ping程序能将ping请求发送到指定的主机，间隔大约一秒钟。每个消息包含一个带有时间戳的数据包。每个数据包发送完后，程序最多等待一秒，用于接收响应。如果一秒后服务器没有响应，那么客户端应假设ping数据包或pong数据包在网络中丢失（或者服务器已关闭）。
  
## 详细描述
[Socket5_ICMPpinger(chap4)](Socket5_ICMPpinger(chap4).pdf)

## 代码

    import socket
    import os
    import sys
    import struct
    import time
    import select
    import binascii

    ICMP_ECHO_REQUEST = 8



    def checksum(str):
        csum = 0
        countTo = (len(str) / 2) * 2
        count = 0
        while count < countTo:
            thisVal =  str[count + 1] * 256 + str[count]
            csum = csum + thisVal
            csum = csum & 0xffffffff
            count = count + 2

        if countTo < len(str):
            csum = csum + ord(str[len(str) - 1])
            csum = csum & 0xffffffff

        csum = (csum >> 16) + (csum & 0xffff)
        csum = csum + (csum >> 16)
        answer = ~csum
        answer = answer & 0xffff
        answer = answer >> 8 | (answer << 8 & 0xff00)
        return answer

    def receiveOnePing(mySocket, ID, timeout, destAddr):
        global rtt_min, rtt_max, rtt_sum, rtt_cnt
        timeLeft = timeout

        while 1:
            startedSelect = time.time()
            whatReady = select.select([mySocket], [], [], timeLeft)
            howLongInSelect = (time.time() - startedSelect)
            if whatReady[0] == []: # Timeout
                return "Request timed out."

            timeReceived = time.time()
            recPacket, addr = mySocket.recvfrom(1024)

            #Fill in start

            #Fetch the ICMP header from the IP packet
            icmpheader=recPacket[20:28] #ICMP报文首部在ip数据报的第20字节到27字节共八字节，前20字节是ip首部
            type,code,checksum,id,seq=struct.unpack('bbHHh',icmpheader)#按格式解压，!表示是网络的大端存储，b表示signed char，1个字节，
                                                                                      #H表示unsigned short，两个字节，h表示signed short，两字节。
                                                                                      #而icmp报文首部格式:类型(1个字节)，代码（1个字节)，检验和(两个字节)
                                                                                      #ID号(两个字节)，序号（两字节）
            # 回返报文的type=0,code=0,id=ID
            if type !=0:
                return 'expected type=0,but got {}'.format(type)
            if code != 0:
                return "expect code=0,but got {}".format(code)
            if ID != id:
                return 'expected id ={},but got {]'.format(ID,id)
            send_time, = struct.unpack('d',recPacket[28:])

            rtt=(timeReceived-send_time)*1000
            rtt_cnt+=1
            rtt_sum+=rtt
            rtt_min=min(rtt_min,rtt)
            rtt_max=max(rtt_max,rtt)

            ip_header=struct.unpack('!BBHHHBBH4s4s',recPacket[:20])
            ttl=ip_header[5]
            saddr=socket.inet_ntoa(ip_header[8])
            length=len(recPacket)-20

            return '{} bytes from {}:icmp_seq={} ttl={} time={:.3f} ms'.format(length,saddr,seq,ttl,rtt)
            #Fill in end

            timeLeft = timeLeft - howLongInSelect
            if timeLeft <= 0:
              return "Request timed out."

    def sendOnePing(mySocket, destAddr, ID):
        # Header is type (8), code (8), checksum (16), id (16), sequence (16)

        myChecksum = 0
        # Make a dummy header with a 0 checksum.
        # struct -- Interpret strings as packed binary data
        header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
        data = struct.pack("d", time.time())
        # Calculate the checksum on the data and the dummy header.
        myChecksum = checksum(header + data)

        # Get the right checksum, and put in the header
        if sys.platform == 'darwin':
            myChecksum = socket.htons(myChecksum) & 0xffff
            #Convert 16-bit integers from host to network byte order.
        else:
            myChecksum = socket.htons(myChecksum)

        header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
        packet = header + data

        mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
        #Both LISTS and TUPLES consist of a number of objects
        #which can be referenced by their position number within the object

    def doOnePing(destAddr, timeout):
        icmp = socket.getprotobyname("icmp")

        #SOCK_RAW is a powerful socket type. For more details see: http://sock-raw.org/papers/sock_raw

        #Fill in start

        #Create Socket here
        mySocket=socket.socket(socket.AF_INET,socket.SOCK_RAW,icmp)

        #Fill in end

        myID = os.getpid() & 0xFFFF #Return the current process i
        sendOnePing(mySocket, destAddr, myID)
        delay = receiveOnePing(mySocket, myID, timeout, destAddr)

        mySocket.close()
        return delay

    def ping(host, timeout=1):
        #timeout=1 means: If one second goes by without a reply from the server,
        #the client assumes that either the client’s ping or the server’s pong is lost
        global rtt_min,rtt_max,rtt_sum,rtt_cnt
        rtt_min=float('+inf')
        rtt_max=float('-inf')
        rtt_cnt=0
        rtt_sum=0
        cnt=0
        dest = socket.gethostbyname(host)
        print("Pinging " + dest + " using Python:")

        #Send ping requests to a server separated by approximately one second
        try:
            while True:
                cnt+=1
                print(doOnePing(dest,timeout))
                time.sleep(1)
        except KeyboardInterrupt:
            if cnt !=0 :
                print('--- {} ping statistics ---'.format(host))
                print('{} packets transmitted, {} packets received, {:.1f}% packet loss'.format(cnt, rtt_cnt, 100.0 - rtt_cnt * 100.0 / cnt))
                if rtt_cnt != 0:
                    print('round-trip min/avg/max {:.3f}/{:.3f}/{:.3f} ms'.format(rtt_min, rtt_sum / rtt_cnt, rtt_max))


    ping("www.baidu.com")
    
  ## 运行结果
  ![homework5_1.png](../img/homework5_1.png)

