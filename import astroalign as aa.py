import astroalign as aa
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from plotting import show_image

curpath = "/home/fmahnken/data/2023-09-25/lightCor"

def loadImages(folder_name):
    folder_path = os.path.join(curpath, folder_name)
    target_size = 2048
    images = []
    headers = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.fit') or filename.endswith('.fits'):
            file_path = os.path.join(folder_path, filename)
            
            with fits.open(file_path) as hdul:
                header = hdul[0].header
                headers.append(header)
                naxis1 = header.get('NAXIS1', -1)
                naxis2 = header.get('NAXIS2', -1)
                if naxis1 == target_size and naxis2 == target_size:
                    images.append(hdul[0].data)
                elif naxis1 > 0 and naxis2 > 0:
                    binning_factor = max(naxis1 // target_size, naxis2 // target_size)
                    binned_data = hdul[0].data.reshape(naxis2 // binning_factor, binning_factor, naxis1 // binning_factor, binning_factor).mean(1).mean(2)
                    images.append(binned_data)

                hdul.close()

    return images, headers



images, header = loadImages(curpath)
source = images[0] #x,y,image_number
target = images[1]

fig, ax = plt.subplots(1,2)
show_image(source, ax=ax[0], fig=fig)
show_image(target, ax=ax[1], fig=fig)
plt.show()

#registered_image, footprint = aa.register(source, target)
