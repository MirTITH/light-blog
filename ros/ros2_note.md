# ROS 2 笔记

## 安装

见 [linux 开发软件安装.md](../Linux/linux%20开发软件安装.md) ROS 2 部分

（建议也安装 colcon mixin，方法同见 [linux 开发软件安装.md](../Linux/linux%20开发软件安装.md)）

## vscode debug 方法

>  先安装 colcon mixin 和 VSCode 的 ROS，C/C++ 扩展

1. 使用 colcon 编译，确保是 debug 版本：

   ```shell
   # 执行下面的命令需要安装 colcon mixin
   # debug: debug 编译
   # compile-commands: 编译时生成 compile_commands.json，使得 vscode clangd 插件能够智能提示（不使用 clangd 时可以不加）
   colcon build --symlink-install --mixin debug compile-commands
   ```

2. 正常运行需要 Debug 的节点
3. 在VS Code左侧的`运行和调试`页面添加 ROS Attach
4. 启动调试，并选择对应的进程
5. 允许使用管理员权限以调试进程

如果不想每次都输入密码，可以执行：

```shell
# 临时设置，重启后失效
sudo sysctl -w kernel.yama.ptrace_scope=0
```

To permanently change the value of `kernel.yama.ptrace_scope` to 0, you can edit the file `/etc/sysctl.d/10-ptrace.conf` and change the line `kernel.yama.ptrace_scope = 1` to `kernel.yama.ptrace_scope = 0`. You will then need to reboot your system for the change to take effect.
