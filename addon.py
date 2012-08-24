import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,os,xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.image.xumblr')
__language__ = __settings__.getLocalizedString
__home__ = __settings__.getAddonInfo('path')

# set our library path
sys.path.append (xbmc.translatePath( os.path.join(__home__, 'resources', 'lib')))

# import tumblr module
import tumblr

thisPlugin = int(sys.argv[1])

# ---------- Settings ----------

BLOG=xbmcplugin.getSetting(thisPlugin, 'blog')
EMAIL=xbmcplugin.getSetting(thisPlugin, 'email')
PASSWORD=xbmcplugin.getSetting(thisPlugin, 'password')
LIMIT=xbmcplugin.getSetting(thisPlugin, 'limit')

# ---------- Callbacks ----------

def CATEGORIES():
      addDir("Dashboard","",1,"")
      
def DASHBOARD():
  images = tumblr.dashboard(EMAIL, PASSWORD, LIMIT)

  i=0
  for p in images['posts']:
    i+=1
    addImage(p['tumblelog']['name'] + " at " + p['date'], p['photo-url-1280'])

# ---------- List handlers ----------
  
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

# Parameters
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


# ---------- Main ----------

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

# some debugging output
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

# ####################
# Routing
# ####################
if mode==None:
  CATEGORIES()
       
elif mode==1:
  DASHBOARD()


xbmcplugin.endOfDirectory(int(sys.argv[1]))