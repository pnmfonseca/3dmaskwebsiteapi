#!/usr/bin/env bash

logfile=reload.log
now=$(date +%Y%m%d\ %H:%M:%S)
echo "Reloading at $now" >> $logfile
curl -s -H "Authorization: $MASK_TOKEN" -X POST $URL/voluntario/reload >> $logfile #2>&1
