 

# Linux 软件安装

## 通用

### 字体

firacode

```bash
sudo apt install fonts-firacode
```

思源黑体

https://github.com/adobe-fonts/source-han-sans/releases

### 输入法(选1个)

#### fcitx5

[fcitx5.md](./fcitx5/fcitx5.md)

#### 搜狗输入法

https://pinyin.sogou.com/linux/?r=pinyin

不显示问题：安装以下依赖

```bash
# sudo apt install libqt5qml5 libqt5quick5 libqt5quickwidgets5 qml-module-qtquick2
sudo apt install libgsettings-qt1
```



<!-- ### icalingua

新版：**icalingua++**（感谢大佬接手）

https://github.com/Icalingua-plus-plus/Icalingua-plus-plus

直接下载安装即可

**以下为原版（原作者删库，不再更新）**

*软件本体太大，不放在仓库中*

deb包只有2.4.5版本

如果要用2.5.6版本：

> 只有 AppImage

复制文件

```bash
sudo mkdir /opt/Icalingua/
sudo cp Icalingua-2.4.6.AppImage /opt/Icalingua/
sudo cp icalingua.png /opt/Icalingua/
```

确保`Icalingua-2.4.6.AppImage`有可执行权限

复制.desktop

```bash
sudo cp icalingua.desktop /usr/share/applications/
```

确保`icalingua.desktop `有可执行权限 -->



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



### Edge

官网下载安装包



**如果遇到`GPG error "NO_PUBKEY"`：**

Execute the following commands in terminal

```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys <PUBKEY>
```

where `<PUBKEY>` is your missing public key for repository, e.g. `8BAF9A6F`.

Then update   

```bash
sudo apt-get update
```



**如果遇到Warning: apt-key is deprecated:** 

https://askubuntu.com/questions/1398344/apt-key-deprecation-warning-when-updating-system



### git

```bash
sudo apt install git

git config --global user.email "1023515576@qq.com"
git config --global user.name "X. Y."
git config --global core.quotepath false
```

ssh 目录

> ~/.ssh
>
> /etc/ssh



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



如果需要临时切换到bash: 

```bash
exec bash
```

#### Oh My Zsh

需要先安装Zsh

```bash
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

**皮肤**

https://github.com/romkatv/powerlevel10k

#### 插件

https://zhuanlan.zhihu.com/p/61447507

### tldr

> https://tldr.sh/
>
> 似乎 Node.js 版本不会显示中文文档，并且高亮不如python版本
>
> 但 Node.js 会缓存所有文档，查询比python版本快
>
> python 版本在没梯子时贼慢，几乎不能用

Node.js 版本：

```bash
sudo apt install npm
sudo npm install -g tldr
```

或者安装python版本：

```
pip3 install tldr
```

### Qt Creator

官网下载安装包

如果要换源：
```
./qt-unified-linux-x64-4.5.1-online.run --mirror https://ipv4.mirrors.ustc.edu.cn/qtproject
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



### samba

参考[samba使用教程.md](../samba/samba使用教程.md)



## KDE 推荐安装

### language package

```bash 
sudo apt install $(check-language-support)

# 安装中文语言包
sudo apt install language-pack-zh-han*

# 安装gnome包
sudo apt install language-pack-gnome-zh-han*

# 安装kde包
sudo apt install language-pack-kde-zh-han*
```

**zsh使用通配符要加单引号**

> `fcitx-ui-qimpanel `  in $(check-language-support) is confilct with sogoupinyin. Do not install it if using sogoupinyin. 
>
> Some input methods in the list is not needed when using other input methods. 

### Nautilus

```bash
 sudo apt install nautilus nautilus-share
```

### gnome-disk-utility

```bash
sudo apt install gnome-disk-utility
```

### gnome-keyring

```bash
sudo apt install gnome-keyring
```

### yakuake

```bash
 sudo apt install yakuake
```

然后在设置-开机和关机-自动启动里添加启动项



### flameshot 截图工具

> https://github.com/flameshot-org/flameshot

安装：

```
sudo apt install flameshot
```

设置快捷键：

**On KDE Plasma desktop**

To make configuration easier, there's a [file](https://github.com/flameshot-org/flameshot/blob/master/docs/shortcuts-config/flameshot-shortcuts-kde.khotkeys) in the repository that more or less automates this process. This file will assign the following keys to the following actions by default:

| Keys                  | Description                                                  |
| --------------------- | ------------------------------------------------------------ |
| Prt Sc                | Start the Flameshot screenshot tool and take a screenshot    |
| Ctrl + Prt Sc         | Wait for 3 seconds, then start the Flameshot screenshot tool and take a screenshot |
| Shift + Prt Sc        | Take a full-screen (all monitors) screenshot and save it     |
| Ctrl + Shift + Prt Sc | Take a full-screen (all monitors) screenshot and copy it to the clipboard |

If you don't like the defaults, you can change them manually later.

Steps for using the configuration:

1. The configuration file configures shortcuts so that Flameshot automatically saves (without opening the save dialog) screenshots to `~/Pictures/Screenshots` folder. Make sure you have that folder by running the following command:

   ```bash
   mkdir -p ~/Pictures/Screenshots
   ```

   (If you don't like the default location, you can skip this step and configure your preferred directory later.)

2. Download the configuration file:

   ```bash
   cd ~/Desktop
   wget https://raw.githubusercontent.com/flameshot-org/flameshot/master/docs/shortcuts-config/flameshot-shortcuts-kde.khotkeys
   ```

3. Make sure you have the `khotkeys` installed using your package manager to enable custom shortcuts in KDE Plasma.

4. Go to *System Settings* → *Shortcuts* → *Custom Shortcuts*.

5. If there's one, you'll need to disable an entry for Spectacle, the default KDE screenshot utility, first because its shortcuts might collide with Flameshot's ones; so, just uncheck the *Spectacle* entry.

6. Click *Edit* → *Import...*, navigate to the Desktop folder (or wherever you saved the configuration file) and open the configuration file.

7. Now the Flameshot entry should appear in the list. Click *Apply* to apply the changes.

8. If you want to change the defaults, you can expand the entry, select the appropriate action and modify it as you wish; the process is pretty self-explanatory.

9. If you installed Flameshot as a Flatpak, you will need to create a symlink to the command:

   ```bash
   ln -s /var/lib/flatpak/exports/bin/org.flameshot.Flameshot ~/.local/bin/flameshot
   ```



### latte-dock

在 `light-blog-resource/latte-dock-0.10.8` 文件夹中编译安装

然后在`Linux/latte-dock`中使用配置文件

对于0.10.8版本：

布局备份：`TITH-latte10.layout.latte`

面板备份：`TITH-主显示器面板.view.latte`



## GNOME 推荐安装

### komorebi（动态壁纸）

> https://github.com/cheesecakeufo/komorebi

需要安装视频解码器

N卡可能需要使用闭源驱动

### terminator

复制 `.config/terminator` 文件夹到`~/.config`

```bash
sudo apt install terminator
```

