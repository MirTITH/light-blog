# git 笔记

## GitHub 下载文件夹

右键点击文件夹，复制链接，粘贴进下面网址：

https://download-directory.github.io/

## 显示远程库

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

```shell
git submodule update
```

更新子模块为远程项目的最新版本

```shell
git submodule update --remote
```

### Clone包含子模块的项目

#### 基本用法

```shell
git clone --recursive <project url>
```

或

```shell
git clone --recurse-submodules <project url>
```

或

```shell
git clone <project url>
git submodule init
git submodule update
```

或

在子模块目录下`git pull`

> 以上方案完全等效

#### 进阶用法

```shell
git clone --recurse-submodules -b v1.64.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc
```

解释：

1. `--recurse-submodules`：这个选项告诉 Git 在克隆仓库时，同时初始化并更新任何子模块。子模块是 Git 仓库中的其他 Git 仓库。
2. `-b v1.64.0`：这个选项指定要克隆的仓库的分支或标签。在这个例子中，是克隆 `v1.64.0` 标签。
3. `--depth 1`：这个选项用于执行浅克隆，只获取指定深度的提交历史。在这个例子中，只克隆最新的一次提交。这样可以减少克隆的时间和空间。
4. `--shallow-submodules`：这个选项用于对子模块也执行浅克隆，只获取指定深度的提交历史。
5. `https://github.com/grpc/grpc`：这是要克隆的远程仓库的 URL。

### 删除子模块

1. Run: 

    ```shell
    git rm <path-to-submodule>
    ```

2. Commit

### 克隆子模块出现网络错误如何重试

```shell
git submodule update --init --recursive --depth 1
```

如果不希望执行浅克隆，可以删除 `--depth 1`

