
import signal
import pyuv
import time

def timeout_cb(handler):
    print time.time()
    print "time out"

def idle_cb(handler):
    print "idle"

def sig_cb(handle, signum):
    handle.close()
        
print("PyUV version %s" % pyuv.__version__)

loop = pyuv.Loop.default_loop()

timer = pyuv.Timer(loop)
timer.start(timeout_cb,1,0)
 
signal_h = pyuv.Signal(loop)
signal_h.start(sig_cb, signal.SIGINT)

async = pyuv.Async(loop,idle_cb)
async.send()

loop.run()

print("Stopped!")