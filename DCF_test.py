import ads1256 as adc
import numpy as np
from time import sleep
import datetime as dt
import signal
import sys
def signal_handler(signal, frame):
    global interupted
    interupted = True

def readADC_volts(channel = 5):
    # Read voltage from ADS1256
    reading = float(adc.read_channel(channel))
    voltage = reading/8388607 * 5
    return voltage

adc.start("1", "2d5")

signal.signal(signal.SIGINT, signal_handler)
interupted = False

dataLog = open("dcf_datalog.txt", "w")
dataLog.write("%5s %5s"%("Time", "Volts\n"))

print "DCF Survival Test"
print "Start time: ", dt.datetime.now().strftime('%Y-%m-%d - %H:%M:%S')


print "Press CTRL-C to exit safely"
count = 0
while True:
    dataLine = (dt.datetime.now().strftime('%Y-%m-%d - %H:%M:%S'), readADC_volts(channel = 7))
    dataLog.write("%s %s \n"%dataLine)
    count+=1
    sys.stdout.write("\r" + "Measurement Number: " + str(count))
    sys.stdout.flush()

    if interupted:
        print "\n Closing"
        break
    sleep(5)

dataLog.close()
adc.stop()
