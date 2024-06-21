# Linux 实用命令和技巧

## 终端连接 wifi 

1. 列出网卡设备`nmcli d`

2. Enable WiFi (if disabled): Use `nmcli r wifi on`

3. scan for wifi networks:  `sudo iwlist scan`

4. List available networks: Use `nmcli d wifi list` to see a list of SSIDs, security types, and signal strength.

5. Connect to a network: 

   ```shell
   # 二选一：
   sudo nmcli --ask device wifi connect <SSID> # 询问密码
   sudo nmcli d wifi connect <SSID> password <password> # 直接指定密码
   ```

