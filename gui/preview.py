import wx
import cv, cv2

class Preview(wx.Panel):
    def __init__(self,w,h, fps=20):
        style =  wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP
        self.frame = wx.Frame(None, title="Preview")
        wx.Panel.__init__(self, self.frame)

        self.capture = cv2.VideoCapture(1)
        self.capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, w)
        self.capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, h)
        self.frame.Show()

        ret, frame = self.capture.read()

        height, width = frame.shape[:2]
        print width, height
        self.frame.SetSize((400, 320))
        frame = cv2.resize(frame, (400, 320),interpolation=cv2.INTER_CUBIC)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.bmp = wx.BitmapFromBuffer(400, 320, frame)

        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)

    def Quit(self):
        self.frame.Close()

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, event):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()



