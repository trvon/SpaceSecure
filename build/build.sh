#!/bin/bash

function trap_ctrlc 
{
    #Show a terminal message to the user that Clean up is being performed.
    echo -e "\n\nKeyboard Interrupt"
    echo -e "Ctrl-C caught...performing clean up\n"

    # perform cleanup here
    if [[ -f ./*.pyc ]] || [[ -f ./*.txt ]] ; then
		rm -rf ./*.pyc ./*.txt
    	# exit shell script with error code 2
    	# if omitted, shell script will continue execution
    	echo "Clean up finished!"
	fi
    echo "Exitting!!"
    exit 130
}

function checkCompatability
{
    #Check if arp-scan is installed on the system
    which arp-scan > /dev/null
    if [ $? -ne 0 ];then
        echo -e "\nInstall arp-scan and then try again!"
        exit 1
    fi

    #check if sshpass is installed on the system
    which sshpass > /dev/null
    if [ $? -ne 0 ];then
        echo -e "\nInstall sshpass and then try again!"
        exit 0
    fi
	
    # which python-tk > /dev/null
    #if [ $? -ne 0 ]; then 
    #    echo -e "\nInstall python-tk and then try again"
    #    exit 0
    #fi
}

function main
{
    #Set up a trap to do clean up when the user presses Ctrl+C
    trap "trap_ctrlc" 2
    
    checkCompatability
    #Compile all python files and move it to build Directory
    python -m compileall ../src/*
    if [ -d ../src/__pycache__ ] ; then 
		mv -f ../src/__pycache__/*.pyc .
	else
		mv -f ../src/*.pyc .
	fi
    
    if [ ! -d ../src/import  ]; then
        mkdir ../src/import
    fi
    
    #Start the Application
	gui=$(ls | grep gui)
	python $gui #2>/dev/null

    #Normal Clean Up once the application is closed
    rm -rf *.pyc *.txt
}


#Program execution starts here
main

