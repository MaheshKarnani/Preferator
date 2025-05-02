import qwiic_rfid
import serial
import time as tim
import sys
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from datetime import datetime, date, timedelta, time
import pandas as pd
import os

#init
    #antenna coil
RFID1 = qwiic_rfid.QwiicRFID(0x13)
if RFID1.begin() == False:
    print("\nThe Qwiic RFID Reader isn't connected to the system. Please check your connection", file=sys.stderr)
print("\nReady to scan some tags!")
RFID1.clear_tags()
RFID1_detect = DigitalInputDevice(4)
    
    #initials
mode=1
licks1=0
licks2=0
drinks1=0
drinks2=0

    #saving
savepath="/home/preferator/Documents/Data/"
tag1=0 #initialize animal
event_list1 = {
    "Mode" : ["initialize"], 
    "Start_Time": [datetime.now()],
    "Animal": [tag1],
    "Unit":1,
    "Licks1" : [licks1],
    "Licks2" : [licks2],
    "Drinks1" : [drinks1],
    "Drinks2" : [drinks2],
}
class SaveData:
    def append_event(self,event_list):
        df_e = pd.DataFrame(event_list)
        datetag=str(date.today())
        if not os.path.isfile(savepath + datetag + "_events.csv"):
            df_e.to_csv(savepath + datetag + "_events.csv", encoding="utf-8-sig", index=False)
        else:
            df_e.to_csv(savepath + datetag + "_events.csv", mode="a+", header=False, encoding="utf-8-sig", index=False)
save = SaveData()
save.append_event(event_list1)
    
    #serial to arduino
ser = serial.Serial('/dev/ttyUSB0', 115200)
tim.sleep(2)

    #upload frequency and safety timer
upload_time=datetime.now()
upload_interval=timedelta(hours=6) #minimum interval between uploads, hours suggested
action_time=datetime.now()
action_interval=timedelta(minutes=15) #safe interval from last detection to start upload, 15 min suggested

event_list1.update({'Mode': [mode]})

#experiment routine
while True:
    
    if RFID1_detect.value == 0:
        print("unit1")
        tag1=int(RFID1.get_tag())
        ser.write(str.encode('a'))
        Ard_data = ser.readline()
        Ard_data = Ard_data.decode("utf-8","ignore")
        print(Ard_data)
        licks1,drinks1,licks2,drinks2,e = Ard_data.split(",")  
        event_list1.update({'Licks1':[licks1]})#for previous animal
        event_list1.update({'Licks2':[licks2]})#for previous animal
        event_list1.update({'Drinks1':[drinks1]})#for previous animal
        event_list1.update({'Drinks2':[drinks2]})#for previous animal
        save.append_event(event_list1)#for previous animal
        licks1=0
        licks2=0
        drinks1=0
        drinks2=0
        event_list1.update({'Start_Time': [datetime.now()]})
        event_list1.update({'Animal': [tag1]})
        action_time=datetime.now()
