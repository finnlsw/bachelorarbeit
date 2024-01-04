import numpy as np
from matplotlib import pyplot as plt
from astropy.io import fits
import glob
import os
from plotting import show_image
from saving import save_image
from stacking import stack_images
from datetime import datetime


file_path = '/home/finn/visual_Studio_Code/data/2023-10-01/lightCor/lightCor_HIP75458_defocused2_B (Johnson)_1.5s_' #put filename without exptime,nr and .fit here
exptimeList=[1.5] #stack (single[.] or multiple[.,.,.]) exptimes seperatly in same loop
batch_size = 30 # adjust desired number of images for one stack

output_path= file_path[:46]+"stacked" #change number for different pc !!!!!!!!!!!!!!!!!!!!!!!!!1change stacked old !!!!!!!!!!!!!!!!!1
input_files = glob.glob(os.path.join(file_path + '*.fit')) 
print('Number of input files:', len(input_files), '<- if zero check filepath')
text= f"{batch_size}_images_stacked" 

for exptime in exptimeList:
    input_files_with_exptime = [file for file in input_files if fits.getheader(file)['EXPTIME'] == exptime]
    input_files_with_exptime.sort(key=lambda file_path: datetime.strptime(fits.getheader(file_path).get('DATE-OBS', ''), '%Y-%m-%dT%H:%M:%S')) #sort by time 
    print('finished sorting and starting stacking')
    for i in range(0, len(input_files_with_exptime), batch_size):
        stackedImage, stackedHeader = stack_images(input_files_with_exptime[i:i+batch_size], exptime, mean=True) # change mean=True for mean stacking
        save_image(output_path, stackedImage, stackedHeader, custom_text=text)
        print("success for batch",int(1+(i)/batch_size))

print("finished stacking")
