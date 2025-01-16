from utime import sleep, ticks_ms
from header import all_nodes, broadcast_lora, lora, CARETAKER_ADDRESS
import body_temp_header
import pulse_sensor_header

can_continue_broadcasting = True
n = 2
has_patient_tripped = False
determined_building = None
determined_floor = None
pulse_threshold = 58000
time_of_last_pulse = 0
body_temp = 0
heart_rate = 0

DEFAULT_ERROR_LOCATION = 3

# init_adxl345(i2c)


def on_recv(payload):
    
    global can_continue_broadcasting, determined_building, determined_floor
    
    message = payload.message.decode()
    
    if "Continue" in message: 
        print("can continue broadcasting")
        can_continue_broadcasting = True
        
    elif "B" in message: # B stands for building, from the caretaker to the patient, indicating
        # the determined buildin
        print("received building payload")
        _, determined_building = message.split(',')
        print(f"building: {determined_building}")
        print("can continue broadcasting")
        can_continue_broadcasting = True
    
    elif "F" in payload.message: # F stands for floor, from the caretaker to the patient, indicating
        # the determined floor
        print("received floor payload")
        _, determined_floor = message.split(',')
        print(f"floor: {determined_floor}")
        print("can continue broadcasting")
        can_continue_broadcasting = True
        

# set callback
lora.on_recv = on_recv


while True:
    
    if can_continue_broadcasting == True:
        
        if determined_building == 'e' or determined_floor == 'e':
            
            determined_building = DEFAULT_ERROR_LOCATION
            determined_floor = DEFAULT_ERROR_LOCATION            
            determined_building = None
            determined_floor = None
            
        print("About to start broadcasting")
        
        broadcast_lora(all_nodes, n, determined_building, determined_floor)
        
        can_continue_broadcasting = False
        
        if determined_building != None and determined_floor != None:
            
            determined_building = None
            determined_floor = None
    
        
    samples_average = body_temp_header.get_samples_average()
    body_temp = body_temp_header.Compute_Temp(samples_average)
    #print(f"Body temp: {body_temp}")

    bpm = pulse_sensor_header.get_bpm()
    #print(f"{bpm}")  

    lora.send_to_wait(f"V,{bpm},{body_temp}", CARETAKER_ADDRESS)

    # we don't need to check for fall detection. It is handled through interrupt and interrupt handlers
    
    sleep(0.1)

