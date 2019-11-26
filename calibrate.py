import ADS1256
import DAC8532 as dac
import RPi.GPIO as GPIO
import numpy as np
from time import sleep
import datetime as dt
import csv
import RPi.GPIO as GPIO 

def readADC_volts(Sensor_channel = 7):
    # Read voltage from ADS1256
    reading = ADC.ADS1256_GetChannalValue(Sensor_channel)
    voltage = reading/8388607 * 5
    return voltage

def led_brightness(level):
    trig_volt = {"1": 1.0, "2": 2.0, "3": 2.5, "4": 3.0, "5": 3.5}
    DAC.DAC8532_Out_Voltage(dac.channel_A, trig_volt[level])

def calibrate():
    led_levels = np.arange(0,5.5,0.5)
    calibration_data["LEDv"] = led_levels
    response2LED = np.zeros(len(led_levels))
    print heading("NTU Value: " + str(NTU_value))

    for i, y in enumerate(led_levels):
        DAC.DAC8532_Out_Voltage(dac.channel_A, y)
        sleep(0.2)
        average = np.zeros(10)
        for j, x in enumerate(average):
            if j == 0: readADC_volts()
            average[j] = readADC_volts()
            sleep(0.02)

        response2LED[i] = np.average(average)
        print "LED Voltage: ", y, "Sensor Voltage: ", response2LED[i]
    
        if np.average(average) == 5: break

    return response2LED

def header_make():
        
    title = "Calibration file for turbity fibre optics system"
    datetime  = "Date and Time of Calibration: " + dt.datetime.now().strftime('%Y-%m-%d - %H:%M:%S')    
    header = [title, datetime]
    return header

def heading(text, width= 40):
    stars = "*" * width
    pad = (width +len(text))//2
    return '{0}\n{1:>{2}}\n{0}'.format(stars, text, pad)

def file_output(dictionary, header=header_make()):
    calib_out = open('calibration.txt', "w")
    for i in header_make():
        calib_out.write(i+"\n")
    
    sort_ind = np.argsort(dictionary.keys())
    colhdr = np.array(dictionary.keys())[sort_ind]
    colhdr = np.roll(colhdr, 2)
    
    colhdr = tuple(colhdr)
    colhdr = "%6s "*len(colhdr)%colhdr
    print colhdr
    
    calib_data = np.array(dictionary.values()).T
       
    if calib_data.ndim == 1:
        calib_data = calib_data[sort_ind]
    else: 
        calib_data = calib_data[:,sort_ind]

    # roll the array 1 place to the right i.e. last column becomes first
    calib_data = np.roll(calib_data,2, axis=1)
    
    
    np.savetxt(calib_out,calib_data, header = colhdr, fmt="%1.4f", comments = "")    
    #data_row = csv.DictWriter(calib_out, dictionary.keys())
    #print data_row
    #data_row.writerow(dictionary)
    #calib_out.write(key +" , "+ data_row.writerow(dictionary[key]) + "\n")
    #file.write(str(calibration_data))
    calib_out.close()    

GPIO.setmode(GPIO.BCM)

# Initialize communication with ADS1256
ADC = ADS1256.ADS1256()

# DAC Intitialisation
DAC = dac.DAC8532()
DAC.DAC8532_Out_Voltage(dac.channel_A, 0)

calibration_data = {}

print 'Turbidity calibration routine'
print "To calibrate for air, enter 'air' below"
print 'For calibration standards, enter the NTU value below'
print "Once you are done, enter 'done' "

NTU_value = None
while NTU_value != 'done':
    NTU_value = raw_input("Enter value here: ")

    if NTU_value == "air":
        calibration_data["air"] = calibrate()

    else:
        if NTU_value != "done":
            NTU_value = float(NTU_value)
            calibration_data[str(NTU_value)] = calibrate()


file_output(calibration_data)


DAC.DAC8532_Out_Voltage(dac.channel_A, 0)
adc.stop()
GPIO.cleanup()
