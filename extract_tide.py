#########################################
# Developed by: Débora Rodrigues Pereira
# MARETEC IST, 05/03/2024
#########################################

import os
import sys
import h5py
import numpy as np
import pandas as pd
from tqdm import tqdm 

hdf_path = 'C:/YourPath/Tide/FES/FES2014.hdf5'
points_path = 'C:/YourPath/Tide/Points.txt'
output_folder = 'C:/YourPath/Tide/Output'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

#Separate the points file with the delimeter
points_data = np.loadtxt(points_path, delimiter=',')

# Open the HDF file 
with h5py.File(hdf_path, 'r') as hdf:

    # Extract necessary HDF information
    latitudes = hdf ['Grid']['Latitude'][:]
    longitudes = hdf ['Grid']['Longitude'][:] 
    results = hdf['Results']
    water_level = results['water level']

    # Extract tidal components for each subgroup within 'water level'
    harmonics = list(water_level.keys())
    
    # Progress bar
    total_points = len(points_data)
    progress_bar = tqdm(total=total_points, desc="Processing Points")    
    
    # Create an initial dataframe
    df_results = pd.DataFrame(columns=['Harmonics', 'Amplitude', 'Phase'])
    
    for lon, lat in points_data:
        # Find the closest latitude and longitude in the dataset
        distances = np.sqrt((lat - latitudes[:, None])**2 +
                    (lon- longitudes[:, None])**2)
        closest_indices = np.unravel_index(np.argmin(distances), distances.shape)
        lat_index = closest_indices[0]
        lon_index = closest_indices[2]

        tidal_data_for_point = []
        
        # Extract tidal data for each harmonic
        for subgroup_name in harmonics:
            subgroup = water_level[subgroup_name]
            dataset_names = list(subgroup.keys())
            
            # Define the groups             
            amplitude = subgroup['amplitude']
            phase = subgroup['phase']
            # Extract the information according to lat and lon 
            amp = amplitude[lat_index, lon_index]
            pha = phase[lat_index, lon_index]    

            # Iterate for all harmonics and append
            tidal_data_for_point.append((subgroup_name, amp, pha))                              
                           
        # Save tidal data for the point to the DataFrame
        for harmonic, amp, pha in tidal_data_for_point:
            df_point = pd.DataFrame({'Harmonics': [harmonic], 'Amplitude': [amp], 'Phase': [pha]})
          
            # Add the actual dataframe to the general dataframe
            df_results = pd.concat([df_results, df_point], ignore_index=True, sort=False)
                
        df_results.to_csv(os.path.join(output_folder, f'tidal_data_point_{lat}_{lon}.txt'), index=False)
    
        # Clear the DataFrame for the next point
        df_results = pd.DataFrame(columns=['Harmonics', 'Amplitude', 'Phase'])

        # Update the progress bar
        progress_bar.update(1)
        
    progress_bar.close()    
    
    # Print a message indicating successful execution
    print("Tidal data extraction completed and saved.")
