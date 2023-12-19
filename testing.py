import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from plotting import show_image

# Function to load and plot FITS images
def open_image(file_path):
    with fits.open(file_path) as hdul:
        image = hdul[0].data  # Get image data
    return image

'''
file_paths = [
    '/home/finn/visual_Studio_Code/data/2023-09-25/stacked/lightCor_HIP100587_B (Johnson)_40.0s_10_images_stacked_0.fit',
    '/home/finn/visual_Studio_Code/data/2023-09-25/stacked/lightCor_HIP100587_B (Johnson)_40.0s_10_images_stacked_1.fit',
    '/home/finn/visual_Studio_Code/data/2023-09-25/stacked/lightCor_HIP100587_B (Johnson)_40.0s_10_images_stacked_2.fit',
    '/home/finn/visual_Studio_Code/data/2023-09-25/stacked/lightCor_HIP100587_B (Johnson)_40.0s_10_images_stacked_3.fit',
    '/home/finn/visual_Studio_Code/data/2023-09-25/stacked/lightCor_HIP100587_B (Johnson)_40.0s_10_images_stacked_4.fit',
    '/home/finn/visual_Studio_Code/data/2023-09-25/stacked/lightCor_HIP100587_B (Johnson)_40.0s_10_images_stacked_5.fit',
    '/home/finn/visual_Studio_Code/data/2023-09-25/stacked/lightCor_HIP100587_B (Johnson)_40.0s_10_images_stacked_6.fit'
]

fig, ax = plt.subplots(2, 4)
for i, path in enumerate(file_paths):
    image = open_image(path)
    if i < 4:
        show_image(image, ax=ax[0,i], fig=fig)
    else:
        show_image(image, ax=ax[1,i-5], fig=fig)

        

plt.show()
'''


# File paths for the FITS images
file_path_1 = '/home/finn/visual_Studio_Code/data/2023-09-25/stacked/lightCor_HIP100587_B (Johnson)_40.0s_10_images_stacked_6.fit'
file_path_2 = '/home/finn/visual_Studio_Code/data/2023-09-25/stacked_old/lightCor_HIP100587_B (Johnson)_40.0s_long-short-series_10_images_stacked_6.fit'
file_path_3 = '/home/finn/visual_Studio_Code/data/2023-09-25/lightCor/lightCor_HIP100587_B (Johnson)_40.0s_6.fit'

mean_stacked = open_image(file_path_1)
median_stacked = open_image(file_path_2)
raw = open_image(file_path_3)
fig, ax = plt.subplots(1,3)
show_image(raw, ax=ax[0], fig=fig)
show_image(median_stacked, ax=ax[1], fig=fig)
show_image(mean_stacked, ax=ax[2], fig=fig)
ax[0].set_title('unstacked image')
ax[1].set_title('stacked using median')
ax[2].set_title('stacked using mean')
plt.show()


#### todo search same image in stacked old, new and with other method (aa)