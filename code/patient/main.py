from utime import sleep, ticks_ms
from patient_header_file import all_nodes, broadcast_lora, pulse_sensor_pin, lora, CARETAKER_ADDRESS, i2c, init_adxl345, read_accel_data
from ulora import LoRa
from machine import Pin, ADC



can_continue_broadcasting = True
has_patient_tripped = False
determined_building = None
determined_floor = None
pulse_threshold = 58000
time_of_last_pulse = 0
body_temp = 0


init_adxl345(i2c)


def on_recv(payload):
    
    global can_continue_broadcasting, determined_building, determined_floor
    
    if payload.message.contains("continue"):
        
        can_continue_broadcasting = True
        
    elif payload.message.contains("building"):
        
        _, determined_building = payload.message.split(',')
        
    elif payload.message.contains("floor"):
        
        _, determined_floor = payload.message.split(',')
        
    
        
# set callback
lora.on_recv = on_recv

# set to listen continuously
lora.set_mode_rx()


while True:
    
    if can_continue_broadcasting == True:
        
        broadcast_lora(all_nodes, determined_building, determined_floor)
        
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
    
    
    has_patient_tripped = check_patient_tripping()
    
    if has_patient_tripped:
        
        lora.send_to_wait("tripped", CARETAKER_ADDRESS)
        
    
    
    
        

