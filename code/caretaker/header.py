from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C
from ulora import LoRa, ModemConfig, SPIConfig


# Lora Parameters
RFM95_RST = 2
RFM95_SPIBUS = SPIConfig.rp2040_zero
RFM95_CS = 5
RFM95_INT = 3
RF95_FREQ = 868.0
RF95_POW = 20
CARETAKER_ADDRESS = 1
PATIENT_ADDRESS = 2

lora = LoRa(RFM95_SPIBUS, RFM95_INT, CARETAKER_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)


def get_location(all_nodes, p):
    
    all_location_results = []
    latest_location_score_sum = 0
    num_of_nodes_in_latest_location = 0
    previous_location = all_nodes[0]["location"] 
    
    q = 1 - p


    for idx, node in enumerate(all_nodes):
        
        is_last_node = idx == len(all_nodes) - 1
        
        this_location = node["location"]
        
        is_new_location = this_location != previous_location
        
        if not is_last_node and is_new_location:
            
            latest_location_average_score = (
                latest_location_score_sum / num_of_nodes_in_latest_location
            )
            
            
            this_location_hashmap = {
            
                "location": previous_location,
                "average_score": latest_location_average_score,
            
            }
            
            all_location_results.append(this_location_hashmap)

           
            this_node_score = p * float(node["RSSI"]) + q * float(node["SNR"])
            
            latest_location_score_sum = 0
            num_of_nodes_in_latest_location = 0
            
            latest_location_score_sum += this_node_score
            num_of_nodes_in_latest_location += 1
            
        
        elif not is_last_node and not is_new_location:
            
            this_node_score = p * float(node["RSSI"]) + q * float(node["SNR"])
            latest_location_score_sum += this_node_score
            num_of_nodes_in_latest_location += 1
            
    
        elif is_last_node and is_new_location:
            
            latest_location_average_score = (
                latest_location_score_sum / num_of_nodes_in_latest_location
            )
            
            
            this_location_hashmap = {
            
                "location": previous_location,
                "average_score": latest_location_average_score,
            
            }
            
            all_location_results.append(this_location_hashmap)
            
            
            this_node_score = p * float(node["RSSI"]) + q * float(node["SNR"])
            
            this_location_hashmap = {
            
                "location": this_location,
                "average_score": this_node_score,
            
            }
            
            all_location_results.append(this_location_hashmap)
            
            
        elif is_last_node and not is_new_location:
            
            this_node_score = p * float(node["RSSI"]) + q * float(node["SNR"])
            latest_location_score_sum += this_node_score
            num_of_nodes_in_latest_location += 1
            
            latest_location_average_score = (
                latest_location_score_sum / num_of_nodes_in_latest_location
            )
            
            this_location_hashmap = {
            
                "location": previous_location,
                "average_score": latest_location_average_score,
            
            }
            
            all_location_results.append(this_location_hashmap)
       
        previous_location = node["location"]

    print(all_nodes)

    max_score = float("-inf")
    determined_location = None

    for location_result in all_location_results:
        if location_result["average_score"] > max_score:
            max_score = location_result["average_score"]
            determined_location = location_result["location"]

    return determined_location




i2c = SoftI2C(scl=Pin(15), sda=Pin(14))

oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)



buzzer_pin = Pin(18, Pin.OUT)
patient_tripping_acknowledged_pin = Pin(26, Pin.IN, Pin.PULL_DOWN)

def handle_patient_tripping_acknowledged(pin):

    global buzzer_pin

    buzzer_pin.off()


