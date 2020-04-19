#!/usr/bin/env bash

logfile=reload.log
now=$(date +%Y%m%d\ %H:%M:%S)
maskToken="YOUR-TOKEN-HERE"
echo "Reloading at $now" >> $logfile
url="http://localhost:5000"
curl -H "Authorization: $maskToken" -X POST $url/voluntario/reload >> $logfile 2>&1le 2>&1
