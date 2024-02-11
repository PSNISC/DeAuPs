# 𝘿𝙀𝘼𝙐𝙋𝙎

## Deauthentication tool

<br>

- ***Aircrack-ng suite gets used in this tool.***

<br>

- To run the tool, your network interface needs to be in monitoring mode to allow the tool to create the capture files using `airodump-ng`. You only need to set monitor mode network interface in the command with option i ( -i ) after installing. It will take approximately 14 seconds to capture the fish( wifi ESSID or wifi names ), and then the tool will display their names. Then choose the target wifi name whatever you like.

<br>

- ###You need to have Python's inquirer package. ( `pip install inquirer` )

<br>

```python


1. git clone https://github.com/PSNISC/DeAuPs.git


```

```python


2. cd DeAuPs


```

```python


3. python3 install.py


```


<br>


- After running   `python3 install.py`, you will see the message saying that you can start using the `deaups` command. Now `deaups` command is available to use.

<br>


```python


deaups -i <interface>


```

<br>


- *The program will work by sending DeAuth frames to the target client device for 25 seconds and then take a nap for 50 seconds. It will automatically create a directory in the current directory where you run `deaups -i <interface>` after running the script and will create the needed files ( targetBssid.py, targetChannel.py, etc... ) in the created directory. It will continue to work correctly even if the channel has been changed and will stop only when you manually terminate the process by continuously pressing 'Control + C'. Is the target WiFi turned off during the attack? Don't worry about the program not continuing to work. It will wait for the target WiFi you selected to turn on again to resume the attack. Have you ever seen such reliable DeAuth tools before?*

<br>


- Allow your neighbors to enjoy uninterrupted connectivity 😸

<br>
