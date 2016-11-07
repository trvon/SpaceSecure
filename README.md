# SpaceSecure

## Idea
The motivation behind SpaceSecure was to give network savvy and regular people an easy way to scan their network for vunerable IoT devices. SpaceSecure then tries to gain root access to the vunerable devices by trying to brute using defualt passwords and any similar hacker exploit imported into the code. Then when the program verifies root access and it gives the owner the option to change of devices password to something more secure. 

With other devices tested against exploits, it gives administrators a head start on patching devices that were previously unknown to be vunerable to the exploits tested them. We hope this inspires individuals to be more safe on the web, and to update freqently.

## Run the Application
Navigate to the build directory and execute the following command 
**./build.sh**

## About Importing Scripts
When importing scripts, make sure the scripts can take input of the device that they are going to be pointed at. ( RIght now the IP address is what is being outputed to the scripts on the run command ) After import scripts, the user simple needs to select the script they would like to run and the device they would like to run it against. 

### Needs to be added to Scripts
* Ability to see sucess of scripts in status bar. ( ex. Username, Password of sucessful brute force, or if device is vunerable to script/exploit )
* Ability to input Username and Password of devices, user already knows credentials for. 

## To Integrate
Drammer: A bot used to control android devices. More info on this can be found on 
1) https://www.vusec.net/projects/drammer/ 
2) https://vvdveen.com/publications/drammer.pdf


## Support
The program is supportable on linux devices and an windows machine with a command terminal emulator equipped with the correct scan utilities.

## Future Functionality
- [x] Add support for easy script import
- [ ] Working on adding default script library for testing in gui
- [ ] UI overhaul for a more compact program
- [ ] Add support for more devices, with a quick and easy install
- [ ] Add threading

~ More organization coming soon 

Authors
- [GitHub] (https://github.com/Paxion42) Paxion42
- [GitHub] (https://github.com/rahulr56) Rahul
- [GitHub] (https://github.com/Tremaux) Tremaux

Created at HackNC
