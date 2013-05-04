import urllib,urllib2,urlparse,re,sys,xbmcplugin,xbmcgui
import cookielib,os,string,cookielib,StringIO
import os,time,base64,logging,calendar
import xbmcaddon
from xml.dom.minidom import parse, parseString
#Willow TV
wtv=xbmcaddon.Addon(id='plugin.video.willowtv')

addonPath=wtv.getAddonInfo('path')
artPath=addonPath+'/resources/art'
defaultIconImg=os.path.join(xbmc.translatePath( artPath ), "cricket-icon.png") 

login = 'http://m.willow.tv/Login_jq.asp'
loginSuccess = False
cookiejar = cookielib.LWPCookieJar()
cookiejar = urllib2.HTTPCookieProcessor(cookiejar) 

def loginWillowTV(url):
        try:
                print url
                opener = urllib2.build_opener(cookiejar)
                urllib2.install_opener(opener)
                email = wtv.getSetting('email')
                pwd = wtv.getSetting('password')
                values = {'Email': email,'Password': pwd, 'KeepSigned': 'true', 'LoginFormSubmit': 'true'}
                headers = { 'User-Agent' : 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3' }
                data = urllib.urlencode(values)
                req = urllib2.Request(url, data, headers)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                web = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
                match=re.compile('Your email or password is incorrect').findall(web)
                if(len(match)>0):
                        d = xbmcgui.Dialog()
                        d.ok('Login Failed', 'Error: Your email or password is incorrect.','Please verify your login details.')
                        return False
                else:
                        loginSuccess =  True
                        return True
        except:
                d = xbmcgui.Dialog()
                d.ok('LOGIN Failed', 'Its not your fault. BREAK TIME!','Please go out of Willow TV and try again.')
                return False

def HOME():
	
	addDir('Live Matches','willow',1,os.path.join(xbmc.translatePath( artPath ), "refresh.png"),'')


def GETMATCHES ():
	
	try:
		url = 'http://m.willow.tv/iOS.asp?e=#animations'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		myweb = link
		myweb = ''.join(link.splitlines()).replace('\t','').replace('\'','"').replace('\r','')
		
		# myRegex = re.compile('<ul class=\'edit rounded\'><li><font color=\'#AA0000\'>.+</font><hr /><br /><font color=\'\'>(.+?)</font><br /><br /><br /><font color=\'black\'><video controls width=\'320\' height=\'240\' x-webkit-airplay=\'allow\' src=\'(.+?)\'></video>')

		myRegex2 = re.compile('<font color="black"><a.+?href="(.+?)" rel="external" class="submit whiteButton">(.+?)</a></font>');
		
		myRegex = re.compile('<ul class="edit rounded"><li>.+><font color="">(.+?)</font><br /><br /><br /><font color="black">(.+?)</ul>');
		
		
		
		print "Looking for matches"
		match = myRegex.findall(myweb)
		
		for matchName,videoLinks in match:
			print " Found MATCH: " + str(matchName)
			sources = myRegex2.findall(videoLinks)
			counter = 1 
			for streamURL,sourceName in sources:
				print " Found Source: " + str(sourceName)
				addLink(matchName + " - Source " + str(counter)  ,streamURL,'','');
				counter = counter + 1
	
	
	except:
        	raise
        	xbmc.executebuiltin("XBMC.Notification(Willow TV is DOWN,Please use WILLOW TV [BACKUP PLAN],5000,)")
				        

def addLink(name,url,iconimage,fanart=''):
        if(iconimage == ''):
                iconimage = defaultIconImg
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        if(fanart==''):
                fanart=os.path.join(xbmc.translatePath( artPath ), "lords.jpg")
        liz.setProperty('fanart_image',fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage,fanart):
        if(iconimage == ''):
                iconimage = defaultIconImg
        if (url == None and mode == None ):
		u=sys.argv[0]
	else:
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        if(fanart==''):
                fanart=os.path.join(xbmc.translatePath( artPath ), "lords.jpg")
        liz.setProperty('fanart_image',fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addDirWithOption(name,url,option,mode,iconimage,fanart):
        if(iconimage == ''):
                iconimage = defaultIconImg
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&option="+urllib.quote_plus(option)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        if(fanart==''):
                fanart=os.path.join(xbmc.translatePath( artPath ), "lords.jpg")
        liz.setProperty('fanart_image',fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
def unescape(url):
        htmlCodes = [
                ['&', '&amp;'],
                ['<', '&lt;'],
                ['>', '&gt;'],
                ['"', '&quot;'],
        ]
        for code in htmlCodes:
                url = url.replace(code[1], code[0])
        return url

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


def check_settings():
        email = wtv.getSetting('email')
        pwd   = wtv.getSetting('password')
        if (not email or email == '') or (not pwd or pwd == ''):
                d = xbmcgui.Dialog()
                d.ok('Welcome to Willow TV', 'To watch LIVE CRICKET on your favorite Willow TV,','please provide your login details for both Willow TV and YouTube.')
                wtv.openSettings(sys.argv[ 0 ]) 

params=get_params()
url=None
name=None
option=None
mode=None
lastPageNbr=None


check_settings()
email = wtv.getSetting('email')
pwd = wtv.getSetting('password')

if not loginSuccess == True :
	print "$$$$ Login"	
	loginCheck = loginWillowTV(login)

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        option=params["option"]
except:
        pass
try:
        lastPageNbr=int(params["lastPageNbr"])
except:
        pass

print "Params : " + str(params) + " and URL : "+ str(url)


if mode==None or url==None or len(url)<1:
        HOME()

elif mode==1:
	GETMATCHES()	
		
		

xbmcplugin.endOfDirectory(int(sys.argv[1]))
