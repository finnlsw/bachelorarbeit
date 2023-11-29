import numpy as np
from astropy.io import fits
import cv2

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
    #print('number of images to stack:', len(imageList))

    # stacking
    middle_index = len(imageList) // 2
    reference_image = imageList[middle_index].astype(np.float32)
    aligned_images = [reference_image]
    warp_mode = cv2.MOTION_TRANSLATION
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 1000, 1e-5)  # 1000: max number of iterations, 1e-5: epsilon(desired accuracy)
    for i, image in enumerate(imageList):
        if i == middle_index:
            continue
        image = image.astype(np.float32)
        _, warp_matrix = cv2.findTransformECC(reference_image, image, warp_matrix, warp_mode, criteria)
        aligned_image = cv2.warpAffine(image, warp_matrix, reference_image.shape[::-1],
                                       flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        aligned_images.append(aligned_image)
    final_stacked_image = np.mean(aligned_images, axis=0) # use mean to keep linearity
    return final_stacked_image, headerList[len(imageList) // 2]