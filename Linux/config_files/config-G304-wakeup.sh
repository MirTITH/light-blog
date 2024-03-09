#!/bin/bash

# From lsusb: Bus 005 Device 008: ID 046d:c53f Logitech, Inc. USB Receiver
idVendor=046d
idProduct=c53f

# Get sys device path by vendorId and productId
function find_device()
{
    local vendor=$1
    local product=$2
    vendor_files=( $(egrep --files-with-matches "$vendor" /sys/bus/usb/devices/*/idVendor) )
    for file in "${vendor_files[@]}"; do
       local dir=$(dirname "$file")
       if grep -q -P "$product" "$dir/idProduct"; then
         printf "%s\n" "$dir"
         return
       fi
    done
}

sysdev=$(find_device $idVendor $idProduct)

if [ ! -r "$sysdev/power/wakeup" ]; then
    echo $idVendor:$idProduct not found 1>&2
    exit 1
fi

case "$1" in
    enabled|disabled)
    echo $1 > "$sysdev/power/wakeup"
    ;;
    *)
    echo "$0 enabled   -- to enable the wakeup for this device"
    echo "$0 disabled  -- to disable the wakeup for this device"
    ;;
esac

grep --color=auto -H ".*" "$sysdev/power/wakeup"
exit 0