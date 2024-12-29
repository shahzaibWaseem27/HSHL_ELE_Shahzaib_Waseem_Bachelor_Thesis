from utime import sleep
from ulora import LoRa, ModemConfig, SPIConfig
import caretaker_header
from random import randint
from machine import Pin


can_determine_location = False
patient_tripping_acknowledged = False
patient_pulse = "69"
patient_body_temp = "37"
has_patient_tripped = False
all_nodes = []

lora_sent_LED_pin = Pin(28, Pin.OUT)
# lora_received_LED_pin = Pin(27, Pin.OUT)

    
location = ""
determined_building = ""
determined_floor = ""
determined_room = ""
combined_location = "L"

p = 0.5

location_determination_counter = 0

caretaker_header.patient_tripping_acknowledged_pin.irq(trigger=Pin.IRQ_RISING, handler=caretaker_header.handle_patient_tripping_acknowledged)


def on_recv(payload):
    
    global can_determine_location, all_nodes, patient_pulse, patient_body_temp, has_patient_tripped, location_determination_counter
    
    message = payload.message.decode()
    
    if "D" in message: #D stands for done, from patient to caretaker, saying that it is done with broadcasting to all locations
#         lora_received_LED_pin.on()
#         sleep(0.2)
#         lora_received_LED_pin.off()
        can_determine_location = True
        print("can determine location now")
        location_determination_counter += 1
        
    elif "L" in message: #L stands for location, from a location reference node to caretaker, providing RSSI and SNR data
#         lora_received_LED_pin.on()
#         sleep(0.2)
#         lora_received_LED_pin.off()        
       
        _, RSSI, SNR = message.split(',')
        
        this_node_data = {
        
            "location": payload.header_from,
            "RSSI": RSSI,
            "SNR": SNR
        
        }
        
        all_nodes.append(this_node_data)
    
    elif "V" in message: #V stands for vitals, from patient to caretaker, providing vitals data like pulse rate and body temperature
#         lora_received_LED_pin.on()
#         sleep(0.2)
#         lora_received_LED_pin.off()        
       
        _, patient_pulse, patient_body_temp = message.split(',')
        
    elif "E" in message: #E stands for emergency, from patient to caretaker, providing a notification for an emergency
#         lora_received_LED_pin.on()
#         sleep(0.2)
#         lora_received_LED_pin.off()        
        buzzer_pin.on()
        
    else:
        
        pass
        
# set callback
lora.on_recv = on_recv
# 
# # set to listen continuously
lora.set_mode_rx()




while True:
    
    if can_determine_location:
        
        location = get_location(all_nodes, p) if len(all_nodes) != 0 else "e"
        print(location)
#         can_determine_location = False
        
        if location_determination_counter == 1:
            
            determined_building = location
            print(determined_building)
            
            lora.send_to_wait(f"B,{determined_building}".encode(), PATIENT_ADDRESS)
            lora_sent_LED_pin.on()
            sleep(0.2)
            lora_sent_LED_pin.off()
            
        elif location_determination_counter == 2:
        
            determined_floor = location
            print(determined_floor)
                                
            lora.send_to_wait(f"F,{determined_floor}".encode(), PATIENT_ADDRESS) 
            lora_sent_LED_pin.on()
            sleep(0.2)
            lora_sent_LED_pin.off()
        
        elif location_determination_counter == 3:
        
            determined_room = location
            lora.send_to_wait("Continue".encode(), PATIENT_ADDRESS)
            lora_sent_LED_pin.on()
            sleep(0.2)
            lora_sent_LED_pin.off()
            
            location_determination_counter = 0
        
       
        else:
            
            pass


        all_nodes = list()
        can_determine_location = False
        combined_location = f"L{determined_building}.{determined_floor}.{determined_room}" if determined_building != 'e' else "Le"
        
    
    if combined_location != "":
        
        #display determined room location
        oled.text(f"Location: {combined_location}", 0, 25)
        
        
    
    if patient_pulse != "":
        
        #display patient's pulse data
        oled.text(f"Pulse: {patient_pulse} BPM", 0, 40)
        

    
    if patient_body_temp != "":
        
        #display patient's body temp
        oled.text(f"Temp: {patient_body_temp} C", 0, 56)
     
    oled.show()


    oled.fill(0)
    
    
    


