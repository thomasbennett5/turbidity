import matplotlib.pyplot as plt
import numpy as np

calib_data = open("data_calibration/271119-NTUstds-sensgain10_rep7.txt")
raw_data = calib_data.readlines()
header = raw_data[2].split()

data = raw_data[3:]

for idx, row in enumerate(data):
    data[idx] = row.strip()
    data[idx] = row.split()

data = np.array(data).astype(np.float)

print (header)
plt.figure(1)
x_ax = data[:,0]
for i in range(1,6):
    plt.plot(x_ax,data[:,i], label = header[i])
plt.legend()

sens_header = header.copy()
sens_header.remove("LEDv")
sens_data = np.delete(data,0,1)

if sens_header[0] == "air":
    sens_header[0] = 0

sens_header = np.array(sens_header).astype(np.float)

plt.figure(2)

sorted_idx = sens_header.argsort()

sens_header = sens_header[sorted_idx]
sens_data   = sens_data[:,sorted_idx]

print (sens_data)
print (sens_header)
calibration_range = int(np.where(sens_data[:,1] == 5.0)[0]) - 1

#print (calibration_range)

sens_header = sens_header[1:]
sens_data = sens_data[:,1:]

calibration_fit = []
for i in range(len(sens_data[:calibration_range,0])):
    fit = np.polyfit(sens_data[i,:],sens_header,1)
    calibration_fit.append(fit)
    plt.plot(sens_data[i,:], sens_header)

print ("FIt is ",fit)
x = data[:,0]
#fit_data = fit[0]*(x**2)  + fit[1]*x + fit[2]
fit_data  = fit[0]*x + fit[1]
print (fit_data)
plt.plot(data[:,0],fit_data)
#plt.show()

#print (calibration_fit)

calibration_fit = np.array(calibration_fit)

plt.figure(3)
plt.plot(data[:calibration_range,0],calibration_fit[:,0])
plt.plot(data[:calibration_range,0],calibration_fit[:,1])
#plt.plot(data[:calibration_range,0],calibration_fit[:,2])
plt.show()

