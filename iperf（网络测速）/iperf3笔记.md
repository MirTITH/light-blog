# iperf3 笔记

> 官网 https://iperf.fr/

作用：测量两台主机的网络通信速率，支持TCP和UDP

## 服务端

```bash
iperf3 -s -p 5201
```

参数：

-s    服务端模式

-p    使用哪个端口（可省略）

## 客户端

### 测试TCP速度

```bash
iperf3 -c host -t 10 -p 5201 -R
```

参数：

-c    客户端模式

host    服务端ip、主机名等

-t    传输时间（可省略，默认10s）

-p   端口（可省略）

-R    测试接收速度（去掉该项为测试发送速度）

-6    使用ipv6

-4   使用ipv4

### 测试UDP速度

```bash
iperf3 -u -c host -b 100m -t 10 -p 5201 -R
```

参数：

-u    UDP模式

-c    客户端模式

host    服务端ip、主机名等

-t    传输时间（可省略，默认10s）

-p   端口（可省略）

-b    带宽（默认1 Mbps）

-R    测试接收速度（去掉该项为测试发送速度）

-6    使用ipv6

-4   使用ipv4
