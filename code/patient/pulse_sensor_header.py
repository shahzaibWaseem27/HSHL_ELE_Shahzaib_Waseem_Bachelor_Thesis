from machine import ADC



pulse_sensor_pin = ADC(29)


def is_pulse_detected(signal_val, threshold):
    
    return signal_val >= threshold


def calc_heart_rate(time_of_this_pulse, time_of_last_pulse):
    
    # x seconds --> 1 pulse
    # 1 second --> 1/x pulses
    # 60 seconds --> 60/x pulses
    
    return 60 / (ticks_diff(time_of_this_pulse, time_of_last_pulse) / 1E3) #converting milliseconds result into seconds
