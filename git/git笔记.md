# git 笔记

## GitHub 下载文件夹

右键点击文件夹，复制链接，粘贴进下面网址：

https://download-directory.github.io/

## 远程库

```bash
git remote      # 查看远程库名称
git remote -v   # 查看远程库地址
```

## git status 显示中文

```bash
git config --global core.quotepath false
```

## 子模块

> https://zhuanlan.zhihu.com/p/404615843

### 添加子模块

```bash
git submodule add <url> <repo_name>
```

> url: 远程库的地址
>
> repo_name: 创建的子目录名称，留空则为git仓库名称

例如：

```bash
git submodule add https://github.com/iphysresearch/GWToolkit.git GWToolkit
```

### 查看子模块

```bash
git submodule
```

### 更新子模块

更新项目内子模块到最新版本：

```bash
git submodule update
```

更新子模块为远程项目的最新版本

```bash
git submodule update --remote
```

### Clone包含子模块的项目

```bash
git clone --recursive <project url>
```

或

```bash
git clone --recurse-submodules <project url>
```

或

```bash
git clone <project url>
git submodule init
git submodule update
```

或

在子模块目录下`git pull`

> 以上方案完全等效

### 删除子模块

1. Run: 

    ```shell
    git rm <path-to-submodule>
    ```

2. Commit