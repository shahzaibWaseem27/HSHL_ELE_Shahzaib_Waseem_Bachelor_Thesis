from machine import Pin, I2C
import time

# I2C setup (move to global scope)
i2c = I2C(0, scl=Pin(21), sda=Pin(20))  # Adjust pins as per your hardware

# ADXL345 I2C Address and Register Definitions
ADXL345_ADDR = 0x53
REG_POWER_CTL = 0x2D
REG_INT_ENABLE = 0x2E
REG_INT_MAP = 0x2F
REG_INT_SOURCE = 0x30
REG_THRESH_FF = 0x28
REG_TIME_FF = 0x29
REG_THRESH_ACT = 0x24
REG_THRESH_INACT = 0x25
REG_TIME_INACT = 0x26
REG_ACT_INACT_CTL = 0x27
REG_DATA_FORMAT = 0x31
FREE_FALL_INT = 0x04
ACTIVITY_INT = 0x10
INACTIVITY_INT = 0x08

# Timing thresholds (ms)
FREE_FALL_TO_ACTIVITY_MAX_TIME = 1000
ACTIVITY_TO_INACTIVITY_MAX_TIME = 5000

# Interrupt tracking flags and timestamps
fall_state = {
    "free_fall_detected": False,
    "activity_detected": False,
    "inactivity_detected": False,
    "last_event_time": 0
}

# GPIO setup for buzzer and button
buzzer = Pin(15, Pin.OUT)
button = Pin(16, Pin.IN, Pin.PULL_DOWN)
int1 = Pin(17, Pin.IN, Pin.PULL_DOWN)

def initialize_adxl345():
    """
    Initializes the ADXL345 accelerometer for fall detection.
    """
    global i2c
    i2c.writeto_mem(ADXL345_ADDR, REG_POWER_CTL, b'\x08')
    i2c.writeto_mem(ADXL345_ADDR, REG_INT_MAP, b'\x00')
    i2c.writeto_mem(ADXL345_ADDR, REG_INT_ENABLE, bytes([FREE_FALL_INT | ACTIVITY_INT | INACTIVITY_INT]))
    i2c.writeto_mem(ADXL345_ADDR, REG_THRESH_FF, b'\x06')
    i2c.writeto_mem(ADXL345_ADDR, REG_TIME_FF, b'\x14')
    i2c.writeto_mem(ADXL345_ADDR, REG_THRESH_ACT, b'\x18')
    i2c.writeto_mem(ADXL345_ADDR, REG_THRESH_INACT, b'\x08')
    i2c.writeto_mem(ADXL345_ADDR, REG_TIME_INACT, b'\x0A')
    i2c.writeto_mem(ADXL345_ADDR, REG_ACT_INACT_CTL, b'\xFF')
    i2c.writeto_mem(ADXL345_ADDR, REG_DATA_FORMAT, b'\x0B')

def reset_fall_state():
    """
    Resets the state for fall detection.
    """
    global fall_state
    fall_state = {
        "free_fall_detected": False,
        "activity_detected": False,
        "inactivity_detected": False,
        "last_event_time": 0
    }

def fall_interrupt_handler(pin):
    """
    Handles interrupts from the ADXL345 accelerometer.
    """
    global fall_state, i2c
    
    int_source = i2c.readfrom_mem(ADXL345_ADDR, REG_INT_SOURCE, 1)[0]
    current_time = time.ticks_ms()

    if int_source & FREE_FALL_INT:
        print("Free Fall Detected")
        fall_state["free_fall_detected"] = True
        fall_state["last_event_time"] = current_time

    if int_source & ACTIVITY_INT:
        print("Impact Detected")
        if fall_state["free_fall_detected"] and time.ticks_diff(current_time, fall_state["last_event_time"]) <= FREE_FALL_TO_ACTIVITY_MAX_TIME:
            fall_state["activity_detected"] = True
            fall_state["last_event_time"] = current_time
        else:
            print("Invalid sequence: Activity interrupt without Free Fall")
            reset_fall_state()

    if int_source & INACTIVITY_INT:
        print("Inactivity Detected")
        if fall_state["activity_detected"] and time.ticks_diff(current_time, fall_state["last_event_time"]) <= ACTIVITY_TO_INACTIVITY_MAX_TIME:
            fall_state["inactivity_detected"] = True
            print("Fall confirmed! Triggering buzzer.")
            buzzer.on()
            reset_fall_state()
        else:
            print("Invalid sequence: Inactivity interrupt without prior Activity")
            reset_fall_state()

def button_pressed(pin):
    """
    Handles button press to turn off the buzzer and reset state.
    """
    if pin.value():
        print("Buzzer turned off by button press.")
        buzzer.off()
        reset_fall_state()
