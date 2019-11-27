import matplotlib.pyplot as plt
import numpy as np

calib_data = open("261119-NTUstds-sensgain10.txt")

raw_data = calib_data.readlines()

header = raw_data[2].split()

data = raw_data[3:]

for idx, row in enumerate(data):
    data[idx] = row.strip()
    data[idx] = row.split()

data = np.array(data).astype(np.float)
print (data)

plt.figure()
x_ax = data[:,1]
for i in [0,2,3,4]:
    plt.plot(x_ax,data[:,i], label = header[i])
plt.legend()
plt.show()