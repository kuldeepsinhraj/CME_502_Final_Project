import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.signal import find_peaks,peak_widths

# Open data file
infilename = input('Input filename.extension for input: ')
dsc_data = open(infilename, 'r', encoding="latin-1")

# dsc_data = open('pla_ori_1030.pdid.txt', 'r', encoding="latin-1")

# Open a file to write to
cut_data = open('dsc_intermediate.txt', 'w')

# Read file
for line in range(2742):                                                # line 2742 starts cooling
    if line < 42-1:                                                     # 42-1 to remove header
        dsc_data.readline()
    elif line == 101 or line == 2742 or line == 2803 or line == 3464:
        dsc_data.readline()
    else:
        # Write to new file
        cut_data.write(dsc_data.readline())

# Close files
dsc_data.close()
cut_data.close()

# Initialize empty lists for each column
time = []
heatflow_unsubtracted = []
heatflow_baseline = []
temperature_program = []
temperature_sample = []
gasflow = []
heatflow_calibration = []

# Open the tab-delimited file for reading
with open('dsc_intermediate.txt','r',encoding='latin-1') as file:
    for line in file:
        # Split each line by tabs to separate the columns
        columns = line.strip().split('\t')

        # Check if the line has at least 3 columns (you can adjust this as needed)
        if len(columns) >= 7:
            # Save each column's data into the respective lists
            time.append(float(columns[0]))
            heatflow_unsubtracted.append(float(columns[1]))
            heatflow_baseline.append(float(columns[2]))
            temperature_program.append(float(columns[3]))
            temperature_sample.append(float(columns[4]))
            gasflow.append(float(columns[5]))
            heatflow_calibration.append(float(columns[6]))

ith_row = 7  
jth_column = 1

# Initialize a variable to store the extracted value
sample_weight = 0.0

# Open the tab-delimited file for reading with the appropriate encoding
with open('pla_ori_1030.pdid.txt','r',encoding='latin-1') as file:
    for i, line in enumerate(file):
        # Check if the current line matches the target row
        if i == ith_row:
            # Split the line by tabs to access columns
            columns = line.strip().split('\t')
            
            # Check if the target column exists
            if jth_column < len(columns):
                # Extract the value in the jth column of the ith row
                sample_weight = float(columns[jth_column])
                break

arr = np.array(heatflow_unsubtracted)
max_ind = np.argmax(arr)

# Remove unstable early data points
n = max_ind
while arr[n] > 0:
    n += 1

result = arr/sample_weight
heatflow_normalized = result.tolist()

heatflow = np.array(heatflow_normalized)
temperature = np.array(temperature_sample)
time_arr = np.array(time)

delta = []
for i in range(len(time)-1):
    delta.append(heatflow[i+1]-heatflow[i])

delta = np.array(delta)

# # Define fit function
# def f(t,a,b,c,d,e):
#     return np.exp(d*t)*(a*t**2+b*t+c)+e

# p0 = [-0.005,-0.02,0.2,-0.1,-0.1] # based on test data
# popt,pcov = scipy.optimize.curve_fit(f,temperature[n:],heatflow[n:],p0=p0)
# heat_fit = f(temperature,*popt)

# Fit curve with polynomial
coefficients = np.polyfit(time[n:],heatflow[n:], deg=2)
fit_funct = np.poly1d(coefficients)
heat_fit = fit_funct(time)

corr_heatflow = heatflow-heat_fit
print(corr_heatflow[n:])

# Create plot
# plt.plot(temperature[n:],heatflow[n:],'r-')
# plt.plot(temperature[n:],heatflow_unsubtracted[n:],'r-')
# plt.plot(temperature[n:],heatflow_baseline[n:],'k--')
plt.plot(temperature[n:],corr_heatflow[n:],'r-') # normalized heat flow plot
# plt.plot(temperature[n:],heat_fit[n:],'k--')

# Set axis titles
plt.xlabel("Temperature [°C]")
plt.ylabel("Heat Flow [W/g]")

# Find peaks
h_peak = max(corr_heatflow[n:])/5 # define minimum height of peak
pos_peaks,pos_info = find_peaks(corr_heatflow[n:],height=h_peak)
neg_peaks,neg_info = find_peaks(-corr_heatflow[n:],height=h_peak)

