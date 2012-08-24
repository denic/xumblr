import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,os

#set our library path
print xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ))
sys.path.append (xbmc.translatePath( os.path.join( os.getcwd(), 'plugin.image.xumblr', 'resources', 'lib' ) ))
import tumblr

thisPlugin = int(sys.argv[1])

# ---------- Settings ----------

BLOG=xbmcplugin.getSetting(thisPlugin, 'blog')
EMAIL=xbmcplugin.getSetting(thisPlugin, 'email')
PASSWORD=xbmcplugin.getSetting(thisPlugin, 'password')
LIMIT=xbmcplugin.getSetting(thisPlugin, 'limit')

# ---------- 

def CATEGORIES():
      addDir("Dashboard","",1,"")
      
def INDEX(url):
  images = tumblr.dashboard(EMAIL, PASSWORD, LIMIT)

  i=0
  for p in images['posts']:
    i+=1
    addImage(p['tumblelog']['name'] + " at " + p['date'], p['photo-url-1280'])
  
def addDir(name,url,mode,iconimage):
  u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
  ok = True
  liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png",thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name })
  ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
  return ok  
  
def addImage(name, url):
  ok = True
  liz = xbmcgui.ListItem(name)
  liz.setInfo(type="Image", infoLabels={ "Title": name })
  ok=xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url, listitem=liz)
  return ok
  
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

params=get_params()

url=None
name=None
mode=None

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

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None:
  print ""
  CATEGORIES()
       
elif mode==1:
  print ""+url
  INDEX(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))