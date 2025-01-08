# Import required libraries
import machine  # For interfacing with hardware components like ADC
from utime import sleep    # For time-related functions, such as sleep
 
# Initialize the ADC (Analog to Digital Converter) on pin 26 for reading LM35 temperature sensor
LM35 = machine.ADC(28)
 
# Define a calibration offset value. This is determined through practical testing to correct systematic error.
Cal_Offset = -1650
 
# Function to compute temperature from the averaged analog readings
def Compute_Temp(Avg_A):
    # Add calibration adjustment to the average ADC value
    LM35_A = Avg_A + Cal_Offset
    # Convert the adjusted analog reading to voltage (assuming each ADC unit represents .00005 Volts)
    LM35_V = LM35_A * .00005
    # Convert the voltage to temperature in Celsius (since LM35 has a scale factor of 10mV/°C)
    Tmp_C = round((LM35_V * 100), 1)
    # Convert temperature from Celsius to Fahrenheit
    #Tmp_F = round((Tmp_C * 1.8 + 32), 1)

    return Tmp_C
 
# Initialize variables for accumulating samples and counting the number of samples
Samples = 0
Num_Samples = 1

def get_samples_average():
    
    global Num_Samples, Samples 
    
    while True:
        # Check if fewer than 10 samples have been collected
        if Num_Samples <= 10:
            # Read the current temperature sensor value from the ADC
            LM35_A = LM35.read_u16()
            # Add the current reading to the total samples accumulator
            Samples += LM35_A
            # Increment the counter for the number of samples collected
            Num_Samples += 1
        else:
            # Calculate the average of the collected samples
            Avg_A = Samples / 10
            # Reset the samples accumulator and samples counter for the next batch of readings
            Samples = 0
            Num_Samples = 1

            return Avg_A
        sleep(0.001)

