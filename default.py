import urllib,urllib2,re,xbmc,xbmcaddon,xbmcgui,os,sys,shutil
from elementtree.SimpleXMLWriter import XMLWriter
import word_resolver

settings = xbmcaddon.Addon( id = 'script.service.twitter' )
twitter_icon = os.path.join( settings.getAddonInfo( 'path' ), 'thumbnails', 'twitter-icon.png' )
userdata = xbmc.translatePath('special://userdata/keymaps')
twitter_file = os.path.join(userdata, 'twitter.xml')
default_twitter_file = os.path.join( settings.getAddonInfo( 'path' ), 'default_keymap.xml' )

if not os.path.exists(twitter_file):
	shutil.copy(default_twitter_file, twitter_file)
	xbmc.sleep(1000)
	xbmc.executebuiltin('Action(reloadkeymaps)')




def _record_key():
    	dialog = KeyListener()
    	dialog.doModal()
    	key = dialog.key
    	del dialog
	w = XMLWriter(twitter_file, "utf-8")
	doc = w.start("keymap")
	w.start("global")
	w.start("keyboard")
        w.element("key", "addon.opensettings(script.service.twitter)", id=str(key))
	w.end()
	w.end()
	w.start("fullscreenvideo")
	w.start("keyboard")
	w.element("key", "addon.opensettings(script.service.twitter)", id=str(key))
	w.end()
	w.end()
	w.end()
	w.close(doc)

class KeyListener(xbmcgui.WindowXMLDialog):
  def __new__(cls):
    return super(KeyListener, cls).__new__(cls, "DialogKaiToast.xml", "")
  
  def onInit(self):
    try:
      self.getControl(401).addLabel('Twitter Settings')
      self.getControl(402).addLabel('Press the key you want to assign now')
    except:
      self.getControl(401).setLabel('Twitter Settings')
      self.getControl(402).setLabel('Press the key you want to assign now')
  
  def onAction(self, action):
    self.key = action.getButtonCode()
    self.close()

class TextBox:
    # constants
    WINDOW = 10147
    CONTROL_LABEL = 1
    CONTROL_TEXTBOX = 5

    def __init__(self, *args, **kwargs):
        # activate the text viewer window
        xbmc.executebuiltin("ActivateWindow(%d)" % ( self.WINDOW, ))
        # get window
        self.win = xbmcgui.Window(self.WINDOW)
        # give window time to initialize
        xbmc.sleep(1000)
        self.setControls()

    def setControls(self):
        # set heading
        heading = "Twitter Feeds by Romans I XVI"
        self.win.getControl(self.CONTROL_LABEL).setLabel(heading)
        # set text
        root = settings.getAddonInfo( 'path' )
        faq_path = os.path.join(root, 'instructions.txt')
        f = open(faq_path)
        text = f.read()
        self.win.getControl(self.CONTROL_TEXTBOX).setText(text)

try:
	if sys.argv[1] == 'set_key':
		_record_key() 
		xbmc.sleep(1000)
		xbmc.executebuiltin('Action(reloadkeymaps)')
		sys.exit(0)
except:
	pass

try:
	if sys.argv[1] == 'display_file':
		TextBox()
except:
	pass

if (not settings.getSetting("firstrun")):
	dialog = xbmcgui.Dialog()
	dialog.ok('Twitter Feeds','I will now open your twitter settings.','You can access these settings at any time using', 'the twitter hotkey. (Default "t")')
	settings.openSettings()
        settings.setSetting("firstrun", "1")


while (not xbmc.abortRequested):


	try:
		if sys.argv[1] == 'display_file':
			go = False
		if sys.argv[1] == 'set_key':
			go = False
	except:
		go = True

	if go == True:
		if settings.getSetting("enable_service") == 'true':
			try:
				old_text = old_text
			except:
				old_text = ''
			language = settings.getSetting('language')
			language = re.sub("( \(.*?\))", "", language)
			language = word_resolver.lang(language)
			search_string = settings.getSetting("search_string")
			search_string = word_resolver.searchstr(search_string)
			if language != 'all':
				search_string = search_string + '%20lang%3A'+language
			xbmc.log('Twitter Search '+search_string)
			display_time = settings.getSetting("display_time")
			display_time = str(display_time)+'000'
			display_time = int(display_time)
			wait_time = settings.getSetting("wait_time")
			wait_time = str(wait_time)+'000'
			wait_time = int(wait_time)
			req = urllib2.Request('http://www.twitter.com/search?q='+search_string+'&f=realtime')
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()
			try:
				name=re.compile('data-screen-name="(.+?)" data-name="(.+?)"').findall(link)
				name=str(name[0])
				name=re.compile("'(.+?)'").findall(name)
				dispname=str(name[1])
				dispname=word_resolver.name(dispname)
				text=re.compile('<p class="js-tweet-text tweet-text">(.+?)</p>').findall(link)
				text=text[0]
				text = word_resolver.text(text)
				if old_text != text:
					xbmc.executebuiltin('XBMC.Notification("%s","%s",%d,"%s")' % (dispname+'  @'+str(name[0]), text, display_time, twitter_icon))
					xbmc.sleep(wait_time)
					old_text = text
				else:
					xbmc.sleep(500)
			except:
				xbmc.executebuiltin('XBMC.Notification("Search Error", "No Results")')
				xbmc.sleep(500)			
		
		else:
			xbmc.sleep(1000)
	

