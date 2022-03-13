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

.ssh目录权限

> drwx------  2 xy   xy   4096 3月  13 20:27 .ssh
>
> -rw------- 1 xy xy 399 2月  12 16:12 id_ed25519
>
> -rw-r--r-- 1 xy xy  92 2月  12 16:12 id_ed25519.pub
>
> -rw-r--r-- 1 xy xy 444 3月  13 20:27 known_hosts
>

