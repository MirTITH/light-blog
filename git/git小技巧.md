# git 小技巧

## GitHub 下载文件夹

右键点击文件夹，复制链接，粘贴进该网址：<https://download-directory.github.io>

## 显示远程库

```bash
git remote      # 查看远程库名称
git remote -v   # 查看远程库地址
```

## git status 显示中文

```bash
git config --global core.quotepath false
```

## 忽略文件权限

有时候在 linux 中处理 exfat 或 NTFS 分区中的仓库时，会出现一大堆修改，使用 git diff 检查时，显示的是文件权限的更改。遇到此情况，可以忽略文件权限的更改。

```shell
git config core.fileMode false # 对单个仓库
git config --global core.fileMode false # 对全局
```

