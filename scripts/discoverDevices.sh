#!/bin/bash


OUTPUT_FILE="connectedDevices.txt"

#Get a name for intermediate temporary file
REGEXP_IP='^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])0'
TEMPDIR=$(mktemp -d)
DATE=$(date +%d%m%y_%H%M%N | md5sum | awk '{print $1}')
TEMPFILE=$(echo "$TEMPDIR/$DATE")

#Start arp scanning
arp-scan -r 4 -l -t 2000  > "$TEMPFILE"
resp=$?
if [ $resp -eq 139 ]; then
	#Require Super User Permissions
    echo "Run the application as super-user or install arp-scan and try again!"
	exit 1
elif [ $resp -eq 1 ];then
    #Error in ARP-SCAN
    echo "Internal Error occured! Proceeding with the scanned devices!"
fi

#Format the arp output
grep -E '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])' "$TEMPFILE" > "$OUTPUT_FILE"

#delete the temporary filenames
rm -rf "$TEMPDIR"-
