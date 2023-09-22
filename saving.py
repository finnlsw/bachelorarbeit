import os
import numpy as np
from astropy.io import fits


def save_image(output_path, image_list, header_list):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for i in range(len(image_list)):
        header = header_list[i]
        image = image_list[i].astype(np.float32)
        filename = f"lightCor_{header['OBJECT']}_{header['FILTER']}_{header['EXPTIME']}s_{i}.fit"
        fits_path = os.path.join(output_path, filename)
        hdu = fits.PrimaryHDU(image, header=header)  # Use the stored header
        hdul = fits.HDUList([hdu])
        hdul.writeto(fits_path, overwrite=True)
        hdul.close()
        if i % 50 == 0:
            print(i)

    print(f"Number of files saved: {i+1}")
