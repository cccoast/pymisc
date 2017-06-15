import os
import setproctitle

setproctitle.setproctitle('DataServer')
tarFolder = r"E:\winDataServer\DataCenter\HistTick\Tick"
DataServer = r'E:\winDataServer\App\DataServer'

os.chdir(tarFolder.split(':')[0] + ':')
os.chdir(tarFolder)

ShmCreateCmd = "{0} -c -i -f ShmAlloc.ini".format(DataServer)
print "Command : " + ShmCreateCmd
os.system(ShmCreateCmd)

