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

## 文件位置

共享目录记录位置

> /var/lib/samba/usershares

smb.conf文件位置

> /etc/samba/smb.conf

注：

> 在smb.conf中也可以添加共享目录，这与在usershares文件夹中添加是等效的
