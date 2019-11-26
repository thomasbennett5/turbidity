import ADS1256
import RPi.GPIO as GPIO 
from time import sleep

GPIO.setmode(GPIO.BCM) 

def readADC_volts(Sensor_channel = 7):
    # Read voltage from ADS1256
    reading = ADC.ADS1256_GetChannalValue(Sensor_channel)
    voltage = reading/8388607 * 5
    return voltage

# Initialize communication with ADS1256
ADC = ADS1256.ADS1256()
ADC.ADS1256_ConfigADC(1,00x03)

for i in range(1000):    
    #reading = ads1256.read_all_channels()
    reading = readADC_volts(7)
    print reading
    sleep(0.01)
