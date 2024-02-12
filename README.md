# 𝘿𝙀𝘼𝙐𝙋𝙎

## Deauthentication tool

<br>

- ***Aircrack-ng suite gets used in this tool.***

<br>

- To run deaups tool, your network interface needs to be in monitoring mode to allow the tool to create the capture files using `airodump-ng`. You only need to set monitor mode network interface in the command with option i ( -i ) after installing. It will take approximately 14 seconds to capture the fish( wifi ESSID or wifi names ), and then the tool will display their names. Then choose the target wifi name whatever you like.

<br>

- You need to have Python's inquirer package. ( `pip install inquirer` )

<br>

<br>

***

***To use this tool, there are only 4 steps to configure. As a first step,***

<br>

1. run the following command in your terminal.

```pythongit clone https://github.com/PSNISC/DeAuPs.git```

<br>

<br>


2. Go to the `DeAuPs` directory with `cd`( change directory ) commnad.


```python


cd DeAuPs


```

<br>

<br>

3. In order to use `deaups` command instead of `python3 install.py`, run the following command in the `DeAuPs` directory.

```python


python3 install.py


```


<br>

<br>

4. Now, run the tool with `deaups` command.


```python


deaups -i <interface>


```
<br>

***

## ***How does deaups tool work?***

<br>

- *The tool will work by sending DeAuth frames to the target client device for 25 seconds and then take a nap for 50 seconds. It will automatically create a directory in the current directory where you run `deaups -i <interface>` after running the script and will create the needed files ( targetBssid.py, targetChannel.py, etc... ) in the created directory. It will continue to work correctly even if the channel has been changed and will stop only when you manually terminate the process by continuously pressing 'Control + C'. Is the target WiFi turned off during the attack? Don't worry about the program not continuing to work. It will wait for the target WiFi you selected to turn on again to resume the attack. Have you ever seen such reliable DeAuth tools before?*

<br>


- Allow your neighbors to enjoy uninterrupted connectivity 😸

<br>
