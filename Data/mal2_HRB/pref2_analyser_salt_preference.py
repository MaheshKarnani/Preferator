import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.stats as stats
import numpy as np
import pandas as pd
from IPython.display import display
from datetime import datetime, date, timedelta, time
import matplotlib.dates as mdates
import statistics
from collections import Counter

start_date=date(2025,11,15) # 
last_date=date.today() #OR TYPE DESIRED DATE ON NEXT LINE AND UNCOMMENT IT
last_date=date(2025,12,2)
datetag=str(last_date)
d=last_date-start_date
days_to_plot=d.days

loadpath="/home/maheshkarnani/Documents/Code/Preferator/Data/mal2_HRB/"
#concatenate
datetag=str(last_date)
d=last_date-start_date
days_to_plot=d.days
data_coll = pd.read_csv(loadpath + str(start_date) + "_events.csv")

for j in range(days_to_plot):
    day=start_date+timedelta(days = j+1) 
    data = pd.read_csv(loadpath + str(day) + "_events.csv") 
    frames=[data_coll,data]
    data_coll=pd.concat(frames)

df=data_coll.reset_index()
df['Start_Time']=pd.to_datetime(df['Start_Time'])
df['Animal']=df['Animal'].astype(int)
# df = df.drop('Unit', axis=1)
#outlier exclusion
df1 = df[df.Licks1 >= 0]
df2 = df1[df1.Licks2 >= 0]
print('excluded',(len(df)-len(df2)),'rows with negative lick values')
df3 = df2[df2.Drinks2 < 100]
df4 = df3[df3.Drinks1 < 100]
print('excluded',(len(df2)-len(df4)),'rows with >100 drink values')
del df
df=df4
#correct to ml
df.Drinks1=df.Drinks1*0.013
df.Drinks2=df.Drinks2*0.013
# print(df)

display(df.head(5))
known_tags=[121835736,
             12184102124,
             12184189167,
             121833859,
             12185199220]

#analyse MQ water v MQ water
t0=datetime(2025,11,29,15,30) #start
t1=datetime(2025,11,30,16,15) #swap
t2=datetime(2025,12,1,12,4) #end
data1=df[(df['Start_Time']>t0) & (df['Start_Time']<t1)]
data2=df[(df['Start_Time']>t1) & (df['Start_Time']<t2)]
data2.rename(columns={"Licks1": "Licks2", "Licks2": "Licks1", "Drinks1": "Drinks2", "Drinks2": "Drinks1"}, inplace=True)
del data
data=pd.concat([data1,data2])
# print(data)

totals=data.groupby(['Animal']).sum(numeric_only=True).reset_index()
totals = totals.drop(totals.index[0])

fig1 = plt.figure(figsize=(10, 3))
plot_range=[0, 20]
# plot MQ v MQ 
ax1 = fig1.add_subplot(161)
for i in range(len(known_tags)):
    an_data=totals.loc[totals['Animal'] == known_tags[i]][['Drinks1','Drinks2']]
    y1=[float(an_data['Drinks1'].iloc[0]), float(an_data['Drinks2'].iloc[0])]
    x1=["Water1","Water2"]
    ax1.plot(x1,y1,linestyle='-', marker='o', color=[.2*i, 1-.2*i, 1-.2*i, .5], linewidth=2)
A=list(totals['Drinks1'])
B=list(totals['Drinks2'])
s,p=stats.ttest_rel(A,B)
ax1.set_title(f'p = {p:.4f}')
ax1.plot(x1,[statistics.mean(A),statistics.mean(B)],linestyle='-', marker='s', color=[0,0,0,0.8], linewidth=4)
ax1.set_ylabel("consumed over 48h, ml")
ax1.set_ylim(plot_range)
del totals,data1,data2

# 0.45% to come here**********************

#analyse 0.9%NaCl v MQ water
t0=datetime(2025,11,27,12,20)
t1=datetime(2025,11,28,12,35)
t2=datetime(2025,11,29,12,35)
data1=df[(df['Start_Time']>t0) & (df['Start_Time']<t1)]
data2=df[(df['Start_Time']>t1) & (df['Start_Time']<t2)]
data2.rename(columns={"Licks1": "Licks2", "Licks2": "Licks1", "Drinks1": "Drinks2", "Drinks2": "Drinks1"}, inplace=True)
del data
data=pd.concat([data1,data2])
# print(data)
totals=data.groupby(['Animal']).sum(numeric_only=True).reset_index()
totals = totals.drop(totals.index[0])
# plot 0.9%NaCl v MQ 
ax1 = fig1.add_subplot(163)
for i in range(len(known_tags)):
    an_data=totals.loc[totals['Animal'] == known_tags[i]][['Drinks1','Drinks2']]
    y1=[float(an_data['Drinks1'].iloc[0]), float(an_data['Drinks2'].iloc[0])]
    x1=["0.9% NaCl","Water"]
    ax1.plot(x1,y1,linestyle='-', marker='o', color=[.2*i, 1-.2*i, 1-.2*i, .5], linewidth=2)