# results_half = peak_widths(corr_heatflow[n:],pos_peaks,rel_height=0.5)
# print(*results_half[1:])

# Print peak temperatures
print("Positive peaks")
for i in pos_peaks:
    print(f"{temperature[n+i]} °C")
print("Negative peaks")
for i in neg_peaks:
    print(f"{temperature[n+i]} °C")

# Find peak boundaries function
def peak_bounds(heatflow_array,peak_position,low):
    n_peaks = len(peak_position)
    scan_range = 40
    bounds = []
    for i in range(n_peaks):
        # upper bound
        peak = peak_position[i]
        upper = peak+scan_range
        thres = 0.1*heatflow_array[low+peak_position[i]]
        forward_slope = abs(heatflow_array[upper+scan_range]-heatflow_array[upper])
        backward_slope = abs(heatflow_array[upper-scan_range]-heatflow_array[upper])
        while abs(forward_slope-backward_slope)/((forward_slope+backward_slope)/2) < 1.75 and upper+1+scan_range < len(heatflow_array) and heatflow_array[low+upper] > thres:
            upper += 1
            forward_slope = abs(heatflow_array[upper+scan_range]-heatflow_array[upper])
            backward_slope = abs(heatflow_array[upper-scan_range]-heatflow_array[upper])
        # lower bound
        lower = peak-scan_range
        forward_slope = abs(heatflow_array[lower+scan_range]-heatflow_array[lower])
        backward_slope = abs(heatflow_array[lower-scan_range]-heatflow_array[lower])
        while abs(abs(forward_slope-backward_slope)/((forward_slope+backward_slope)/2)) < 1.75 and lower-1-scan_range > low and heatflow_array[low+lower] > thres:
            lower -= 1
            forward_slope = abs(heatflow_array[lower+scan_range]-heatflow_array[lower])
            backward_slope = abs(heatflow_array[lower-scan_range]-heatflow_array[lower])
        bounds.append([lower-1,upper+1])
    return bounds

# Find positive bounds 
bounds = peak_bounds(corr_heatflow,pos_peaks,n)
print(temperature[n+bounds[1][0]],temperature[n+bounds[1][1]])

# Calculate enthalpy by numerically integrating over the peak area and print results
print("Positive peak areas (enthalpy)")
for i in range(len(pos_peaks)):
    lower = bounds[i][0]
    upper = bounds[i][1]
    enthaply = np.trapz(corr_heatflow[n+lower:n+upper],temperature[n+lower:n+upper])*12 # temperature rate
    # -np.trapz(corr_heatflow[n+lower:n+upper],x=[temperature[n+lower],temperature[n+upper]])
    print(f"{enthaply} J/g")
    plt.hlines(0.05*corr_heatflow[n+pos_peaks[i]],temperature[n+lower],temperature[n+upper], color='C2', linestyle='-', label='Peak Widths (FWHM)')

# Find negative bounds
bounds = peak_bounds(-corr_heatflow,neg_peaks,n)
# print(temperature[n+bounds[0][0]],temperature[n+bounds[0][1]])

# Calculate enthalpy by numerically integrating over the peak area and print results
print("Negative peak areas (enthalpy)")
for i in range(len(neg_peaks)):
    lower = bounds[i][0]
    upper = bounds[i][1]
    enthaply = np.trapz(corr_heatflow[n+lower:n+upper],temperature[n+lower:n+upper])*12 # temperature rate
    print(f"{enthaply} J/g")
    # plt.hlines(0.05*corr_heatflow[n+neg_peaks[i]],temperature[n+lower],temperature[n+upper],color='C2',linestyle='-')
# Show the plot
plt.show()

# Percent cystallity can be calcuted by using the equation
# \chi_c = \frac{\Delta H_m-\Delta H_{cc}}{\Delta H_m^0} \times \frac{100}{w}
# where ∆H_m is the enthalpy of melting, ∆H_cc is the enthaply of cold crsytallization, ∆H_m^0 is the enthaply of melting for a 100% crsytalline PLA sample
# (∆H_m^0 = 93.7 J/g) and w is the PLA weight fraction in the blend
# ref. Tisserat et al. Ind. Crops & Prod., 2012