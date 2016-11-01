#!/bin/bash

function trap_ctrlc 
{
    #Show a terminal message to the user that Clean up is being performed.
    echo -e "\n\nKeyboard Interrupt"
    echo -e "Ctrl-C caught...performing clean up\n"

    # perform cleanup here
    rm -rf ./*.pyc ./*.txt
    # exit shell script with error code 2
    # if omitted, shell script will continue execution
    echo "Clean up finished!"
    echo "Exitting!!"
    exit 130
}

function main
{
	#Set up a trap to do clean up when the user presses Ctrl+C
	trap "trap_ctrlc" 2

	#Compile all python files and move it to build Directory
	python -m compileall ../src/
	mv ../src/*.pyc .
	
	#Start the Application
	python gui.pyc 2>/dev/null

	#Normal Clean Up once the application is closed
	rm -rf *.pyc *.txt
}


#Program execution starts here
main

