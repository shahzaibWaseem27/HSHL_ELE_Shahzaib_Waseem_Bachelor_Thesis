from machine import Pin, ADC, I2C
from ulora import LoRa, ModemConfig, SPIConfig
from utime import ticks_diff, sleep
import ustruct
from math import sqrt

# Lora Parameters
RFM95_RST = 2
RFM95_SPIBUS = SPIConfig.rp2040_zero
RFM95_CS = 5
RFM95_INT = 3
RF95_FREQ = 868.0
RF95_POW = 20
CARETAKER_ADDRESS = 1
PATIENT_ADDRESS = 2

lora_sent_LED_pin = Pin(14, Pin.OUT)


lora = LoRa(RFM95_SPIBUS, RFM95_INT, PATIENT_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)

# set to listen continuously
lora.set_mode_rx()


all_nodes = {
    
    "3" : {
        
        "3" : [
        
            "3",
            "4"
            
        ],
        
        "4" : [
            
            "3",
            "4"
        
        ]
        
    },
    
    "4" : {
        
        "3" : [
        
            "3",
            "4"
            
        ],
        
        "4" : [
            
            "3",
            "4"
        
        ]
        
    },
    
}




def broadcast_lora(all_nodes, n=1, determined_building=None, determined_floor=None):


    if determined_building == None and determined_floor == None:
        
        nodes = list(all_nodes.keys())                                
                                              
    elif determined_building != None and determined_floor == None:
        
        nodes = list(all_nodes[determined_building].keys())
            
    elif determined_building != None and determined_floor != None:
    
        nodes = list(all_nodes[determined_building][determined_floor])
        
    else:
        
        nodes = nodes = list(all_nodes.keys()) 

    for i in range(len(nodes)):
        nodes[i] = int(nodes[i])
        
    print(f"{nodes}: {type(nodes)}")   

    for node in nodes:
        print(f"n is {n}")
        for i in range(n):
            print("about to send lora packet")
            lora.send_to_wait("broadcast".encode(), node) # location reference nodes don't care what the payload is from the patient. They only forward the RSSI
            # and SNR of this payload to caretaker
            print(f"sent lora packet {i + 1} to {node}")
            lora_sent_LED_pin.on()
            sleep(0.2)
            lora_sent_LED_pin.off()
            print("reached end of loop")
            
    
    print("about to send done")
    lora.send_to_wait("D, done".encode(), CARETAKER_ADDRESS) #D stands for done, from patient to caretaker, indicating that the broadcast is done
    lora_sent_LED_pin.on()
    sleep(0.2)
    lora_sent_LED_pin.off()
    print("sent done")



        
        
    
        
        
        
        
        


    
    
