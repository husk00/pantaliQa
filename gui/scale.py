import wx, sys, os
from wx.lib.pubsub import Publisher

class Scale(wx.Frame):

    def __init__(self,parent):
       self.parent = parent
       style =  wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP
       wx.Frame.__init__(self, parent, wx.ID_ANY, "Scale", wx.DefaultPosition, wx.Size(200, 300), style)

       #Widget
       self.sizeLabel = wx.StaticText(self, label='Scale' )
       self.zeroLabel = wx.StaticText(self, label='0')
       self.resetBtn = wx.Button(self, label="reset")
       self.fullBtn = wx.Button(self, label="fullscreen")
       self.maxLabel = wx.StaticText(self, label='Max')
       self.sizeSlider = wx.Slider(self, value=50, name="sizeSlider", minValue=0, maxValue=100, pos=(20, 20), size=(150, -1), style=wx.SL_HORIZONTAL)

       #widgets binding
       self.sizeSlider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
       self.resetBtn.Bind(wx.EVT_BUTTON, self.OnReset)
       self.fullBtn.Bind(wx.EVT_BUTTON, self.OnFull)
        
       #sizers
       self.mainSizer = wx.BoxSizer(wx.VERTICAL)
       self.first_line_sizer = wx.BoxSizer(wx.HORIZONTAL)
       self.size_sizer = wx.BoxSizer(wx.HORIZONTAL)
       self.labels_sizer =wx.BoxSizer(wx.HORIZONTAL)
       self.second_line_sizer = wx.BoxSizer(wx.HORIZONTAL)

       self.first_line_sizer.Add(self.sizeLabel)

       self.labels_sizer.Add(self.zeroLabel)
       self.labels_sizer.Add((20,20))
       self.labels_sizer.Add(self.resetBtn)
       self.labels_sizer.Add((20,0))
       self.labels_sizer.Add(self.maxLabel)
       self.size_sizer.Add(self.sizeSlider)
       self.second_line_sizer.Add(self.fullBtn)

       self.mainSizer.Add(self.first_line_sizer, 0, wx.CENTER|wx.ALL,8)
       self.mainSizer.Add(self.labels_sizer, 0, wx.CENTER|wx.ALL, 8)
       self.mainSizer.Add(self.size_sizer, 0, wx.CENTER,5)
       self.mainSizer.Add(self.second_line_sizer, 0, wx.CENTER,5)
       self.SetSizer(self.mainSizer)
       self.Centre()
       self.SetPosition(wx.Point(700,0))
    
        
    def OnSliderScroll(self, event):
       obj = event.GetEventObject()
       val = obj.GetValue()
       name = obj.GetName()
       val = float(val)/100
       Publisher().sendMessage(("scale.channel"), (val, name))
  
    def OnReset(self, event):
       self.sizeSlider.SetValue(50)
       Publisher().sendMessage(("scale.channel"), (0.25, "sizeSlider"))

    def OnFull(self, event):
       self.sizeSlider.SetValue(50)
       Publisher().sendMessage(("scale.channel"), (0.5, "fullscreen"))

    

       
