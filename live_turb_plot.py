import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ADS1256
import numpy as np
from matplotlib import ticker
from matplotlib.widgets import Button, RadioButtons
from time import sleep
import DAC8532
import RPi.GPIO as GPIO


def volts_to_ntu(sens_V, led_V, calib_in):
    sens_order  = fit_power_law(led_V , calib_in[0], calib_in[1], calib_in[2])
    turbidity   = fit_power_law(sens_V,       order, calib_in[3], calib_in[4]))
    return turbidity

def fit_power_law(x,a,b,n):
    return a*(x**n) + b

# Function to stop the animation on button press and save data gathered
def savquit(event):
    ani.event_source.stop()
    dataOut = np.array([xs_master, ys_master]).T
    fname = "turbidity_"+dt.datetime.now().strftime('%y%m%d%H%M%S')+".txt"
    #print dataOut
    np.savetxt(fname, dataOut, fmt="%s")
    return

# Function to stop the animation on button press
def quit(event):
    ani.event_source.stop()
    return

def readADC(Sensor_channel = 7):
    # Read voltage from ADS1256
    reading = float(ADC.ADS1256_GetChannalValue(Sensor_channel))
    voltage = reading/8388607 * 5
    return voltage

def led_brightness(volts):
    trig_volt = {"0":0.0, "1": 1.0, "2": 2.0, "3": 2.5, "4": 3.0, "5": 3.5}
    DAC.DAC8532_Out_Voltage(DAC8532.channel_A, trig_volt[volts])
    
# This function is called periodically from FuncAnimation
def animate(i, ys, xs):
    
    voltage = readADC()
    
    # Add x and y to lists
    xs_master.append(dt.datetime.now()) #.strftime('%H:%M:%S'))
    ys_master.append(voltage)
    
    # Limit x and y lists to 20 items
    xs = xs_master[-plot_buffer:]
    ys = ys_master[-plot_buffer:]
    
    line.set_ydata(ys)
    line.set_xdata(xs)

    live_line.set_ylim(min(ys)-0.2,max(ys)+0.2)
    live_line.set_xlim(min(xs), max(xs))
    #live_line.yaxis.set_major_locator(ticker.AutoLocator)
    #print voltage,"Volts    \r",
    
    #ax_tb = plt.axes([0.125, 0.01, 0.775, 0.075])
    live_num.clear()
    live_num.text(0.1, 0.1, "Voltage: %.5s" % voltage, fontsize = 20)
    
    return line,

def init
# Create figure for plotting
fig = plt.figure()
plt.ion()

live_line = fig.add_subplot(2, 2, 1)
# Format live line plot
plt.xticks(rotation=45, ha='right')
plt.title('Voltage over Time')
plt.ylabel('Voltage (V)')

live_num  = fig.add_subplot(2, 2, 2)
# Format live number plot
live_num.set_frame_on(False)
live_num.get_xaxis().set_visible(False)
live_num.get_yaxis().set_visible(False)

radio_butts = fig.add_subplot(2, 2, 3)
# Format radiobutton plot
radio_butts.set_frame_on(False)
radio_butts.get_xaxis().set_visible(False)
radio_butts.get_yaxis().set_visible(False)

# Set up radio buttons
rax = plt.axes([0.1,0.1,0.25,0.25])
volt_select = RadioButtons(rax, ("0","1", "2", "3", "4", "5"))
volt_select.on_clicked(led_brightness)

# Initialise data
plot_buffer = 100
xs_master = []
ys_master = []
line, = live_line.plot(xs_master,ys_master)

# Initialize communication with ADS1256
ADC = ADS1256.ADS1256()
if (ADC.ADS1256_init() == -1):
    exit()

# DAC Intitialisation
DAC = DAC8532.DAC8532()
DAC.DAC8532_Out_Voltage(DAC8532.channel_A, 1.0)

# Make a button
quit_butt_location = plt.axes([0.65, 0.05, 0.15, 0.04])
quit_butt = Button(quit_butt_location, "Quit")
quit_butt.on_clicked(quit)

savquit_butt_location = plt.axes([0.81, 0.05, 0.15, 0.04])
savquit_butt = Button(savquit_butt_location, "Save & Quit")
savquit_butt.on_clicked(savquit)

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(ys_master,xs_master,), interval=1)

plt.show()

DAC.DAC8532_Out_Voltage(DAC8532.channel_A, 0)
GPIO.cleanup()

