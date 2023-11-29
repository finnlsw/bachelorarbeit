import numpy as np
from matplotlib import pyplot as plt
from astropy.io import fits
import glob
import os
from plotting import show_image
from saving import save_image
from stacking import stack_images
from datetime import datetime


base_path = "/home/finn/visual_Studio_Code/data/2023-09-26/" ####change here for different pc
#base_path = "/home/fmahnken/PycharmProjects/data/2023-09-25/"
input_path = os.path.join(base_path,"lightCor")
output_path= base_path+"stacked"


input_files = glob.glob(os.path.join(input_path, 'lightCor_HIP102488_defocused_B (Johnson)*.fit')) #put filename without exptime and nr here
print('Number of input files:', len(input_files), '<- if zero check path/filename')
exptimeList=[1.5] #stack exptimes seperatly in same loop
batch_size = 25 # adjust desired number of images to stack
text= f"{batch_size}_images_stacked" 


for exptime in exptimeList:
    input_files_with_exptime = [file for file in input_files if fits.getheader(file)['EXPTIME'] == exptime]
    input_files_with_exptime.sort(key=lambda file_path: datetime.strptime(fits.getheader(file_path).get('DATE-OBS', ''), '%Y-%m-%dT%H:%M:%S')) #sort by time 
    for i in range(0, len(input_files_with_exptime), batch_size):
        stackedImage, stackedHeader = stack_images(input_files_with_exptime[i:i+batch_size], exptime)
        save_image(output_path, stackedImage, stackedHeader, custom_text=text)
        print("success for batch",int(1+(i)/batch_size))

print("finished code")

