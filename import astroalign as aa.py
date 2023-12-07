import astroalign as aa
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from plotting import show_image
from datetime import datetime

curpath = "/home/fmahnken/data/2023-09-25/test"

def loadImages(folder_name):
    folder_path = os.path.join(curpath, folder_name)
    target_size = 2048
    images = []
    headers = []
    timestamps = []  # To store timestamps
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.fit') or filename.endswith('.fits'):
            file_path = os.path.join(folder_path, filename)
            
            with fits.open(file_path) as hdul:
                header = hdul[0].header
                headers.append(header)
                
                # Extract timestamp from the header
                date_obs = header.get('DATE-OBS', '')
                timestamp = datetime.strptime(date_obs, '%Y-%m-%dT%H:%M:%S')
                timestamps.append(timestamp)

                naxis1 = header.get('NAXIS1', -1)
                naxis2 = header.get('NAXIS2', -1)
                if naxis1 == target_size and naxis2 == target_size:
                    images.append(hdul[0].data)
                elif naxis1 > 0 and naxis2 > 0:
                    binning_factor = max(naxis1 // target_size, naxis2 // target_size)
                    binned_data = hdul[0].data.reshape(naxis2 // binning_factor, binning_factor, naxis1 // binning_factor, binning_factor).mean(1).mean(2)
                    images.append(binned_data)
                hdul.close()

    # Sort images and headers based on timestamps
    sorted_indices = sorted(range(len(timestamps)), key=lambda k: timestamps[k])
    sorted_images = [images[i] for i in sorted_indices]
    sorted_headers = [headers[i] for i in sorted_indices]

    return sorted_images, sorted_headers

image_list, header_list = loadImages(curpath)
images = np.zeros((2048, 2048, len(image_list)), dtype=np.float32) 

#for i, im in enumerate(image_list):
 #   images[:, :, i] = im

images = np.array(image_list)
source = images[200] 
target = images[201]


fig, ax = plt.subplots(1,2)
show_image(source, ax=ax[0], fig=fig)
show_image(target, ax=ax[1], fig=fig)
plt.show()

registered_image, footprint = aa.register(source, target)

'''
file_path = '/home/fmahnken/data/2023-09-25/lightCor/lightCor_HIP100587_B (Johnson)_40.0s_' #put filename without exptime,nr and .fit here
image_list = []
header_list = []
titles = []

for fits_path in glob.glob(os.path.join(file_path + '*fit')):
    with fits.open(fits_path) as hdul:
        image_list.append(hdul[0].data)
        exptime_short = hdul[0].header["EXPTIME"]
        header_list.append(hdul[0].header)
        titles.append(hdul[0].header['DATE-OBS'][:10] +"_" + os.path.splitext(os.path.basename(fits_path))[0])

# Reihenfolge noch nicht korrekt !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
source = image_list[0]
target = image_list[1]


fig, ax = plt.subplots(1,2)
show_image(source, ax=ax[0], fig=fig)
show_image(target, ax=ax[1], fig=fig)
ax[0].set_title(titles[0])
ax[1].set_title(titles[1])
plt.tight_layout
plt.show()


registered_image, footprint = aa.register(source, target)
'''