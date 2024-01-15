import numpy as np
from matplotlib import pyplot as plt
from astropy.io import fits
import glob
import os
from plotting import show_image
from saving import save_image
from stacking import stack_images
from datetime import datetime


file_path = '/home/finn/visual_Studio_Code/data/2024-01-11/lightCor/lightCor_HIP100587_ms_R_35_R (Johnson)_35.0s' #put filename without exptime,nr and .fit here
exptimeList=[35.0] #stack single[.] or multiple[.,.,.] exptimes seperatly in same loop
batch_size = 10 # adjust desired number of images for one stack
mode = 'median' 

if mode == 'median':
    output_path= file_path[:46]+"stacked_median" #change number for different pc !!!!!!!!!!!!!!!!!!!!!!!!
if mode == 'mean':
    output_path= file_path[:46]+"stacked"   
    

input_files = glob.glob(os.path.join(file_path + '*.fit')) 
print('Number of input files:', len(input_files), '<- if zero check filepath')
text= f"{batch_size}_images_stacked" 

for exptime in exptimeList:
    input_files_with_exptime = [file for file in input_files if fits.getheader(file)['EXPTIME'] == exptime]
    input_files_with_exptime.sort(key=lambda file_path: datetime.strptime(fits.getheader(file_path).get('DATE-OBS', ''), '%Y-%m-%dT%H:%M:%S')) #sort by time 
    print('finished sorting and starting stacking')
    for i in range(0, len(input_files_with_exptime), batch_size):
        stackedImage, stackedHeader = stack_images(input_files_with_exptime[i:i+batch_size], exptime, mode = mode) # mode defined above
        save_image(output_path, stackedImage, stackedHeader, custom_text=text)
        print("success for batch",int(1+(i)/batch_size))

print("finished stacking")
