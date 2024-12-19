from utime import sleep
from ulora import LoRa, ModemConfig, SPIConfig
#also need to import lora when actually testing
from caretaker_header import get_location, oled, PATIENT_ADDRESS, buzzer_pin, patient_tripping_acknowledged_pin
from random import randint

last_state = True

can_determine_location = False
patient_tripping_acknowledged = False
patient_pulse = "69"
patient_body_temp = "37"
has_patient_tripped = False
all_nodes = []

    
location = ""
determined_building = ""
determined_floor = ""
determined_room = "L3.2.2"


def on_recv(payload):
    
    global can_determine_location, all_nodes, patient_pulse, patient_body_temp, has_patient_tripped
    
    if "done" in payload.message:
        
        can_determine_location = True
        
    elif "location" in payload.message:
        
        _, RSSI, SNR = payload.message.split(',')
    
        this_node_data = {
        
            "location": payload.header_from,
            "RSSI": RSSI,
            "SNR": SNR
        
        }
        
        all_nodes.append(this_node_data)
    
    elif "vitals" in payload.message:
        
        _, patient_pulse, patient_body_temp = payload.message.split(',')
        
    elif "tripped" in payload.message:
        
        has_patient_tripped = True
        
    else:
        
        pass
        
# set callback
# lora.on_recv = on_recv
# 
# # set to listen continuously
# lora.set_mode_rx()




while True:
    
#     if can_determine_location:
#         
#         location = get_location(all_nodes)
#         
#         num_of_decimals = location.count('.')
#         
#         match num_of_decimals:
#             
#             case 0:
#                 
#                 determined_building = location
#                 
#                 lora.send_to_wait(f"building,{determined_building}", PATIENT_ADDRESS)
#         
#             case 1:
#                 
#                 determined_floor = location
#                 
#                 lora.send_to_wait(f"floor,{determined_floor}", PATIENT_ADDRESS)
#                 
#             case 2:
#                 
#                 determined_room = location
# 
# 
#             case others:
#                 
#                 determined_room = "error"
# 
# 
#         all_nodes = list()
#         can_determine_location = False
#         
#         lora.send_to_wait("continue", PATIENT_ADDRESS)
# 
    
    if determined_room != "":
        
        #display determined room location
        oled.text(f"Location: {determined_room}", 0, 25)
        
        
    
    if patient_pulse != "":
        
        #display patient's pulse data
        oled.text(f"Pulse: {patient_pulse} BPM", 0, 40)
        

    
    if patient_body_temp != "":
        
        #display patient's body temp
        oled.text(f"Temp: {patient_body_temp} C", 0, 56)


    # this is just for simulating changing data when used in the real world
    # starts here
    sleep(1)
    
    if last_state:
        determined_room = "L3.2.1"
        patient_pulse = int(patient_pulse) + randint(-2, 2)
        patient_pulse = str(patient_pulse)
        patient_body_temp = int(patient_body_temp) + randint(-2, 2)
        patient_body_temp = str(patient_body_temp)
    else:
        determined_room = "L3.2.2"
    
    last_state = not last_state
    
    # ends here
    
    oled.show()


    oled.fill(0)
    
    if has_patient_tripped:
        
        #turn on alarm
        buzzer_pin.on()
        


    #read emergency_acknowledged input button state
    patient_tripping_acknowledged = patient_tripping_acknowledged_pin.value()


    if has_patient_tripped and patient_tripping_acknowledged:
        
        #turn off alarm
        buzzer_pin.off()
        has_patient_tripped = False

