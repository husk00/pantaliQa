#!/usr/bin/python


import wx,os,sys
from wx.lib.pubsub import Publisher


keycode2id = [ "81","87","69","82","84","89","85","73","79","80","65","83","68","70","71","72","74","75","76","90"]

class MySnap(wx.StaticBitmap):
        def __init__(self, parent, id):
                self.id = id
                self.parent = parent
                self.img = wx.EmptyImage(100,60)
                self.path = ""
                wx.StaticBitmap.__init__(self, parent,bitmap=wx.BitmapFromImage(self.img))
                self.Bind(wx.EVT_LEFT_DOWN, self.onClick)
                Publisher().subscribe(self.getKeyEvents, ("snap.channel"))
                self.key = keycode2id[self.id]
    
        def onClick(self, event):
                Publisher().sendMessage(("mediagrid.channel"), self.path)

        def loadThumb(self, img):
                self.SetBitmap(wx.BitmapFromImage(wx.Image(img, wx.BITMAP_TYPE_ANY).Rescale(97, 57)))

        def getKeyEvents(self, keycode):
                if str(keycode.data) == self.key:
                    Publisher().sendMessage(("mediagrid.channel"), self.path)

class Mediagrid(wx.Frame):
        def __init__(self, parent, id,col, rows, title):
                style =  wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP
                wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(400, 300), style)
                Publisher().subscribe(self.getScreenInfo, ("screen.channel"))
                #some var
                self.panel = self
                self.currentDirectory = os.getcwd()
                self.currentSnap = 0
                self.numThumb = 0
                self.picvideoReference = {}
                wx.EVT_MENU(self, 22, self.OnClose)
                #sizers
                vsizer = wx.BoxSizer(wx.VERTICAL)
                hsizer = wx.BoxSizer(wx.VERTICAL)
                #butto for add media to grid
                self.addBtn = wx.Button(self, label="Pick a dir" )
                self.addBtn.Bind(wx.EVT_BUTTON, self.OnAdd)
                #add to sizer
                hsizer.Add(self.addBtn, flag=wx.CENTER|wx.TOP|wx.BOTTOM, border=4)
                vsizer.Add(hsizer, flag=wx.CENTER|wx.TOP|wx.BOTTOM, border=4)
                #list of snap
                self.col = col
                self.rows = rows
                self.snapList = []
                self.DIR = '/tmp/pantaliQa/'
                gs = wx.GridSizer(self.col, self.rows, 3, 3)
                for i in range(0, self.col*self.rows):
                        self.snapList.append(MySnap(self.panel,i))  
                        gs.Add(self.snapList[i], 0, wx.EXPAND)
                vsizer.Add(gs, 0)
                self.SetSizer(vsizer)
                self.Centre()

        def getScreenInfo(self, info):
                print "info data ",info.data
                #bottom right window alignment
                dw,dh = info.data
                #dw, dh = wx.DisplaySize()
                w, h = self.GetSize()
                x = dw - w
                y = dh - h
                self.SetPosition((x, y))
                

        def OnClose(self, event):
                self.Close()
        
        def OnAdd(self, event):
                dlg = wx.DirDialog(
                self, message="Choose a file",
                defaultPath=self.currentDirectory, 
                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                )
                if dlg.ShowModal() == wx.ID_OK:
                        path = dlg.GetPath()
                        self.createThumb(path)
                dlg.Destroy()
                
                for i in range(self.currentSnap,self.currentSnap+self.numThumb ):
                        img = self.DIR+"snap"+str(self.currentSnap+1)+".jpg"
                        self.snapList[i].loadThumb(img)
                        self.snapList[i].path = self.picvideoReference[str(i)]
                        self.currentSnap +=1
                #print "reference ", self.picvideoReference
                

        def createThumb(self,directory):
                if not os.path.exists("/tmp/pantaliQa/"):
                        os.makedirs("/tmp/pantaliQa/")
                for file in os.listdir(directory):
                        if file.endswith(".mov"):
                                absolute_path = directory+"/"+file
                                snapId = str(self.numThumb)
                                self.numThumb +=1
                                os.system("avconv -y -ss 00:00:01 -i %s -vcodec mjpeg -vframes 1 -an -f rawvideo -s 120x80 /tmp/pantaliQa/snap%i.jpg" % (absolute_path, self.numThumb))
                                self.picvideoReference[snapId] = absolute_path
