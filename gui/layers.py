import wx
#from mediagrid import *
from wx.lib.pubsub import Publisher

class Layer():
    """
    This class draws layers gui widgets
    The wx.frame where this class is istanciated is in MainPanel in ../pantaliqa.py
    """
    def __init__(self,parent, id):
       self.id = id
       self.img = wx.EmptyImage(80,50)
       self.parent = parent
       self.path = ""
       self.val = 0.0
       self.selected = False 
       #Widget
       self.snap = wx.StaticBitmap(parent,bitmap=wx.BitmapFromImage(self.img))
       self.slider = wx.Slider(parent, value=0, minValue=0, maxValue=100, pos=(20, 20), size=(150, -1), style=wx.SL_HORIZONTAL)
       #binds
       self.slider.Bind(wx.EVT_SLIDER, self.OnSliderScroll)
       self.snap.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        
       #sizers
       self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
       self.mainSizer.Add(self.snap)
       self.mainSizer.Add(self.slider)
    
        
    def OnSliderScroll(self, event):
       obj = event.GetEventObject()
       val = obj.GetValue()
       self.val = float(val)/100
       Publisher().sendMessage(("layers.channel"), (self.val, self.id))
  
    def OnClick(self, event):
       self.selected = True
       Publisher().sendMessage(("layers.channel"), (None,self.id))
    
    def loadThumb(self, img):
       self.snap.SetBitmap(wx.BitmapFromImage(wx.Image(img, wx.BITMAP_TYPE_ANY).Rescale(80, 50)))
       

       
