import qwiic_rfid
import time
import sys

#init
    #antenna coil
RFID1 = qwiic_rfid.QwiicRFID()
    if RFID1.begin() == False:
        print("\nThe Qwiic RFID Reader isn't connected to the system. Please check your connection", file=sys.stderr)
        return
    print("\nReady to scan some tags!")
    RFID1.clear_tags()
RFID1_detect = DigitalInputDevice(4)
        
    #setup counter channels for licks
licks1=0
lick_port1=DigitalInputDevice(5)
def count_licks1():
    global licks1
    licks1+=1
licks2=0
lick_port1=DigitalInputDevice(6)
def count_licks2():
    global licks2
    licks2+=1
    
    #give water outputs   
drink1=DigitalOutputDevice(7)
drink2=DigitalOutputDevice(8)
drink_interval=timedelta(seconds=1)
    
    #saving
savepath="/home/pi/Documents/Data/"
tag1=0 #initialize animal
event_list1 = {
    "Mode" : ["initialize"], 
    "Start_Time": [datetime.now()],
    "Animal": [tag1],
    "Unit":1,
    "Licks1" : [licks1],
    "Licks2" : [licks2],
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

    #upload frequency and safety timer
upload_time=datetime.now()
upload_interval=timedelta(hours=6) #minimum interval between uploads, hours suggested
action_time=datetime.now()
action_interval=timedelta(minutes=15) #safe interval from last detection to start upload, 15 min suggested
    
    
#experiment routine
while True:
    lick1.when_activated=count_licks1
    lick2.when_activated=count_licks2
    
    if RFID1_detect.value == 0:
        print("unit1")
        tag1=int(RFID1.get_tag())
        event_list1.update({'Licks1':[licks1]})#for previous animal
        event_list1.update({'Licks2':[licks2]})#for previous animal
        save.append_event(event_list1)#for previous animal
        licks1=0
        licks2=0
        event_list1.update({'Start_Time': [datetime.now()]})
        event_list1.update({'Animal': [tag1]})
        action_time=datetime.now()


