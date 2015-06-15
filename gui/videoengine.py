import sys, subprocess
sys.path.append('../libs/pyata')
sys.path.append('../libs/pyata/src/')
from Pd import *
from basic_classes.box import *
import time 

class VideoEngine():
    """
    Through this class the gui communicates with puredata-vanilla by using pyata
    """
    def __init__(self):
        #creates an instance of Pd
        self.pd = Pd()
        #initializes Pyata
        self.pd.init()
        self.pd.clear() 

    def quit(self):
        self.pd.quit()

    def initbang(self,name):
        command = "init "+name+" loadbang;"
        self.sendCommand(command)

    def createOutput(self):
        self.outputWin = Object(50, 40, "qwin 320 240")
        createMsg = Message(50, 20, "create, 1")
        connect(createMsg,0, self.outputWin,0)
        self.initbang("qwin")
        createMsg.click()
        createMsg.delete()

    def createLayer(self, layer_num):
        obj1 = "qvideoplayer p"+str(layer_num)
        videoplayer = Object((100*layer_num), 130,obj1) 
        obj = "qscreen p"+str(layer_num)
        screen = Object((100*layer_num), 400, obj)
        connect(videoplayer, 0, screen, 0)
        self.initbang("p"+str(layer_num))
        self.getOutDim()
        msg = "set /q/screen/p"+str(layer_num)+"/fullscreen 1;"
        self.sendCommand(msg)
        self.setAlpha(layer_num, 0)

    def resizeOutput(self, width, height):
        msg = "destroy, dimen "+width+" "+height+",create"
        createMsg = Message(50, 20, msg)
        createMsg.click()
        createMsg.delete()
        

    def removeLayer(self, channel):
        # I can't understand what happen here: I have to reproduce same procedure for each object in layer....loop is not enough
        for i in memory_box:
            if hasattr(i, "label"):
                if channel in i.label:
                    i.delete()
        for i in memory_box:
            if hasattr(i, "label"):
                if channel in i.label:
                    i.delete()

    def openVideo(self, channel, path):
        msg = "video /q/videoplayer/p"+str(channel)+"/video "+path+";"
        self.sendCommand(msg)

    def setSpeed(self, channel, val):
        msg = "set /q/videoplayer/p"+str(channel)+"/speed "+ str(val) +";"
        self.sendCommand(msg)

    def setScratch(self, channel, val):
        msg = "set /q/videoplayer/p"+str(channel)+"/scratch "+ str(val) +";"
        self.sendCommand(msg)

    def setLoopin(self, channel, val):
        msg = "set /q/videoplayer/p"+str(channel)+"/loopin "+ str(val) +";"
        self.sendCommand(msg)

    def setLoopout(self, channel, val):
        msg = "set /q/videoplayer/p"+str(channel)+"/loopout "+ str(val) +";"
        self.sendCommand(msg)

    def setAlpha(self, channel, val):
        msg = "set /q/screen/p"+str(channel)+"/alpha "+ str(val) +";"
        self.sendCommand(msg)

    def setPlay(self, channel, val):
        msg = "set /q/videoplayer/p"+str(channel)+"/play "+ str(val) +";"
        self.sendCommand(msg)

    def setStop(self, channel, val):
        msg = "set /q/videoplayer/p"+str(channel)+"/stop "+ str(val) +";"
        self.sendCommand(msg)

    def setRewind(self, channel, val):
        msg = "set /q/videoplayer/p"+str(channel)+"/begin "+ str(val) +";"
        self.sendCommand(msg)

    def setSize(self, channel, val):
        msg = "set /q/screen/p"+str(channel)+"/size "+ str(val) +";"
        self.sendCommand(msg)

    def setFullscreen(self, channel):
        msg = "set /q/screen/p"+str(channel)+"/fullscreen ;"
        self.sendCommand(msg)

    def setRotateX(self, channel, val):
        msg = "set /q/screen/p"+str(channel)+"/rotate/x "+ str(val) +";"
        self.sendCommand(msg)

    def setRotateY(self, channel, val):
        msg = "set /q/screen/p"+str(channel)+"/rotate/y "+ str(val) +";"
        self.sendCommand(msg)

    def setPositionX(self, channel, val):
        msg = "set /q/screen/p"+str(channel)+"/translate/x "+ str(val) +";"
        self.sendCommand(msg)

    def setPositionY(self, channel, val):
        msg = "set /q/screen/p"+str(channel)+"/translate/y "+ str(val) +";"
        self.sendCommand(msg)

    def setColorR(self, channel, val):
        msg = "set /q/screen/p"+str(channel)+"/color/r "+ str(val) +";"
        self.sendCommand(msg)

    def setColorG(self, channel, val):
        msg = "set /q/screen/p"+str(channel)+"/color/g "+ str(val) +";"
        self.sendCommand(msg)

    def setColorB(self, channel, val):
        msg = "set /q/screen/p"+str(channel)+"/color/b "+ str(val) +";"
        self.sendCommand(msg)

    def sendCommand(self, command):
        self.pd.c.send_pd(command)

    def getOutDim(self):
        command = "set Qwin.getdim 1;"
        self.sendCommand(command)

    def setOutputFullscreen(self, w,h):
        createMsg = Message(50, 20, "destroy")
        connect(createMsg,0, self.outputWin,0)
        createMsg.click()
        createMsg.delete()
        dimen = "dimen "+str(w)+" "+str(h) 
        createMsg = Message(50, 20, dimen)
        connect(createMsg,0, self.outputWin,0)
        createMsg.click()
        self.getOutDim()

    def createPreview(self):
        self.preview =  Object(50, 90, "v4l2loopback preview")
        self.getOutDim()
        self.initbang("preview")


