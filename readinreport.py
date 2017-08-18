
# coding: utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as pp
%matplotlib inline
# In[2]:

def turnintotable(content):
    try1=pd.DataFrame()
    tryall=pd.DataFrame()
    for i in range(len(context)):
        line=context[i].strip()
        if 'ending' in line:
            fielddate=line.split()[-2].split(',')[0]
        if 'Route' in line:
            fieldroute=line.split(',')[1]
        if 'Direction' in line:
            fieldirection=line.split(',')[1]
        if 'Stop' in line:
            fieldstop=line.split(',')[1]
        if line.strip().split(',')[0].isdigit():#this is wonderful!!!!
            if context[i+1].strip()=='': #len(context[i+1])==0:
                #print(context[i])
                fields=line.split(',')
                a=pd.DataFrame([fields],columns=['Vehicle','Job','Scheduled','Actual','Difference'])
                try1=try1.append(a,ignore_index=True)#!!!you need to assign the append df to sth or it will be discard
                try1['date']=fielddate
                try1['route']=fieldroute
                try1['Direction']=fieldirection
                try1['stop']=fieldstop
                clear=caltable(try1)
                #print(try1)
                tryall=tryall.append(clear,ignore_index=True)
                try1=pd.DataFrame()
            else:
                fields=line.split(',')
                a=pd.DataFrame([fields],columns=['Vehicle','Job','Scheduled','Actual','Difference'])
                #print(a)
                try1=try1.append(a)#!!!you need to assign the append df to sth or it will be discard
    return tryall


# In[3]:

#from stackflow
from datetime import datetime, time as datetime_time, timedelta

def time_diff(start, end):
    start=datetime.strptime(start, '%H:%M:%S')
    end=datetime.strptime(end, '%H:%M:%S')
    if isinstance(start, datetime_time): # convert to datetime
        assert isinstance(end, datetime_time)
        start, end = [datetime.combine(datetime.min, t) for t in [start, end]]
    if start <= end: # e.g., 10:33:26-11:15:49
        diff=end - start
    else: # end < start e.g., 23:55:00-00:25:00
        end += timedelta(1) # +day
        assert end > start
        diff=end - start
    return diff.seconds/60


# In[4]:

import glob
path = "H:/HRao/Bus_headway_file/dupont circle/*.csv"
table=pd.DataFrame()
tableall=pd.DataFrame()
for fname in glob.glob(path):
    
    table=pd.DataFrame()
    print(fname)
    context=open(fname,'r').readlines()
    
    table=turnintotable(context)
    print('done')
    tableall=tableall.append(table,ignore_index=True)


def caltable(table):
    table['date']=table['date'].apply(int)
    
    sortsch=table.sort_values(['Scheduled']).reset_index(drop=True)
    sortsch['diffsch']=''
    for i in range(len(sortsch)-1):
        i=i+1
        sortsch['diffsch'][i]=int(time_diff(sortsch['Scheduled'][i-1],sortsch['Scheduled'][i]))
    
    sortsch['diffact']=''
    sortact=sortsch.sort_values(['Actual']).reset_index(drop=True)
    for i in range(len(sortact)-1):
        i=i+1
        sortact['diffact'][i]=round(time_diff(sortact['Actual'][i-1],sortact['Actual'][i]))
    
    for i in range(len(sortact['Scheduled'])):
        sortact['Scheduled'][i]=datetime.strptime(sortact['Scheduled'][i], '%H:%M:%S').time()
        
    print('one stop one day clean')
    return sortact    
    
    
'''    
# In[21]:

sorttry=tableall.sort_values(['stop','Direction','date','Scheduled']).reset_index(drop=True)
# so the difference can be calculated right


# In[22]:

sorttry['diffsch']=''
for i in range(len(sorttry)-1):
    i=i+1
    sorttry['diffsch'][i]=time_diff(sorttry['Scheduled'][i-1],sorttry['Scheduled'][i])


# In[23]:

sortact=sorttry.sort_values(['stop','Direction','date','Actual']).reset_index(drop=True)


# In[24]:

sortact['diffact']=''
sortact['diffsch_min']=''
for i in range(len(sortact)-1):
    i=i+1
    sortact['diffact'][i]=time_diff(sortact['Actual'][i-1],sortact['Actual'][i])
    sortact['diffsch_min'][i]=sortact['diffsch'][i].seconds/60


# In[38]:

for i in range(len(sortact['Scheduled'])):
    sortact['Scheduled'][i]=datetime.strptime(sortact['Scheduled'][i], '%H:%M:%S').time()


# In[48]:

sortact['diffsch_min'][1::]=sortact['diffsch_min'][1::].apply(int)

'''
# In[55]:

A=sortact[1::].loc[sortact['date']=='01']
pp.plot(range(len(A.loc[A['diffsch_min']<=50]['Scheduled'])),A.loc[A['diffsch_min']<=50]['diffsch_min'])
#pp.plot(range(len(sortact.loc[sortact['date']=='01']['Scheduled'])-1),sortact.loc[sortact['date']=='01']['diffsch_min'][1::])

'''
# In[63]:

sortact['diffact_min']=''
for i in range(len(sortact)-1):
    i=i+1
    sortact['diffact_min'][i]=round(sortact['diffact'][i].seconds/60)
'''

# In[66]:

A=sortact[1::].loc[sortact['date']=='01']
pp.plot(range(len(A.loc[A['diffact_min']<=50]['Scheduled'])),A.loc[A['diffact_min']<=50]['diffact_min'])


# In[84]:

pp.figure(figsize=(12,5))
Aw=sortact[(sortact['date']=='01')& (sortact['Direction']=='Westbound')][1::]
pp.plot(range(len(Aw.loc[Aw['diffact_min']<=50]['Scheduled'])),Aw.loc[Aw['diffact_min']<=50]['diffact_min'])
Ae=sortact[(sortact['date']=='01')& (sortact['Direction']=='Eastbound')][1::]
pp.plot(range(len(Ae.loc[Ae['diffact_min']<=50]['Scheduled'])),Ae.loc[Ae['diffact_min']<=50]['diffact_min'])


# In[87]:

import seaborn
seaborn.distplot(A.loc[A['diffact_min']<=50]['diffact_min'])


# In[94]:

B=sortact[1::]
seaborn.distplot(B.loc[B['diffact_min']<=50]['diffact_min'])
seaborn.distplot(A.loc[B['diffsch_min']<=50]['diffsch_min'])


# In[ ]:



