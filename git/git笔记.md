# git 笔记

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

​	在子模块目录下`git pull`

> 以上方案完全等效

### 删除子模块

**删除子模块比较麻烦，需要手动删除相关的文件，否则在添加子模块时有可能出现错误**同样以删除 `GWToolkit` 子模块仓库文件夹为例：

1. 删除子模块文件夹

```bash
$ git rm --cached GWToolkit
$ rm -rf GWToolkit
```

2. 删除 `.gitmodules` 文件中相关子模块的信息，类似于：

```bash
[submodule "GWToolkit"]
        path = GWToolkit
        url = https://github.com/iphysresearch/GWToolkit.git
```

3. 删除 `.git/config` 中相关子模块信息，类似于：

```bash
[submodule "GWToolkit"]
        url = https://github.com/iphysresearch/GWToolkit.git
        active = true
```

4. 删除 `.git` 文件夹中的相关子模块文件

```bash
$ rm -rf .git/modules/GWToolkit
```