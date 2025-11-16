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
known_tagsA=[12186189165,
             1111111199198,
             1111110210210,
             1111110192192,
             1111111248249,
             196471892,
             19647186244,
             1111110190190]

known_tagsB=[12186189165,
             1111111199198,
             1111110210210,
             19645674,
             1111110209209,
             11111114041] #unknown potential spurious 19647186244,1964711262, 1102000232 
             
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
def scan_tag3(mux,port):
    antennas = []
    bus = create_bus()
    port = port
    enable_port(mux, port)
    my_RFID3 = qwiic_rfid.QwiicRFID(0x12)
    if not my_RFID3.begin():
        # print(f"NOT CONNECTED TO : {port} \n")
        disable_port(mux, port)
    tag3 = my_RFID3.get_tag()
#     scan_time = my_RFID.get_prec_req_time()
    disable_port(mux, port)
    bus.close()
    return tag3
mux = create_instance()
tag1=int(scan_tag1(mux[0]["instance"],0))
tag2=int(scan_tag2(mux[0]["instance"],1))
tag3=int(scan_tag3(mux[0]["instance"],6))
print(tag1)
print(tag2)
print(tag3)
RFIDA_detect = DigitalInputDevice(17)#, pull_up=True)
RFIDB_detect = DigitalInputDevice(21)#, pull_up=False)
RFIDC_detect = DigitalInputDevice(20)#, pull_up=False)

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
    "Licks3" : [licks3],
    "Licks4" : [licks4],
    "Drinks3" : [drinks3],
    "Drinks4" : [drinks4],
}

class SaveData:
    def append_event1(self,event_list):
        df_e = pd.DataFrame(event_list)
        datetag=str(date.today())
        if not os.path.isfile(savepath + datetag + "_eventsA.csv"):
            df_e.to_csv(savepath + datetag + "_eventsA.csv", encoding="utf-8-sig", index=False)
        else:
            df_e.to_csv(savepath + datetag + "_eventsA.csv", mode="a+", header=False, encoding="utf-8-sig", index=False)
    def append_event2(self,event_list):
        df_e = pd.DataFrame(event_list)
        datetag=str(date.today())
        if not os.path.isfile(savepath + datetag + "_eventsB.csv"):
            df_e.to_csv(savepath + datetag + "_eventsB.csv", encoding="utf-8-sig", index=False)
        else:
            df_e.to_csv(savepath + datetag + "_eventsB.csv", mode="a+", header=False, encoding="utf-8-sig", index=False)
save = SaveData()
save.append_event1(event_list1)
save.append_event2(event_list2)
    
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
            save.append_event1(event_list1)#for previous animal
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
            licks4,drinks4,licks3,drinks3,e = Ard_data.split(",")
            print('spout3')
            print(licks3,drinks3)
            print('spout4')
            print(licks4,drinks4)
            event_list2.update({'Licks3':[licks3]})#for previous animal
            event_list2.update({'Licks4':[licks4]})#for previous animal
            event_list2.update({'Drinks3':[drinks3]})#for previous animal
            event_list2.update({'Drinks4':[drinks4]})#for previous animal
            save.append_event2(event_list2)#for previous animal
            licks3=0
            licks3=0
            drinks4=0
            drinks4=0
            event_list2.update({'Start_Time': [datetime.now()]})
            event_list2.update({'Animal': [tag2]})
            action_time=datetime.now()

#manual rfid reader on port 7 of mux board for weighing
    if RFIDC_detect.value == 0:
        print("unit3 manual")
        tag3=int(scan_tag3(mux[0]["instance"],6))
        print(tag3)
        
    #add upload and plotting?
        
        # force data collection and upload when user presses alt
    if keyboard.is_pressed('alt'):
        
        ser.write(str.encode('a'))
        Ard_data = ser.readline()
        Ard_data = Ard_data.decode("utf-8","ignore")
        print(Ard_data)
        licks1,drinks1,licks2,drinks2,e = Ard_data.split(",")  
        event_list1.update({'Licks1':[licks1]})#for previous animal
        event_list1.update({'Licks2':[licks2]})#for previous animal
        event_list1.update({'Drinks1':[drinks1]})#for previous animal
        event_list1.update({'Drinks2':[drinks2]})#for previous animal
        save.append_event1(event_list1)#for previous animal
        licks1=0
        licks2=0
        drinks1=0
        drinks2=0
        event_list1.update({'Start_Time': [datetime.now()]})
        event_list1.update({'Animal': [99]}) #notes previous was forced
    
        ser.write(str.encode('b'))
        Ard_data = ser.readline()
        Ard_data = Ard_data.decode("utf-8","ignore")
        print(Ard_data)
        licks4,drinks4,licks3,drinks3,e = Ard_data.split(",")
        print('spout3')
        print(licks3,drinks3)
        print('spout4')
        print(licks4,drinks4)
        event_list2.update({'Licks3':[licks3]})#for previous animal
        event_list2.update({'Licks4':[licks4]})#for previous animal
        event_list2.update({'Drinks3':[drinks3]})#for previous animal
        event_list2.update({'Drinks4':[drinks4]})#for previous animal
        save.append_event2(event_list2)#for previous animal
        licks3=0
        licks3=0
        drinks4=0
        drinks4=0
        event_list2.update({'Start_Time': [datetime.now()]})
        event_list2.update({'Animal': [99]})#notes previous forced
        
        print("last entries saved from all units")     
        upload_time=datetime.now()-upload_interval
        action_time=datetime.now()-action_interval
        
    time_since_upload=datetime.now()-upload_time
    time_since_action=datetime.now()-action_time
    
    if time_since_upload>upload_interval:
        if time_since_action>action_interval:
            try:
                import pref1_fig_generator.py
            except:
                print("fig creation raised messages")
            try:
                #deposit weight data to public repository
                upload_time=datetime.now()
                g = Github("")
                repo = g.get_user().get_repo('Preferator') # repo name
                file_list=list()
                file_names=list()
                datetag=str(date.today())
#                 file_list.append(savepath + datetag + "_eventsA.csv")
#                 file_names.append("Data/c1_3m_102025_testing/" + datetag + "_eventsA.csv")
                file_list.append(savepath + datetag + "eventsB.csv")
                file_names.append("Data/c1_3m_102025_testing/" + datetag + "_eventsB.csv")
                datetag=str(date.today()-timedelta(days = 1))
#                 file_list.append(savepath + datetag + "_eventsA.csv")
#                 file_names.append("Data/c1_3m_102025_testing/" + datetag + "_eventsA.csv")
                file_list.append(savepath + datetag + "eventsB.csv")
                file_names.append("Data/c1_3m_102025_testing/" + datetag + "_eventsB.csv")
                file_list.append(savepath + "pref1output.svg")
                file_names.append("Data/c1_3m_102025_testing/pref1output.svg")
                commit_message = 'automated upload from preferator1'
                master_ref = repo.get_git_ref('heads/main')
                master_sha = master_ref.object.sha
                base_tree = repo.get_git_tree(master_sha)
                element_list = list()
                for i, entry in enumerate(file_list):
                    with open(entry) as input_file:
                        data = input_file.read()
                    element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
                    element_list.append(element)
                tree = repo.create_git_tree(element_list, base_tree)
                parent = repo.get_git_commit(master_sha)
                commit = repo.create_git_commit(commit_message, tree, [parent])
                master_ref.edit(commit.sha)
                print("database updated")
            except:
                print("database update failed")
        
