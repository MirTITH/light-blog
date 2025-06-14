# SSH笔记

## 文件权限

~/.ssh

```
drwx------  2 xy xy 4096 3月  15 23:48 ./	#.ssh 文件夹
drwxrwxrwx 26 xy xy 4096 3月  18 18:21 ../	#home 文件夹
-rw-------  1 xy xy   98 3月  15 23:48 authorized_keys
-rw-------  1 xy xy  399 2月  12 16:12 id_ed25519
-rw-r--r--  1 xy xy   92 2月  12 16:12 id_ed25519.pub
-rw-r--r--  1 xy xy  888 3月  15 23:53 known_hosts
```

/etc/ssh

```
drwxr-xr-x   4 root root   4096 3月  15 23:46 ./
drwxr-xr-x 147 root root  12288 3月  18 21:20 ../
-rw-r--r--   1 root root 535195 12月  3 06:38 moduli
-rw-r--r--   1 root root   1603 5月  29  2020 ssh_config
drwxr-xr-x   2 root root   4096 5月  29  2020 ssh_config.d/
-rw-r--r--   1 root root   3289 12月  3 06:38 sshd_config
drwxr-xr-x   2 root root   4096 12月  3 06:38 sshd_config.d/
-rw-------   1 root root   1405 3月  15 23:46 ssh_host_dsa_key
-rw-r--r--   1 root root    620 3月  15 23:46 ssh_host_dsa_key.pub
-rw-------   1 root root    525 3月  15 23:46 ssh_host_ecdsa_key
-rw-r--r--   1 root root    192 3月  15 23:46 ssh_host_ecdsa_key.pub
-rw-------   1 root root    419 3月  15 23:46 ssh_host_ed25519_key
-rw-r--r--   1 root root    112 3月  15 23:46 ssh_host_ed25519_key.pub
-rw-------   1 root root   2622 3月  15 23:46 ssh_host_rsa_key
-rw-r--r--   1 root root    584 3月  15 23:46 ssh_host_rsa_key.pub
-rw-r--r--   1 root root    342 3月  15 23:43 ssh_import_id
```



## 端口转发

### 命令解释：

-f    在后台执行

-N    不实际连接而是做 port forwarding

-R    远程端口转发

-L    本地端口转发

-C    启用压缩(经测试高速时反而会降低速度)

-p    端口

## **远程端口转发**

```bash
ssh -R [收听接口:]收听端口:目标主机:目标端口 username@hostname
```

#### 实现公网访问内网（大概是内网穿透）

（A: 公网客户端; B: 内网服务器）

**在B执行：**

```bash
B$ ssh -NfR A_port:localhost:B_port A_username@A_IP -p 22

# 以上命令执行后可能会存在终端关不掉的情况，需要结束ssh进程才能关掉
# 使用nohup命令可以解决这个问题：
B$ nohup ssh -NfR A_port:localhost:B_port A_username@A_IP -p 22
```

**效果**

​	A:A_port-> B:B_port （访问 A 的 A_port 端口就相当于访问 B 的 B_port 端口）

**注意**

- **修改公网机器A的SSH配置文件/etc/ssh/sshd_config**

	添加：

	```text
	GatewayPorts yes
	```

	这样可以把监听的端口绑定到任意IP 0.0.0.0上

	否则只有本机127.0.0.1可以访问

- **A开启对应端口的防火墙**

### **本地端口转发**

```bash
ssh -L [收听接口:]收听端口:目标主机:目标端口 username@hostname
```

> 命令中方括号内的部分，即第一个参数可以不写；它的默认值一般是0.0.0.0（OpenSSH客户端配置文件「ssh_config」中「GatewayPorts」选项的值一般为「yes」），意味着SSH隧道会收听所有接口，接受来自任何地址的应用访问请求并进行转发。而如果在此处填写了绑定地址（bind address），SSH隧道连接就会只处理来自绑定地址的应用请求，而对其他地址发来的请求置之不理；如同在（真实世界的）隧道入口设立哨卡，只对白名单牌号的车辆放行。例如在此处填写127.0.0.1，即可实现只有来自主机A本机的应用请求才被SSH隧道转发的效果。
>
> 需留意，收听接口是站在主机A的视角上去规定允许与A连接的设备，解决「能够使用SSH端口转发的应用请求从何处来」的问题，类似防火墙的入站；收听端口则依旧是主机A上的那个端口X，不能够跑到别的主机上去。

