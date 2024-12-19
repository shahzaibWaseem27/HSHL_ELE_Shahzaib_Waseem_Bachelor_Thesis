from machine import Pin, ADC
from utime import ticks_diff
import ustruct
from math import sqrt

# Lora Parameters
RFM95_RST = 27
RFM95_SPIBUS = SPIConfig.rp2_0
RFM95_CS = 5
RFM95_INT = 28
RF95_FREQ = 868.0
RF95_POW = 20
CARETAKER_ADDRESS = 1
PATIENT_ADDRESS = 2

time_of_last_pulse = 0


lora = LoRa(RFM95_SPIBUS, RFM95_INT, PATIENT_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)

pulse_sensor_pin = ADC(Pin(28))



all_nodes = {
    
    "L2" : {
        
        "L2.0" : [
            
            "L2.0.1",
            "L2.0.2"
            
        ],
        
        "L2.1" : [
            
            "L2.1.1",
            "L2.1.2",
            "L2.1.3"
            
        ]
        
    },
    
    "L3" : {
        
        "L3.0" : [
        
            "L3.0.1",
            "L3.0.2"
            
        ],
        
        "L3.1" : [
            
            "L3.1.1",
            "L3.1.2",
            "L3.1.3"
        
        ]
        
    },
    
    "L4" : {
        
        "L4.0" : [
        
            "L4.0.1",
            "L4.0.2"
            
        ],
        
        "L4.1" : [
            
            "L4.1.1",
            "L4.1.2",
            "L4.1.3"
        
        ]
        
    },
    
}



def broadcast_lora(all_nodes, determined_building=None, determined_floor=None):


    if determined_building == None and determined_floor == None:
        

        nodes = all_nodes.keys()
        
        for node in nodes:
            lora.send_to_wait("broadcast", node)
        
        #sleep(1)
            
        lora.send_to_wait("done", CARETAKER_ADDRESS)
            
    elif determined_building != None and determined_floor == None:
        
        
        nodes = all_nodes[determined_building].keys()
        
        for node in nodes:
            lora.send_to_wait("broadcast", node)
        
        #sleep(1)
            
        lora.send_to_wait("done", CARETAKER_ADDRESS)
            
    elif determined_building != None and determined_floor != None
    
    
        nodes = all_nodes[determined_building][determined_floor]
    
        for node in nodes:
            lora.send_to_wait("broadcast", node)
            
        
        lora.send_to_wait("done", CARETAKER_ADDRESS)
    

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
    
        
        
        
    
        
        
        
        
        


    
    

