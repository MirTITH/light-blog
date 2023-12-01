# samba 使用教程

## 软件安装

```bash
sudo apt install samba
sudo smbpasswd -a <用户名>
```

> **<用户名>** 必须是已经存在系统中的用户名
>
> 之后提示输入New SMB password，此处的密码可与系统密码不同

## 配置 smb.conf

在 /etc/samba/smb.conf 的 [global] 下添加

```
# 共享 owner 不是自己的文件，比如 NTFS 磁盘
usershare owner only = false
# 允许软链接
unix extensions = No
follow symlinks = Yes
wide links = Yes
```

## 重启

```bash
sudo service smbd restart
```

## 文件位置

共享目录记录位置

> /var/lib/samba/usershares

smb.conf文件位置

> /etc/samba/smb.conf

注：

> 在smb.conf中也可以添加共享目录，这与在usershares文件夹中添加是等效的

## 常见问题

#### net usershare”返回错误 255

在`smb.conf`的 [global]下添加：

```
usershare owner only = false
```

> net usershare add: cannot share path /mnt/E/_XY as we are restricted to only sharing directories we own.
> 	Ask the administrator to add the line "usershare owner only = false" 
> 	to the [global] section of the smb.conf to allow this.

### 软链接支持

在[global]下添加：

```
unix extensions = No
follow symlinks = Yes
wide links = Yes
```

#### daemon failed to start: Samba cannot init registry

https://blog.csdn.net/u013310025/article/details/86721604

```bash
sudo rm /var/lib/samba/registry.tdb
```

