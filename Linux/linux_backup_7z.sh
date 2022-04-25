 #!/bin/bash

backup_file_path=/mnt/XY_disk/Backup/Ubuntu/kubuntu_backup@`date +%Y-%m-%d`.tar.7z

echo "Backup start."

echo "Writing to $backup_file_path"

sudo tar -cpf - \
--exclude=/proc \
--exclude=/tmp \
--exclude=/lost+found \
--exclude=/media \
--exclude=/mnt \
--exclude=/sys \
--exclude=/run \
/ \
| 7za a -si -t7z -m0=lzma2 -mx=9 -mfb=64 -md=64m -ms=on \
$backup_file_path

echo "Backup end."
echo "Backup file saved in $backup_file_path"
