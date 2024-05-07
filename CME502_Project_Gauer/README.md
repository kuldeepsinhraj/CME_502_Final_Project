DSC Data Analysis for PLA (Polylactic Acid) Polymer

This repository contains a Python script (dsc.py) that performs data analysis on Differential Scanning Calorimetry (DSC) data from Perkin-Elmer Pyris Diamond DSC instrument for the semi-crystalline polymer Polylactic Acid (PLA). The script is designed to normalize DSC data, plot the data, identify peak positions, and calculate enthalpy by numerical integration.

Contents

    dsc.py: Python script for analyzing DSC data.
    testfile.pdid.txt: Sample input file containing DSC data for testing.
    presentation.pdf: Presentation file explaining the analysis process and results.

Usage
Requirements

    Python 3.x
    Required Python libraries: numpy, matplotlib, and scipy

Install the required Python libraries:

Running the Script

    Ensure your DSC data file is in a compatible format (.txt).
    Type path to data file directly into the terminal when prompted.

Output

    The script will generate plots showing the normalized DSC data and identified peak positions.
    Enthalpy values will be calculated based on the integrated areas under the peaks.

Additional Notes

    Feel free to modify the script or incorporate it into your own projects and tune parameters for your own data.
    For detailed explanation and results, refer to the presentation.pdf file.
