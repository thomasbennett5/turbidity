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
    header = raw_data[4].split()
    standard_data = raw_data[5:]
    for idx, row in enumerate(standard_data):
        standard_data[idx] = row.strip()
        standard_data[idx] = row.split()
    print (header)
    standard_data       = np.array(standard_data).astype(np.float)
    header_num          = np.array(header[3:]).astype(np.float) 
    sort_idx            = header_num.argsort()
    header[3:]          = header_num[sort_idx]
    standard_data[:,3:] = standard_data[:,3:][:,sort_idx]

    return standard_data, header

def plot_all_data(data):
    '''
    Function to plot all raw calibration data for inspection
    Expects sorted numpy array of all numerical data gathered from calibrate.py

    returns: nothing
    '''
    plt.figure(1)
    x_ax = data[:,0]
    for i in range(1,7):
        plt.plot(x_ax,data[:,i], label = header[i])
    plt.legend()
    plt.show()

def plot_turbidity(data, header):
    '''
    Function to plot the detector voltage against NTU value given by the standards
    Expects:
        1. Sorted numpy array of all numerical data gathered from calibrate.py
        2. Header which includes numerical values for turbidity standards
    
    Produces plot of 1 line for each LED brightness recorded in the calibration

    returns nothing 

    '''
    plt.figure(2)
    if 5.0 in data[:,3:]:
        calibration_range = int(np.where(data[:,3] == 5.0)[0]) - 1
    else: calibration_range =len(data[:,3])

    for i in range(len(data[:calibration_range,0])):
        plt.plot(data[i,3:], header[3:])

def fit_power_law(x,a,b,n):
    '''
    Equation for a power law to be called by scipy-optimize function
    '''
    return a*(x**n) + b

def fit_line(x,a,b):
    '''
    Equation for a line to be called by scipy-optimize function
    '''
    return a*x + b

def turb_fitting_routine(data, header, plot=False, func='LIN'):
    '''
    Routine for fitting detector voltage against turbidity (NTU)
    Expects: 
        1. numerical data for sensor voltage
        2. header which contains NTU values for turbidity standards
    Optional: 
        plot -  a boolean for whether or not you would like the calculated fits to be plotted
        func -  string to specify what type of funciton you would like to fit
                (either 'LIN' (linear) or 'PL' Power Law)
    Returns: 2D array of fit parameters (one for each LED brighntess)
    '''

    if plot == True: plt.figure(2)
    
    ## Set fitting function depending on func string
    if func == 'LIN':
        fit_func = fit_line
    if func == 'PL': 
        fit_func = fit_power_law

    ## Determine the range of voltages before saturation (at 5.0 V)
    if 5.0 in data[:,3:]:
        calibration_range = int(np.where(data[:,3] == 5.0)[0]) - 1
    else: calibration_range = len(data[:,2])

    ## perform scipy-curve_fit on every LED brightness agaist NTU standards
    calibration_fit = []
    ## Ignore first 2 LED brightness due to discontinuity
    for i in range(2,calibration_range):
        fit, tmp  = spo.curve_fit(fit_func, data[i,3:],header[3:])
        calibration_fit.append(fit)
        if plot == True:
            ## Number of parameters returned is dependant on functional form of fit
            if func == 'PL':
                fit_data  = fit_func(data[:,0],fit[0], fit[1], fit[2])
            if func == 'LIN':
                fit_data  = fit_func(data[:,0],fit[0], fit[1])
            
            plt.plot(data[:,0],fit_data)
        
    if plot == True: plt.show()
    # create empty array with height and width one larger than the input data
    calibration_fit = np.array(calibration_fit)
    width_arr = len(calibration_fit[0,:])+1
    height_arr = len(calibration_fit[:,0])
    calibration_Volts = np.zeros((height_arr,width_arr))
    calibration_Volts[:,1:] = calibration_fit
    calibration_Volts[:,0]  = data[2:calibration_range,0] 

    ## if the fit is a power law, b and n are approximately constant so they are averaged
    ## to simplify backfitting
    if func == 'PL':
        fit_approx = calibration_Volts
        fit_approx[:,2] = np.average(calibration_Volts[:,2])
        fit_approx[:,3] = np.average(calibration_Volts[:,3])
    
    ## No approximation can be done for linear fits
    if func == 'LIN':
        fit_approx = calibration_Volts
    return fit_approx

