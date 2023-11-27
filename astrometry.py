import glob
import os
from astroquery.astrometry_net import AstrometryNet
from astropy.io import fits

path = "/home/finn/visual_Studio_Code/data/2023-09-30/stacked/"

def plate_solve(path):
    input_files = glob.glob(os.path.join(path, '*.fit')) 
    ast = AstrometryNet()
    ast.api_key = 'fpcodtulvgmteoid'  # XXXXXXXXXXXXXXXXX change personal api key at end for other persons XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    for i, file in enumerate(input_files):
        try:
            wcs_header = ast.solve_from_image(file) #determines and upload source list to plate solve 
            if wcs_header is None or len(wcs_header) == 0: 
                wcs_header = ast.solve_from_image(file, force_image_upload=True) # if its not working upload image (=slower)
                print(f"Image {i+1} solved using force_image_upload")
            else:
                print(f"Image {i+1} solved using source list")
            
            hdul = fits.open(file, mode='update')
            hdul[0].header.extend(wcs_header, useblanks=True)
            hdul.flush() #write changes to disk
            hdul.close()
        except Exception as e:
            print(f"Error processing image {i+1}: {str(e)}")
    print("finished for all images")
plate_solve(path)