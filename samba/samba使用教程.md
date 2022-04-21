# samba 使用教程

## 软件安装

1. 在nautilus文件管理器中点击共享，会自动安装
2. 添加用户：

```bash
sudo smbpasswd -a username
```

> username 必须是已经存在系统中的用户名
>
> 之后提示输入New SMB password，此处的密码可与系统密码不同

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

net usershare add: cannot share path /mnt/E/_XY as we are restricted to only sharing directories we own.
	Ask the administrator to add the line "usershare owner only = false" 
	to the [global] section of the smb.conf to allow this.

#### daemon failed to start: Samba cannot init registry

https://blog.csdn.net/u013310025/article/details/86721604

```bash
sudo rm /var/lib/samba/registry.tdb
```

