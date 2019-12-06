import datetime as dt
import ADS1256
import numpy as np
from time import sleep
import DAC8532
import RPi.GPIO as GPIO
import sys

def volts_to_ntu(sens_V, led_V, calib_in, func = 'LIN'):
    fit_a       = fit_power_law(led_V, calib_in[0,0], calib_in[0,1], calib_in[0,2])
    fit_b       = fit_power_law(led_V, calib_in[1,0], calib_in[1,1], calib_in[1,2])
    turbidity   = fit_line(sens_V,   fit_a, fit_b)

    return turbidity

def fit_line(x,a,b):
    return a*x + b

def fit_power_law(x,a,b,n):
    return a*(x**n) + b

def readADC(Sensor_channel = 7):
    # Read voltage from ADS1256
    reading = float(ADC.ADS1256_GetChannalValue(Sensor_channel))
    voltage = reading/8388607 * 5
    return voltage

def led_brightness(volts):
    DAC.DAC8532_Out_Voltage(DAC8532.channel_A, volts)

def measure_turbidity(calibration, led_v):
    sens_v = readADC()
    return volts_to_ntu(sens_v, led_v, calibration), sens_v

def empty_check():
    print 'Performing empty check'
    print 'Please ensure no sample is present'

    led_std  = 2.0
    expected = 2.9082
    offset = 0
    led_brightness(led_std)
    while readADC() > expected:
        offset -= 0.1
        led_brightness(led_std+offset)
        sleep(0.1)
    
    while readADC() < expected:
        offset += 0.1
        led_brightness(led_std+offset)
        sleep(0.1)
    
    print 'Empty check complete'
    print 'offset = ', offset
    return offset

# Initialize communication with ADS1256
ADC = ADS1256.ADS1256()
if (ADC.ADS1256_init() == -1):
    exit()

# DAC Intitialisation
DAC = DAC8532.DAC8532()
DAC.DAC8532_Out_Voltage(DAC8532.channel_A, 1.0)


offset_test = raw_input("Would you like to perform an offset check? (yes/no)")

if offset_test == 'yes':
    offset = empty_check()

else: offset = 0

calibration = np.loadtxt("calibration.fit")

led_volts = input("Enter LED voltage here :")
led_volts = led_volts
led_brightness(led_volts+offset)

while True:

    buffer      = 10.0
    turb_avg    = 0
    sens_v_avg  = 0

    for i in np.arange(buffer):
        turb, sens_volts = measure_turbidity(calibration,led_volts)
        turb_avg        += turb
        sens_v_avg  += sens_volts
        sleep(0.1)
    
    turb_res = turb_avg / buffer
    sens_v_res = sens_v_avg / buffer

    sys.stdout.write("\r" + "Turbidity: " + str(turb_res) + ' NTU - Sens_v : ' +str(sens_v _res) )
    sys.stdout.flush()
    sleep(0.5)


DAC.DAC8532_Out_Voltage(DAC8532.channel_A, 0)
GPIO.cleanup()
