echo --------------------
efibootmgr | grep ubuntu
echo --------------------
echo
echo 若ubuntu的启动id为 0004，按 Enter 立即执行
echo 否则请 ctrl+c 然后输入：
echo
echo sudo efibootmgr --bootnext xxxx
echo
read -p Continue?

sudo efibootmgr --bootnext 0004
sudo reboot
