#set text(font: "Sarasa Fixed SC", lang: "zh", region: "cn")
#show link: set text(fill: blue)
#set heading(numbering: "1.")
#set document(
  title: [使用Rust进行ESP32开发的工具链安装和配置],
)
#set par(
  first-line-indent: (
    amount: 2em,
  ),
  justify: true,
)

#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.8": *
#codly(languages: codly-languages)
#show: codly-init.with()

#title()

= Rustup 安装
#h(2em) 使用Rust进行ESP32开发，首先需要安装Rustup来管理cargo、rust编译器等。可以使用包管理器安装Rustup,例如使用Paru：
```shell
paru -S rustup
```
或者在#link("https://rust-lang.org/zh-CN/learn/get-started/")[官网]找到其他安装方式。

= 其他Rust编译器安装

#h(2em) 完成上一步后，通常会自动安装针对本地系统的最新稳定版Rust编译器。如果需要安装特定版本的Rust编译器，可以使用Rustup来安装，例如，安装nightly版本：
```shell
rustup install nightly
```
#h(2em) 目前的ESP32主要有两种架构：Xtensa和RISC-V。对于不同的架构，需要安装对应的交叉编译工具链。

== RISC-V架构
#h(2em) 对于RISC-V架构的ESP32芯片，可以直接使用Rustup安装RISC-V交叉编译工具链：
```shell
rustup target add riscv32imc-unknown-none-elf
```
#text(fill: gray)[对于某些稍新一些的芯片，可能略有不同，如`riscv32imac-unknown-none-elf`等。]

== Xtensa架构
#h(2em) 对于Xtensa架构的ESP32芯片，目前Rust官方并未提供直接支持。因此，需要使用乐鑫科技提供的`espup`工具来安装对应的交叉编译工具链。 首先，安装`espup`：
```shell
cargo install espup
```
然后，使用`espup`安装Xtensa交叉编译工具链：
```shell
espup install
```
这将自动下载并配置适用于ESP32的Xtensa交叉编译工具链。然后需要配置两个环境变量，`espup`会在安装完成后生成脚本（通常是`$HOME/export-esp.sh`），根据脚本内容为各shell配置环境变量。在终端中输入以下命令验证安装和配置是否成功：
```shell
xtensa-esp32-elf-gcc --version
$env.LIBCLANG_PATH
```

= 安装开发流工具

使用Cargo安装模板工程生成工具`esp-generate`和烧录工具`espflash`：
```shell
cargo install esp-generate espflash
```

= 其他工具

== Wokwi 仿真器
Wokwi的VSCode扩展允许在本地开发环境中使用Wokwi仿真器进行ESP32开发。可以从#link("vscode:extension/wokwi.wokwi-vscode")[VSCode扩展市场]安装该扩展，并按照提示在网页中登录账号并键入License Key以启用仿真功能。