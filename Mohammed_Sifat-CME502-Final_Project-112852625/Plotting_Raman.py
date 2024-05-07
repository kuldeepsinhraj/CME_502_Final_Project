# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 19:39:51 2024

@author: mohammed sifat
"""
import matplotlib.pyplot as plt
import pandas as pd

x = []
y_list = []

while True:
    filename = input("Enter the name of the file (or type 'done' to finish): ")
    if filename.lower() == 'done':
        break
    else:
        # Open and read data from the file
        with open(filename, 'r') as file:
            x_values = []
            y_values = []
            for line in file:
                data = line.split()
                x_values.append(eval(data[0]))
                y_values.append(eval(data[1]))
            x.append(x_values)
            y_list.append(y_values)

# Normalization Sequence:

# Specify the reference normalization peak by indexing the respective location in lists' x axis
refpeak_start = float(input("Enter starting x-value (Raman shift) of reference peak height range: ")) # value for CeO2 F2g peak is 465.82
refpeak_end = float(input("Enter ending x-value (Raman shift) of reference peak height range: ")) # value chosen for end of peak range is 801.573
ref_index = x[0].index(refpeak_start)
ref_y = [[y_list[i][ref_index]] for i in range(len(y_list))]  # Get corresponding y value from each spectrum
ref_baseline = x[0].index(refpeak_end)  # Determine a corresponding baseline value to establish each peak height

peakheight = [[ref_y[i][0] - y_list[i][ref_baseline] for y in y_list[i]] for i in range(len(y_list))]  # Subtract baselines from corresponding y values to get peak height
ref_peak = max(max(peakheight))  # Largest peak height is selected as reference peak

factors = [ref_peak / max(peakheight[i]) for i in range(len(y_list))]  # Divide largest peak height by each peak height to get respective factor
normalized_y_list = [[factors[i] * y for y in y_list[i]] for i in range(len(y_list))]  # Wavenumber (y-axis) values normalized by multiplying by respective factors

# If the plots need to be translated vertically to be more distinguishable, enter values to shift each respective spectrum by. Otherwise entire a list of '0' values:
shift_values_str = input("Enter list of values (i.e., [X, Y, Z] to shift each respective spectrum by (make sure list is same length as number of spectra): ")  # Define shift values for each spectrum (ex. [0, 1000, -1750, 1200])
shift_values = shift_values_str.strip('[]').split(', ')  # Remove square brackets and split the string separated by commas
shift_values = [float(value) for value in shift_values]  # Convert each value to float

# Apply shifts to normalized spectra
shifted_normalized_y_list = [[shift_values[i] + value for value in normalized_y_list[i]] for i in range(len(y_list))]

# Plotting:

for i, shifted_normalized_y in enumerate(shifted_normalized_y_list):
    plt.plot(x[i], shifted_normalized_y, label = f'Spectrum {i+1}')

plt.gca().axes.get_yaxis().set_ticks([]) # Hide the y-axis ticks
plt.gca().axes.get_yaxis().set_ticklabels([]) # Hide the y-axis scale
plt.xlim(100, 2000)
plt.ylabel('Intensity (a.u.)', fontdict = {"fontname":"Courier New"})
plt.xlabel('Raman shift (cm$^{-1}$)', fontdict = {"fontname":"Courier New"})
plt.title('Normalized Raman Spectra', fontdict = {"fontname":"Courier New", "fontsize":16}, loc = 'center')
plt.legend()
plt.show()

# Data Storage:

dfs = []

for i in range(len(y_list)):
    data = {'Raman shift (cm^-1)': x[i],
            'Intensity (a.u.)': shifted_normalized_y_list[i]}
    df = pd.DataFrame(data)
    dfs.append(df)

final_df = pd.concat(dfs, axis=1)

final_df.to_csv('Normalized_Raman_Spectra.csv', index=False)