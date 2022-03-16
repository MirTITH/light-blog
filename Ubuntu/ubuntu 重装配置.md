# ubuntu 重装配置

## 系统配置

### 换源

在软件更新器中换



### DNS

> https://dns.icoa.cn/

119.29.29.29

1.2.4.8

240C::6666

2402:4e00::



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



### R7000P 亮度调节

ubuntu 20.04 安装510版本nvidia 驱动直接解决

> 无效则参考以下链接
>
> https://zhuanlan.zhihu.com/p/348624522?ivk_sa=1024320u



## 软件安装

### 输入法
搜狗输入法

https://pinyin.sogou.com/linux/?r=pinyin

不显示问题：安装以下依赖

```bash
sudo apt install libqt5qml5 libqt5quick5 libqt5quickwidgets5 qml-module-qtquick2
sudo apt install libgsettings-qt1
```

### git

~/.ssh权限

> drwx------  2 xy   xy   4096 3月  13 20:27 .ssh
>
> -rw------- 1 xy xy 399 2月  12 16:12 id_ed25519
>
> -rw-r--r-- 1 xy xy  92 2月  12 16:12 id_ed25519.pub
>
> -rw-r--r-- 1 xy xy 444 3月  13 20:27 known_hosts

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



### samba

参考[samba使用教程.md](../samba/samba使用教程.md)