#   __  ___ _       __  __ 
 /  )(_  /_| /  //__)(   
/(_/ /__(  |(__//   __)  
𝒯𝒽ℯ 𝓇ℯ𝓁𝒾𝒶𝒷𝓁ℯ

## Deauthentication tool

- ***This tool is based on aircrack-ng suite.***

- To run the deaups.py script, your network interface needs to be in monitoring mode to allow the script to create the capture files using airodump-ng. You only need to set monitor mode network interface in the command with option i ( -i ). It will take approximately 14 seconds to capture the fish( wifi ESSID or wifi names ), and then the program will display their names. Then choose the target wifi name whatever you like.

- You need to have Python's inquirer package. ( pip install inquirer )


- Usage: python3 deaups.py -i ( interface )


```python


Eg: python3 deaups.py -i wlan0mon


```

- The program will work by sending DeAuth frames to the target client device for 25 seconds and then take a nap for 50 seconds. It will automatically create a directory in the current directory after running the script and will write the needed files ( targetBssid.py, targetChannel.py, etc... ) in the created directory. It will continue to work correctly even if the channel has been changed and will stop only when you manually terminate the process by continuously pressing 'Control + C'. Is the target WiFi turned off during the attack? Don't worry about the program not continuing to work. It will wait for the target WiFi you selected to turn on again to resume the attack. Have you ever seen such reliable DeAuth tools before?


- Allow your neighbors to enjoy uninterrupted connectivity :3
