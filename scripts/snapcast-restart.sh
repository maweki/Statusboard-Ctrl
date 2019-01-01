#!/bin/sh
# this should be nicer
ssh root@192.168.1.210 systemctl restart snapserver &
ssh root@192.168.1.210 systemctl restart snapclient &
ssh root@192.168.1.210 systemctl restart cpiped &
ssh root@192.168.1.202 systemctl restart snapclient &
ssh root@192.168.1.203 systemctl restart snapclient &
ssh root@192.168.1.40 systemctl restart snapclient &
wait
