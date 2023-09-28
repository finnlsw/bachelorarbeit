
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import glob
import os
import shutil
from plotting import show_image
from saving import save_image

#change path here#
curpath = "/home/finn/visual_Studio_Code/data/2023-09-25"
#curpath =  "/home/fmahnken/PycharmProjects/data/2023-09-25"

# 0. define Important functions
def loadImages(folder_name):
    folder_path = os.path.join(curpath, folder_name)
    image_list = glob.glob(os.path.join(folder_path, '*.fit')) + glob.glob(os.path.join(folder_path, '*.fits'))
    num_files = len(image_list)
    print('Found %d files in %s' % (num_files, folder_name))
    target_size = 2048
    images = np.zeros((target_size, target_size, num_files),dtype=np.float32) #float32 because orignial files are in int16
    # use binning to compress larger images (e.g. 4096) to 2048
    for i in range(num_files):
        with fits.open(image_list[i]) as hdul:
            naxis1 = hdul[0].header.get('NAXIS1', -1) #get size information from the header
            naxis2 = hdul[0].header.get('NAXIS2', -1)
            if naxis1 == target_size and naxis2 == target_size:
                images[:, :, i] = hdul[0].data
            elif naxis1 > 0 and naxis2 > 0:
                binning_factor = max(naxis1 // target_size, naxis2 // target_size)
                binned_data = hdul[0].data.reshape(naxis2 // binning_factor, binning_factor, naxis1 // binning_factor, binning_factor).mean(1).mean(2)
                images[:, :, i] = binned_data
            hdul.close()
    return images
#flatImages = loadImages('FLAT') # Example usage


# 1. Bias
biasImages=loadImages('BIAS')
masterBias = np.median(biasImages, axis=2).astype(np.float32)

#2. Dark
darkImages = loadImages('DARK')
darkImages -= masterBias[:, :, np.newaxis]

darkPath = os.path.join(curpath, 'DARK')
darkFiles = [file for file in os.listdir(darkPath) if file.endswith('.fit') or file.endswith('fits')]
masterDarkFrames = {}  # Dictionary to store master dark frames

for i, fits_file in enumerate(darkFiles):
    fits_path = os.path.join(darkPath, fits_file)
    hdul = fits.open(fits_path)
    header = hdul[0].header
    exptime = header['EXPTIME']

    # Check if the data is a valid array
    if isinstance(darkImages[:, :, i], np.ndarray) and darkImages[:, :, i].shape != ():
        if exptime not in masterDarkFrames:
            masterDarkFrames[exptime] = [darkImages[:, :, i]]
        else:
            masterDarkFrames[exptime].append(darkImages[:, :, i])
    hdul.close()

for exptime, dark_frames in masterDarkFrames.items():
    masterDarkFrames[exptime] = np.median(dark_frames, axis=0)


#3. Flat
flatImages = loadImages('FLAT')

flatPath = os.path.join(curpath, 'FLAT')
flatFiles = [file for file in os.listdir(flatPath) if file.endswith('.fit') or file.endswith('fits')]
masterFlatFrames = {}  # Dictionary to store master flat frames

for i, fits_file in enumerate(flatFiles):
    fits_path = os.path.join(flatPath, fits_file)
    hdul = fits.open(fits_path)
    header = hdul[0].header
    filter_value = header['FILTER']
    # Check if the data is a valid array
    if isinstance(flatImages[:, :, i], np.ndarray) and flatImages[:, :, i].shape != ():
        if filter_value not in masterFlatFrames:
            masterFlatFrames[filter_value] = [flatImages[:, :, i]]
        else:
            masterFlatFrames[filter_value].append(flatImages[:, :, i])
    hdul.close()

# Calculate the median for each master flat frame
for filter_value, flat_frames in masterFlatFrames.items():
    masterFlatFrames[filter_value] = np.median(flat_frames, axis=0)
# Normalize the master flat frames
for filter_value, master_flat in masterFlatFrames.items():
    masterFlatFrames[filter_value] /= np.median(master_flat)

#check everything
for filter_value, master_flat in masterFlatFrames.items():
    print(f"flats Filter: {filter_value}")
for exptime, master_dark in masterDarkFrames.items():
    print(f"darks Exposure Time: {exptime}")
first_filter = next(iter(masterFlatFrames)) #get first flat filter from library
first_dark= next(iter(masterDarkFrames)) #get first dark exptime from library
fig, (ax1,ax2) = plt.subplots(1,2,figsize=(20,10))
show_image(masterFlatFrames[first_filter], ax=ax1, fig=fig)
show_image(masterDarkFrames[first_dark], ax=ax2, fig=fig)
plt.show()

#4. Image correction
# Create a list for light images and header as tuple
lightPath = os.path.join(curpath, 'LIGHT')
lightFiles = [file for file in os.listdir(lightPath) if file.endswith('.fit') or file.endswith('.fits')]
output_path = os.path.join(curpath, "lightCor")
if os.path.exists(output_path):
    shutil.rmtree(output_path) 

for i, fits_file in enumerate(lightFiles):
    fits_path = os.path.join(lightPath, fits_file)
    hdul = fits.open(fits_path)
    header = hdul[0].header
    #bin image if neccesary:
    naxis1 = header.get('NAXIS1', -1) #get size information from the header
    naxis2 = header.get('NAXIS2', -1)
    target_size=2048
    if naxis1 == target_size and naxis2 == target_size:
        image = hdul[0].data
    elif naxis1 > 0 and naxis2 > 0:
        binning_factor = max(naxis1 // target_size, naxis2 // target_size)
        binned_data = hdul[0].data.reshape(naxis2 // binning_factor, binning_factor, naxis1 // binning_factor, binning_factor).mean(1).mean(2)
        image = binned_data

    #image = hdul[0].data
    exptime = header['EXPTIME']
    filter_value = header['FILTER']
    # Perform image corrections and store the corrected image
    nearest_exptime_master_dark = min(masterDarkFrames.keys(), key=lambda x: abs(x - exptime))
    masterDarkFrame = masterDarkFrames[nearest_exptime_master_dark]
    correction_factor = exptime / nearest_exptime_master_dark  # dark should have the same exptime as light
    if filter_value not in masterFlatFrames: #just skip image if there is no flat with same filter
        continue
    masterFlat = masterFlatFrames[filter_value]
    corrected_image = (image - masterBias - masterDarkFrame * correction_factor) / masterFlat
    #Store image and its header in new list:
    #lightsCor.append(corrected_image)
    #lightsRaw.append(image)
    #headerList.append(header)
    save_image(output_path,corrected_image,header)
    hdul.close()
    if i%50 ==  0:
        print(i,"files saved")
print("finished with", i+1, "files saved")
#plot some of the results
corrected_files = glob.glob(os.path.join(output_path, '*.fit')) + glob.glob(os.path.join(output_path, '*.fits'))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
corrected_image1 = fits.getdata(corrected_files[0])
show_image(corrected_image1, ax=ax1, fig=fig)
ax1.set_title('corrected_image1')
corrected_image10 = fits.getdata(corrected_files[10])
show_image(corrected_image10, ax=ax2, fig=fig)
ax2.set_title('corrected_image10')
plt.show()


# XXXXXXXXXXXXXX waere cool wenn ich das wieder mit roh und korrigierem bild hinkriege.
'''
print(len(lightsCor),len(lightsRaw))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
show_image(lightsRaw[0], ax=ax1, fig=fig)
ax1.set_title('Raw Image')
show_image(lightsCor[0], ax=ax2, fig=fig)
ax2.set_title('Corrected Image')
plt.show()

output_path = os.path.join(curpath, "lightCor")
save_image(output_path,lightsCor, headerList)
'''