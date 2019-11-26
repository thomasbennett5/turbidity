import ads1256
from time import sleep
import numpy as np


def volts2turb(volts):
	""" from manufacturer callibration curve """
	turbidity = -1120.4*(volts**2) + 5742.3*volts - 4352.9
	return turbidity

ads1256.start("1", "10")



data = []
mean = []
count = 0

for i in range(7500*60*10):

	reading = float(ads1256.read_channel(7))
	#print reading
	voltageOut = reading/8388607 * 5
	#print voltageOut,"Volts    \r",
	sleep(0.1)
	mean.append(voltageOut)

	if i % 1 == 0:
		avgVolts = float(sum(mean))/len(mean)
		data.append(avgVolts)
		mean = []
		count += 1
		print count, avgVolts, " Volts", reading
		#print volts2turb(avgVolts), "NTU \r",

np.savetxt("Settling Data.txt", np.array(data))

ads1256.stop()




