import numpy as np
from matplotlib import pyplot as plt
from astropy.io import fits
import glob
import os
import cv2
import sys
from astropy import visualization as aviz
from astropy.nddata.blocks import block_reduce
from plotting import show_image
from saving import save_image

base_path = "/home/finn/visual_Studio_Code/data/2023-09-11/" ####change here for different pc
input_path = os.path.join(base_path,"lightCor")

input_files = glob.glob(os.path.join(input_path, 'lightCor_HIP100587_focused_I (Johnson)_*.fit'))
input_files2 = glob.glob(os.path.join(input_path, 'lightCor_HIP100587_focused_H-alpha_*.fit'))
input_files3 = glob.glob(os.path.join(input_path, 'lightCor_HIP100587_focused_R Johnson_*.fit'))
input_files4 = glob.glob(os.path.join(input_path, 'lightCor_HIP100587_focused_B (Johnson)_*.fit'))
input_file_list= [input_files,input_files2,input_files3,input_files4]

def stack_images(inputPath, exptime):
    # import images
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
    print('number of images to stack:', len(imageList))

    # stacking
    middle_index = len(imageList) // 2
    reference_image = imageList[middle_index].astype(np.float32)
    aligned_images = [reference_image]
    warp_mode = cv2.MOTION_TRANSLATION
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 1000,
                1e-5)  # 1000: max number of iterations, 1: epsilon(desired accuracy)
    for i, image in enumerate(imageList):
        if i == middle_index:
            continue
        image = image.astype(np.float32)
        _, warp_matrix = cv2.findTransformECC(reference_image, image, warp_matrix, warp_mode, criteria)
        aligned_image = cv2.warpAffine(image, warp_matrix, reference_image.shape[::-1],
                                       flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        aligned_images.append(aligned_image)
        if i % 10 == 0:
            print('number of processed images:', i)
    final_stacked_image = np.median(aligned_images, axis=0)
    return final_stacked_image, headerList[0]

stackedImage, stackedHeader = stack_images(input_file_list[3], 2.0)

show_image(stackedImage)
plt.show()

output_path = "/home/finn/visual_Studio_Code/data/2023-09-11/stacked"
save_image(output_path, stackedImage, stackedHeader)

'''
stackedImageList = []
stackedHeaderList = []
for wantedFile in input_file_list:
    stackedImage, stackedHeader = stack_images(wantedFile, 1.0)
    stackedImageList.append(stackedImage)
    stackedHeaderList.append(stackedHeader)


fig, ax = plt.subplots(1,3)
for i in range (len(stackedImageList)):
  ax[i]=show_image(stackedImageList[i])


output_path = '/content/drive/MyDrive/ColabNotebooks/data/2023-09-11/stacked'
save_image(stackedImageList, stackedHeaderList, output_path)
'''
