import ShmPython as sm

ipc_key = '0x0f0f0123'
info_key = '0x0e0e0123'
shmapi = sm.Shm(ipc_key)

ind_index = shmapi.id2index_ind(0)
ins_index = shmapi.id2index_ins(110010001)

global datas
datas = [float(i) for i in range(12500)]

def fetch():
    for i in range(1000):
        shmapi.fetchDoubleDataList(ind_index,ins_index,0,12500)

def fetch2():
    shmapi.fetchCrossSectionData(ind_index,0,12500)

def dump():
    for i in range(1000):
        shmapi.dumpDoubleDataList(datas,ind_index,ins_index,0,12500)

def dump2():
    for i in range(1000):
        spot = 0
        for data in datas:
            shmapi.dumpDoubleData(data,ind_index,ins_index,spot)
            spot += 1
               
if __name__ == '__main__': 
    import cProfile
    cProfile.run("fetch()")
    cProfile.run("dump2()")
    