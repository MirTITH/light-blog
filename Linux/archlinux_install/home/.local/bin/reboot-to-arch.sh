#!/bin/bash

set -e

search_result=$(efibootmgr | grep Arch)
boot_id=${search_result:4:4}

# echo --------------------
# echo $search_result
# echo --------------------
# echo
# echo 若 ubuntu 的启动 id 为 $boot_id, 按 Enter
# echo 否则请 ctrl+c 然后输入： sudo efibootmgr --bootnext xxxx
# echo 
# read -p Continue?

sudo efibootmgr --bootnext $boot_id
sudo reboot
