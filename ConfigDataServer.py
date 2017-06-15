
import os
import ConfigParser

tarFolder = r"E:\winDataServer\DataCenter\HistTick\Tick"

HeadMap = {}
HeadMap['LIMIT_SIZE'] = 1000000
HeadMap['IPC_KEY'] = '0x0f0f0123'
HeadMap['AUTH'] = 0666

HeadMap['INFO_KEY'] = '0x0e0e0123'
HeadMap['INFO_SIZE'] = 10240000
HeadMap['INFO_AUTH'] = 06666

alloc_config = os.path.join(tarFolder,"ShmAlloc.ini")
basic_config = os.path.join(tarFolder,"config.ini")
bin_data     = os.path.join(tarFolder,'data.bin')
extra_info_path = os.path.join(tarFolder,"CommodityInfo.csv")

DataServer = r'E:\winDataServer\App\DataServer'
DataLoader = r'E:\winDataServer\App\DataLoader'
DataFiller = r'E:\winDataServer\App\DataFiller'

to_lower = lambda x: x.lower()
DesMap = {}
DesMap['STREAM_TYPE'] = 0x1303
DesMap['SUB_INSTRUMENTS_LIST_FILE'] = 'insList.list'
DesMap['INDICATORS_LIST_FILE'] = 'indList.list'
DesMap['SPOTS_COUNT'] = 0
DesMap['SPOTS_COUNT_PERDAY'] = -1
DesMap['SPOTS_INTERVAL'] = -1
DesMap['BEGIN_DATE'] = -1
DesMap['LAST_AVAILABLE_SPOT'] = -1
DesMap['HISTORY_DATA_DURATION'] = 1
DesMap['BEGIN_MILLISEC_IN_DAY'] = 32400000

tmpMap = {}
for k,v in DesMap.iteritems():
    tmpMap[to_lower(k)]= v
DesMap = tmpMap


def process_config():
    scp = ConfigParser.SafeConfigParser()
    scp.read(basic_config)
    for sec in scp.sections():
        options = scp.options(sec)
        for op in options:
            value = scp.get(sec,op)
            DesMap[op] = value
    
    _size = os.path.getsize(bin_data)
    
    scp.add_section('SHM')
    scp.set('SHM','LIMIT_SIZE',str(_size) )
    scp.set('SHM','IPC_KEY',str(HeadMap['IPC_KEY']) )
    scp.set('SHM','AUTH',str(HeadMap['AUTH']) )
    scp.set('SHM','INFO_SIZE',str(HeadMap['INFO_SIZE']) )
    scp.set('SHM','INFO_KEY',str(HeadMap['INFO_KEY']) )
    scp.set('SHM','INFO_AUTH',str(HeadMap['AUTH']) )
    
    if ( int(DesMap[to_lower('SPOTS_COUNT')]) > 0  ):
        DesMap[to_lower('SPOTS_COUNT')]=int(DesMap[to_lower('SPOTS_COUNT')])+int(DesMap[to_lower('SPOTS_COUNT_PERDAY')])
        
    cur_section = 'HEADER_BLOCK'
    for k,v in DesMap.iteritems():
        scp.set(cur_section,k,str(v) )
                        
    scp.add_section('INFO_HEADER')
    scp.set('INFO_HEADER','TRADING_DATE_LIST','tradingDay.list')
    scp.set('INFO_HEADER','COMMODITY_INFO_LIST','CommodityInfo.list')
    scp.set('INFO_HEADER','INSTRUMENTS_PAIR_LIST','instrumentsPair.list')
    scp.set('INFO_HEADER','INDICATOR_PAIR_LIST','indicatorsPair.list')
    
    with open(alloc_config,'w+') as fout:
        scp.write(fout)

#######  System Call to [ShmManger] ############################################
def create_shm(_dataServer):
    ShmCreateCmd = "{0} -c -f -i ShmAlloc.ini -i".format(_dataServer)
    print "Command : " + ShmCreateCmd
    os.system(ShmCreateCmd)

def load_data(_dataloader,CurFolder):
    #####   System Call to [DataLoader] ###########################################
    DataLoadCmd = "{0} -w {1} -i {2}".format(_dataloader, CurFolder, HeadMap['IPC_KEY'])
    print "Command : " + DataLoadCmd
    os.system(DataLoadCmd)
    
if __name__ == '__main__':
    
    process_config()