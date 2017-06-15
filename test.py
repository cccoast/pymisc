import pandas as pd
import time
import numpy as np

start = pd.to_datetime("09:00:00")
pd.datetime.i
print start

drange = pd.date_range(start = start,periods = 46802,freq = '500ms')
df = pd.DataFrame(index = drange);
print df.head()

df.to_csv("e:/QtWorkspace/calander.csv")