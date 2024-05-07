This following scripts are used to read and process Raman spectra of similar material.

Included are 4 Raman spectra of Ni and Ni-Ba based material supported on CeO2 that are used for Ethanol Steam Reforming. The files can be renamed to Spectrum 1-4 for easier accessing of files through Python.



The first script (Plotting_Raman.py) takes the following inputs:

1. File name - in the format "filename.txt" without the " ". Once done, type "done" without the " ".
2. Start and end range Raman shift values (in cm-1) of desired peak to normalize by. The values for the range can be obtained from any Raman spectra as the instruments returns spectra within a fixed range and interval of wavenumbers.
3. List of the intensity values to shift each respective spectra by (i.e., [100, 200, 300, 400]), which can be a list of 0s totaling the number of spectral inputs

The resulting data results a plot and outputs a csv (dataframe) including normalized and shifted spectra Intensity and Raman shift values.




The second script (Curve_Fitting.py) takes the following inputs: 

1. Name of file to fit peak in (same file input syntax as first script).
2. Start and end range of peak to fit. The range can be adjusted as well as the starting parameters (p0) for better fit of peaks.

The resulting data outputs a fit of the desired peak using both Gaussian and Lorentzian curve fitting with an area value corresponding to each fit peak.