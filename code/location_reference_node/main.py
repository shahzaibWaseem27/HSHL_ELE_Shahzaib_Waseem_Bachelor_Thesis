from time import sleep
from ulora import LoRa, ModemConfig, SPIConfig

# Lora Parameters
RFM95_RST = 27
RFM95_SPIBUS = SPIConfig.rp2_0
RFM95_CS = 5
RFM95_INT = 28
RF95_FREQ = 868.0
RF95_POW = 20

NODE_ADDRESS = 1
CARETAKER_ADDRESS = 2

# initialise radio
lora = LoRa(RFM95_SPIBUS, RFM95_INT, SERVER_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)

# This is our callback function that runs when a message is received
def on_recv(payload):
    
    lora.send_to_wait(f"{payload.RSSI},{payload.SNR}", CARETAKER_ADDRESS)
    




# set callback
lora.on_recv = on_recv

# set to listen continuously
lora.set_mode_rx()

# loop and wait for data
while True:
    sleep(0.1)

