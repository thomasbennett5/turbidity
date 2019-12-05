import datetime as dt
import ADS1256
import numpy as np
from time import sleep
import DAC8532
import RPi.GPIO as GPIO

def volts_to_ntu(sens_V, led_V, calib_in):
    sens_order  = fit_power_law(led_V , calib_in[0], calib_in[1], calib_in[2])
    turbidity   = fit_power_law(sens_V,       order, calib_in[3], calib_in[4])
    return turbidity

def fit_power_law(x,a,b,n):
    return a*(x**n) + b

def readADC(Sensor_channel = 7):
    # Read voltage from ADS1256
    reading = float(ADC.ADS1256_GetChannalValue(Sensor_channel))
    voltage = reading/8388607 * 5
    return voltage

def led_brightness(volts):
    DAC.DAC8532_Out_Voltage(DAC8532.channel_A, trig_volt[volts])

def measure_turbidity(calibration, led_v):
    sens_v = readADC()
    return volts_to_ntu(sens_v, led_v, calibration)
  

# Initialize communication with ADS1256
ADC = ADS1256.ADS1256()
if (ADC.ADS1256_init() == -1):
    exit()

# DAC Intitialisation
DAC = DAC8532.DAC8532()
DAC.DAC8532_Out_Voltage(DAC8532.channel_A, 1.0)

calibration = np.loadtxt("calibration.fit")
led_volts = 2.5

led_brightness(led_volts)


while True:
    measure_turbidity(calibration,led_volts)
    sleep(0.5)


DAC.DAC8532_Out_Voltage(DAC8532.channel_A, 0)
GPIO.cleanup()