def volt_fitting_routine(data,func='PL', turb='LIN'):
    '''
    Function to fit a function to backfit the LED voltage to the relevant gradient/intercept
    of turbidity fit.

    Expects:
        Raw calibration data
    Optional: 
        func - type of fit required (defaults to power law (PL))
        turb - type of fit used for the turbidity fitting

    Returns: power law fit (1 D array)
    '''
    
    ## Select functional form based on func input
    if func == 'PL':
        fit_func = fit_power_law
    if func == 'LIN':
        fit_func = fit_line
    

    if turb == 'PL':
        fit_a, tmp  = spo.curve_fit(fit_func, data[:,0], data[:,1])
        fit_b, tmp  = spo.curve_fit(fit_func, data[:,0], data[:,2])
        fit = np.array([fit_a, fit_b])
    if turb == 'LIN':
        fit_a, tmp  = spo.curve_fit(fit_func, data[:,0], data[:,1],  [-1000,-50,-1])
        fit_b, tmp  = spo.curve_fit(fit_func, data[:,0], data[:,2],  [100,2000,-1])
        fit = np.array([fit_a, fit_b])
    return fit

def reject_outliers(data, m=2, colIdx=1):
    '''
    Experimental and unused function to reject outlying calibration results
    '''
    return data[abs(data[:,colIdx] - np.mean(data[:,colIdx])) < m * np.std(data)]

def save_final_calibration(turb_cal, volt_cal):
    '''
    Function to save the fit parameters for backfitting LED brightness and Sensor Voltage to turbidity
    '''
    if len(turb_cal[1,:]) == 4:
        final_calib_data = np.array((volt_cal[0],volt_cal[1],volt_cal[2], turb_cal[0,2], turb_cal[0,3]))
    
    if len(turb_cal[1,:]) == 3:
        final_calib_data = volt_cal #np.array((volt_cal[0],volt_cal[1], turb_cal[0,1]))
    np.savetxt('calibration.fit', final_calib_data)


def volts_to_ntu(sens_V, led_V, calib_in, func = 'LIN'):
    '''
    Back fitting function
    '''
    
    fit_a       = fit_power_law(led_V, calib_in[0,0], calib_in[0,1], calib_in[0,2])
    fit_b       = fit_power_law(led_V, calib_in[1,0], calib_in[1,1], calib_in[1,2])
    turbidity   = fit_line(sens_V,   fit_a, fit_b)

    return turbidity

## ~~~~~~~~~~~~~~~~~~~~
##         MAIN
## ~~~~~~~~~~~~~~~~~~~~
fname = "calibration.raw"

data, header = read_in(fname)

plot_all_data(data)
plot_turbidity(data, header)

turb_calibration = turb_fitting_routine(data,header, plot=True, func = 'LIN')
volt_calibration = volt_fitting_routine(turb_calibration, func = 'PL')
print (turb_calibration)
print (volt_calibration)
save_final_calibration(turb_calibration, volt_calibration)



##~~~~~~~~~~~~~~~~~~~
## TEST SPACE
##~~~~~~~~~~~~~~~~~~~
'''
print (data)
plt.figure(11)
plt.plot(turb_calibration[:,0],turb_calibration[:,1],'r')
plt.plot(turb_calibration[:,0], fit_power_law(turb_calibration[:,0], volt_calibration[0,0], volt_calibration[0,1], volt_calibration[0,2]))
plt.plot(turb_calibration[:,0], fit_power_law(turb_calibration[:,0], volt_calibration[1,0], volt_calibration[1,1], volt_calibration[1,2]))
plt.plot(turb_calibration[:,0],turb_calibration[:,2])
plt.show()

'''
plt.figure(12)

calibration = np.loadtxt("calibration.fit")
sensor  = np.arange(1,5,1)
led     = np.arange(1,5,1)

print (data[10,3:])
plt.plot(sensor, volts_to_ntu(sensor,2, calibration))
plt.plot(data[10,3:],header[3:])
plt.show()
