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


file_paths = [
                '/home/finn/visual_Studio_Code/data/2023-09-26/test/lightCor__B (Johnson)_10.0s_0.fit',
                '/home/finn/visual_Studio_Code/data/2023-09-26/test/lightCor__B (Johnson)_10.0s_1.fit',
                '/home/finn/visual_Studio_Code/data/2023-09-26/test/lightCor__B (Johnson)_10.0s_2.fit'
            ]

titles = ['PI.02 Cygni_B_10s_0.2mm', 'PI.02 Cygni_B_10s_0.5mm', 'PI.02 Cygni_B_10s_1.0mm']

fig, ax = plt.subplots(1, 3, figsize=(21,7))
for i, path in enumerate(file_paths):
    image = open_image(path)
    show_image(image, ax=ax[i], fig=fig, percl=99.5)
    ax[i].set_title(f'2023-09-26_{titles[i]}')
plt.tight_layout()
plt.savefig('/home/finn/Pictures/Different_mesh_size_B.png')
plt.show()

'''


# File paths for the FITS images
file_path_1 = '/home/finn/visual_Studio_Code/data/2023-09-04/LIGHT/HIP_100587-001_30.fit'
file_path_2 = '/home/finn/visual_Studio_Code/data/2023-09-04/stacked_old/lightCor_HIP_100587_B (Johnson)_30.0s_long_short_10_images_stacked_0.fit'
#file_path_3 = '/home/finn/visual_Studio_Code/data/2023-09-25/lightCor/lightCor_HIP100587_B (Johnson)_40.0s_6.fit'

image_1 = open_image(file_path_1)
image_2 = open_image(file_path_2)
#raw = open_image(file_path_3)
fig, ax = plt.subplots(1,2, figsize=(20,10))
#show_image(raw, ax=ax[0], fig=fig)
show_image(image_1, ax=ax[0], fig=fig)
show_image(image_2, ax=ax[1], fig=fig)
ax[0].set_title('Raw image')
ax[1].set_title('Corrected and stacked image')
#ax[2].set_title('stacked using mean')
#plt.tight_layout()
plt.show()


#### todo search same image in stacked old, new and with other method (aa)
'''