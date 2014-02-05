import urllib,urllib2,re,xbmc,xbmcaddon,os


settings = xbmcaddon.Addon( id = 'script.program.twitter' )
twitter_icon = os.path.join( settings.getAddonInfo( 'path' ), 'thumbnails', 'twitter-icon.png' )




##################################################################################################################################

def MAIN(old_text=''):
	if settings.getSetting("enable_service") == 'true':
		search_string_original = settings.getSetting("search_string")
		search_string = search_string_original.replace('#','%23')
		search_string = search_string.replace(' ','%20')
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
				xbmc.executebuiltin('XBMC.Notification("%s","%s",%d,"%s")' % (str(name[1])+'  @'+str(name[0]), text, display_time, twitter_icon))
				xbmc.sleep(wait_time)
			else:
				xbmc.sleep(500)
			MAIN(text)
		except:
			xbmc.executebuiltin('XBMC.Notification("Search Error", "No Results")')
			xbmc.sleep(500)			
			MAIN()
		
	else:
		xbmc.sleep(100)
	
	MAIN()
MAIN()
