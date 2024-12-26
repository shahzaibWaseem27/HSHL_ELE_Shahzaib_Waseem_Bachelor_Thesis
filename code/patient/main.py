from utime import sleep, ticks_ms
from header import all_nodes, broadcast_lora, pulse_sensor_pin, lora, CARETAKER_ADDRESS, i2c, init_adxl345, read_accel_data
import adxl345



can_continue_broadcasting = True
n = 2
has_patient_tripped = False
determined_building = None
determined_floor = None
pulse_threshold = 58000
time_of_last_pulse = 0
body_temp = 0

DEFAULT_ERROR_LOCATION = 3

adxl345.initialize_adxl345()

# Setup interrupts
adxl345.int1.irq(trigger=Pin.IRQ_RISING, handler=adxl345.fall_interrupt_handler)
adxl345.button.irq(trigger=Pin.IRQ_RISING, handler=adxl345.button_pressed)


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
    
    elif "F" in message: # F stands for floor, from the caretaker to the patient, indicating
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
    
        print("Done broadcasting")
#         lora.send_to_wait("D, done".encode(), CARETAKER_ADDRESS)
        
        can_continue_broadcasting = False
        
        if determined_building != None and determined_floor != None:
            
            determined_building = None
            determined_floor = None
            
            
    
    if is_pulse_detected(pulse_sensor_pin.read_u16(), pulse_threshold):
         
         time_of_this_pulse = ticks_ms()
         
         heart_rate = calc_heart_rate(time_of_this_pulse, time_of_last_pulse)
         
         time_of_last_pulse = time_of_this_pulse
         
     
     body_temp = get_body_temp()
     
     lora.send_to_wait(f"vitals,{heart_rate},{body_temp}", CARETAKER_ADDRESS)

