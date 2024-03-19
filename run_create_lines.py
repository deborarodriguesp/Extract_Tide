#########################################
# Developed by: Débora Rodrigues Pereira
# MARETEC IST, 19/03/2024
#########################################

import os
import sys
import pandas as pd
import numpy as np

def calculate_left_right(coordinates, lon_to_find, lat_to_find):
    half_cell_size = 0.005
    
    lines_center = []
    lines_right = []
    
    for lon, lat in coordinates:
        if lon == lon_to_find:
            top = (lon, lat + half_cell_size)
            bottom = (lon, lat - half_cell_size)
            lines_right.append((top, bottom))
            
            filename = os.path.join(output_folder, f"tidal_line_{lat}_{lon}.lin")

            with open(filename, "w") as file:
                file.write(proj4_string)
                file.write(begin_line)
                file.write(f"{top[0]} {top[1]} NaN\n")
                file.write(f"{bottom[0]} {bottom[1]} NaN\n")
                file.write(end_line)
            
        elif lat == lat_to_find:
            left = (lon - half_cell_size, lat)
            right = (lon + half_cell_size, lat)
            lines_center.append((left, right))
            
            filename = os.path.join(output_folder, f"tidal_line_{lat}_{lon}.lin")
            
            with open(filename, "w") as file:
                file.write(proj4_string)
                file.write(begin_line)
                file.write(f"{left[0]} {left[1]} NaN\n")
                file.write(f"{right[0]} {right[1]} NaN\n")
                file.write(end_line) 
                
    return lines_center, lines_right
           
            
output_folder = 'D:\DOUTORAMENTO\Tide\Tide_Extractor\output_lines'  
proj4_string = "+proj=longlat +datum=WGS84 +no_defs\n"
begin_line = "<begin_line>\n"
end_line = "<end_line>\n"   
  
# Coordenadas que se repetem: 
lon_to_find = -46.1629690
lat_to_find = -0.0931790

# Define o tamanho da célula em km
cell_size = 1  # 1 km

# Lê as coordenadas do arquivo de entrada
input_filename = "foz_grid_boundary_removed_points.txt"
coordinates = np.loadtxt(input_filename, delimiter=',')
coordinates = np.array(coordinates)

lines_center, lines_right = calculate_left_right(coordinates, lon_to_find, lat_to_find)
