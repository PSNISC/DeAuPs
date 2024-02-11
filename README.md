# 𝘿𝙀𝘼𝙐𝙋𝙎

## Deauthentication tool

- ***This tool is based on aircrack-ng suite.***

- To run the deaups.py script, your network interface needs to be in monitoring mode to allow the script to create the capture files using airodump-ng. You only need to set monitor mode network interface in the command with option i ( -i ). It will take approximately 14 seconds to capture the fish( wifi ESSID or wifi names ), and then the program will display their names. Then choose the target wifi name whatever you like.

- You need to have Python's inquirer package. ( ```python pip install inquirer ``` )


```python


1. git clone https://github.com/PSNISC/DeAuPs.git

2. cd DeAuPs

3. python3 install.py



```

- After running   ```python3 install.py```, you will see the message saying you can start use the ```deaups``` command. Now ```deaups``` command is available to use.

- ```deaups -i <interface>```

- The program will work by sending DeAuth frames to the target client device for 25 seconds and then take a nap for 50 seconds. It will automatically create a directory in the current directory after running the script and will write the needed files ( targetBssid.py, targetChannel.py, etc... ) in the created directory. It will continue to work correctly even if the channel has been changed and will stop only when you manually terminate the process by continuously pressing 'Control + C'. Is the target WiFi turned off during the attack? Don't worry about the program not continuing to work. It will wait for the target WiFi you selected to turn on again to resume the attack. Have you ever seen such reliable DeAuth tools before?


- Allow your neighbors to enjoy uninterrupted connectivity :3
