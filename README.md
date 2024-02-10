
1. To run the deaups.py script, your network interface needs to be in monitoring mode to allow the script to create a capture file using airodump-ng. You only need to set monitoring mode network interface in the command with option i ( -i ). It will take approximately 14 seconds to capture the fish( wifi ESSID or wifi names ), and then the program will display their names. Then choose the target wifi name whatever you like.

2. You need to have python inquirer package.



Usage: python3 deaups.py -i ( interface )

Eg: python3 deaups.py -i wlan0mon



The program will work by sending DeAuth frames to the target client device for 25 seconds and then take a nap for 50 seconds. It will keep working correctly even if the channel could have been changed and will stop only when you manually terminate the process pressing 'Control + C' continuously. Have you ever seen the reliable DeAuth tools before!



Allow your neighbors to enjoy uninterrupted connectivity :3
