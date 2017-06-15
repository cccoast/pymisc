import os
import numpy as np
import pandas as pd
import ShmPython as sm
import setproctitle
import matplotlib.pyplot as plt
import scipy.io as sio

setproctitle.setproctitle('DataFiller')

root_dir = r'E:\BaiduYunDownload\000300.SH_2015-01-04_2015-11-27\000300.SH_2015-01-04_2015-11-27'
root_dir2 = r'E:\BaiduYunDownload\000905.SH_2015-01-04_2015-11-27\000905.SH_2015-01-04_2015-11-27'
root_dir3 = r'E:\BaiduYunDownload\tinysoftdata'

data_cfg = r'E:\winDataServer\DataCenter\AshareMin\Min'
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

def fill_the_last(shmapi):
    last_spot = shmapi.getLastSpot(0)
    shm_header = shmapi.getHeader()
    inds = shm_header.getIndicatorsCount()
    inss = shm_header.getInstrumentsCount()
    for iind in range(inds):
        datas = np.array( shmapi.fetchFloatCrossSectionData(iind,last_spot-1,last_spot), dtype = float)
        if iind == 3:
            print datas
        i = 0
        for iins in range(inss):
            shmapi.dumpFloatData(datas[i],iind,iins,last_spot)
            i += 1
            
def data_filler(base_dir,shmapi):
    files = os.listdir(base_dir)
    counter = 0
    indname2index = {}
    cindex = []
    for ifile in files:
        ins_name = ifile.split('.')[0]
        print counter,ins_name
        counter += 1
        ins_id = ins_name2id[ins_name]
        ins_index = shmapi.id2index_ins(ins_id)
        infile = os.path.join(base_dir,ifile)
        df = pd.read_excel(infile,index_col = 0,parse_dates = True)
        
        if len(cindex) == 0:
            cindex = df.index
            
        if len(df) != len(cindex):
            df = df.reindex(cindex,method = 'pad')
            volume = df['volume'].fillna(0)
            df.fillna(method = 'backfill',inplace = True)
            df['volume'] = volume
        else:
            df['volume'].fillna(0,inplace = True)
            
        if len(indname2index) == 0:
            for ind_name,ind_values in df.iteritems():
                indname2index[ind_name] = shmapi.id2index_ind(ind_name2id[ind_name])
                
        max_len = len(df)
        for ind_name,ind_values in df.iteritems():
            ind_index = indname2index[ind_name]
            shmapi.dumpFloatDataList(ind_values.values.astype(float),ind_index,ins_index,0,max_len)
    
def back_up(backup_dir,shmapi):
    shmapi.export_shm(backup_dir,220,0)

def test(shmapi):
    header = shmapi.getHeader()
    inds = header.getIndicatorsCount()
    root_dir = r'E:\BaiduYunDownload\000300.SH_2015-01-04_2015-11-27\000300.SH_2015-01-04_2015-11-27'
    files = os.listdir(root_dir)
    for ifile in files: 
        ins_id = int(ifile.split('.')[0])
        print ins_id
        ins_index = shmapi.id2index_ins(ins_id)
        infile = os.path.join(root_dir,ifile)
        df = pd.read_excel(infile,index_col = 0,parse_dates = False)
        for ind_id in range(inds-3):
            ind_index = shmapi.id2index_ind(ind_id)
            datas = np.array(shmapi.fetchFloatDataList(ind_index,ins_index,0,53239),dtype = np.float)    
            datas2 = df[df.columns[ind_id]].values
            minus = np.sum(datas - datas2)
            if minus > 1:
                print 'fuck',ins_index,minus

def test2(shmapi):
    header = shmapi.getHeader()
    inds = header.getIndicatorsCount()
    root_dir = r'E:\BaiduYunDownload\000300.SH_2015-01-04_2015-11-27\000300.SH_2015-01-04_2015-11-27'
    files = os.listdir(root_dir)
    for ifile in files: 
        ins_id = int(ifile.split('.')[0])
        ins_index = shmapi.id2index_ins(ins_id)
        if ins_index != 121:
            continue
        print ins_id
        infile = os.path.join(root_dir,ifile)
        df = pd.read_excel(infile,index_col = 0,parse_dates = False)
        for ind_id in range(inds-3):
            ind_index = shmapi.id2index_ind(ind_id)
            datas = np.array(shmapi.fetchFloatDataList(ind_index,ins_index,0,10000),dtype = np.float)    
            datas2 = df[df.columns[ind_id]].values[:53240]
            print np.sum(datas - datas2)
            plt.plot(datas)
            plt.plot(datas2)
            plt.show()
    
    
if __name__ == '__main__':
    shmapi = sm.Shm('0x0f0f0123')
#     data_filler(root_dir2,shmapi)
#     back_up(r"E:\winDataServer\DataCenter\AshareMin\backup",shmapi)
    test(shmapi)
#     fill_the_last(shmapi)

    