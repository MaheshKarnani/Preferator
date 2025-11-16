import matplotlib.pyplot as plt
import scipy.signal as sig
import numpy as np
import pandas as pd
from IPython.display import display
from datetime import datetime, date, timedelta, time
import matplotlib.dates as mdates
import statistics
from collections import Counter

start_date=date(2025,10,29) # 
last_date=date.today() #OR TYPE DESIRED DATE ON NEXT LINE AND UNCOMMENT IT
#last_date=date(2025,10,30)
datetag=str(last_date)
d=last_date-start_date
days_to_plot=d.days

loadpath="/home/preferator2/Documents/Data/"
#concatenate
datetag=str(last_date)
d=last_date-start_date
days_to_plot=d.days
data_coll = pd.read_csv(loadpath + str(start_date) + "_eventsB.csv")

for j in range(days_to_plot):
    day=start_date+timedelta(days = j+1) 
    data = pd.read_csv(loadpath + str(day) + "_eventsB.csv") 
    frames=[data_coll,data]
    data_coll=pd.concat(frames)

df=data_coll.reset_index()
df['Start_Time']=pd.to_datetime(df['Start_Time'])
df['Animal']=df['Animal'].astype(int)
# print(df)

display(data.head(5))
known_tags=[19645674,
             1111110209209,
             11111114041]

#diagnosing unique tags per unit
data_unitB=data.loc[data['Unit'] == 'B'] 
tags_unitB=list(set(data_unitB['Animal']))
print("UNIT B:")
print(tags_unitB)

totals=data_unitB.groupby(['Animal']).sum().reset_index()
print(totals)

fig1 = plt.figure(figsize=(8, 20))
# plot filtered weights
ax1 = fig1.add_subplot(221)
ax1.set_title(f"total drops consumed")
ax2 = fig1.add_subplot(222)
ax2.set_title(f"total licks")
for i in range(len(known_tags)):
    an_data=totals.loc[totals['Animal'] == known_tags[i]][['Drinks3','Drinks4']]
    y1=[float(an_data['Drinks3'].iloc[0]), float(an_data['Drinks4'].iloc[0])]
    x1=["Drinks3","Drinks4"]
    ax1.plot(x1,y1,linestyle='-', marker='o', color=[.2*i, 1-.2*i, 1-.2*i, .5], linewidth=5)

    an_data=totals.loc[totals['Animal'] == known_tags[i]][['Licks3','Licks4']]
    y2=[float(an_data['Licks3'].iloc[0]), float(an_data['Licks4'].iloc[0])]
    x2=["Licks3","Licks4"]
    ax2.plot(x2,y2,linestyle='-', marker='o', color=[.2*i, 1-.2*i, 1-.2*i, .5], linewidth=3)
    # ax1.set_xticks(x)
    
ax1.set_ylabel("consumed, *4ul")
ax2.set_ylabel("spout contact, arbitrary")
fig1.tight_layout() 
#plt.show()
plt.savefig(loadpath + "pref1output.svg", bbox_inches='tight', pad_inches=0)
