# WireSharkLab-TCP

## 实验材料
[Wireshark_TCP_v6.0](Wireshark_TCP_v6.0.pdf)

## 概述
  通过实例来详细地研究TCP协议，具体是通从你的计算机过到一个远程主机传输一个150KB的文件
  （包含Lewis Carrol’s Alice’s Adventures in Wonderland的文本）来分析TCP报文段的发送和接收。
  包含以下内容：
  
1. 学习TCP利用序号(seq)和确认号(ack)来提供数据的可靠传输。
2. 学习TCP拥塞控制算法——慢启动和拥塞避免。
3. 学习TCP的接收器通知流控制机制。
4. 考虑TCP连接设置并研究计算机和服务器之间TCP连接的性能（吞吐量和往返时间）。

## 捕获从计算机到远程服务器的批量TCP传输

1. 从http://gaia.cs.umass.edu/wireshark-labs/alice.txt复制全文，在你的计算机上建立新的文本文件TCP.txt，
把复制的文本粘贴到TCP.txt,保存。
2. 打开http://gaia.cs.umass.edu/wireshark-labs/TCP-wireshark-file1.html，点击网页中的选择文件按钮，选择
TCP.txt文件。注意先别点击开始上传按钮。
3. 打开WireShark，启动开始捕获，回到浏览器点击“Upload alice.txt file”按钮，等上传完毕，浏览器会出现一条
congratulations信息。
4. 停止捕获。

### 结果如下：
![Lab4_1.png](../img/Lab4_1.png)

## 首先看一下捕获的信息

  首先，在显示过滤器那里输入tcp，回车。现在，你看到的应该是你的计算机和gaia.cs.umass.edu之间的
  一系列TCP或者HTTP信息。
  
  ** 可以看到tcp建立连接的三次握手（包含一个SYN信息）： **
![Lab4_2.png](../img/Lab4_2.png)
  
  ** 可以看到一条HTTP POST信息（可看到HTTP POST是在所有TCP报文段传输后才一次性传输过去的) **
![Lab4_3.png](../img/Lab4_3.png)

  ** 取决于你的WireShark版本，可能看到一系列HTTP Continuation信息，本人的版本并没有显示，
  其实实际上没有HTTP Continuation这种信息，这只是WireShark来告知你有很多TCP报文段被用来传
  输同一个HTTP信息（因为文件太大了，需要分组）。**
  
  **更多的，最近的几个版本的WireShark，你可以在WireShark分组列表的信息（info)列看到
  “[TCP segmentof a reassembled PDU]”，表明这些TCP报文段属于一个更上层协议的信息
  （在这个例子中，便是HTTP信息）。**
![Lab4_4.png](../img/Lab4_4.png)
  
  **同时，也能看到从gaia.cs.umass.edu传回你的计算机的确认号，表明某个分组确认收到了。**
![Lab4_5.png](../img/Lab4_5.png)

  ** 在我的这一次TCP传输文件过程中，还发生过分组到目的主机超时，引起计算机重新发送分组，结果造成
  有两个一样的分组到达目的主机的情况（后一个分组目的主机会丢弃）**
![Lab4_6.png](../img/Lab4_6.png)

### 问题解答

