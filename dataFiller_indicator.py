import os
import numpy as np
import pandas as pd
import ShmPython as sm
import setproctitle
import matplotlib.pyplot as plt

root_dir = r'E:\BaiduYunDownload\zz800'
export_dir = r'E:\winDataServer\DataCenter\AShareDay\backup'
indicators = map(lambda x:x.split('.')[0],os.listdir(root_dir))
ipckey = '0x0f0f0223'

data_cfg = r'E:\winDataServer\DataCenter\AShareDay\Day'
ins_pairf = r'instrumentsPair.list'
ind_pairf = r'indicatorsPair.list'

ins_name2id = {}
ind_name2id = {}

with open(os.path.join(data_cfg,ins_pairf),'r') as fin: 
    for line in fin.readlines():
        ins_name,ins_id = line.split()
        ins_name2id[ins_name] = int(ins_id)

with open(os.path.join(data_cfg,ind_pairf),'r') as fin: 
    for line in fin.readlines():
        ind_name,ind_id = line.split()
        ind_name2id[ind_name] = int(ind_id)

def filler(shmapi):
    for ifile in os.listdir(root_dir):
        infile = os.path.join(root_dir,ifile)
        ind_index = shmapi.id2index_ind(ind_name2id[ifile.split('.')[0]])
        df = pd.read_csv(infile,index_col = 0,parse_dates = True)
        df_len = len(df)
        print ifile.split('.')[0],ind_name2id[ifile.split('.')[0]]
        for col,vals in df.iteritems():
            ins_index = shmapi.id2index_ins(ins_name2id[col.split('.')[0]])
            shmapi.dumpDoubleDataList(vals.values.astype(float),ind_index,ins_index,0,df_len)
            
def test(shmapi):
    header = shmapi.getHeader()
    files = os.listdir(root_dir)
    for ifile in files: 
        infile = os.path.join(root_dir,ifile)
        ind_index = shmapi.id2index_ind(ind_name2id[ifile.split('.')[0]])
        df = pd.read_csv(infile,index_col = 0,parse_dates = True)
        df_len = len(df)
        print ifile.split('.')[0]
        for col,vals in df.iteritems():
            ins_index = shmapi.id2index_ins(ins_name2id[col.split('.')[0]])
            datas = np.array(shmapi.fetchDoubleDataList(ind_index,ins_index,0,df_len),dtype = np.float)    
            datas2 = vals.values
            if np.sum(datas - datas2) > 1:
                print ifile.split('.')[0],(datas - datas2)

       
if __name__ == '__main__':
    shmapi = sm.Shm(ipckey)
    
#     print 'fill data'
#     filler(shmapi)
#     print 'backup data'
#     days = len(shmapi.getTradingDayList())
#     shmapi.export_shm(export_dir, days - 1, 0)
    
    datas = shmapi.fetchDoubleDataList(6,0,0,300)
    plt.plot(datas)
    plt.show()
    