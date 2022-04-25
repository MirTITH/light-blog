 #!/bin/bash

# 要压缩率后缀名写.tar.xz
# 要速度后缀名写.tar.gz

sudo tar -cvpaf \
/mnt/XY_disk/Backup/Ubuntu/kubuntu_backup@`date +%Y-%m-%d`.tar.xz \
--exclude=/proc \
--exclude=/tmp \
--exclude=/lost+found \
--exclude=/media \
--exclude=/mnt \
--exclude=/sys \
--exclude=/run \
/
