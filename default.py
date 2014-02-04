import urllib,urllib2,re,xbmc,xbmcaddon,os


settings = xbmcaddon.Addon( id = 'script.program.twitter' )
twitter_icon = os.path.join( settings.getAddonInfo( 'path' ), 'thumbnails', 'twitter-icon.png' )




##################################################################################################################################

def MAIN(old_text=''):
	req = urllib2.Request('http://www.twitter.com/search?q=%23bachelor&f=realtime')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	text=re.compile('<p class="js-tweet-text tweet-text">(.+?)</p>').findall(link)
	text=text[0]
	text = re.sub("(<.*?>)", "", text)
	text = text.replace("&#39;","'")
	text = text.replace("&nbsp;", " ")
	text = text.replace('&quot;', '"')
	text = text.replace('&amp;', '&')
	text = text.replace('&lt;', '<')
	text = text.replace('&gt;', '>')
	if old_text != text:
		xbmc.executebuiltin('XBMC.Notification("%s","%s",%d,"%s")' % ('#Bachelor', text,15000, twitter_icon))
		xbmc.sleep(15000)
	else:
		xbmc.sleep(500)
	MAIN(text)
	
MAIN()
