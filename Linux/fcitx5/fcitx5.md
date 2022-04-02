# fcitx5 安装 

> https://plumz.me/archives/11740/?replyTo=125225

## 卸载fcitx

```bash
sudo apt purge *fcitx*
```

## 安装 fcitx5

```sudo
sudo add-apt-repository ppa:hosxy/fcitx5
sudo apt-get update
sudo apt install fcitx5 fcitx5-frontend-qt5 fcitx5-frontend-gtk3 fcitx5-frontend-gtk2 fcitx5-chinese-addons
```

## 配置 fcitx5

将fcitx5 文件夹复制到 ~/.config/

```bash
cp -r fcitx5 ~/.config/
```



## 安装词典

中文维基

https://github.com/felixonmars/fcitx5-pinyin-zhwiki

萌娘百科

https://github.com/outloudvi/mw2fcitx/releases



Copy into ~/.local/share/fcitx5/pinyin/dictionaries/ (create the folder if it does not exist)

```
mkdir -p ~/.local/share/fcitx5/pinyin/dictionaries/
```

## 安装皮肤

> https://www.cnblogs.com/maicss/p/15056420.html

```bash
mkdir -p ~/.local/share/fcitx5/themes/
cp -r fcitx5-simple-themes/* ~/.local/share/fcitx5/themes
gedit ~/.config/fcitx5/conf/classicui.conf
# 修改为 Simple-white 或 Simple-dark
```

## 启用fcitx5

```bash
im-config
```

然后选择fcitx5 
