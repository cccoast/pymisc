# -*- coding: utf-8 -*-
from WindPy import *
from datetime import *

import pandas as pd
import numpy as np
import os 

incomp = u'E:\Data\指数成分.xls'
start_date = '2010-01-25'
end_date   = '2015-10-13'
inds = ['open','high','low','close','volume','float_a_shares']
# inds = ['float_a_shares']
options = 'Priceadj=f;fill=previous'

sectors = pd.read_csv(r'E:\Data\sectors.csv',header = None,encoding = 'cp936')
sheet_names = sectors[0]
print sheet_names

outdir = os.path.join('E:\Data\Data',sector)
if not os.path.exists(outdir):
    os.mkdir(outdir)

print outdir

w.start()
days = map(lambda x:x.year * 10000 + x.month *100 + x.day,w.tdays(start_date,end_date).Data[0])
indf = pd.read_excel(incomp,sheetname = sheetno,encoding = 'utf8',skiprows = 4)
inss = indf[indf.columns[1]].values
outdfs = {}

for iind in inds:
    outdfs[iind] = pd.DataFrame(index = days,columns = inss,dtype = np.float)
    
for iins in inss:
    print iins
    data = w.wsd(iins,inds,start_date,end_date,options).Data
    for i,iind in enumerate(inds):
        ioutdf = outdfs[iind]
        ioutdf[iins].loc[:] = np.array(data[i],dtype = np.float)

for iind in inds:
    outfile = os.path.join(outdir,iind + '.csv')
    outdfs[iind].to_csv(outfile)
    
# w.start()
# a = w.wsd(ins,inds,start_date,end_date,options)
# print a
