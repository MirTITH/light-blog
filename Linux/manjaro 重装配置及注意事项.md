# manjaro 重装配置及注意事项

## 重装配置

### 更新系统
```shell
# 换源
sudo pacman-mirrors -c China

#更新系统
sudo pacman -Syu
```

### 安装 AUR 助手等
```bash
# AUR 助手
sudo pacman -Ss yay

# v2raya，没有梯子寸步难行
yay -S v2raya-bin

sudo systemctl disable v2ray --now
sudo systemctl start v2raya.service
sudo systemctl enable v2raya.service

# 浏览器（没有梯子安装慢）
yay -S microsoft-edge-stable-bin

# 另一个 AUR 助手（没有梯子装不上）
yay -S paru-bin
```

```bash
# 编辑配置
kate /etc/pacman.conf /etc/makepkg.conf /etc/paru.conf
```

并进行如下修改：

| 文件         | 修改                               |
| ------------ | ---------------------------------- |
| pacman.conf  | 取消注释：`#Color`                 |
| makepkg.conf | MAKEFLAGS="-j2" -> MAKEFLAGS="-j8" |
| paru.conf    | 取消注释：`#BottomUp` `#SudoLoop`  |


### 删除 firefox
```bash
sudo pacman -Rs firefox

# 如果说会破坏依赖，可以尝试如下命令，删除软件包和所有依赖这个软件包的程序
sudo pacman -Rsc firefox
```

### 安装中文输入法
```bash
paru -S manjaro-asian-input-support-fcitx5 fcitx5-chinese-addons fcitx5-pinyin-zhwiki fcitx5-pinyin-moegirl
```

### 修改 grub
```bash
kate /etc/default/grub
```

### 安装 arm-none-eabi 套件
```bash
paru arm none eabi
# 然后选择安装需要的 arm-none-eabi-gcc arm-none-eabi-gdb arm-none-eabi-newlib
```

### 其他软件
- gdb
- cmake ninja
- linuxqq
- qqmusic
- netease-cloud-music
- noto cjk
- dotnet-runtime-6.0

> 另见 [linux 软件安装.md](linux%20软件安装.md)

### 禁用鼠标键盘唤醒
[ubuntu 重装配置.md](ubuntu%20重装配置.md##%20禁用鼠标键盘唤醒)

### reboot-to-manjaro.sh
```bash
mkdir ~/.local/bin
cp ./reboot-to-manjaro.sh ~/.local/bin/
```

## 注意事项

### 安装软件时密钥出错
Signature from "User <email@gmail.com>" is unknown trust, installation failed

<https://wiki.archlinuxcn.org/wiki/Pacman#Signature_from_%22User_%3Cemail@gmail.com%3E%22_is_unknown_trust,_installation_failed>