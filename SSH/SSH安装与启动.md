# SSH 安装与启动

## 安装服务端

Windows:

> [几步命令轻松搭建Windows SSH服务端 - 云+社区 - 腾讯云 (tencent.com)](https://cloud.tencent.com/developer/article/1611035)

Linux:

```bash
sudo apt install openssh-server
```

## 启动服务端

Windows:

```powershell
Start-Service sshd
```

Linux:（安装后默认启动）

```bash
sudo service ssh start
```

## 重启服务端

Linux:

```bash
sudo service ssh restart
```

## 查询SSH服务状态

```bash
sudo service ssh status
```

## 免密登录

```bash
# 在客户端操作

# 检查客户端是否已有密钥：
ls ~/.ssh
# 如果有类似于 id_ed25519  id_ed25519.pub 的文件，则已经有密钥了

# 如果客户端不存在密钥，需要生成密钥：
ssh-keygen -t ed25519 -C "your_email@example.com"

# 将公钥上传到服务器：
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@IP
```

> 输入 -i 之后直接tab会自动补全

## 路径

> /etc/ssh
>
> ~/.ssh
