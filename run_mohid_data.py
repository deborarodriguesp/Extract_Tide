#########################################
# Developed by: Débora Rodrigues Pereira
# MARETEC IST, 20/03/2024
#########################################

import os
import pandas as pd
from datetime import datetime
from tqdm import tqdm

def generate_boundary_file(output_folder, line_folder, timeseries_folder):
    
    print ('\nBoundary file initialization...\n')
    
    filename = os.path.join(output_folder, 'Final_Boundary_File.txt')
    
    with open(filename, "w") as file:      
        # Loop through the files in the line folder
        for root, dirs, files in os.walk(line_folder):
            for line_filename in files:
                if line_filename.endswith('.lin'):
                    # Extract latitude and longitude from the line file name
                    lat, lon = line_filename.split('_')[2:4]
                    line_filepath = os.path.join(line_folder, line_filename)
                    
                    # Construct the corresponding prediction file name
                    timeseries = f'TidePara_FES2014_{lat}_{lon}'
                    timeseries = timeseries.replace('.lin', '.dat')
                    timeseries_filepath = os.path.join(timeseries_folder, timeseries)
                    
                    # Write the details to the boundary file
                    file.write('<begin_boundary_line>\n')
                    file.write(f'LINE_FILENAME           : {line_filepath}\n')
                    file.write(f'VARIABLE_WATER_LEVEL    : 1\n')
                    file.write(f'DEFAULTVALUE            : 0\n')
                    file.write(f'FILENAME                : {timeseries_filepath}\n')
                    file.write(f'DATA_COLUMN             : 2\n')
                    file.write('<end_boundary_line>\n\n')

def process_predict_files(predict_folder, timeseries_folder):
    print('\nProcessing Predict Files...\n')
    
    # List all files in the predict folder
    file_list = os.listdir(predict_folder)
    
    # Initialize tqdm to track progress
    progress_bar = tqdm(file_list, desc="Processing Predict Files", unit="file")
    
    for file_name in progress_bar:
        if file_name.endswith('.txt'):
            file_path = os.path.join(predict_folder, file_name)
            
            # Load the tidal prediction data
            predict_data = pd.read_csv(file_path, sep='\t')
            
            # Convert the date column to datetime type
            predict_data['Date'] = pd.to_datetime(predict_data['Date'])
            
            # Set the start date and desired time step in hours
            start_date = pd.to_datetime('2012-11-01')
            mohid_date = start_date.strftime('%Y %m %d %H %M %S')
            time_step = pd.Timedelta(hours=1)
            
            # Calculate the number of time steps elapsed since the start of the period
            predict_data['TimeStep'] = (predict_data['Date'] - start_date) // time_step
            
            # Resample the data to match the desired time step interval
            resampled_data = predict_data.set_index('TimeStep').reindex(range(len(predict_data['TimeStep'])))
            resampled_data.index = resampled_data.index - 4 # UTM correction
            
            # Extract latitude and longitude from the file name  
            lat_lon = file_name.split('_')[-2:] 
            lat_lon = '_'.join(lat_lon)[:-4]  # Remove the .txt extension
            latitude, longitude = map(float, lat_lon.split('_'))
           
            # Save the data in MOHID timeseries format
            filename = f'TidePara_FES2014_{latitude:.6f}_{longitude:.6f}.dat'
            output_file = os.path.join(timeseries_folder, filename)
            with open(output_file, 'w') as f:
                f.write(f'NAME                    : {filename}\n')
                f.write(f'SERIE_INITIAL_DATA      : {mohid_date}\n')
                f.write('TIME_UNITS              : HOURS\n')
                f.write('!time waterlevel\n')
                f.write('<BeginTimeSerie>\n')
                for idx, row in resampled_data.iterrows():
                    f.write(f"{int(idx)}\t{row['Tide']}\n")
                f.write('<EndTimeSerie>\n')

# Folders
output_folder = 'D:/DOUTORAMENTO/Tide/Tide_Extractor/'
line_folder = 'D:/DOUTORAMENTO/Tide/Tide_Extractor/output_lines/'
timeseries_folder = 'D:/DOUTORAMENTO/Tide/Tide_Extractor/output_timeseries/'
predict_folder = 'D:/DOUTORAMENTO/Tide/Tide_Extractor/output_predict/'

# Process
process_predict_files(predict_folder, timeseries_folder)
generate_boundary_file(output_folder, line_folder, timeseries_folder)
print ('\nBoundary file created!\n')
