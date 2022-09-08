from DriverAgent import DriverAgent  # see DriverAgent repo
import urllib.request
import os

dlDir = os.getcwd()
agent = DriverAgent( dlDir )
agent.getBrowser()
driver = agent.driver

# example URL base where same int appears in two segments
urlBaseLi = [
    "https://www.c82.net/images/iconography/architecture/plate-",
    "/plate-",
    ".jpg"
    ]

imageXP = "/html/body/img"


def findMaxValid( pos ):
    def testValid( _pos ):
        try: driver.get( str( _pos ).join( urlBaseLi ) )
        except Exception as e:
            print( f'exc on get url: {type( e ).__name__}\n' )
            return False
        else:
            imgEC = agent.xpathEC( imageXP, waitLo=5, waitHi=6 )
            if not imgEC: return False
            else: return True
    
    valid = testValid( pos )
    maxValid = minFail = pos
    
    if valid:
        while valid:  # double valid until fail
            maxValid = pos
            pos = minFail = pos * 2
            valid = testValid( pos )
    else:
        while not valid:  # halve fails until valid
            minFail = pos
            pos = maxValid = pos - round( pos / 2 )
            valid = testValid( pos )
    
    while maxValid != minFail - 1:
        # set pos to min-max midpoint (rounded)
        pos = maxValid + round( (minFail - maxValid) / 2 )
        if testValid( pos ): maxValid = pos
        else: minFail = pos
    
    print( f"arrived at maxValid: {maxValid}\n" )
    
    return maxValid  # return max when bounds minFail


def requestImg( imgOb, pos ):
    try: src = imgOb.get_attribute( 'src' )
    except Exception as exc:
        print( f'exc on get src: {type( exc ).__name__}\n{exc}' )
        return False
    else:
        try: urllib.request.urlretrieve( src, f"imgs\\{str( pos )}.jpg" )
        except Exception as exc:
            print( f'exc on req img: {type( exc ).__name__}\n{exc}' )
            return False
    return True


def tryImgGet( dex ):
    try: driver.get( str( dex ).join( urlBaseLi ) )
    except Exception as e: print( f'exc on get url: {type( e ).__name__}\n{e}' )
    
    imgEC = agent.xpathEC( imageXP )
    if not imgEC: return False
    
    else: return requestImg( imgEC, dex )


# findMaxValid( 1 )  # 60
for i in range( 1, 60 ): tryImgGet( i )

driver.quit()
