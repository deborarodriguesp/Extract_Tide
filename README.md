# Extract Tide
A Python code to extract tidal harmonic components from a hdf5 file.

**Points/Cells Coordinates** 

The first step is to obtain the point coordinates that will be used to extract the information from the HDF5 file.
Here, the coordinates are from a MOHID Land grid file, which the DTM was exported as XYZ. In GIS software, only the boundary coordinates were kept and saved into a txt file.

**FES Model**

The tidal model used is FES2014, and it can be downloaded here http://wiki.mohid.com/index.php?title=FES2014 

**Tidal Extraction** 

The script opens the HDF file, finds close coordinates between the Points and the FES2014 coordinates, and extracts the amplitude and phase for each harmonic available. 
The script also save in a text file the amplitudes and phases for each Point coordinate, as:

>Harmonics, Amplitude, Phase
>
>M2,1.6089622497558593,256.92163848876953
>
>N2,0.3257173156738281,243.20376586914062
>
>O1,0.09126119613647461,242.03919219970703
>
>S2,0.49927242279052736,289.93888092041016


# Predict Tide

The second script is developed in Matlab, but it can be easily transformed into Python. Here, the tide prediction is done using 
the formula  (Foreman and Henry, 1989):
>
>signal = amplitude * cos((frequency * time) - phase)
>
The only function from t_tide used here is to find the frequency for each component (t_tide_name2freq)

link: https://www.researchgate.net/publication/222121668_The_harmonic_analysis_of_tidal_model_time_series

# Create Lines

Now, you have points, but to add boundary value in each grid, you need a line for each cell. 
This script will help you to create those lines. 

Keep in mind that you need to change 'half_cell_size' according to your cell size. 
Since the coordinates are in degrees, this variable has to be in degrees. 

This will save different lines for each cell, allowing you to impose different water levels for each cell.  
