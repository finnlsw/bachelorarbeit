import os
import numpy as np
from astropy.io import fits


def save_image(output_path, image_list, header_list, custom_text=None):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if not isinstance(image_list, list): 
        image_list = [image_list]
    if not isinstance(header_list, list):
        header_list = [header_list]
    for i in range(len(image_list)):
        header = header_list[i]
        image = image_list[i].astype(np.float32)
        target = header['OBJECT']
        target = target.replace('/', '_')
        # Construct the filename with custom_text and suffix
        suffix = 0
        while True:
            if custom_text:
                filename = f"lightCor_{target}_{header['FILTER']}_{header['EXPTIME']}s_{custom_text}_{suffix}.fit"
            else:
                filename = f"lightCor_{target}_{header['FILTER']}_{header['EXPTIME']}s_{suffix}.fit"
            
            fits_path = os.path.join(output_path, filename)
            if not os.path.exists(fits_path):
                break
            suffix += 1
        
        fits_path = os.path.join(output_path, filename)
        hdu = fits.PrimaryHDU(image, header=header)  # Use the stored header
        hdul = fits.HDUList([hdu])
        hdul.writeto(fits_path, overwrite=True)
        hdul.close()

