# ubuntu 重装配置

## 修改 efi 位置

1. 删除 /boot/efi/EFI/ubuntu

2. `lsblk` 找到新的 efi 设备分区，如 `nvme1n1p5`

3. `sudo blkid /dev/设备分区` 得到 UUID. 如 `5C51-1F97`

4. 修改 `/etc/fstab` 中 `UUID=XXXX-XXXX /boot/efi vfat umask=0077 0 1` 行，将 `XXXX-XXXX` 换成第 3 步中得到的 UUID

5. 卸载旧分区，挂载新分区： 

   ```shell
   sudo umount /boot/efi
   sudo mount /boot/efi
   ```

6. ```shell
   sudo grub-install
   sudo update-grub
   ```

完成！

## 换源
**适用于 ubuntu 20.04.**
- ubuntu 22.04 请将 focal 替换为 jammy
- ubuntu 18.04 请将 focal 替换为 bionic
- ubuntu 16.04 请将 focal 替换为 xenial

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

# deb http://security.ubuntu.com/ubuntu/ focal-security main restricted universe multiverse
# # deb-src http://security.ubuntu.com/ubuntu/ focal-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.osa.moe/ubuntu/ focal-proposed main restricted universe multiverse
# # deb-src https://mirrors.osa.moe/ubuntu/ focal-proposed main restricted universe multiverse
```

## DNS

> https://dns.icoa.cn/

```
119.29.29.29,1.2.4.8

2402:4e00::,240c::6666
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

## Keychron键盘 F1-F12映射修复(Ubuntu 22 is not needed)

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
mkdir -p ~/.local/bin/
cp ./reboot-to-ubuntu.sh ~/.local/bin/
```

## 开机挂载硬盘

仿照如下修改 fstab

或者直接使用 gnome-disk-utility 配置 `sudo apt install gnome-disk-utility`

另外 kubuntu 22.04 自带的 KDE 分区管理器也好用（20.04的似乎不好用）

```
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system>                             <mount point>        <type> <options>     <dump>  <pass>
# / was on /dev/nvme1n1p6 during installation
UUID=bc37ee02-3ac4-44da-b6ad-34f43a80673b   /                    ext4   errors=remount-ro   0 1 
# /boot/efi was on /dev/nvme1n1p5 during installation
UUID=5C51-1F97                              /boot/efi            vfat   umask=0077          0 1 
# swap was on /dev/nvme1n1p4 during installation
UUID=4b888711-6ff2-480f-9615-700ec0e7a8c4   none                 swap   sw                  0 0 
UUID=f4bc711c-5c5e-40e0-92e5-38a351d20f43   /mnt/ubuntu          ext4   defaults            0 0 
UUID=7080BF8880BF5378                       /mnt/win_e           ntfs   defaults            0 0 
UUID=7C506F8E506F4DC8                       /mnt/win_d           ntfs   defaults            0 0 
/mnt/ubuntu/home/xy/Documents               /home/xy/Documents   none   bind                0 0
/mnt/ubuntu/home/xy/Downloads               /home/xy/Downloads   none   bind                0 0
/mnt/ubuntu/home/xy/Music                   /home/xy/Music       none   bind                0 0
/mnt/ubuntu/home/xy/Pictures                /home/xy/Pictures    none   bind                0 0
/mnt/ubuntu/home/xy/Videos                  /home/xy/Videos      none   bind                0 0
```



## KDE Dolpnin 无法访问 Windows 共享文件夹

### The file or folder smb://ip does not exist.

> https://forum.manjaro.org/t/dolphin-the-file-or-folder-smb-sharename-does-not-exist/114900/10

A user on Reddit found a fix: In System Settings–>Network Settings–>Windows Shares, add ANY text to the user and password fields and restart Dolphin. Now I get a password prompt and can view and mount shares.

