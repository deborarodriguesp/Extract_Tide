import os

def generate_boundary_file(output_folder_path, line_folder_path, predict_folder_path):
    filename = os.path.join(output_folder_path, 'Final_Boundary_File.txt')
    with open(filename, "w") as file:      
        
        for root, dirs, files in os.walk(line_folder_path):
            for filename in files:
                if filename.endswith('.lin'):
                    lat, lon = filename.split('_')[2:4] 

                    line_filename = os.path.join(line_folder_path, f'tidal_line_{lat}_{lon}')
                    predict_filename = os.path.join(predict_folder_path, f'tidal_predict_{lat}_{lon}')
                    predict_filename = predict_filename.replace('.lin', '.txt')
                    
                    file.write('<begin_boundary_line>\n')
                    file.write(f'LINE_FILENAME           : {line_filename}\n')
                    file.write(f'VARIABLE_WATER_LEVEL    : 1\n')
                    file.write(f'DEFAULTVALUE            : 0\n')
                    file.write(f'VALUE_TYPE              : TIMESERIE\n')
                    file.write(f'FILENAME                : {predict_filename}\n')
                    file.write(f'DATA_COLUMN             : 2\n')
                    file.write('<end_boundary_line>\n\n')

# Exemplo de uso
output_folder_path = 'D:/DOUTORAMENTO/Tide/Tide_Extractor/'
line_folder_path = 'D:/DOUTORAMENTO/Tide/Tide_Extractor/output_lines/'
predict_folder_path = 'D:/DOUTORAMENTO/Tide/Tide_Extractor/output_predict/'

generate_boundary_file(output_folder_path, line_folder_path, predict_folder_path)