#### 主机(A)通过主机(B)访问主机(C)

**在A执行**：

```bash
A$ ssh -NfL A_port:C_ip:C_port B_user@B_ip -p 22
```

**效果**

A:A_port-> C:C_port

（访问 A 的 A_port 端口就相当于访问 C 的 C_port 端口）

**注意**

需满足：

- A能够访问B
- B能够访问C

#### 主机(A)访问主机(B)

**在A执行**：

```bash
A$ ssh -NfL A_port:localhost:B_port B_user@B_ip -p 22
```

或

```bash
A$ ssh -NfL A_port:B_ip:B_port B_user@B_ip -p 22
```

**效果**

A:A_port-> B:B_port

（访问 A 的 A_port 端口就相当于访问 B 的 B_port 端口）

**注意**

需满足：A能够访问B

### 动态端口转发（像VPN）

```bash
ssh -ND [收听接口:]收听端口 username@hostname
```

在本地发起的请求，需要由Socket代理([Socket Proxy](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/SOCKS))转发到收听端口



**应用场景:**

> *远程云主机B1运行了多个服务，分别使用了不同端口，本地主机A1需要访问这些服务。*

**为啥需要动态端口转发呢？**

> *一方面，由于安全限制，本地主机A1并不能直接访问远程云主机B1上的服务，因此需要进行端口转发；另一方面，为每个端口分别创建本地端口转发非常麻烦。*

**什么是动态端口转发？**

对于**本地端口转发**和**远程端口转发**，都存在两个一一对应的端口，分别位于SSH的客户端和服务端，而**动态端口转发**则只是绑定了一个**本地端口**，而**目标地址:目标端口**则是不固定的。**目标地址:目标端口**是由发起的请求决定的，比如，请求地址为**192.168.1.100:3000**，则通过SSH转发的请求地址也是**192.168.1.100:3000**。

### 链式端口转发

**本地端口转发**与**远程端口转发**结合起来使用，可以进行链式转发。假设A主机在公司，B主机在家，C主机为远程云主机。A主机上运行了前文的Node.js服务，需要在B主机上访问该服务。由于A和B不在同一个网络，且A主机没有独立公共IP地址，所以无法直接访问服务。

通过本地端口转发，将发送到B主机3000端口的请求，转发到远程云主机C的2000端口。

```bash
# 在B主机登陆远程云主机C，并进行本地端口转发
ssh -L localhost:3000:localhost:2000 root@103.59.22.17
```

通过远程端口转发，将发送到远程云主机C端口2000的请求，转发到A主机的3000端口。

```bash
# 在A主机登陆远程云主机C，并进行远程端口转发
ssh -R localhost:2000:localhost:3000 root@103.59.22.17
```

这样，在主机B可以通过访问[http://localhost:3000](https://link.zhihu.com/?target=http%3A//localhost%3A3000/)来访问主机A上的服务。

```text
# 在主机B访问主机A上的服务
curl http://localhost:3000
Hello Fundebug
```



## autossh

注意:此前提是可以本地可以免密登录服务器

```text
$  apt-get install autossh
# 我的本机是ubuntu
# 如果是centos 
#使用命令 $ yum install autossh
$ autossh -M 8888 -NCfR 1111:localhost:22 -o ServerAliveInterval=60 公网服务器登录名@公网ip -p 22
```

有可能长时间没有操作

会断开

用autossh 自动重连

我们用一个端口8888去监听

并且用-o ServerAliveInterval=60

每隔60秒去操作一下(比较接地气的说法)

# 参考资料

[反向ssh代理远程访问处于内网的电脑 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/94871997)

 [SSH正向与反向代理_李跃东的专栏-CSDN博客_ssh正向代理](https://blog.csdn.net/dliyuedong/article/details/49804825)

[彻底搞懂SSH端口转发命令 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/148825449)

[玩转SSH端口转发 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/26547381)

