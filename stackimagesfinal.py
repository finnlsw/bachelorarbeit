import numpy as np
from matplotlib import pyplot as plt
from astropy.io import fits
import glob
import os
import cv2
from astropy import visualization as aviz
from astropy.nddata.blocks import block_reduce
from plotting import show_image
from saving import save_image


base_path = "/home/finn/visual_Studio_Code/data/2023-09-25/" ####change here for different pc
input_path = os.path.join(base_path,"lightCor")
input_files = glob.glob(os.path.join(input_path, 'lightCor_HIP100587_B (Johnson)_0.7*.fit'))
#input_files2 = glob.glob(os.path.join(input_path, 'lightCor_HIP100587_focused_H-alpha_*.fit'))
#input_files3 = glob.glob(os.path.join(input_path, 'lightCor_HIP100587_focused_R Johnson_*.fit'))
#input_files4 = glob.glob(os.path.join(input_path, 'lightCor_HIP100587_focused_B (Johnson)_*.fit'))
#input_file_list= [input_files,input_files2,input_files3,input_files4]

def stack_images(inputPath, exptime):
    # import images
    imageList = []
    headerList = []
    for file in inputPath:
        hdul = fits.open(file)
        header = hdul[0].header
        image = hdul[0].data
        #if header['EXPTIME'] == exptime:
        if abs(header['EXPTIME'] - exptime) < 0.09:
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

output_path= base_path+"stacked"

'''
exptimeList=[1.0,2.0,3.0,4.0,5.0,10.0]
for exptime in exptimeList:
    stackedImage, stackedHeader = stack_images(input_files, exptime)
    save_image(output_path, stackedImage, stackedHeader, custom_text="10_images_stacked")
print("finished")
'''
exptimeList=[0.7, 40.0]
for exptime in exptimeList:
    batch_size = 10
    for i in range(0, len(input_files), batch_size):
        stackedImage, stackedHeader = stack_images(input_files[i:i+batch_size], exptime)
        #show_image(stackedImage)
        #plt.show()
        save_image(output_path, stackedImage, stackedHeader, custom_text=f"long-short-series_{batch_size}_images_stacked")
        print("success for badge",int(1+(i)/batch_size))
print("finished")

