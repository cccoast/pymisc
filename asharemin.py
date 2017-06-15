import os
import numpy as np
import pandas as pd

root_dir = r'E:\BaiduYunDownload\000300.SH_2015-01-04_2015-11-27\000300.SH_2015-01-04_2015-11-27'
root_dir2 = r'E:\BaiduYunDownload\000905.SH_2015-01-04_2015-11-27\000905.SH_2015-01-04_2015-11-27'
tar_folder = r'E:\winDataServer\DataCenter\AshareMin\Min'

def generate_commodity_info_list():
    fname = 'CommodityInfo.list'
    code_str = '{0}    {1}    {2}    33600000    54900000    -9999    20150105    20151127    300    -9999    -9999    -9999    -9999    -9999    -9999    41700000    46800000    -9999    -9999    -9999    0    0   0    0    0   0    0    0    0    0\n'
    tarf = os.path.join(tar_folder,fname)
#     ins_ids = map(lambda x:x.split('.')[0],os.listdir(root_dir) + os.listdir(root_dir2))
#     ins_names = map(lambda x:x.split('.')[0] + '.' + x.split('.')[1],os.listdir(root_dir) + os.listdir(root_dir2))
    sectorf = os.path.join(tar_folder,'sector.csv')
    df = pd.read_csv(sectorf,header = None,index_col = 0)
    with open(tarf,'a') as fout:
        fout.write('\n')
        for index,row in df.iterrows():
            fout.write(code_str.format(index.split('.')[0],row[3],index))

def generate_tradingday_list():
    fname = 'tradingDay.list'
    tarf = os.path.join(tar_folder,fname)
    example = os.path.join(root_dir,os.listdir(root_dir)[0])
    df = pd.read_excel(example,index_col = 0)
    dates = sorted(set(map(lambda x:str(10000*x.year + 100*x.month + x.day),df.index)))
    with open(tarf,'w+') as fout:
        fout.writelines(i + '\n' for i in dates)

def generate_ind_list_and_pair():
    byte = 4
    fname = 'indList.list'
    fname2 = 'indicatorsPair.list'
    backup_ind = ['bk1','bk2','bk3']
    tarf = os.path.join(tar_folder,fname)
    tarf2 = os.path.join(tar_folder,fname2)
    example = os.path.join(root_dir,os.listdir(root_dir)[0])
    df = pd.read_excel(example,index_col = 0)
    ind_names = list(df.columns.values)
    ind_names.extend(backup_ind)
    ind_ids   = range(len(ind_names))
    ind_pairs = zip(ind_names,ind_ids)
    sbyte = ' %d\n' %(byte)
    with open(tarf,'w+') as fout:
        fout.writelines(str(i) + sbyte for i in range(len(ind_names)))
    with open(tarf2,'w+') as fout:
        for i in ind_pairs:
            fout.write('{0} {1}\n'.format(*i))
            
def generate_ins_list_and_pair():
    fname = 'insList.list'
    fname2 = 'instrumentsPair.list'
    tarf = os.path.join(tar_folder,fname)
    ins_ids = map(lambda x:x.split('.')[0],os.listdir(root_dir) + os.listdir(root_dir2))
    with open(tarf,'w+') as fout:
        fout.writelines(i + '\n' for i in ins_ids)
    tarf2 = os.path.join(tar_folder,fname2)
    with open(tarf2,'w+') as fout:
        for i in ins_ids:
            fout.write('{0} {1}\n'.format((i),int(i)))   
    
if __name__ == '__main__':
#     print 'generate ins'
#     generate_ins_list_and_pair()
#     print 'generate ind'
#     generate_ind_list_and_pair()
#     print 'generate trading day list'
#     generate_tradingday_list()
    print 'commodityInfoList'
    generate_commodity_info_list()