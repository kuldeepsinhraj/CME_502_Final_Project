# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 00:20:16 2024

@author: mohammed sifat
"""
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.integrate import simps

filename = input("Enter the name of the file: ")
with open(filename, 'r') as file:
    lines = file.readlines()

raman_shift = []
intensity = []

for line in lines:
    data = line.split()
    raman_shift.append(float(data[0]))
    intensity.append(float(data[1]))

data = {'Raman shift': raman_shift, 
        'Intensity': intensity
        }
df = pd.DataFrame(data)

Raman_shift = df['Raman shift']
Intensity = df['Intensity']

fitpeak_start = float(input("Enter the start range (Raman shift) of peak to be fit: ")) # Example Peak 1 Range: [1274.58, 1425.54]
fitpeak_end = float(input("Enter the end range (Raman shift) of peak to be fit: ")) # Example Peak 2 Range: [1499.91, 1701.08]

# Gaussian function:
def gauss_func(x, A, mu, sig):
    return A * np.exp(-(x - mu) ** 2 / (2 * sig ** 2))

# Lorentzian function:
def lorentzian_func(x, A, mu, gamma):
    return A / np.pi * (gamma / ((x - mu) ** 2 + gamma ** 2))

x_data = Raman_shift[(Raman_shift > fitpeak_start) & (Raman_shift < fitpeak_end)]
y_data = Intensity[(Raman_shift > fitpeak_start) & (Raman_shift < fitpeak_end)]

peakmax = np.argmax(y_data)
peakmax_shift = x_data.iloc[peakmax]

params_gauss, cov_gauss = curve_fit(gauss_func, x_data, y_data, p0=[peakmax, peakmax_shift, 50])
params_lorentzian, cov_lorentzian = curve_fit(lorentzian_func, x_data, y_data, p0=[peakmax, peakmax_shift, 50])

x_model = np.linspace(min(x_data), max(x_data), 1000)
y_model_gauss = gauss_func(x_model, *params_gauss)
y_model_lorentzian = lorentzian_func(x_model, *params_lorentzian)

# Statistical Parameters for Gaussian and Lorentzian fits:
residuals_gauss = y_data - gauss_func(x_data, *params_gauss)
ss_res_gauss = np.sum(residuals_gauss**2)
ss_tot_gauss = np.sum((y_data - np.mean(y_data))**2)
r_squared_gauss = 1 - (ss_res_gauss / ss_tot_gauss)

residuals_lorentzian = y_data - lorentzian_func(x_data, *params_lorentzian)
ss_res_lorentzian = np.sum(residuals_lorentzian**2)
ss_tot_lorentzian = np.sum((y_data - np.mean(y_data))**2)
r_squared_lorentzian = 1 - (ss_res_lorentzian / ss_tot_lorentzian)

# Calculation of area under each curve:
area_gauss = simps(y_model_gauss, x_model)
area_lorentzian = simps(y_model_lorentzian, x_model)

fit_results = pd.DataFrame({
    'Fitting Method': ['Gaussian', 'Lorentzian'],
    'R^2': [r_squared_gauss, r_squared_lorentzian],
    'Area': [area_gauss, area_lorentzian]
})

# Plotting original and fitted data:
plt.plot(x_data, y_data, color='b', label='Original Peak')
plt.plot(x_model, y_model_gauss, color='r', label='Gaussian Fit')
plt.plot(x_model, y_model_lorentzian, color='g', label='Lorentzian Fit')
plt.xlabel('Raman shift (cm$^{-1}$)')
plt.ylabel('Intensity (a.u.)')
plt.title('Peak Fitting')
plt.legend()
plt.show()
print('\n')
print(fit_results.to_string(index=False)) 