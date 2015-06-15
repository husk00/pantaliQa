import wx, sys, platform, time
import subprocess as s
from wx.lib.pubsub import Publisher
sys.path.append('gui/')
sys.path.append('libs/pyata')
sys.path.append('libs/pyata/src/')
sys.path.append('images/')
from Pd import *
from mediagrid import *
from videoengine import *
from playoptions import *
from position import *
from scale import *
from layers import *
from colours import *
from rotate import *
from preview import *






### HANDLE GLOBAL KEY EVENTS
def OnKeyPress(event):
    keycode = event.GetKeyCode()
    Publisher().sendMessage(("snap.channel"), keycode)
    event.Skip()

#####################################################
#LAYER wx.frame AND MAIN PANEL FROM WHERE ALL OTHERS FRAMES ARE ISTANCIATED

########################################################################
class MainPanel(wx.Panel):
    def __init__(self, parent):
        self.panel = wx.Panel.__init__(self, parent=parent)
        self.frame = parent

        #Publishers from gui panels
        Publisher().subscribe(self.getVideoPath, ("mediagrid.channel"))
        Publisher().subscribe(self.getLayersValues, ("layers.channel"))
        Publisher().subscribe(self.getPlayValues, ("play.channel"))
        Publisher().subscribe(self.getPositionValues, ("position.channel"))
        Publisher().subscribe(self.getScaleValues, ("scale.channel"))
        Publisher().subscribe(self.getColoursValues, ("colours.channel"))
        Publisher().subscribe(self.getRotateValues, ("rotate.channel"))

        #buttons
        imgPath = os.getcwd()+"/gui/images/"
        bmp = wx.BitmapFromImage(wx.Image(imgPath+"add.png", wx.BITMAP_TYPE_ANY).Rescale(30,20))
        self.addBtn = wx.BitmapButton(self, -1, bmp, name="Add", size=wx.Size(25,25))
        imgPath = os.getcwd()+"/gui/images/"
        bmp = wx.BitmapFromImage(wx.Image(imgPath+"minus.png", wx.BITMAP_TYPE_ANY).Rescale(30,20))
        self.removeBtn = wx.BitmapButton(self, -1, bmp, name="Minus", size=wx.Size(25,25))
        #self.addBtn = wx.Button(self, label="add")
        self.addBtn.Bind(wx.EVT_BUTTON, self.onAddLayer)
        #self.removeBtn = wx.Button(self, label="remove")
        self.removeBtn.Bind(wx.EVT_BUTTON, self.onRemoveLayer)

 
        #sizers
        self.main_vsizer = wx.BoxSizer(wx.VERTICAL)
        self.controls_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.layers_vbox = wx.BoxSizer(wx.VERTICAL)
        self.play_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.play_out_vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.controls_sizer.Add(self.addBtn, 0, wx.CENTER|wx.ALL, 5)
        self.controls_sizer.Add(self.removeBtn, 0, wx.CENTER|wx.ALL, 5)
        self.main_vsizer.Add(self.controls_sizer, 0, wx.CENTER|wx.ALL,5)
        self.main_vsizer.Add(self.layers_vbox, 0, wx.ALIGN_LEFT, 5)
        
        #### GUI FRAME (STATIC) WIDGETS
        #mediagrid
        self.mediagrid = Mediagrid(None, -1,4,4, 'mediagrid')
        self.mediagrid.Show()
  
        #play options panel
        self.play_options = PlayOpt(self)
        self.play_options.Show()

        #position panel
        self.position_panel = Position(self)
        self.position_panel.Show()

        #scale panel
        self.scale_panel = Scale(self)
        self.scale_panel.Show()

        #colours panel
        self.colours_panel = Colours(self)
        self.colours_panel.Show()

        #rotate panel
        self.rotate_panel = Rotate(self)
        self.rotate_panel.Show()

        ### END

        #self.main_vsizer.Add(self.play_options.mainSizer,0, wx.EXPAND, 25)
        self.SetSizer(self.main_vsizer)

        #vars
        self.numLayers = 0
        self.selectedLayer = 0
        self.layers = {}
        #video engine (pd vanilla+gem+pyata)
        self.videoEngine = VideoEngine()
        self.videoEngine.createOutput()
             
        #menu bar
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        outputMenu = wx.Menu()
        deviceMenu = wx.Menu()

        quit = wx.MenuItem(fileMenu, 100, '&Quit\tCtrl+Q')
        fullscreen = wx.MenuItem(outputMenu, 101, 'Fullscreen\tCtrl+F')
        self.libmapper = wx.MenuItem(deviceMenu,102, "libmapper", "", wx.ITEM_CHECK)
        self.previewMenu = wx.MenuItem(outputMenu,103, "preview window", "", wx.ITEM_CHECK)

        menubar.Append(fileMenu, '&File')
        menubar.Append(outputMenu, '&Output')
        menubar.Append(deviceMenu, '&Devices')

        fileMenu.AppendItem(quit)
        outputMenu.AppendItem(fullscreen)
        deviceMenu.AppendItem(self.libmapper)
        outputMenu.AppendItem(self.previewMenu)
        self.frame.Bind(wx.EVT_MENU, self.OnMenu )
        self.frame.SetMenuBar(menubar)

        #display manager 
        self.secondScreen = None
        display = self.GetScreensInfo()

    
    #----------------------------------------------------------------------
    def OnMenu(self, event):
       objId = event.Id
       if objId == 100:
            self.videoEngine.quit()
            self.mediagrid.Close()
            if self.previewMenu.IsChecked() : self.preview.Quit()
            if self.libmapper.IsChecked(): self.timer.Stop()
            self.frame.Close()
       if objId == 101 :
            if self.secondScreen is not None:
                    if str(platform.system()) == "Linux":
                        w,h = self.secondScreen
                        self.videoEngine.setOutputFullscreen(w,h)
                        command = 'wmctrl -r "pantaliQa-output" -e 1,'+str(self.firstScreen[0])+',0,'+str(self.secondScreen[0])+','+str(self.secondScreen[1])+''
                        command = os.getcwd()+"/libs/scripts/move.sh "
                        command += str(self.firstScreen[0])+" "
                        command += str(self.secondScreen[0])+" "
                        command += str(self.secondScreen[1])
                        sleep(0.3)
                        os.system(command)
                        for e in range(0, len(self.layers)):
                            self.videoEngine.setFullscreen(e+1)

                    else:
                        print "no linux"
       if objId == 102 :
            if self.libmapper.IsChecked():
                print "importing libmapper"
                try: 
                    import mapper
                    self.dev = mapper.device("pantaliQa") 
                    self.ActivateSignals()
                    self.timer = wx.Timer(self, id=1)
                    self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
                    self.timer.Start(milliseconds=500, oneShot=False)
                    print "lib mapper is running"
                except Exception, e:
                    print e
       if objId == 103:
            if self.secondScreen is not None:
                if self.previewMenu.IsChecked():
                  self.videoEngine.createPreview() 
                  sleep(1)
                  self.preview = Preview(self.secondScreen[0], self.secondScreen[1])
                else:
                  self.preview.Quit()
            else:
                print "You must have a second monitor COnnected to open the Preview window"
    
    #libmapper 
    def OnTimer(self, evt):
       if evt.GetId() == 1:
            self.dev.poll(10) 

    def ActivateSignals(self):
        #per tutti i layer attivi
        self.prop = ["Alpha","Scratch", "Speed", "LoopIn", "LoopOut", "PLay", "Stop", "Rewind", "Position_X", "Position_y", "Rotation_X", "Rotation_Y", "Color_R", "Color_B", "Color_G"]
        if len(self.layers) > 0:
            for e in range(0, len(self.layers)):
                for p in self.prop:
                    oscAddress = "/layer/"+str(e+1)+"/"+str(p)
                    self.dev.add_input(oscAddress, 1, "f", None, 0.0,1.0, self.signals_handler)

    def signals_handler(self, sig, id, val, timetag):
        oscMsg = getattr(sig, "name")
        n,layer, channel, prop = oscMsg.split("/")
        print prop.strip()
        if prop.strip() == "Alpha": 
            self.layers[int(channel)].slider.SetValue(val*100)
            self.videoEngine.setAlpha(channel, val) 
        if prop.strip() == "Scratch": 
            self.play_options.scratchSlider.SetValue(val*100)
            self.videoEngine.setScratch(channel, val) 
        if prop.strip() == "Speed": 
            self.play_options.speedSlider.SetValue(val*100)
            self.videoEngine.setSpeed(channel, val) 
        

    def onAddLayer(self, event):
       #gui layer
       self.numLayers += 1
       self.layers[self.numLayers] = Layer(self, self.numLayers)
       self.layers_vbox.Add(self.layers[self.numLayers].mainSizer,0, wx.CENTER|wx.ALL, 5)
       self.frame.main_sizer.Layout()
       #video layer
       self.videoEngine.createLayer(self.numLayers)
       
 
    #----------------------------------------------------------------------
    def GetScreensInfo(self):
        screenDisplays = (wx.Display(i) for i in range(wx.Display.GetCount()))
        numScreen = wx.Display.GetCount()
        screenSizes = [display.GetGeometry().GetSize() for display in screenDisplays]
        if numScreen == 1:
            self.firstScreen = screenSizes[0]
            Publisher().sendMessage(("screen.channel"), screenSizes[0])
        else :
            self.firstScreen = screenSizes[0]
            self.secondScreen = screenSizes[1]
            Publisher().sendMessage(("screen.channel"), self.firstScreen)
            

    def onRemoveLayer(self, event):
        if self.layers_vbox.GetChildren():
            self.layers_vbox.Hide(self.numLayers-1)
            self.layers_vbox.Remove(self.numLayers-1)
            self.frame.main_sizer.Layout()
            #video layer
            self.videoEngine.removeLayer("p"+str(self.numLayers))
            del self.layers[self.numLayers]
            self.numLayers -= 1
 
 
    #----------------------------------------------------------------------
    def getVideoPath(self, msg):
        path = msg.data
        self.videoEngine.openVideo(self.selectedLayer, path)  
        for key, value in self.mediagrid.picvideoReference.iteritems():
            if value == path:
                img = "/tmp/pantaliQa/snap"+str((int(key)+1))+".jpg"
        self.layers[self.selectedLayer].loadThumb(img)

    #----------------------------------------------------------------------
    def getLayersValues(self, msg):
        val, channel = msg.data
        self.selectedLayer = channel
        if val != None : self.videoEngine.setAlpha(channel, val) 
 
    #----------------------------------------------------------------------
    def getPlayValues(self, msg):
        val, name = msg.data
        if name == "Rewind" : self.videoEngine.setRewind(self.selectedLayer, val) 
        if name == "Stop" : self.videoEngine.setStop(self.selectedLayer, val) 
        if name == "Play" : self.videoEngine.setPlay(self.selectedLayer, val) 
        if name == "Scratch" : self.videoEngine.setScratch(self.selectedLayer, val) 
        if name == "Speed" : self.videoEngine.setSpeed(self.selectedLayer, val) 
        if name == "Loopin" : self.videoEngine.setLoopin(self.selectedLayer, val) 
        if name == "Loopout" : self.videoEngine.setLoopout(self.selectedLayer, val) 
    def getPositionValues(self, msg):
        val, name = msg.data
        if name == "positionX" : self.videoEngine.setPositionX(self.selectedLayer, val) 
        if name == "positionY" : self.videoEngine.setPositionY(self.selectedLayer, val) 

    def getScaleValues(self, msg):
        val, name = msg.data
        if name == "sizeSlider" : self.videoEngine.setSize(self.selectedLayer, val) 
        if name == "fullscreen" : self.videoEngine.setFullscreen(self.selectedLayer) 

    def getColoursValues(self, msg):
        val, name = msg.data
        if name == "Red" : self.videoEngine.setColorR(self.selectedLayer, val) 
        if name == "Green" : self.videoEngine.setColorG(self.selectedLayer, val) 
        if name == "Blue" : self.videoEngine.setColorB(self.selectedLayer, val) 
        if name == "colorList" : 
                r,g,b = val
                r = r/255
                g = g/255
                b = b/255
                self.videoEngine.setColorR(self.selectedLayer, r) 
                self.videoEngine.setColorG(self.selectedLayer, g) 
                self.videoEngine.setColorB(self.selectedLayer, b) 
    def getRotateValues(self, msg):
        val, name = msg.data
        if name == "xSlider" : self.videoEngine.setRotateX(self.selectedLayer, val) 
        if name == "ySlider" : self.videoEngine.setRotateY(self.selectedLayer, val) 

########################################################################
class MainFrame(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        mystyle =  wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP
        wx.Frame.__init__(self, None, wx.ID_ANY, "Layers", wx.Point(220,10), size=(300,900), style=mystyle)
        panel = MainPanel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.main_sizer)
        #self.Fit()
        self.Show()
        self.SetPosition(wx.Point(0,0))

 
#----------------------------------------------------------------------
if __name__ == "__main__":
    pantaliQa = wx.App(False)
    frame = MainFrame()
    frame.Show()
    pantaliQa.Bind(wx.EVT_KEY_DOWN, OnKeyPress)
    pantaliQa.MainLoop()
