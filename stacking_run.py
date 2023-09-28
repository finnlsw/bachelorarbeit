import numpy as np
from matplotlib import pyplot as plt
from astropy.io import fits
import glob
import os
from plotting import show_image
from saving import save_image
from stacking import stack_images


base_path = "/home/finn/visual_Studio_Code/data/2023-09-25/" ####change here for different pc
#base_path = "/home/fmahnken/PycharmProjects/data/2023-09-25/"
input_path = os.path.join(base_path,"lightCor")
output_path= base_path+"stacked"


#change here:
input_files = glob.glob(os.path.join(input_path, 'lightCor_HIP102488_R (Johnson)_*.fit')) #change here 
print('Number of input files:', len(input_files))
exptimeList=[2.0,5.0]
batch_size = 10
text= f"mesh_{batch_size}_images_stacked_testestetest"


for exptime in exptimeList:
    input_files_with_exptime = [file for file in input_files if fits.getheader(file)['EXPTIME'] == exptime]
    for i in range(0, len(input_files_with_exptime), batch_size):
        stackedImage, stackedHeader = stack_images(input_files_with_exptime[i:i+batch_size], exptime)
        save_image(output_path, stackedImage, stackedHeader, custom_text=text)
        print("success for badge",int(1+(i)/batch_size))

print("finished code")

