                      
1. To run the deaups.py script, your network interface needs to be in monitoring mode to allow the script to create the capture files using airodump-ng. You only need to set monitor mode network interface in the command with option i ( -i ). It will take approximately 14 seconds to capture the fish( wifi ESSID or wifi names ), and then the program will display their names. Then choose the target wifi name whatever you like.

2. You need to have Python's inquirer package.



3. Usage: python3 deaups.py -i ( interface )

4. Eg: python3 deaups.py -i wlan0mon



5. The program will work by sending DeAuth frames to the target client device for 25 seconds and then take a nap for 50 seconds. It will keep working correctly even if the channel has been changed and will stop only when you manually terminate the process by pressing 'Control + C' continuously. Is the target WiFi turned off during the attack? Don't worry about the program not continuing to work. It will wait for the target WiFi you selected to turn on again to resume the attack. Have you ever seen such reliable DeAuth tools before?



6. Allow your neighbors to enjoy uninterrupted connectivity :3
