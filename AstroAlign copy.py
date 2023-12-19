import astroalign as aa
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from plotting import show_image
from datetime import datetime
from saving import save_image

curpath = "/home/finn/visual_Studio_Code/data/2023-09-25/test6"



def stack_images(inputPath, exptime):
    imageList = []
    headerList = []
    for file in inputPath:
        hdul = fits.open(file)
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
        registered_image, footprint = aa.register(source, target)
        aligned_images.append(registered_image)
    final_stacked_image = np.mean(aligned_images, axis=0) # use mean to keep linearity
    #final_stacked_image_median = np.median(aligned_images, axis=0)
    return final_stacked_image, headerList[len(imageList) // 2]



file_path = '/home/finn/visual_Studio_Code/data/2023-09-25/lightCor/lightCor_HIP100587_B (Johnson)_' #put filename without exptime,nr and .fit here
exptimeList=[40.0] #stack exptimes seperatly in same loop
batch_size = 10 # adjust desired number of images for one stack

output_path= file_path[:46]+"stacked_aa" #change number for different pc
input_files = glob.glob(os.path.join(file_path + '*.fit')) 
print('Number of input files:', len(input_files), '<- if zero check filepath')
text= f"{batch_size}_images_stacked" 

for exptime in exptimeList:
    input_files_with_exptime = [file for file in input_files if fits.getheader(file)['EXPTIME'] == exptime]
    input_files_with_exptime.sort(key=lambda file_path: datetime.strptime(fits.getheader(file_path).get('DATE-OBS', ''), '%Y-%m-%dT%H:%M:%S')) #sort by time 
    for i in range(0, len(input_files_with_exptime), batch_size):
        stackedImage, stackedHeader = stack_images(input_files_with_exptime[i:i+batch_size], exptime)
        save_image(output_path, stackedImage, stackedHeader, custom_text=text)
        print("success for batch",int(1+(i)/batch_size))

print("finished stacking")


'''
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
'''


