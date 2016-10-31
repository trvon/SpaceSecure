import os

# defines and returns list of login/password combinations derived from the
# MIRAI exploit(https://github.com/jgamblin/Mirai-Source-Code)


def __commonAuthSetup():

    global authPairs
    authPairs.append(["root", "xc3511"])
    authPairs.append(["root", "vizxv"])
    authPairs.append(["root", "admin"])
    authPairs.append(["admin", "admin"])
    authPairs.append(["root", "888888"])
    authPairs.append(["root", "xmhdipc"])
    authPairs.append(["root", "default"])
    authPairs.append(["root", "juantech"])
    authPairs.append(["root", "123456"])
    authPairs.append(["root", "54321"])
    authPairs.append(["support", "support"])
    authPairs.append(["root", ""])
    authPairs.append(["admin", "password"])
    authPairs.append(["root", "root"])
    authPairs.append(["root", "12345"])
    authPairs.append(["user", "user"])
    authPairs.append(["admin", ""])
    authPairs.append(["root", "password"])
    authPairs.append(["admin", "admin1234"])
    authPairs.append(["root", "1111"])
    authPairs.append(["admin", "smcadmin"])
    authPairs.append(["admin", "1111"])
    authPairs.append(["admin", "1111"])
    authPairs.append(["root", "666666"])
    authPairs.append(["root", "password"])
    authPairs.append(["root", "1234"])
    authPairs.append(["666666", "666666"])
    authPairs.append(["888888", "888888"])
    authPairs.append(["ubnt", "ubnt"])
    authPairs.append(["root", "klv1234"])
    authPairs.append(["root", "Zte521"])
    authPairs.append(["root", "hi3518"])
    authPairs.append(["root", "jvbzd"])
    authPairs.append(["root", "anko"])
    authPairs.append(["root", "z1xx"])
    authPairs.append(["root", "7ujMko0vizxv"])
    authPairs.append(["root", "7ujMko0admin"])
    authPairs.append(["root", "system"])
    authPairs.append(["root", "ikwb"])
    authPairs.append(["root", "dreambox"])
    authPairs.append(["root", "user"])
    authPairs.append(["root", "realtek"])
    authPairs.append(["root", "0"])
    authPairs.append(["admin", "1111111"])
    authPairs.append(["admin", "1234"])
    authPairs.append(["admin", "12345"])
    authPairs.append(["admin", "54321"])
    authPairs.append(["admin", "123456"])
    authPairs.append(["admin", "7ujMko0admin"])
    authPairs.append(["admin", "pass"])
    authPairs.append(["admin", "meinsm"])
    authPairs.append(["tech", "tech"])


def loadCredFromFile():
    file = open("~/credentials.txt", "r")
    for line in file:
        cred = line.split()
        authPairs.append([cred[0], cred[1]])

# must be run once for other functions in the program to work(could fix
# later with try:catch), takes opitional runtime ARG for the location of
# the sql server, or uses a default location


def initialSetup():
    # commonAuthSetup()
    # global authDatabase = "AuthPairs.txt"
    print " "


# called by frontend to write a txt file of scanned devices on the network
# and their security status
def getDeviceList():
    # calls the SH script that scans the network
    os.system("/scripts/.discoverDevices.sh")

    # opens output recieved from script
    outputFile = open('connectedDevices.txt', 'r')
    returnList = [()]
    # iterates through the output file and pulls individaul info
    for row in outputFile:
        counter = 0
    while row[counter] != '\t':
        counter += 1
    firstString = row[:counter]
    startpoint = counter
    counter += 1
    while row[counter] != '\t':
        counter += 1
        secondString = row[startpoint:counter]
    startpoint = counter
    counter += 1
    while row[counter] != '\n':
        counter += 1
    thirdString = row[startpoint:counter]
    returnList.append([firstString, secondString, thirdString, 'untested'])
    outputFile.close()
    return returnList

# this should attempt to connect to target ip with the provided username
# and password combination, authcode[0] and authcode[1], and then change
# the password to newpass, returning false if the attempt fails


def secureTest(target):
    if os.system("/scripts/.sshVulnerabilityCheck.sh " + target) == 1:
        return True
    else:
        return False


# takes a list of IP's determined to be insecure and new passwords to
# replace them with.
def updatePasswords(changeTargets):
    for target in changeTargets:
        for pair in authPairs:
            if changeAttempt(target[0], target[1], pair) == True:
                break
# continues attempts until one is succesfull
