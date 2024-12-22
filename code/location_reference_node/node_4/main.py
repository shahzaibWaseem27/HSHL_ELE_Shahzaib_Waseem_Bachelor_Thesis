from time import sleep
from machine import Pin
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
LOCATION_REFERENCE_NODE_ADDRESS = 4

lora_sent_LED_pin = Pin(14, Pin.OUT)


# initialise radio
lora = LoRa(RFM95_SPIBUS, RFM95_INT, LOCATION_REFERENCE_NODE_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)

# This is our callback function that runs when a message is received
def on_recv(payload):
    print("received")
    lora.send_to_wait(f"L,{payload.rssi},{payload.snr}".encode(), CARETAKER_ADDRESS)
    lora_sent_LED_pin.on()
    sleep(0.2)
    lora_sent_LED_pin.off()
    
    
    
# # set callback
lora.on_recv = on_recv 

# # set to listen continuously
lora.set_mode_rx()



# loop and wait for data
while True:
    sleep(0.1)


