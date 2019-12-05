import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo



def read_in(fname):
    '''
    Function to read in data collected by TB's calibration data collection script
    This function expects a two line descriptive header, followed by column headers

    Numerical data is expected from line 4 onwards

    Returns: 
        numerical data array (sorted)
        character vector of column headers (sorted)
    '''

    calib_data = open("data_calibration/"+fname)
    raw_data = calib_data.readlines()
    header = raw_data[2].split()
    standard_data = raw_data[3:]
    for idx, row in enumerate(standard_data):
        standard_data[idx] = row.strip()
        standard_data[idx] = row.split()
    print (header)
    standard_data       = np.array(standard_data).astype(np.float)
    header_num          = np.array(header[2:]).astype(np.float) 
    sort_idx            = header_num.argsort()
    header[2:]          = header_num[sort_idx]
    standard_data[:,2:] = standard_data[:,2:][:,sort_idx]

    return standard_data, header

def plot_all_data(data):
    plt.figure(1)
    x_ax = data[:,0]
    for i in range(1,6):
        plt.plot(x_ax,data[:,i], label = header[i])
    plt.legend()
    plt.show()

def plot_turbidity(data, header, air = False):
    plt.figure(2)
    if 5.0 in data[:,2:]:
        calibration_range = int(np.where(data[:,2] == 5.0)[0]) - 1
    else: calibration_range =len(data[:,2])
    for i in range(len(data[:calibration_range,0])):
        plt.plot(data[i,2:], header[2:])
    #plt.show()

def fit_power_law(x,a,b,n):
    return a*(x**n) + b

def fit_line(x,a,b):
    return a*x + b

def turb_fitting_routine(data, header, plot=False, func='LIN'):
    if plot == True: plt.figure(2)
    
    if func == 'LIN':
        fit_func = fit_line

    if func == 'PL': 
        fit_func = fit_power_law
    if 5.0 in data[:,2:]:
        calibration_range = int(np.where(data[:,2] == 5.0)[0]) - 1
    else: calibration_range = len(data[:,2])

    calibration_fit = []
    for i in range(2,len(data[:calibration_range,0])):
        fit, tmp  = spo.curve_fit(fit_func, data[i,2:],header[2:])
        calibration_fit.append(fit)
        #print (i, fit)
        if plot == True:
            if func == 'PL':
                fit_data  = fit_func(data[:,0],fit[0], fit[1], fit[2])
            if func == 'LIN':
                fit_data  = fit_func(data[:,0],fit[0], fit[1])
            
            plt.plot(data[:,0],fit_data)
        
    if plot == True: plt.show()

    calibration_fit = np.array(calibration_fit)
    width_arr = len(calibration_fit[0,:])+1
    height_arr = len(calibration_fit[:,0])

    calibration_Volts = np.zeros((height_arr,width_arr))
    calibration_Volts[:,1:] = calibration_fit
    calibration_Volts[:,0]  = data[2:calibration_range,0] 

    #np.savetxt("current_cal.fit", calibration_Volts)
    if func == 'PL':
        fit_approx = calibration_Volts
        fit_approx[:,2] = np.average(calibration_Volts[:,2])
        fit_approx[:,3] = np.average(calibration_Volts[:,3])
    if func == 'LIN':
        fit_approx = calibration_Volts
        #fit_approx[:,2] = np.average(calibration_Volts[:,2])
    
    return fit_approx

def volt_fitting_routine(data,func='LIN', turb='LIN'):
    if func == 'PL':
        fit_func = fit_power_law
    if func == 'LIN':
        fit_func = fit_line
    
    if turb == 'PL':
        fit_a, tmp  = spo.curve_fit(fit_func, data[:,0], data[:,1])
        fit_b, tmp  = spo.curve_fit(fit_func, data[:,0], data[:,2])
        fit = [fit_a, fit_b]
    if turb == 'LIN':
        fit_a, tmp  = spo.curve_fit(fit_func, data[:,0], data[:,1], [1,1,-10])
        fit_b, tmp  = spo.curve_fit(fit_func, data[:,0], data[:,2], [1,1,-10])
        fit = [fit_a, fit_b]
    return fit

def save_final_calibration(turb_cal, volt_cal):
    if len(turb_cal[1,:]) == 4:
        final_calib_data = np.array((volt_cal[0],volt_cal[1],volt_cal[2], turb_cal[0,2], turb_cal[0,3]))
    
    if len(turb_cal[1,:]) == 3:
        final_calib_data = volt_cal #np.array((volt_cal[0],volt_cal[1], turb_cal[0,1]))
    np.savetxt('calibration.fit', final_calib_data)

    '''
    calib_save = open("calibration.fit", 'w')
    for i in final_calib_data:
        calib_save.write(str(i)+'\n')
    calib_save.close()
    '''

def volts_to_ntu(sens_V, led_V, calib_in, func = 'LIN'):
    
    fit_a       = fit_power_law(led_V, calib_in[0,0], calib_in[0,1], calib_in[0,2])
    fit_b       = fit_power_law(led_V, calib_in[1,0], calib_in[1,1], calib_in[1,2])
    turbidity   = fit_line(sens_V,   fit_a, fit_b)

    return turbidity

## ~~~~~~~~~~~~~~~~~~~~
##         MAIN
## ~~~~~~~~~~~~~~~~~~~~
fname = "calibration.raw"

data, header = read_in(fname)

#plot_all_data(data)
#plot_turbidity(data, header)

turb_calibration = turb_fitting_routine(data,header, plot=False, func = 'LIN')
volt_calibration = volt_fitting_routine(turb_calibration, func = 'PL')
print (turb_calibration)
print (volt_calibration)
save_final_calibration(turb_calibration, volt_calibration)


##~~~~~~~~~~~~~~~~~~~
## TEST SPACE
##~~~~~~~~~~~~~~~~~~~

calibration = np.loadtxt("calibration.fit")
led_volts   = 1.2
sens_volts  = 1.22
spoof_data  = np.arange(0,5, 0.1)

print(volts_to_ntu(sens_volts,led_volts,calibration))
