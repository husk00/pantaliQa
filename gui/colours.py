import wx
from wx.lib.pubsub import Publisher

class Colours(wx.Frame):

    def __init__(self,parent):
       self.parent = parent
       style =  wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP
       wx.Frame.__init__(self, parent, wx.ID_ANY, "Colours", wx.DefaultPosition, wx.Size(200, 300), style)

       #Widget
       self.sizeLabel = wx.StaticText(self, label='Colours' )
       self.redLabel = wx.StaticText(self, label='Red' )
       self.greenLabel = wx.StaticText(self, label='Green' )
       self.blueLabel = wx.StaticText(self, label='Blue' )
       self.cp = wx.ColourPickerCtrl(self, wx.ID_ANY, wx.GREEN, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL )
       self.redSlider = wx.Slider(self, value=100, name="Red",minValue=0, maxValue=100, pos=(20, 20), size=(150, -1), style=wx.SL_HORIZONTAL)
       self.greenSlider = wx.Slider(self, value=100, name="Green",minValue=0, maxValue=100, pos=(20, 20), size=(150, -1), style=wx.SL_HORIZONTAL)
       self.blueSlider = wx.Slider(self, value=100, name="Blue",minValue=0, maxValue=100, pos=(20, 20), size=(150, -1), style=wx.SL_HORIZONTAL)
       self.resetBtn = wx.Button(self, label="Reset")


       #widgets binding
       self.redSlider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
       self.greenSlider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
       self.blueSlider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
       self.cp.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnPickColor)
       self.resetBtn.Bind(wx.EVT_BUTTON, self.OnReset)
        
       #sizers
       self.mainSizer = wx.BoxSizer(wx.VERTICAL)
       self.first_line_sizer = wx.BoxSizer(wx.HORIZONTAL)
       self.size_sizer = wx.BoxSizer(wx.HORIZONTAL)
       self.slider_sizer = wx.BoxSizer(wx.VERTICAL)
       self.btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

       self.first_line_sizer.Add(self.sizeLabel)
       self.size_sizer.Add(self.cp)
       self.slider_sizer.Add(self.redLabel)
       self.slider_sizer.Add(self.redSlider)
       self.slider_sizer.Add(self.greenLabel)
       self.slider_sizer.Add(self.greenSlider)
       self.slider_sizer.Add(self.blueLabel)
       self.slider_sizer.Add(self.blueSlider)
       self.btn_sizer.Add(self.resetBtn)
  
       self.mainSizer.Add(self.first_line_sizer, 0, wx.CENTER|wx.ALL,8)
       self.mainSizer.Add(self.size_sizer, 0, wx.CENTER,5)
       self.mainSizer.Add(self.slider_sizer, 0, wx.CENTER,5)
       self.mainSizer.Add(self.btn_sizer, 0, wx.CENTER,5)
       self.SetSizer(self.mainSizer)
       self.Centre()
       self.SetPosition(wx.Point(1100,0))
    
        

    def OnPickColor(self, evt):
        colorList = evt.GetColour()
        Publisher().sendMessage(("colours.channel"), (colorList, "colorList"))

    def OnSliderScroll(self, event):
       obj = event.GetEventObject()
       val = obj.GetValue()
       name = obj.GetName()
       val = float(val)/255
       Publisher().sendMessage(("colours.channel"), (val, name))

    def OnReset(self, event):
       self.redSlider.SetValue(100)
       self.greenSlider.SetValue(100)
       self.blueSlider.SetValue(100)
       Publisher().sendMessage(("colours.channel"), ((255,255,255), "colorList"))

  
    

       
