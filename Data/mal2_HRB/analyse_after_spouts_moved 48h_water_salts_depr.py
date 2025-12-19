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
# last_date=date(2025,12,8)
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
known_tags=[121833859,
            121835736,
             12184102124,
             12184189167,
             12185199220]

fig1 = plt.figure(figsize=(10, 3))
plot_range=[0, 12]
#spouts far MQ v MQ water
t0=datetime(2025,12,7,13,5)
t1=datetime(2025,12,8,12,22)
t2=datetime(2025,12,10,11,40)
t3=datetime(2025,12,11,11,40)
data1=df[(df['Start_Time']>t0) & (df['Start_Time']<t1)]
data2=df[(df['Start_Time']>t2) & (df['Start_Time']<t3)]
data2.rename(columns={"Licks1": "Licks2", "Licks2": "Licks1", "Drinks1": "Drinks2", "Drinks2": "Drinks1"}, inplace=True)
del data
data=pd.concat([data1,data2])
totals=data.groupby(['Animal']).sum(numeric_only=True).reset_index()
totals = totals.drop(totals.index[0])
# totals = totals.drop(totals.index[5])
# plot MQ v MQ 
ax1 = fig1.add_subplot(161)
for i in range(len(known_tags)):
    an_data=totals.loc[totals['Animal'] == known_tags[i]][['Drinks1','Drinks2']]
    y1=[float(an_data['Drinks1'].iloc[0]), float(an_data['Drinks2'].iloc[0])]
    x1=["MQ1","MQ2"]
    ax1.plot(x1,y1,linestyle='-', marker='o', color=[.2*i, 1-.2*i, 1-.2*i, .5], linewidth=2)
A=list(totals['Drinks1'])
B=list(totals['Drinks2'])
s,p=stats.ttest_rel(A,B)
ax1.set_title(f'p = {p:.4f}')
ax1.plot(x1,[statistics.mean(A),statistics.mean(B)],linestyle='-', marker='s', color=[0,0,0,0.8], linewidth=4)
ax1.set_ylim(plot_range)
ax1.set_ylabel("consumed over 48h, ml")
print(stats.ttest_rel(totals['Drinks1'], totals['Drinks2']))
del totals,data1,data2

# 1.2%NaCl v MQ 
t0=datetime(2025,12,8,12,22)
t1=datetime(2025,12,9,11,40)
t2=datetime(2025,12,10,11,40)
data1=df[(df['Start_Time']>t0) & (df['Start_Time']<t1)]
data2=df[(df['Start_Time']>t1) & (df['Start_Time']<t2)]
data2.rename(columns={"Licks1": "Licks2", "Licks2": "Licks1", "Drinks1": "Drinks2", "Drinks2": "Drinks1"}, inplace=True)
del data
data=pd.concat([data1,data2])
totals=data.groupby(['Animal']).sum(numeric_only=True).reset_index()
totals = totals.drop(totals.index[0])
totals = totals.drop(totals.index[5])
# plot 1.2%NaCl v MQ 
ax1 = fig1.add_subplot(163)
for i in range(len(known_tags)):
    an_data=totals.loc[totals['Animal'] == known_tags[i]][['Drinks1','Drinks2']]
    y1=[float(an_data['Drinks1'].iloc[0]), float(an_data['Drinks2'].iloc[0])]
    x1=["1.2% NaCl","MQ"]
    ax1.plot(x1,y1,linestyle='-', marker='o', color=[.2*i, 1-.2*i, 1-.2*i, .5], linewidth=2)
A=list(totals['Drinks1'])
B=list(totals['Drinks2'])
print(totals)
print(A)
print(B)
pref_bsl=np.divide(A,B)
print(pref_bsl)
s,p=stats.ttest_rel(A,B)
ax1.set_title(f'bsl \np = {p:.4f}')
ax1.plot(x1,[statistics.mean(A),statistics.mean(B)],linestyle='-', marker='s', color=[0,0,0,0.8], linewidth=4)
ax1.axes.yaxis.set_ticklabels([])
ax1.set_ylim(plot_range)
print(stats.ttest_rel(totals['Drinks1'], totals['Drinks2']))
del totals,data1,data2

