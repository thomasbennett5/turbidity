import ads1256
from time import sleep

# Initialize communication with ADS1256

ads1256.start("1", "100")

for i in range(1000):    
    #reading = ads1256.read_all_channels()
    reading = ads1256.read_channel(7)    
    print reading
    sleep(0.01)

ads1256.stop()
