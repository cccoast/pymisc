import ShmPython as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ipc_key = '0x0f0f0123'
info_key = '0x0e0e0123'
shmapi = sm.Shm(ipc_key)

ind_index = shmapi.id2index_ind(0)
ins_index = shmapi.id2index_ins(110010001)
volume_index = shmapi.id2index_ind(1)

global datas
datas = [float(i) for i in [2000] * 12500 ] 

global df
df = pd.DataFrame()

def fetch():
    datas = shmapi.fetchDoubleDataList(ind_index,ins_index,0,12500)


def fetch2():
    datas = shmapi.fetchCrossSectionData(ind_index,0,12500)
    plt.plot(datas)
    plt.show()
    
def dump():
    datas = np.arange(46802,dtype = np.float)
    shmapi.dumpDoubleDataList(datas,ind_index,shmapi.id2index_ins(110010002),0,46802)
    
def create_df():
    global df
    datas = shmapi.fetchCrossSectionData(ind_index,0,12499)
    df = pd.DataFrame.from_dict({'0':datas[:12500],'1':datas[12500:]})
    print df.head()
    
def fetch3():
    ndf = df.iloc[0:12500][['0','1']]
#    //print ndf.head()

def dump2():
    spot = 0
    for data in datas:
        shmapi.dumpDoubleData(data,ind_index,ins_index,spot)
        spot += 1
        
if __name__ == '__main__': 
    dump()
    print fetch2()
    from timeit import Timer
    t1=Timer("fetch()","from __main__ import fetch")
    t2=Timer("fetch2()","from __main__ import fetch2")
    t3=Timer("dump()","from __main__ import dump")
    t4=Timer("dump2()","from __main__ import dump2")
    create_df()
    t5=Timer("fetch3()","from __main__ import fetch3")
    print t1.repeat(5,1000)
    print t2.repeat(5,500)
    print t5.repeat(5,500)
    