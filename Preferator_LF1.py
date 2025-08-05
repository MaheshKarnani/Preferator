import qwiic_rfid
import serial
import time as tim
import sys
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from datetime import datetime, date, timedelta, time
import pandas as pd
import os
import qwiic_tca9548a
import PyNAU7802
import smbus2
import json
import requests
from github import Github, InputGitTreeElement
import keyboard
mode=0
known_tagsA=[1111111199198,
             1111110210210,
             1007,
             1008,
             1009,
             1070]

known_tagsB=[1111111199198,
             1111110210210,
             2007,
             2008,
             2009]
             
#initialize qwiic hardware
def enable_port(mux: qwiic_tca9548a.QwiicTCA9548A, port):
    mux.enable_channels(port)
def disable_port(mux: qwiic_tca9548a.QwiicTCA9548A, port):
    mux.disable_channels(port)
def initialize_mux(address):
    mux = qwiic_tca9548a.QwiicTCA9548A(address=address)
    return mux
def create_instance():
    mux = []
    addresses = [*range(0x70, 0x77 + 1)]
    for address in addresses:
        instance = initialize_mux(address)
        if not instance.is_connected():
            continue
        print("Connected to mux {0} \n".format(address))
        instance.disable_all()
        mux.append({
            "instance": instance,
            "scales": [],
        })
    return mux
def create_bus():
    bus = smbus2.SMBus(1)
    return bus
def scan_tag1(mux,port):
    antennas = []
    bus = create_bus()
    port = port
    enable_port(mux, port)
    my_RFID1 = qwiic_rfid.QwiicRFID(0x12)
    if not my_RFID1.begin():
        # print(f"NOT CONNECTED TO : {port} \n")
        disable_port(mux, port)
    tag1 = my_RFID1.get_tag()
#     scan_time = my_RFID.get_prec_req_time()
    disable_port(mux, port)
    bus.close()
    return tag1
def scan_tag2(mux,port):
    antennas = []
    bus = create_bus()
    port = port
    enable_port(mux, port)
    my_RFID2 = qwiic_rfid.QwiicRFID(0x13)
    if not my_RFID2.begin():
        # print(f"NOT CONNECTED TO : {port} \n")
        disable_port(mux, port)
    tag2 = my_RFID2.get_tag()
#     scan_time = my_RFID.get_prec_req_time()
    disable_port(mux, port)
    bus.close()
    return tag2
mux = create_instance()
tag1=int(scan_tag1(mux[0]["instance"],0))
tag2=int(scan_tag2(mux[0]["instance"],1))
print(tag1)
print(tag2)
RFIDA_detect = DigitalInputDevice(17)#, pull_up=True)
RFIDB_detect = DigitalInputDevice(21)#, pull_up=False)

 #serial to arduino
ser = serial.Serial('/dev/ttyUSB0', 115200)
tim.sleep(2)

#initials
licks1=0
licks2=0
drinks1=0
drinks2=0
licks3=0
licks4=0
drinks3=0
drinks4=0
tag1=0 #initialize animal
tag2=0

    #saving
savepath="/home/preferator2/Documents/Data/"

event_list1 = {
    "Mode" : ["initialize"], 
    "Start_Time": [datetime.now()],
    "Animal": [tag1],
    "Unit":'A',
    "Licks1" : [licks1],
    "Licks2" : [licks2],
    "Drinks1" : [drinks1],
    "Drinks2" : [drinks2],
}

event_list2 = {
    "Mode" : ["initialize"], 
    "Start_Time": [datetime.now()],
    "Animal": [tag2],
    "Unit":'B',
    "Licks1" : [licks3],
    "Licks2" : [licks4],
    "Drinks1" : [drinks3],
    "Drinks2" : [drinks4],
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
save.append_event(event_list2)
    
    #upload frequency and safety timer
upload_time=datetime.now()
upload_interval=timedelta(hours=6) #minimum interval between uploads, hours suggested
action_time=datetime.now()
action_interval=timedelta(minutes=15) #safe interval from last detection to start upload, 15 min suggested

event_list1.update({'Mode': [mode]})
event_list2.update({'Mode': [mode]})

#experiment routine
while True:
    if RFIDA_detect.value == 0:
        print("unit1")
        tag1=int(scan_tag1(mux[0]["instance"],0))
        print(tag1)
        if tag1 in known_tagsA:
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
    if RFIDB_detect.value == 0:
        print("unit2")
        tag2=int(scan_tag2(mux[0]["instance"],1))
        print(tag2)
        if tag2 in known_tagsB:
            ser.write(str.encode('b'))
            Ard_data = ser.readline()
            Ard_data = Ard_data.decode("utf-8","ignore")
            print(Ard_data)
            licks3,drinks3,licks4,drinks4,e = Ard_data.split(",")  
            event_list2.update({'Licks1':[licks3]})#for previous animal
            event_list2.update({'Licks2':[licks4]})#for previous animal
            event_list2.update({'Drinks1':[drinks3]})#for previous animal
            event_list2.update({'Drinks2':[drinks4]})#for previous animal
            save.append_event(event_list2)#for previous animal
            licks3=0
            licks3=0
            drinks4=0
            drinks4=0
            event_list2.update({'Start_Time': [datetime.now()]})
            event_list2.update({'Animal': [tag2]})
            action_time=datetime.now()