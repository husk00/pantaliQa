import wx, sys, os
sys.path.append('images/')
from wx.lib.pubsub import Publisher

class PlayOpt(wx.Frame):

    def __init__(self,parent):
       self.parent = parent
       style =  wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP
       wx.Frame.__init__(self, parent, wx.ID_ANY, "play options", wx.DefaultPosition, wx.Size(200, 300), style)

       #Widget
       self.speedLabel = wx.StaticText(self, label='Speed' )
       self.zeroLabel = wx.StaticText(self, label='0')
       self.resetBtn = wx.Button(self, label="reset")
       self.maxLabel = wx.StaticText(self, label='MaX')
       self.speedSlider = wx.Slider(self, value=50, name="Speed", minValue=0, maxValue=100, pos=(20, 20), size=(150, -1), style=wx.SL_HORIZONTAL)
       self.scratchLabel = wx.StaticText(self, label='Scratch' )
       self.scratchSlider = wx.Slider(self, value=50, name="Scratch",minValue=0, maxValue=100, pos=(20, 20), size=(150, -1), style=wx.SL_HORIZONTAL)
       self.loopLabel = wx.StaticText(self, label='Loop' )
       self.loopinSlider = wx.Slider(self, value=0, minValue=0, name="Loopin",maxValue=100, pos=(20, 20), size=(100, -1), style=wx.SL_HORIZONTAL)
       self.loopoutSlider = wx.Slider(self, value=100, name="Loopout",minValue=0, maxValue=100, pos=(20, 20), size=(100, -1), style=wx.SL_HORIZONTAL)
       imgPath = os.getcwd()+"/gui/images/"
       bmp = wx.BitmapFromImage(wx.Image(imgPath+"media_play.png", wx.BITMAP_TYPE_ANY).Rescale(30,20))
       self.playBtn = wx.BitmapButton(self, -1, bmp, name="Play")
       bmp = wx.BitmapFromImage(wx.Image(imgPath+"media_stop.png", wx.BITMAP_TYPE_ANY).Rescale(30,20))
       self.stopBtn = wx.BitmapButton(self, -1, bmp, name="Stop")
       bmp = wx.BitmapFromImage(wx.Image(imgPath+"media_rewind.png", wx.BITMAP_TYPE_ANY).Rescale(30,20))
       self.rewindBtn = wx.BitmapButton(self, -1, bmp, name="Rewind")

       #widgets binding
       self.speedSlider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
       self.scratchSlider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
       self.loopinSlider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
       self.loopoutSlider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
       self.resetBtn.Bind(wx.EVT_BUTTON, self.OnResetSpeed)
       self.playBtn.Bind(wx.EVT_BUTTON, self.OnMediaBtn)
       self.stopBtn.Bind(wx.EVT_BUTTON, self.OnMediaBtn)
       self.rewindBtn.Bind(wx.EVT_BUTTON, self.OnMediaBtn)
        
       #sizers
       self.mainSizer = wx.BoxSizer(wx.VERTICAL)
       self.first_line_sizer = wx.BoxSizer(wx.HORIZONTAL)
       self.speed_sizer = wx.BoxSizer(wx.HORIZONTAL)
       self.labels_sizer =wx.BoxSizer(wx.HORIZONTAL)
       self.second_line_sizer = wx.BoxSizer(wx.HORIZONTAL)
       self.third_line_sizer = wx.BoxSizer(wx.HORIZONTAL)
       self.fourth_line_sizer = wx.BoxSizer(wx.HORIZONTAL)
       self.scratch_sizer = wx.BoxSizer(wx.HORIZONTAL)
       self.loop_sizer = wx.BoxSizer(wx.HORIZONTAL)

       self.first_line_sizer.Add(self.speedLabel)
       self.second_line_sizer.Add(self.scratchLabel)
       self.third_line_sizer.Add(self.loopLabel)
       self.fourth_line_sizer.Add(self.rewindBtn)
       self.fourth_line_sizer.Add(self.stopBtn)
       self.fourth_line_sizer.Add(self.playBtn)

       self.labels_sizer.Add(self.zeroLabel)
       self.labels_sizer.Add((20,20))
       self.labels_sizer.Add(self.resetBtn)
       self.labels_sizer.Add((20,0))
       self.labels_sizer.Add(self.maxLabel)
       self.speed_sizer.Add(self.speedSlider)
       self.scratch_sizer.Add(self.scratchSlider)
       self.loop_sizer.Add(self.loopinSlider)
       self.loop_sizer.Add(self.loopoutSlider)

       self.mainSizer.Add(self.first_line_sizer, 0, wx.CENTER|wx.ALL,8)
       self.mainSizer.Add(self.labels_sizer, 0, wx.CENTER|wx.ALL, 8)
       self.mainSizer.Add(self.speed_sizer, 0, wx.CENTER,5)
       self.mainSizer.Add(self.second_line_sizer, 0, wx.CENTER|wx.ALL,5)
       self.mainSizer.Add(self.scratch_sizer, 0, wx.CENTER|wx.ALL,5)
       self.mainSizer.Add(self.third_line_sizer, 0, wx.CENTER|wx.ALL,5)
       self.mainSizer.Add(self.loop_sizer, 0, wx.CENTER|wx.ALL,5)
       self.mainSizer.Add(self.fourth_line_sizer, 0, wx.CENTER|wx.ALL,8)
       self.SetSizer(self.mainSizer)
       self.Centre()
       self.SetPosition((300, 0))
       #subscribe for libmapper msg
       Publisher().subscribe(self.MapperOutputs, ("libmapper.channel"))
    
        
    def OnSliderScroll(self, event):
       obj = event.GetEventObject()
       val = obj.GetValue()
       name = obj.GetName()
       val = float(val)/100
       Publisher().sendMessage(("play.channel"), (val, name))
  
    def OnResetSpeed(self, event):
       self.speedSlider.SetValue(50)
       Publisher().sendMessage(("play.channel"), (0.5, "Speed"))

    def OnMediaBtn(self, event):
       obj = event.GetEventObject()
       name = obj.GetName()
       if name =="Rewind" or name == "Stop" or name == "Play":
          val = 0
       Publisher().sendMessage(("play.channel"), (val, name))
    
    def MapperOutputs(self, val):
        print "mapper play opt",val
       
