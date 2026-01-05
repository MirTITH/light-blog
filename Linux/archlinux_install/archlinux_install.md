# Arch Linux 安装配置及注意事项

## 安装

```bash
cd archlinux_install
./pre_install.sh
archinstall --config desktop-xy.json
```

## 配置

### 配置主机名

```bash
kate /etc/hosts
```

加入如下内容：

```conf
# Static table lookup for hostnames.
# See hosts(5) for details.
127.0.0.1        localhost
::1              localhost
127.0.1.1        desktop-xy
```

### 修改 UEFI 入口名称

需谨慎操作，操作不当会丢引导

```bash
sudo grub-install --target=x86_64-efi --efi-directory /boot/efi --bootloader-id="Arch Linux"
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

然后删除多余的入口

### reboot-to-arch.sh

```bash
mkdir ~/.local/bin
cp ./home/.local/bin/reboot-to-arch.sh ~/.local/bin/
```

### 系统配置

比较差异并复制配置文件

```bash
# diff /etc/pacman.conf ./root/etc/pacman.conf
sudo cp ./root/etc/pacman.conf /etc/pacman.conf

sudo pacman -Sy archlinuxcn-keyring
sudo pacman -S paru

sudo cp ./root/etc/makepkg.conf /etc/makepkg.conf
sudo cp ./root/etc/paru.conf /etc/paru.conf
```

### 语言配置

```bash
# 编辑 /etc/locale.gen，取消注释：zh_CN.UTF-8 UTF-8
kate /etc/locale.gen

sudo locale-gen
```

配置 fonts.conf，避免在中文环境中展示日文字形：

```bash
mkdir -p ~/.config/fontconfig/
cp ./home/.config/fontconfig/fonts.conf ~/.config/fontconfig/
# 为当前用户重新生成缓存
fc-cache -f -v
```

### Konsole 配置

```bash
cp ./home/.config/konsolerc ~/.config/
cp -r ./home/.local/share/konsole ~/.local/share/
```

### Git 配置

```bash
git config --global user.email "1023515576@qq.com"
git config --global user.name "Yang XIE"
git config --global core.quotepath false
```

### 修改 grub

```bash
kate /etc/default/grub
```

### 安装包

```bash
paru -U mihomo-party-bin-1.8.4-1-x86_64.pkg.tar.zst
paru -S base-devel bash-completion dosfstools fatresize ntfs-3g gdb cmake ninja make gwenview yakuake timeshift xorg-xhost grub-btrfs htop xorg-xeyes vlc vlc-plugin-ffmpeg kdegraphics-thumbnailers ffmpegthumbs print-manager cups system-config-printer kdenetwork-filesharing samba power-profiles-daemon kwalletmanager filelight
paru -S ttf-lxgw-wenkai ttf-lxgw-wenkai-mono adobe-source-han-sans-otc-fonts noto-fonts-cjk
paru -S zsh oh-my-zsh-git zsh-theme-powerlevel10k-git conda-zsh-completion zsh-autosuggestions zsh-syntax-highlighting ttf-meslo-nerd-font-powerlevel10k

# 安装 time-based job scheduler (Timeshift 自动快照需要)
paru -S cronie
sudo systemctl enable --now cronie.service 

# 其他软件
paru -S typora tldr visual-studio-code-bin moonlight-qt mission-center
```

### 禁用鼠标键盘唤醒

```shell
paru -S wakeup-triggers
sudo systemctl enable --now wakeup-triggers.service
```

### 安装 Wayland 下的 Fcitx5 输入法

> https://fcitx-im.org/wiki/Using_Fcitx_5_on_Wayland  
> https://wiki.archlinux.org/title/Fcitx5

#### 安装

```bash
# 安装 fcitx5
paru -S fcitx5-im fcitx5-chinese-addons fcitx5-mozc fcitx5-pinyin-zhwiki fcitx5-pinyin-moegirl
# 安装添加环境变量的脚本
sudo cp ./root/etc/profile.d/input-support.sh /etc/profile.d/
```

#### 启动

Start fcitx5 by go to "System settings" -> "Virtual keyboard" -> Select Fcitx 5

#### 配置

1. Do NOT set GTK_IM_MODULE environment variable.

2. For Gtk2, Add following content to ~/.gtkrc-2.0
    ```
    gtk-im-module="fcitx"
    ```
3. For Gtk 3, add following content to ~/.config/gtk-3.0/settings.ini
    ```
    [Settings]
    gtk-im-module=fcitx
    ```
4. For Gtk 4, add following content to ~/.config/gtk-4.0/settings.ini
    ```
    [Settings]
    gtk-im-module=fcitx
    ```

### 配置 SSH Server

```bash
paru -S openssh

# 修改配置（最好修改端口，默认的 22 端口容易被攻击）
kate /etc/ssh/sshd_config

sudo systemctl enable --now sshd
```

### 配置 KDE 启动时立刻锁定（配合 SDDM 自动登陆）

```bash
kate ~/.config/kscreenlockerrc
```

添加`LockOnStart=true`：
```
[Daemon]
Timeout=30
LockOnStart=true
```

## 软件安装

### WeChat
```
paru -S wechat
```

### QQ
```bash
paru -S slirp4netns linuxqq-nt-bwrap
mkdir -p ~/.config/QQ          # Bug: 需要手动创建这个文件夹，否则 QQ 启动时会闪退
cp ./home/.config/qq-bwrap-flags.conf ~/.config/
```

### 音乐软件
```bash
paru -S python-pyqt5-webengine feeluown-full
```