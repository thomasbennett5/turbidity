import ADS1256
import RPi.GPIO as GPIO 
from time import sleep
import time
import DAC8532

GPIO.setmode(GPIO.BCM) 

def readADC_volts(Sensor_channel = 7):
    # Read voltage from ADS1256
    reading = float(ADC.ADS1256_GetChannalValue(Sensor_channel))
    #reading  = float(ADC.ADS1256_GetAll()[7])
    voltage  = (reading/0x7fffff) * 5
    return voltage

def led_brightness(volts):
    DAC.DAC8532_Out_Voltage(DAC8532.channel_A, volts)
# Initialize communication with ADS1256
ADC = ADS1256.ADS1256()
if (ADC.ADS1256_init() == -1):
    exit()
ADC.ADS1256_ConfigADC(0,0xE0)

# DAC Intitialisation
DAC = DAC8532.DAC8532()
DAC.DAC8532_Out_Voltage(DAC8532.channel_A, 1.0)

led_volts = input("Enter LED voltage here :")
led_brightness(led_volts)

#start = time.time()
for i in range(1000):    
    #reading = ads1256.read_all_channels()
    reading = readADC_volts(7)
    print reading
    sleep(0.1)

DAC.DAC8532_Out_Voltage(DAC8532.channel_A, 0)
GPIO.cleanup()
#end = time.time()
#elapsed = end - start

#print elapsed
