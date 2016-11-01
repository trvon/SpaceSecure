#!/bin/bash


OUTPUT_FILE="./connectedDevices.txt"

#Get a name for intermediate temporary file
TEMPDIR=$(mktemp -d)
DATE=$(date +%d%m%y_%H%M%N | md5sum | awk '{print $1}')
TEMPFILE=$(echo "$TEMPDIR/$DATE")

#Start arp scanning
arp-scan -l > "$TEMPFILE"
if [ $? -ne 0 ]; then
	echo "Run the application as super-user or install arp-scan and try again!"
	exit 1
fi

#Format the arp output
grep -E '^[0-9]{3}\.[0-9]+' "$TEMPFILE" > "$OUTPUT_FILE"

#delete the temporary files
rm -rf "$TEMPDIR"-