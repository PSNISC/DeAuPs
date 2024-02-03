To run the kidWifi.py script, your network interface needs to be in monitoring mode to allow the script to create a capture file using airodump-ng -i IF(interface).

After you run 'python3 kidWifi.py' in your terminal, two prompts will appear, requesting the network interface and the ESSID (WiFi name) to target. Note: (Requires 'wlan0' or 'wlan0mon' for the network interface and the ESSID).

The program will work by sending DeAuth frames to the target client device for 20 seconds and then take a nap for 1 minute.

Allowing your neighbors to enjoy uninterrupted connectivity :3