A=list(totals['Drinks1'])
B=list(totals['Drinks2'])
s,p=stats.ttest_rel(A,B)
ax1.set_title(f'p = {p:.4f}')
ax1.plot(x1,[statistics.mean(A),statistics.mean(B)],linestyle='-', marker='s', color=[0,0,0,0.8], linewidth=4)
ax1.axes.yaxis.set_ticklabels([])
ax1.set_ylim(plot_range)
print(stats.ttest_rel(totals['Drinks1'], totals['Drinks2']))
del totals,data1,data2


#analyse 1.2%NaCl v MQ water
t0=datetime(2025,11,19,12)
t1=datetime(2025,11,20,12)
t2=datetime(2025,11,21,12)
data1=df[(df['Start_Time']>t0) & (df['Start_Time']<t1)]
data2=df[(df['Start_Time']>t1) & (df['Start_Time']<t2)]
data2.rename(columns={"Licks1": "Licks2", "Licks2": "Licks1", "Drinks1": "Drinks2", "Drinks2": "Drinks1"}, inplace=True)
del data
data=pd.concat([data1,data2])
# print(data)
totals=data.groupby(['Animal']).sum(numeric_only=True).reset_index()
totals = totals.drop(totals.index[0])
# plot 1.2%NaCl v MQ 
ax1 = fig1.add_subplot(164)
for i in range(len(known_tags)):
    an_data=totals.loc[totals['Animal'] == known_tags[i]][['Drinks1','Drinks2']]
    y1=[float(an_data['Drinks1'].iloc[0]), float(an_data['Drinks2'].iloc[0])]
    x1=["1.2% NaCl","Water"]
    ax1.plot(x1,y1,linestyle='-', marker='o', color=[.2*i, 1-.2*i, 1-.2*i, .5], linewidth=2)
A=list(totals['Drinks1'])
B=list(totals['Drinks2'])
s,p=stats.ttest_rel(A,B)
ax1.set_title(f'p = {p:.4f}')
ax1.plot(x1,[statistics.mean(A),statistics.mean(B)],linestyle='-', marker='s', color=[0,0,0,0.8], linewidth=4)
ax1.axes.yaxis.set_ticklabels([])
ax1.set_ylim(plot_range)
print(stats.ttest_rel(totals['Drinks1'], totals['Drinks2']))
del totals,data1,data2

#analyse 1.5%NaCl v MQ water
t0=datetime(2025,11,24,12)
t1=datetime(2025,11,25,12)
t2=datetime(2025,11,26,12)
data1=df[(df['Start_Time']>t0) & (df['Start_Time']<t1)]
data2=df[(df['Start_Time']>t1) & (df['Start_Time']<t2)]
data2.rename(columns={"Licks1": "Licks2", "Licks2": "Licks1", "Drinks1": "Drinks2", "Drinks2": "Drinks1"}, inplace=True)
del data
data=pd.concat([data1,data2])
# print(data)
totals=data.groupby(['Animal']).sum(numeric_only=True).reset_index()
totals = totals.drop(totals.index[0])
# plot 1.5%NaCl v MQ 
ax1 = fig1.add_subplot(165)
for i in range(len(known_tags)):
    an_data=totals.loc[totals['Animal'] == known_tags[i]][['Drinks1','Drinks2']]
    y1=[float(an_data['Drinks1'].iloc[0]), float(an_data['Drinks2'].iloc[0])]
    x1=["1.5% NaCl","Water"]
    ax1.plot(x1,y1,linestyle='-', marker='o', color=[.2*i, 1-.2*i, 1-.2*i, .5], linewidth=2)
A=list(totals['Drinks1'])
B=list(totals['Drinks2'])
s,p=stats.ttest_rel(A,B)
ax1.set_title(f'p = {p:.4f}')
ax1.plot(x1,[statistics.mean(A),statistics.mean(B)],linestyle='-', marker='s', color=[0,0,0,0.8], linewidth=4)
ax1.axes.yaxis.set_ticklabels([])
ax1.set_ylim(plot_range)
print(stats.ttest_rel(totals['Drinks1'], totals['Drinks2']))
del totals,data1,data2


# 3% to come here**********************


fig1.tight_layout() 
# plt.show()
plt.savefig(loadpath + "pref2output.svg", bbox_inches='tight', pad_inches=0)