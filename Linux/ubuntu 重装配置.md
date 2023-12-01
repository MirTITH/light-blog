# ubuntu 重装配置

## 换源

```
# https://mirrors.osa.moe/ubuntu/
# https://mirrors.ustc.edu.cn/ubuntu/

# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.osa.moe/ubuntu/ focal main restricted universe multiverse
# deb-src https://mirrors.osa.moe/ubuntu/ focal main restricted universe multiverse
deb https://mirrors.osa.moe/ubuntu/ focal-updates main restricted universe multiverse
# deb-src https://mirrors.osa.moe/ubuntu/ focal-updates main restricted universe multiverse
deb https://mirrors.osa.moe/ubuntu/ focal-backports main restricted universe multiverse
# deb-src https://mirrors.osa.moe/ubuntu/ focal-backports main restricted universe multiverse
deb https://mirrors.osa.moe/ubuntu/ focal-security main restricted universe multiverse
# deb-src https://mirrors.osa.moe/ubuntu/ focal-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.osa.moe/ubuntu/ focal-proposed main restricted universe multiverse
# deb-src https://mirrors.osa.moe/ubuntu/ focal-proposed main restricted universe multiverse
```

## DNS

> https://dns.icoa.cn/

```
119.29.29.29,1.2.4.8

240C::6666,2402:4e00::
```

## 与windows时间同步

(建议修改 windows 端，与 ubuntu 时间同步)

```bash
# 修改 linux 端
timedatectl set-local-rtc 1 --adjust-system-clock
```

## GRUB2 timeout和关机timeout

GRUB:

```bash
sudo gedit /etc/default/grub
```

Change the value of GRUB_TIMEOUT

Next run:

```bash
sudo update-grub
```

**关机timeout:**

```bash
sudo gedit /etc/systemd/system.conf
```

修改为：（注意删掉文件这两行开头的#）

```
DefaultTimeoutStartSec=30s
DefaultTimeoutStopSec=30s
```

执行：

```bash
systemctl daemon-reload
```

## Keychron键盘 F1-F12映射修复

> https://blog.csdn.net/AlanCorn_02/article/details/118462860

```bash
#输入下面命令后，键盘应该能正常使用，但每次重启要重新输入
echo 0 | sudo tee /sys/module/hid_apple/parameters/fnmode
```

```bash
#输入下面的命令，写入配置文件，重启后就无需再次输入
echo "options hid_apple fnmode=0" | sudo tee -a /etc/modprobe.d/hid_apple.conf

#更新initramfs

# Ubuntu
sudo update-initramfs -u 

# ArchLinux
mkinitcpio -P 
```

## 禁用鼠标键盘唤醒

> https://askubuntu.com/a/713247

### 对于G304鼠标：

```bash
sudo cp config-G304-wakeup.sh /lib/systemd/system-sleep/
sudo chmod +x /lib/systemd/system-sleep/config-G304-wakeup.sh
sudo cp disable-G304-wakeup.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable disable-G304-wakeup.service
```

### 对于其他鼠标：

1. **找到相关设备**

```bash
lsusb
```

>  例如：`Bus 005 Device 003: ID 046d:c53f Logitech, Inc. USB Receiver`
>
> 其中ID格式为：`idVendor:idProduct`

2. **修改脚本**

修改`config-G304-wakeup.sh`脚本中的id（并换个文件名）

**这两行换成在步骤1中查到的id**

```bash
idVendor=046d
idProduct=c53f
```

修改`disable-G304-wakeup.service`中的对应信息（并换个文件名）

3. **部署脚本**

```bash
sudo cp config-新名字-wakeup.sh /lib/systemd/system-sleep/
sudo chmod +x /lib/systemd/system-sleep/config-新名字-wakeup.sh
sudo cp disable-新名字-wakeup.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable disable-新名字-wakeup.service
```

## reboot-to-ubuntu.sh

```bash
cp ./reboot-to-ubuntu.sh ~/.local/bin
```

## KDE Dolpnin 无法访问 Windows 共享文件夹

### The file or folder smb://ip does not exist.

> https://forum.manjaro.org/t/dolphin-the-file-or-folder-smb-sharename-does-not-exist/114900/10

A user on Reddit found a fix: In System Settings–>Network Settings–>Windows Shares, add ANY text to the user and password fields and restart Dolphin. Now I get a password prompt and can view and mount shares.


