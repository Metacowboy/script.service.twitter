import xbmc,xbmcgui,xbmcaddon,os
from xbmcgui import WindowXMLDialog
settings = xbmcaddon.Addon( id = 'script.service.twitter' )

class KeyListener(WindowXMLDialog):
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
        heading = "Twitter Feeds"
        self.win.getControl(self.CONTROL_LABEL).setLabel(heading)
        # set text
        root = settings.getAddonInfo( 'path' )
        faq_path = os.path.join(root, 'help.faq')
        f = open(faq_path)
        text = f.read()
        self.win.getControl(self.CONTROL_TEXTBOX).setText(text)

