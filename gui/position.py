import wx, sys, os
from wx.lib.pubsub import Publisher

class Position(wx.Frame):

    def __init__(self,parent):
       self.parent = parent
       style =  wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP
       wx.Frame.__init__(self, parent, wx.ID_ANY, "Position", wx.Point(300,300), wx.Size(200, 300), style)

       #Widget
       self.translateLabel = wx.StaticText(self, label='Position' )
       self.zeroLabel = wx.StaticText(self, label='X')
       self.resetBtn = wx.Button(self, label="reset")
       self.maxLabel = wx.StaticText(self, label='Y')
       self.xSlider = wx.Slider(self, value=50, name="positionX", minValue=0, maxValue=100, pos=(20, 20), size=(100, -1), style=wx.SL_HORIZONTAL)
       self.ySlider = wx.Slider(self, value=50, name="positionY", minValue=0, maxValue=100, pos=(20, 20), size=(100, -1), style=wx.SL_HORIZONTAL)

       #widgets binding
       self.xSlider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
       self.ySlider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
       self.resetBtn.Bind(wx.EVT_BUTTON, self.OnResetTrans)
        
       #sizers
       self.mainSizer = wx.BoxSizer(wx.VERTICAL)
       self.first_line_sizer = wx.BoxSizer(wx.HORIZONTAL)
       self.trans_sizer = wx.BoxSizer(wx.HORIZONTAL)
       self.labels_sizer =wx.BoxSizer(wx.HORIZONTAL)

       self.first_line_sizer.Add(self.translateLabel)

       self.labels_sizer.Add(self.zeroLabel)
       self.labels_sizer.Add((20,20))
       self.labels_sizer.Add(self.resetBtn)
       self.labels_sizer.Add((20,0))
       self.labels_sizer.Add(self.maxLabel)
       self.trans_sizer.Add(self.xSlider)
       self.trans_sizer.Add(self.ySlider)

       self.mainSizer.Add(self.first_line_sizer, 0, wx.CENTER|wx.ALL,8)
       self.mainSizer.Add(self.labels_sizer, 0, wx.CENTER|wx.ALL, 8)
       self.mainSizer.Add(self.trans_sizer, 0, wx.CENTER,5)
       self.SetSizer(self.mainSizer)
       self.Centre()
       self.SetPosition((500, 0))

    
        
    def OnSliderScroll(self, event):
       obj = event.GetEventObject()
       val = obj.GetValue()
       name = obj.GetName()
       val = float(val)/100
       Publisher().sendMessage(("position.channel"), (val, name))
  
    def OnResetTrans(self, event):
       self.xSlider.SetValue(50)
       self.ySlider.SetValue(50)
       Publisher().sendMessage(("position.channel"), (0.5, "positionX"))
       Publisher().sendMessage(("position.channel"), (0.5, "positionY"))

    

       
