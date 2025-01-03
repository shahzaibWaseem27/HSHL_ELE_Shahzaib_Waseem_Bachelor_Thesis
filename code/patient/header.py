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

pulse_sensor_pin = ADC(Pin(28))
body_temp_sensor_pin = ADC(Pin(29))


# this dictionary only used for basic testing due to limited number of nodes and hardware
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
        
    print(nodes)    

    for i in range(len(nodes)):
        nodes[i] = int(nodes[i])

    for node in nodes:
        for i in range(n):
            lora.send_to_wait("broadcast".encode(), node) # location reference nodes don't care what the payload is from the patient. They only forward the RSSI
            # and SNR of this payload to caretaker
            lora_sent_LED_pin.on()
            sleep(0.2)
            lora_sent_LED_pin.off()
            
    
    lora.send_to_wait("D, done".encode(), CARETAKER_ADDRESS) #D stands for done, from patient to caretaker, indicating that the broadcast is done


def get_body_temp():

    global body_temp_sensor_pin

    # LM35 produces a 10mV change in its signal pin for every 1 degree celcius change in temperature
    # LM35 seemingly also induces a 500mV offset in its voltage reading that needs to be corrected
    # converting millivolts conversion factor to be expressed in microvolts
    # 10mV / C --> 10000uV / C

    #500mV --> 500000 uV

    temperature_reading = (body_temp_sensor_pin.read_uv() - 500E3) / 10E3 # subtract the 500mV offset from voltage value, and use conversion factor to get temperature reading

    return temperature_reading


def is_pulse_detected(signal_val, threshold):
    
    return signal_val >= threshold


def calc_heart_rate(time_of_this_pulse, time_of_last_pulse):
    
    # x seconds --> 1 pulse
    # 1 second --> 1/x pulses
    # 60 seconds --> 60/x pulses
    
    return 60 / (ticks_diff(time_of_this_pulse, time_of_last_pulse) / 1E3) #converting milliseconds result into seconds


    
        
        
        
    
        
        
        
        
        


    
    
