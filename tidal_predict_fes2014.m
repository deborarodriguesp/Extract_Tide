%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Developed by: Débora Rodrigues Pereira
% MARETEC IST, 18/03/2024

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc
clear all
close all

%% Specify the folder where your files are located
folder = 'C:/YourPath/Tide/output_extract/';
output_folder = 'C:/YourPath/Tide/output_predict/';
% Get a list of all files in the folder
fileList = dir(fullfile(folder, 'tidal_data_point_*.txt'));

%% Loop through each file
for i = 1 : numel(fileList)
    % Build the full path to the current file
    filePath = fullfile(folder, fileList(i).name);
    
    % Extract latitude and longitude from the file name
    LatLong = sscanf(fileList(i).name, 'tidal_data_point_%f_%f.txt');
    latitude = LatLong(1);
    longitude = LatLong(2);
    
    start_date = datenum(2012, 11, 01, 00, 00, 00); 
    end_date = datenum(2014, 01, 01, 00, 00, 00);   % 10 de janeiro de 2008
    dt=datenum(0000,00,00,01,00,00);
    t =(start_date:dt:end_date);
    date = datetime(t,'ConvertFrom','datenum');
    %%
    % Read the data from the file
    data = readtable(filePath);
    
    % Extract necessary columns (Harmonics, Amplitude, Phase)
    name = data.Harmonics;
    amplitude = data.Amplitude;
    phase = data.Phase; 
    freq = t_tide_name2freq(name,'unit','rad/day')';
    
    % Select only the valid variables
    const=t_getconsts;
    valid_indices = ismember(name, const.name);
    valid_name = name(valid_indices, :);
    valid_amplitude = amplitude(valid_indices);
    valid_phase = phase(valid_indices);
    
    tidecon= [freq valid_amplitude valid_phase];
    
    %%
    all_signals = zeros(length(t), size(tidecon, 1));

    for i = 1:length(t)
        for k = 1:size(tidecon, 1)
            signal = tidecon(k, 2) * sin((tidecon(k, 1) * t(i)) + tidecon(k, 3));

            all_signals(i, k) = signal;
        end
    end

    % Add all harmonic signals to obtain the total tidal signal for each moment
    tide = sum(all_signals, 2);

%%  Not necessary
    %interval=1; 
    
    %[NAME,FREQ,TIDECON]=t_tide(tide(:,1),interval,'start time',[2012, 11, 01, 00, 00, 00],'latitude',latitude,'synthesis',2);
    %YOUT = t_predic(t,NAME,FREQ,TIDECON,'latitude',latitude,'synthesis',2);
   
%%
    % save the files
    filename = sprintf('tidal_predict_%.6f_%.6f.txt', latitude, longitude);
    filepath = fullfile(output_folder, filename);
    dlmwrite(filepath, tide, 'precision', 4);     
end
