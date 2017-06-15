import os
import ConfigParser

tarFolder = r"E:\winDataServer\DataCenter\HistTick\Tick"
DataLoader = r'E:\winDataServer\App\DataLoader'

os.chdir(tarFolder.split(':')[0] + ':')
os.chdir(tarFolder)

scp = ConfigParser.SafeConfigParser()
scp.read(os.path.join(tarFolder,'ShmAlloc.ini' ))
ipc_key = scp.get('SHM','IPC_KEY')
   
DataLoadCmd = "{0} -w {1} -i {2}".format(DataLoader, tarFolder, ipc_key)
print "Command : " + DataLoadCmd
os.system(DataLoadCmd)

