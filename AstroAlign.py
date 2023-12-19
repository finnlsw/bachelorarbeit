import astroalign as aa
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from plotting import show_image
from datetime import datetime

curpath = "/home/finn/visual_Studio_Code/data/2023-09-25/test6"



def stack_images(inputPath, exptime):
    imageList = []
    headerList = []

    folder_path = os.path.join(inputPath)
    for filename in os.listdir(folder_path):
        if filename.endswith('.fit') or filename.endswith('.fits'):
            file_path = os.path.join(folder_path, filename)
    # import images
            with fits.open(file_path) as hdul:

                header = hdul[0].header
                image = hdul[0].data
                if header['EXPTIME'] == exptime:
                    imageList.append(image)
                    headerList.append(header)
                hdul.close()
    #print('number of images to stack:', len(imageList))
    print('num images:',len(imageList))

    # stacking
    middle_index = len(imageList) // 2
    target = imageList[middle_index].astype(np.float32)
    aligned_images = [target] #create list with source as first entry
    for i, image in enumerate(imageList):
        if i == middle_index:
            continue
        source = image.astype(np.float32)
        registered_image, footprint = aa.register(source, target) #target is reference image
        aligned_images.append(registered_image)
    final_stacked_image = np.mean(aligned_images, axis=0) # use mean to keep linearity
    final_stacked_image_median = np.median(aligned_images, axis=0)
    return final_stacked_image, final_stacked_image_median, headerList[len(imageList) // 2], target

stacked_im, stacked_im_med, stacked_hd, target = stack_images(curpath, 40.0)



fig, ax = plt.subplots(1,3, figsize= (15,5))
show_image(target, ax=ax[0], fig=fig)
show_image(stacked_im_med, ax=ax[1], fig=fig)
show_image(stacked_im, ax=ax[2], fig=fig)
ax[0].set_title('unstacked image')
ax[1].set_title('stacked using median')
ax[2].set_title('stacked using mean')
plt.savefig('/home/finn/Downloads/stacking_aa_example.png')
plt.show()



