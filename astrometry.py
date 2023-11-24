import glob
import os
from astroquery.astrometry_net import AstrometryNet
from astropy.io import fits

path = "/home/finn/visual_Studio_Code/data/2023-09-25/stacked/"
input_files = glob.glob(os.path.join(path, '*.fit')) 

ast = AstrometryNet()
ast.api_key = 'fpcodtulvgmteoid' # own key XXXXXX change at the end for next person

for i,file in enumerate (input_files):
    # detect sources and use source list to obtain wcs information from astronomy.net (add ,force_image_upload=True to upload image instead of use source list (is slower))
    wcs_header = ast.solve_from_image(file) # additional params: FWHM, detect_threshold

    # add wcs information to header
    hdul = fits.open(file, mode='update')
    hdul[0].header.extend(wcs_header, useblanks=True)
    hdul.flush() #write changes to disk
    hdul.close()
    print(f"success for image {i+1}")
    print("")