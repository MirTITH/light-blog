# ubuntu 重装配置

## 系统配置

### 换源

在软件更新器中换

### DNS

> https://dns.icoa.cn/

```
119.29.29.29,1.2.4.8

240C::6666,2402:4e00::
```

### 与windows时间同步

```bash
timedatectl set-local-rtc 1 --adjust-system-clock
```

### GRUB2 timeout

Run in terminal:

```bash
sudo gedit /etc/default/grub
```

Change the value of GRUB_TIMEOUT

Next run:

```bash
sudo update-grub
```

### Keychron键盘 F1-F12映射修复

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



### 禁用鼠标键盘唤醒

> https://askubuntu.com/a/713247

1. **找到相关设备**

```bash
$ lsusb
```

例如：`Bus 005 Device 003: ID 046d:c53f Logitech, Inc. USB Receiver`



2. **创建脚本**

> 名称随意，例如： `config-G304-wakeup.sh`
>
> 位置：`/lib/systemd/system-sleep/`

执行：

```bash
#会自动创建新文件
sudo gedit /lib/systemd/system-sleep/config-G304-wakeup.sh
```

写入如下内容：

> 注意：第4、5行的id修改为步骤1中查到的id

```bash
#!/bin/bash

# From lsusb: Bus 005 Device 008: ID 046d:c53f Logitech, Inc. USB Receiver
idVendor=046d
idProduct=c53f

# Get sys device path by vendorId and productId
function find_device()
{
    local vendor=$1
    local product=$2
    vendor_files=( $(egrep --files-with-matches "$vendor" /sys/bus/usb/devices/*/idVendor) )
    for file in "${vendor_files[@]}"; do
       local dir=$(dirname "$file")
       if grep -q -P "$product" "$dir/idProduct"; then
         printf "%s\n" "$dir"
         return
       fi
    done
}

sysdev=$(find_device $idVendor $idProduct)

if [ ! -r "$sysdev/power/wakeup" ]; then
    echo $idVendor:$idProduct not found 1>&2
    exit 1
fi

case "$1" in
    enabled|disabled)
    echo $1 > "$sysdev/power/wakeup"
    ;;
    *)
    echo "$0 enabled   -- to enable the wakeup for this device"
    echo "$0 disabled  -- to disable the wakeup for this device"
    ;;
esac

grep --color=auto -H ".*" "$sysdev/power/wakeup"
exit 0
```



3. **赋予可执行权限**

```bash
sudo chmod +x /lib/systemd/system-sleep/config-G304-wakeup.sh
```

> 此时执行 `./config-G304-wakeup.sh disabled` 即可禁用唤醒，但重启后失效



4. **设置开机自动运行**

```bash
#会自动创建新文件
sudo gedit /etc/systemd/system/disable-G304-wakeup.service
```

写入如下内容：

> ExecStart 改为对应路径

```bash
[Unit]
Description=Disable wakeup on mouse-move (Logitech G304)
After=default.target

[Service]
ExecStart=/lib/systemd/system-sleep/config-G304-wakeup.sh disabled

[Install]
WantedBy=default.target
```

执行：

```bash
systemctl daemon-reload
systemctl enable disable-G304-wakeup.service
```

完成~



### R7000P 亮度调节

ubuntu 20.04 安装510版本nvidia 驱动直接解决

> 无效则参考以下链接
>
> https://zhuanlan.zhihu.com/p/348624522?ivk_sa=1024320u



## 软件安装

### language package

```bash 
sudo apt install $(check-language-support)
```

### Edge

**GPG error "NO_PUBKEY"**

Execute the following commands in terminal

```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys <PUBKEY>
```

where `<PUBKEY>` is your missing public key for repository, e.g. `8BAF9A6F`.

Then update   

```bash
sudo apt-get update
```

### 输入法(选1个)

#### fcitx5

[fcitx5.md](./fcitx5/fcitx5.md)

#### 搜狗输入法

https://pinyin.sogou.com/linux/?r=pinyin

不显示问题：安装以下依赖

```bash
sudo apt install libqt5qml5 libqt5quick5 libqt5quickwidgets5 qml-module-qtquick2
sudo apt install libgsettings-qt1
```

### v2rayA

> https://v2raya.org/

**安装V2Ray内核**

```bash
curl -Ls https://mirrors.v2raya.org/go.sh | sudo bash
```

安装后可以关掉服务，因为 v2rayA 不依赖于该 systemd 服务。

```bash
sudo systemctl disable v2ray --now
```

**安装 v2rayA**

添加公钥

```bash
wget -qO - https://apt.v2raya.mzz.pub/key/public-key.asc | sudo tee /etc/apt/trusted.gpg.d/v2raya.asc
```

添加软件源

```bash
echo "deb https://apt.v2raya.mzz.pub/ v2raya main" | sudo tee /etc/apt/sources.list.d/v2raya.list
sudo apt update
```

安装

```bash
sudo apt install v2raya
```

**启动**

```bash
sudo systemctl start v2raya.service
```

**设置自动启动**

```bash
sudo systemctl enable v2raya.service
```

**访问**

http://localhost:2017/

### Zsh

> https://github.com/ohmyzsh/ohmyzsh/wiki/Installing-ZSH

 Install Zsh:

```bash
sudo apt install zsh
```

Make it your default shell:

```bash
chsh -s $(which zsh)
```



**Log out and log back in again to use your new default shell.**



Oh My Zsh:

```bash
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

**皮肤**

> https://github.com/romkatv/powerlevel10k

### git

```bash
sudo apt install git

git config --global user.email "1023515576@qq.com"
git config --global user.name "TITH"
git config --global core.quotepath false
```

ssh 目录

> ~/.ssh
>
> /etc/ssh

### tldr

```bash
sudo apt install npm
sudo npm install -g tldr
```

### 视频解码器

> https://linuxhint.com/install-h264-decoder-ubuntu/

直接执行以下命令

（期间会有对话框，前两行命令全选默认的，最后一行接受）

```bash
sudo apt install libdvdnav4 gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly libdvd-pkg -y
sudo dpkg-reconfigure libdvd-pkg
sudo apt install ubuntu-restricted-extras
```

### komorebi（动态壁纸）

> https://github.com/cheesecakeufo/komorebi

需要安装视频解码器

N卡可能需要使用闭源驱动

### terminator

复制 `.config/terminator` 文件夹到`~/.config`

```bash
sudo apt install terminator
```
### samba

参考[samba使用教程.md](../samba/samba使用教程.md)