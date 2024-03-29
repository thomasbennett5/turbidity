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
    reading = float(ADC.ADS1256_GetChannalValue(Sensor_channel))
    voltage = reading/8388607 * 5
    return voltage

def led_brightness(level):
    '''
    Function to set LED brightness

    Currently unused
    '''
    trig_volt = {"1": 1.0, "2": 2.0, "3": 2.5, "4": 3.0, "5": 3.5}
    DAC.DAC8532_Out_Voltage(dac.channel_A, trig_volt[level])

def calibrate():
    ## Create array of led voltages between 0 and 5
    led_levels = np.arange(0,5.2,0.2)
    calibration_data["LEDv"] = led_levels
    response2LED = np.zeros(len(led_levels))
    print heading("NTU Value: " + str(NTU_value))

    for i, y in enumerate(led_levels):
        ## for every specified LED brightness, take 20 or (repeats) measurements of detector
        ## voltage and return the average.
        repeats = 20
        DAC.DAC8532_Out_Voltage(dac.channel_A, y)
        sleep(0.01)
        average = np.zeros(repeats)
        for j, x in enumerate(average):
            if j == 0: readADC_volts()
            average[j] = readADC_volts()
            #sleep(0.001)

        response2LED[i] = np.average(average)
        print "LED Voltage: ", y, "Sensor Voltage: ", response2LED[i]

        ## If the average is exactly 5, the detector is staturated to stop
        if np.average(average) == 5: break

    return response2LED

def header_make():  
    '''
    Function to create the header for the file to be saved

    Tile and date are hard coded
    Gain and comments are requested from the user

    returns header as a list of strings
    '''

    title       = "Calibration file for turbity fibre optics system"
    datetime    = "Date and Time of Calibration: " + dt.datetime.now().strftime('%Y-%m-%d - %H:%M:%S')    
    gain        = 'Detector Gain : ' + raw_input('Please enter detector gain: ')
    comments    = 'User comments : ' + raw_input('Any comments: ')
    header = [title, datetime, gain, comments]
    return header

def heading(text, width= 40):
    '''
    Generates a heading to be displayed to the user during calibration
    '''
    stars = "*" * width
    pad = (width +len(text))//2
    return '{0}\n{1:>{2}}\n{0}'.format(stars, text, pad)

def file_output(dictionary):
    '''
    Function to save the raw calibration data to a text file (.raw)
    '''

    header=header_make()
    calib_out = open('calibration.raw', "w")
    for i in header:
        calib_out.write(i+"\n")
    
    ## Sort the array based on the NTU values stored in the header
    ## Then apply the same sort to the numerical data to keep them in line
    sort_ind = np.argsort(dictionary.keys())
    colhdr = np.array(dictionary.keys())[sort_ind]

    calib_data = np.array(dictionary.values()).T
    if calib_data.ndim == 1:
        calib_data = calib_data[sort_ind]
    else: 
        calib_data = calib_data[:,sort_ind]


    for i in dictionary.keys():
        if i in ['air','empty', 'LEDv']:
            # roll the array 3 place to the right i.e. last column becomes first
            calib_data = np.roll(calib_data,1, axis=1)
            colhdr = np.roll(colhdr, 1)

    colhdr = tuple(colhdr)
    colhdr = "%6s "*len(colhdr)%colhdr
    print len(colhdr)

    np.savetxt(calib_out,calib_data, header = str(colhdr), fmt="%1.4f", comments = "")
    calib_out.close()    


# Set mode of GPIO Pins
GPIO.setmode(GPIO.BCM)

# Initialize communication with ADS1256
ADC = ADS1256.ADS1256()
if (ADC.ADS1256_init() == -1):
    exit()
ADC.ADS1256_ConfigADC(0,0xA1)

# DAC Intitialisation
DAC = dac.DAC8532()
DAC.DAC8532_Out_Voltage(dac.channel_A, 0)

calibration_data = {}

## Print the program start spiel and instructions
print 'Turbidity calibration routine'
print "To calibrate for air, enter 'air' below"
print "To calibrate for an empty cuvette, enter 'empty' below "
print 'For calibration standards, enter the NTU value below'
print "Once you are done, enter 'done' "

NTU_value = None
while True:
    NTU_value = raw_input("Enter value here: ")
    if NTU_value == "air":
        calibration_data["air"] = calibrate()
    if NTU_value == "done":
        break
    if NTU_value == "empty":
        calibration_data["empty"] = calibrate()
    else:
        if NTU_value != "done":
            try:
                NTU_value = float(NTU_value)
                calibration_data[str(NTU_value)] = calibrate()
            except:
                print "pardon?"   

file_output(calibration_data)

DAC.DAC8532_Out_Voltage(dac.channel_A, 0)
GPIO.cleanup()


