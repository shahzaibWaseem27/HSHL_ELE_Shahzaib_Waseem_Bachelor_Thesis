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

# all_nodes = {
#     
#     "3" : {
#         
#         "0" : [
#         
#             "1",
#             "2"
#             
#         ],
#         
#         "1" : [
#             
#             "1",
#             "2",
#             "3"
#         
#         ]
#         
#     },
#     
#     "4" : {
#         
#         "0" : [
#         
#             "1",
#             "2"
#             
#         ],
#         
#         "1" : [
#             
#             "1",
#             "2",
#             "3"
#         
#         ]
#         
#     },
#     
# }



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
    
def is_pulse_detected(signal_val, threshold):
    
    return signal_val >= threshold


def calc_heart_rate(time_of_this_pulse, time_of_last_pulse):
    
    # x seconds --> 1 pulse
    # 1 second --> 1/x pulses
    # 60 seconds --> 60/x pulses
    
    return 60 / (ticks_diff(time_of_this_pulse, time_of_last_pulse) / 1E3) #converting milliseconds result into seconds



 
# Constants
ADXL345_ADDRESS = 0x53
ADXL345_POWER_CTL = 0x2D
ADXL345_DATA_FORMAT = 0x31
ADXL345_DATAX0 = 0x32
 
# Initialize I2C
i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
 
# Initialize ADXL345
def init_adxl345(i2c):
    i2c.writeto_mem(ADXL345_ADDRESS, ADXL345_POWER_CTL, bytearray([0x08]))  # Set bit 3 to 1 to enable measurement mode
    i2c.writeto_mem(ADXL345_ADDRESS, ADXL345_DATA_FORMAT, bytearray([0x0B]))  # Set data format to full resolution, +/- 16g
 
# Read acceleration data
def read_accel_data(i2c):
    data = i2c.readfrom_mem(ADXL345_ADDRESS, ADXL345_DATAX0, 6)
    x, y, z = ustruct.unpack('<3h', data)
    return x, y, z


def check_patient_tripping(i2c, freefall_threshold):
    
    x, y, z = read_accel_data(i2c)
    
    magnitude = sqrt(x**2 + y**2 + z**2)
    
    if magnitude < freefall_threshold:
        
        return True
    
        
        
        
    
        
        
        
        
        


    
    
