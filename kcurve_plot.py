import pandas as pd
import numpy as np
import os
import TickerData as td
import matplotlib
matplotlib.use('Qt4agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

tar_dir = r'/home/xudi/pic'

start_time1 = 3600 * 9 * 1000
end_time1   = 3600 * 11 * 1000 + 1800 * 1000
start_time2 = ( 3600 * 13 + 1800 ) * 1000 
end_time2   = ( 3600 * 15 + 1) * 1000
end_time3   = ( 3600 * 15 + 1800 + 1) * 1000

t1 = np.arange(start_time1,end_time1,500)
t2 = np.arange(start_time2,end_time2,500)
t3 = np.arange(start_time1,end_time3,500)
tt = np.concatenate((t1,t2))

tk = td.TickPrice()
trading_day_list = tk.tradingDayLst
trading_day_length = tk.tradingDayCount

trading_day_length = 1
for i in xrange(trading_day_length):
    
    df = td.gen_dataframe(120080001,i,i+1)
    print df.head()
    
    vol_cum_list = pd.Series( tk.getVolumeLst(120080001, i, i+1), index = t3 )
    vol_cum_list = vol_cum_list.loc[ tt ]
#     print vol_cum_list.head()
    vol_list = vol_cum_list.diff(1)
    vol_list.iloc[0] = vol_cum_list.iloc[0]
#     print vol_list.head()
    vol_delta_list = vol_list.diff(1)
#     print vol_delta_list.head()

    vol_list.hist(bins = 20)
    q = vol_list.quantile(0.99)
    qv = vol_list[ vol_list >= q ]

    for j in qv.index:
        start = max(j - 500 * 20,start_time1)
        if start < end_time1:
            end   = min(j + 500 * 20,end_time1)
        else:
            end   = min(j + 500 * 20,end_time2)
        
        spots = int(end - start)/500
        print start,end,spots
        
        figure = plt.figure()
        G = gridspec.GridSpec(2,1)
        
        price = figure.add_subplot(G[0,0])
        price.set_title('Price Movement')
        price.ticklabel_format(useOffset = False)
        
#         print len(df.loc[start:end]['Bid'].values),len(df.loc[start:end]['Ask'].values),len(df.loc[start:end]['Price'])
        print spots -1,len(df.loc[start:end]['Bid'].values)
        
        price.scatter(range(spots +1),df.loc[start:end]['Bid'].values,s = 10, c="g",edgecolors = "g")
        price.scatter(range(spots +1),df.loc[start:end]['Ask'].values,s = 10, c="r",edgecolors = "r")
        price.scatter(range(spots +1),df.loc[start:end]['Price'].values,s = 10,c="b",marker = "_")
        
        volume = figure.add_subplot(G[1,0],sharex = price)
        volume.set_title('Volume Process')
        
        volume.bar(np.arange(spots +1), 0 - df.loc[start:end]['BVol'].values, width = 0.25, color = "g",edgecolor = "g", align = 'center')
        volume.bar(np.arange(spots +1), df.loc[start:end]['AVol'].values, width = 0.25, color = "r",edgecolor = "r", align = 'center')
        
        volume.bar(np.arange(spots +1) + 0.5, df.loc[start:end]['Vol'].diff().fillna(0).values/2.0, width = 0.25, color = "blue",edgecolor = "k", align = 'center')
        volume.bar(np.arange(spots +1) + 0.5, 0 - df.loc[start:end]['Vol'].diff().fillna(0).values/2.0, width = 0.25, color = "yellow",edgecolor = "k", align = 'center')
        
        volume.set_xlim(-1, spots + 2)
        volume.set_ylim(1.2*np.min(0 - df.loc[start:end]['BVol'].values),1.2*np.max(df.loc[start:end]['AVol'].values))
        
#         plt.savefig(tar_dir + os.sep + trading_day_list[i] + str(j) +'.png',format = 'png')
#         plt.close()
        plt.show()