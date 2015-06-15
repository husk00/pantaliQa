import os,sys
def createThumb(directory):
        if not os.path.exists("/tmp/pantaliQa/"):
          os.makedirs("/tmp/pantaliQa/")
        i = 0
        for file in os.listdir(directory):
                if file.endswith(".mp4"):
                        absolute_path = directory+file
                        i +=1
                        os.system("avconv -y -ss 00:00:22 -i %s -vcodec mjpeg -vframes 1 -an -f rawvideo -s 120x80 /tmp/pantaliQa/test%i.jpg" % (absolute_path, i))

createThumb(sys.argv[1])

