#!/usr/bin/env bash

logfile=reload.log
now=$(date +%Y%m%d\ %H:%M:%S)
maskToken="TYPE-TOKEN-HERE"
echo "Reloading at $now" >> $logfile

curl -H "Authorization: $maskToken" -X POST $URL/voluntario/reload >> $logfile 2>&1
