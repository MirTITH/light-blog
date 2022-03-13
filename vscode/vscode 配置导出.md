# vscode 配置导出

> by TITH


## 设置与快捷键导出

vscode 设置界面 -> 打开设置(json)（在右上角）

## 插件导出

> https://blog.csdn.net/weixin_35744067/article/details/112361132

列出所有已安装的扩展：

```bash
code --list-extensions >> vs_code_extensions_list.txt
```

安装扩展：

```bash
cat vs_code_extensions_list.txt | xargs -n 1 code --install-extension
```
