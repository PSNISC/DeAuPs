1. Run the script in a full-screen terminal.

2. To run the deaups.py script, your network interface needs to be in monitoring mode to allow the script to create a capture file using airodump-ng. You only need to set monitoring mode network interface in the command with option i ( -i ). It will take approximately 11 seconds to capture the fish( wifi ESSID or wifi names ), and then the program will display their names. Then choose the one whatever you like.

3. You need to have python inquirer package.



Usage: python3 deaups.py -i ( interface )

Eg: python3 deaups.py -i wlan0mon



The program will work by sending DeAuth frames to the target client device for 25 seconds and then take a nap for 1 minute. It will loop indefinitely even if the channel could have been changed and will stop only when you manually terminate the process using 'Control + C' or 'Control + Z'. Have you ever seen the reliable DeAuth tools before!



Allow your neighbors to enjoy uninterrupted connectivity :3
