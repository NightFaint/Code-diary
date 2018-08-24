# WireSharkLab-HTTP

## 实验材料

[Wireshark_HTTP_v6.1.pdf](Wireshark_HTTP_v6.1.pdf)

## 1.基本的 HTTP GET/response交互
   目标：下载一个简单地HTML文件。
1.1 打开浏览器。
1.2 打开WireShark，先不要启动捕获，在过滤器中输入http，以便只捕获HTTP信息。
1.3 等待一分钟然后开始捕获。
1.4 在浏览器中输入以下内容 http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file1.html 
您的浏览器应显示非常简单的单行HTML文件。
1.5 停止捕获。

  可看到分组列表中的两个分组信息：GET消息（从您的浏览器发送到gaia.cs.umass.edu 的web服务器）
和从服务器到浏览器的响应消息。

![Lab2_1.png](../img/Lab2_1.png)

关注HTTP报文信息，其他帧、以太网、ip和tcp报文具体信息最小化。

![Lab2_2.png](../img/Lab2_2.png)
![Lab2_3.png](../img/Lab2_3.png)

通过上图，我们可以回答以下问题：

您的浏览器是否运行HTTP版本1.0或1.1？服务器运行什么版本的HTTP？

浏览器HTTP版本1.1，服务器1.1.

您的浏览器会从接服务器接受哪种语言（如果有的话）？

英文、中文

您的计算机的IP地址是什么？ gaia.cs.umass.edu服务器地址呢？

192.168.1.101    128.119.245.12

服务器返回到浏览器的状态代码是什么？

200

服务器上HTML文件的最近一次修改是什么时候？

0.001558秒前

服务器返回多少字节的内容到您的浏览器？

1217字节

通过检查数据包内容窗口中的原始数据，你是否看到有协议头在数据包列表窗口中未显示？ 如果是，请举一个例子。

![Lab2_4.png](../img/Lab2_4.png)

## HTTP条件GET/response交互

1. 启动浏览器，清空缓存
2. 启动WireShark，捕获开始
3. 输入http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html ，
浏览器应显示一个非常简单的五行HTML文件。
4. 再次快速地将相同的URL输入到浏览器中（或者只需在浏览器中点击刷新按钮）。
5. 停止Wireshark数据包捕获，并在display-filter-specification窗口中输入“http”，
以便只捕获HTTP消息，并在数据包列表窗口中显示。

![Lab2_5.png](../img/Lab2_5.png)

** 问题解答 **

检查第一个从您浏览器到服务器的HTTP GET请求的内容。您在HTTP GET中看到了“IF-MODIFIED-SINCE”行吗？

答：没有

检查服务器响应的内容。服务器是否显式返回文件的内容？ 你是怎么知道的？

 答：是的，有个line-based text data首部。

现在，检查第二个HTTP GET请求的内容。 您在HTTP GET中看到了“IF-MODIFIED-SINCE:”行吗？ 如果是，“IF-MODIFIED-SINCE:”头后面包含哪些信息？

答：是，包含了浏览器缓存的文件的修改时间。如果服务器文件的修改时间比浏览器缓存文件的修改时间要晚，
则浏览器会向服务器再发出get请求，否则，直接从浏览器缓存中读取数据给用户。（相当于代理服务器）

针对第二个HTTP GET，从服务器响应的HTTP状态码和短语是什么？服务器是否明确地返回文件的内容？请解释。

304 NOT Modified，服务器没有返回文件内容，因为没有line-based text data行。

# 检索长文件

1. 启动您的浏览器，并确保您的浏览器缓存被清除，如上所述。
2. 启动Wireshark数据包嗅探器
3. 在您的浏览器中输入以下URL http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file3.html 您的浏览器应显示相当冗长的美国权利法案。
4. 停止Wireshark数据包捕获，并在display-filter-specification窗口中输入“http”，以便只显示捕获的HTTP消息。

在分组列表窗口中，您应该看到您的HTTP GET消息，然后是HTTP GET请求的多个分组的TCP响应。（由于请求的html文件过大
被分为几个数据包）

** 问题解答 **
  您的浏览器发送多少HTTP GET请求消息？哪个数据包包含了美国权利法案的消息？
  
  ![Lab2_5.png](../img/Lab2_5.png)
  
  哪个数据包包含响应HTTP GET请求的状态码和短语？
  
  答：25和55
  
  响应中的状态码和短语是什么？
  
  答：200 OK
  
  需要多少包含数据的TCP段来执行单个HTTP响应和权利法案文本？
  