# 3%NaCl v MQ 
t0=datetime(2025,12,13,12,10)
t1=datetime(2025,12,14,12,10)
t2=datetime(2025,12,15,11,50)
data1=df[(df['Start_Time']>t0) & (df['Start_Time']<t1)]
data2=df[(df['Start_Time']>t1) & (df['Start_Time']<t2)]
data2.rename(columns={"Licks1": "Licks2", "Licks2": "Licks1", "Drinks1": "Drinks2", "Drinks2": "Drinks1"}, inplace=True)
del data
data=pd.concat([data1,data2])
totals=data.groupby(['Animal']).sum(numeric_only=True).reset_index()
totals = totals.drop(totals.index[0])
totals = totals.drop(totals.index[5])
# plot 3%NaCl v MQ 
ax1 = fig1.add_subplot(162)
for i in range(len(known_tags)):
    an_data=totals.loc[totals['Animal'] == known_tags[i]][['Drinks1','Drinks2']]
    y1=[float(an_data['Drinks1'].iloc[0]), float(an_data['Drinks2'].iloc[0])]
    x1=["3% NaCl","MQ"]
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

#Na deprived 1.2% v MQ
t0=datetime(2025,12,16,12)
t1=datetime(2025,12,17,11,30)
t2=datetime(2025,12,18,12,3)
t3=datetime(2025,12,19,12,5)
data1=df[(df['Start_Time']>t0) & (df['Start_Time']<t1)]
data2=df[(df['Start_Time']>t2) & (df['Start_Time']<t3)]
data2.rename(columns={"Licks1": "Licks2", "Licks2": "Licks1", "Drinks1": "Drinks2", "Drinks2": "Drinks1"}, inplace=True)
del data
data=pd.concat([data1,data2])
totals=data.groupby(['Animal']).sum(numeric_only=True).reset_index()
totals = totals.drop(totals.index[0])
totals = totals.drop(totals.index[5])
# plot 1.2%NaCl v MQ 
ax1 = fig1.add_subplot(164)
for i in range(len(known_tags)):
    an_data=totals.loc[totals['Animal'] == known_tags[i]][['Drinks1','Drinks2']]
    y1=[float(an_data['Drinks1'].iloc[0]), float(an_data['Drinks2'].iloc[0])]
    x1=["1.2% NaCl","MQ"]
    ax1.plot(x1,y1,linestyle='-', marker='o', color=[.2*i, 1-.2*i, 1-.2*i, .5], linewidth=2)
A=list(totals['Drinks1'])
B=list(totals['Drinks2'])
pref_dep=np.divide(A,B)
print(pref_dep)
s,p=stats.ttest_rel(A,B)
ax1.set_title(f'Na-depleted \n(furo+LSD 1d) \np = {p:.4f}')
ax1.plot(x1,[statistics.mean(A),statistics.mean(B)],linestyle='-', marker='s', color=[0,0,0,0.8], linewidth=4)
ax1.axes.yaxis.set_ticklabels([])
ax1.set_ylim(plot_range)
print(stats.ttest_rel(totals['Drinks1'], totals['Drinks2']))
del totals,data1,data2

#plot fractional preference change upon na depletion
ax2 = fig1.add_subplot(165)
for i in range(len(known_tags)):
    y1=[pref_bsl[i], pref_dep[i]]
    x1=["bsl","Na-depleted"]
    ax2.plot(x1,y1,linestyle='-', marker='o', color=[.2*i, 1-.2*i, 1-.2*i, .5], linewidth=2)
s,p=stats.ttest_rel(pref_bsl,pref_dep)
ax2.set_title(f'1.2% NaCl \npreference \np = {p:.4f}')
ax2.plot(x1,[statistics.mean(pref_bsl),statistics.mean(pref_dep)],linestyle='-', marker='s', color=[0,0,0,0.8], linewidth=4)
ax2.set_ylim([0,3])
ax2.set_ylabel("salt preference \nindex (1.2%NaCl/MQ)")
print(stats.ttest_rel(pref_bsl,pref_dep))

fig1.tight_layout() 
plt.show()
# plt.savefig(loadpath + "fig3t.svg", bbox_inches='tight', pad_inches=0)