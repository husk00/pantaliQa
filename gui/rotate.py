import wx
from wx.lib.pubsub import Publisher

class Rotate(wx.Frame):

    def __init__(self,parent):
       self.parent = parent
       style =  wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP
       wx.Frame.__init__(self, parent, wx.ID_ANY, "Rotate", wx.DefaultPosition, wx.Size(200, 300), style)

       #Widget
       self.rotateLabel = wx.StaticText(self, label='Rotate' )
       self.xLabel = wx.StaticText(self, label='X' )
       self.yLabel = wx.StaticText(self, label='Y' )
       self.xSlider = wx.Slider(self, value=100, name="xSlider",minValue=0, maxValue=100, pos=(20, 20), size=(150, -1), style=wx.SL_HORIZONTAL)
       self.ySlider = wx.Slider(self, value=100, name="ySlider",minValue=0, maxValue=100, pos=(20, 20), size=(150, -1), style=wx.SL_HORIZONTAL)
       self.resetBtn = wx.Button(self, label="Reset")


       #widgets binding
       self.xSlider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
       self.ySlider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
       self.resetBtn.Bind(wx.EVT_BUTTON, self.OnReset)
        
       #sizers
       self.mainSizer = wx.BoxSizer(wx.VERTICAL)
       self.first_line_sizer = wx.BoxSizer(wx.HORIZONTAL)
       self.slider_sizer = wx.BoxSizer(wx.VERTICAL)
       self.btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

       self.first_line_sizer.Add(self.rotateLabel)
       self.slider_sizer.Add(self.xLabel)
       self.slider_sizer.Add(self.xSlider)
       self.slider_sizer.Add(self.yLabel)
       self.slider_sizer.Add(self.ySlider)
       self.btn_sizer.Add(self.resetBtn)
  
       self.mainSizer.Add(self.first_line_sizer, 0, wx.CENTER|wx.ALL,8)
       self.mainSizer.Add(self.slider_sizer, 0, wx.CENTER,5)
       self.mainSizer.Add(self.btn_sizer, 0, wx.CENTER,5)
       self.SetSizer(self.mainSizer)
       self.Centre()
       self.SetPosition(wx.Point(900,0))
    

    def OnSliderScroll(self, event):
       obj = event.GetEventObject()
       val = obj.GetValue()
       name = obj.GetName()
       val = float(val)/100
       Publisher().sendMessage(("rotate.channel"), (val, name))

    def OnReset(self, event):
       self.xSlider.SetValue(100)
       self.ySlider.SetValue(100)
       Publisher().sendMessage(("rotate.channel"), ((100), "xSlider"))
       Publisher().sendMessage(("rotate.channel"), ((100), "ySlider"))

  
    

       
